import { useEffect, useMemo, useRef, useState } from 'react';
import { Code2, Pause, Play, X } from 'lucide-react';
import { BRIDGE_STATEMENTS, CORPUS_MODULES } from '../data/corpusData';
import { buildTesseractGeometry, project4D } from '../utils/visualSimMath';
import { auditS16State, s16Label, s16ToString } from '../utils/yangMillsMath';

export function TesseractAndFlowLab() {
  const [playing, setPlaying] = useState<boolean>(true);
  const [selectedVertex, setSelectedVertex] = useState<number>(12); // (1,1,0,0)
  const [showStrictOp, setShowStrictOp] = useState<boolean>(true);
  const [drawerModuleId, setDrawerModuleId] = useState<string | null>(null);
  const [sourceLines, setSourceLines] = useState<string[]>([]);

  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const anglesRef = useRef({ xw: 0.4, yw: 0.25, yaw: 0.55, pitch: 0.35 });

  const geom = useMemo(() => buildTesseractGeometry(), []);
  const activeBits = geom.vertices[selectedVertex]?.bits ?? [false, false, false, false];
  const audit = useMemo(() => auditS16State(activeBits), [activeBits]);

  const targetIncBits = showStrictOp ? audit.incStrict : audit.incLegacy;
  const targetIncIdx = geom.vertices.findIndex(
    (v) =>
      v.bits[0] === targetIncBits[0] &&
      v.bits[1] === targetIncBits[1] &&
      v.bits[2] === targetIncBits[2] &&
      v.bits[3] === targetIncBits[3],
  );
  const targetWalkIdx = geom.vertices.findIndex(
    (v) =>
      v.bits[0] === audit.walkNext[0] &&
      v.bits[1] === audit.walkNext[1] &&
      v.bits[2] === audit.walkNext[2] &&
      v.bits[3] === audit.walkNext[3],
  );

  // Load raw Lean snippet only when drawer is opened
  useEffect(() => {
    if (!drawerModuleId) return;
    const mod = CORPUS_MODULES.find((m) => m.id === drawerModuleId);
    if (!mod) return;
    fetch(mod.assetPath)
      .then((r) => r.text())
      .then((t) => setSourceLines(t.split('\n').slice(0, 140)))
      .catch(() => setSourceLines(['Could not load source.']));
  }, [drawerModuleId]);

  // 60fps 4D Rotating Tesseract Render
  useEffect(() => {
    let rafId = 0;
    let last = performance.now();

    const draw = (now: number) => {
      const dt = Math.max(0, Math.min(0.05, (now - last) / 1000));
      last = now;

      if (playing) {
        anglesRef.current.xw += dt * 0.52;
        anglesRef.current.yw += dt * 0.31;
        anglesRef.current.yaw += dt * 0.18;
      }

      const canvas = canvasRef.current;
      if (canvas) {
        const ctx = canvas.getContext('2d');
        if (ctx) {
          const dpr = window.devicePixelRatio || 1;
          const rect = canvas.getBoundingClientRect();
          const tw = Math.max(300, Math.floor(rect.width * dpr));
          const th = Math.max(260, Math.floor(rect.height * dpr));
          if (canvas.width !== tw || canvas.height !== th) {
            canvas.width = tw;
            canvas.height = th;
          }
          ctx.save();
          ctx.scale(dpr, dpr);
          const w = rect.width;
          const h = rect.height;

          ctx.fillStyle = '#0b1120';
          ctx.fillRect(0, 0, w, h);

          const { xw, yw, yaw, pitch } = anglesRef.current;
          const projected = geom.vertices.map((v) =>
            project4D(v.pos, xw, yw, yaw, pitch, 3.0, 270, w / 2, h / 2),
          );

          // Draw 32 tesseract edges
          for (const [u, v, axis] of geom.edges) {
            const p1 = projected[u];
            const p2 = projected[v];
            const axisColors = ['#38bdf8', '#818cf8', '#34d399', '#fbbf24'];
            ctx.strokeStyle = axisColors[axis] ?? '#64748b';
            ctx.globalAlpha = 0.38;
            ctx.lineWidth = 1.4;
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
          }
          ctx.globalAlpha = 1;

          // Draw highlighted Inc flow arrow & Walk flow arrow from selectedVertex
          const srcP = projected[selectedVertex];
          if (srcP && targetIncIdx >= 0) {
            const dstP = projected[targetIncIdx];
            ctx.strokeStyle = '#f43f5e';
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(srcP.x, srcP.y);
            ctx.lineTo(dstP.x, dstP.y);
            ctx.stroke();
          }
          if (srcP && targetWalkIdx >= 0) {
            const wP = projected[targetWalkIdx];
            ctx.strokeStyle = '#10b981';
            ctx.lineWidth = 2.5;
            ctx.setLineDash([4, 3]);
            ctx.beginPath();
            ctx.moveTo(srcP.x, srcP.y);
            ctx.lineTo(wP.x, wP.y);
            ctx.stroke();
            ctx.setLineDash([]);
          }

          // Draw 16 vertices
          projected.forEach((pt, idx) => {
            const isSel = idx === selectedVertex;
            const isInc = idx === targetIncIdx;
            const isWalk = idx === targetWalkIdx;
            ctx.beginPath();
            ctx.arc(pt.x, pt.y, isSel ? 7 : isInc || isWalk ? 5.5 : 3.5, 0, Math.PI * 2);
            ctx.fillStyle = isSel
              ? '#ffffff'
              : isInc
                ? '#f43f5e'
                : isWalk
                  ? '#10b981'
                  : '#94a3b8';
            ctx.fill();
            if (isSel || isInc || isWalk) {
              ctx.font = '600 10px "IBM Plex Mono", monospace';
              ctx.fillStyle = '#e2e8f0';
              ctx.textAlign = 'center';
              const lx = Math.max(36, Math.min(w - 36, pt.x));
              const ly = pt.y < 24 ? pt.y + 18 : pt.y - 10;
              ctx.fillText(s16Label(geom.vertices[idx].bits), lx, ly);
            }
          });

          ctx.restore();
        }
      }
      rafId = requestAnimationFrame(draw);
    };

    rafId = requestAnimationFrame(draw);
    return () => cancelAnimationFrame(rafId);
  }, [playing, geom, selectedVertex, targetIncIdx, targetWalkIdx]);

  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;
    const { xw, yw, yaw, pitch } = anglesRef.current;

    let bestIdx = selectedVertex;
    let bestDist = Infinity;
    geom.vertices.forEach((v, idx) => {
      const p = project4D(v.pos, xw, yw, yaw, pitch, 3.0, 270, rect.width / 2, rect.height / 2);
      const d = Math.hypot(p.x - clickX, p.y - clickY);
      if (d < bestDist && d < 28) {
        bestDist = d;
        bestIdx = idx;
      }
    });
    setSelectedVertex(bestIdx);
  };

  return (
    <div className="space-y-5">
      {/* Compact Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 rounded-lg border border-slate-200 bg-white px-5 py-3.5">
        <div>
          <div className="font-mono text-[11px] uppercase tracking-wider text-slate-500">
            §8 / §37 4D Tesseract S16 · §45 Proof Reduction &amp; 9 Bridge Targets
          </div>
          <h1 className="text-lg font-semibold text-slate-900">
            Rotating 4D Hypercube (S₁₆) &amp; Visual Proof Pipeline
          </h1>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setShowStrictOp((v) => !v)}
            className="rounded border border-slate-200 bg-slate-50 px-2.5 py-1 font-mono text-xs text-slate-800 hover:bg-white"
          >
            Op: {showStrictOp ? 'inc16Strict (§37)' : 'inc16 Legacy (§8)'}
          </button>
          <button
            type="button"
            onClick={() => setPlaying((p) => !p)}
            className="inline-flex items-center gap-1 rounded border border-slate-200 bg-white px-2.5 py-1 font-mono text-xs text-slate-700 hover:bg-slate-50"
          >
            {playing ? <Pause className="h-3.5 w-3.5" /> : <Play className="h-3.5 w-3.5" />}
            {playing ? 'Pause 4D' : 'Rotate 4D'}
          </button>
        </div>
      </div>

      {/* Main Grid: 4D Rotating Tesseract Canvas (5 cols) + Visual Proof Pipeline & 9-Bridge Grid (7 cols) */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-12">
        {/* LEFT: 4D Rotating Tesseract */}
        <div className="flex flex-col overflow-hidden rounded-lg border border-slate-200 bg-slate-950 text-slate-100 lg:col-span-5">
          <div className="flex items-center justify-between border-b border-slate-800 bg-slate-900 px-4 py-2 font-mono text-xs">
            <span>4D Tesseract S₁₆ (Click vertex)</span>
            <span className="text-cyan-300">
              x = {s16ToString(activeBits)} {s16Label(activeBits)}
            </span>
          </div>

          <canvas
            ref={canvasRef}
            onClick={handleCanvasClick}
            className="h-[340px] w-full cursor-pointer"
          />

          <div className="space-y-1.5 border-t border-slate-800 bg-slate-900/90 px-4 py-3 font-mono text-[11px]">
            <div className="flex justify-between">
              <span className="text-rose-400">━ {showStrictOp ? 'inc16Strict' : 'inc16'}(x):</span>
              <span>
                {s16ToString(targetIncBits)} ·{' '}
                <strong className={audit.strictNonVoid ? 'text-emerald-400' : 'text-rose-400'}>
                  {showStrictOp
                    ? 'idempotent & non-void'
                    : audit.legacyIdempotent
                      ? 'idempotent'
                      : 'non-idempotent'}
                </strong>
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-emerald-400">┄ walk16(x):</span>
              <span>{s16ToString(audit.walkNext)}</span>
            </div>
          </div>
        </div>

        {/* RIGHT: Visual Proof Flow Diagram (SVG) + Compact 9-Bridge Status Strip */}
        <div className="space-y-4 lg:col-span-7">
          {/* SVG Visual Proof DAG Diagram */}
          <div className="rounded-lg border border-slate-200 bg-white p-4">
            <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
              <span className="font-mono text-xs font-semibold text-slate-800">
                Proof Reduction Graph (Click node to peek .lean)
              </span>
              <span className="font-mono text-[11px] text-slate-500">
                ● Proved · ✖ Toy · ▲ Open
              </span>
            </div>

            <svg viewBox="0 0 640 205" className="w-full" role="img" aria-label="Visual proof dependency graph">
              {/* Edges */}
              <g stroke="#cbd5e1" strokeWidth="1.8" fill="none">
                <line x1="110" y1="55" x2="150" y2="55" />
                <line x1="255" y1="55" x2="295" y2="55" />
                <line x1="400" y1="55" x2="440" y2="55" />
                <line x1="495" y1="80" x2="495" y2="122" />
                <line x1="440" y1="150" x2="400" y2="150" stroke="#f59e0b" strokeDasharray="4 3" />
                <line x1="295" y1="150" x2="255" y2="150" stroke="#f59e0b" strokeDasharray="4 3" />
                <line x1="65" y1="80" x2="65" y2="122" stroke="#e11d48" strokeDasharray="3 3" />
              </g>

              {/* Top Row: Proved Unconditional Spine */}
              {[
                { id: 'Core', x: 15, y: 30, w: 95, label: 'Core (§§1–21)', sub: 'Wilson + S16', color: '#059669', bg: '#ecfdf5' },
                { id: 'CubicHaar4D', x: 150, y: 30, w: 105, label: 'Haar 4D (§36)', sub: 'SU(N) + RP', color: '#059669', bg: '#ecfdf5' },
                { id: 'FeynmanKac', x: 295, y: 30, w: 105, label: 'FK Slices (§42)', sub: 'Z = Tr(T^Lt)', color: '#059669', bg: '#ecfdf5' },
                { id: 'StrongCouplingDobrushin', x: 440, y: 30, w: 185, label: 'Dobrushin Gap (§43–44)', sub: 'α<1 ⇒ m=-½log α > 0', color: '#059669', bg: '#ecfdf5' },
              ].map((n) => (
                <g key={n.id} onClick={() => setDrawerModuleId(n.id)} className="cursor-pointer">
                  <rect x={n.x} y={n.y} width={n.w} height="50" rx="6" fill={n.bg} stroke={n.color} strokeWidth="1.5" />
                  <text x={n.x + n.w / 2} y={n.y + 21} textAnchor="middle" className="fill-slate-900 font-mono text-[10px] font-semibold">
                    {n.label}
                  </text>
                  <text x={n.x + n.w / 2} y={n.y + 37} textAnchor="middle" className="fill-emerald-800 font-mono text-[9px]">
                    ● {n.sub}
                  </text>
                </g>
              ))}

              {/* Bottom Left: Rejected Ising Toy */}
              <g onClick={() => setDrawerModuleId('OSCompletion')} className="cursor-pointer">
                <rect x="15" y="122" width="140" height="54" rx="6" fill="#fff1f2" stroke="#e11d48" strokeWidth="1.5" />
                <text x="85" y="144" textAnchor="middle" className="fill-rose-900 font-mono text-[10px] font-semibold">
                  Ising Toy (§34/§37)
                </text>
                <text x="85" y="160" textAnchor="middle" className="fill-rose-700 font-mono text-[9px]">
                  ✖ Fails trans_inv
                </text>
              </g>

              {/* Bottom Right-to-Left: Inf-Vol -> Open RG -> Clay Strict */}
              <g onClick={() => setDrawerModuleId('CanonicalWitness')} className="cursor-pointer">
                <rect x="440" y="122" width="185" height="54" rx="6" fill="#ecfdf5" stroke="#059669" strokeWidth="1.5" />
                <text x="532" y="144" textAnchor="middle" className="fill-slate-900 font-mono text-[10px] font-semibold">
                  S_inf &amp; Witness (§46W)
                </text>
                <text x="532" y="160" textAnchor="middle" className="fill-emerald-800 font-mono text-[9px]">
                  ● 1 vs (N−4)/N at β₀=1/300
                </text>
              </g>

              <g onClick={() => setDrawerModuleId('ContinuumClosure')} className="cursor-pointer">
                <rect x="295" y="122" width="105" height="54" rx="6" fill="#fffbeb" stroke="#d97706" strokeWidth="1.5" />
                <text x="347" y="144" textAnchor="middle" className="fill-amber-950 font-mono text-[10px] font-semibold">
                  Balaban + OS
                </text>
                <text x="347" y="160" textAnchor="middle" className="fill-amber-800 font-mono text-[9px]">
                  ▲ Open β→∞ Hyps
                </text>
              </g>

              <g onClick={() => setDrawerModuleId('BridgeStatements')} className="cursor-pointer">
                <rect x="175" y="122" width="80" height="54" rx="6" fill="#eff6ff" stroke="#2563eb" strokeWidth="1.5" />
                <text x="215" y="144" textAnchor="middle" className="fill-blue-950 font-mono text-[10px] font-semibold">
                  Clay 4D
                </text>
                <text x="215" y="160" textAnchor="middle" className="fill-blue-800 font-mono text-[9px]">
                  Wightman QFT
                </text>
              </g>
            </svg>
          </div>

          {/* Visual 3x3 Matrix of the 9 BridgeStatements */}
          <div className="rounded-lg border border-slate-200 bg-white p-4">
            <div className="mb-2.5 flex items-center justify-between font-mono text-xs">
              <span className="font-semibold text-slate-800">9 BridgeStatements Scoreboard</span>
              <span className="text-slate-500">6 Strong-Coupling Proved · 3 Partial on Z⁴ · Weak Limit Open</span>
            </div>
            <div className="grid grid-cols-3 gap-2">
              {BRIDGE_STATEMENTS.map((b) => (
                <button
                  key={b.id}
                  type="button"
                  onClick={() => setDrawerModuleId('BridgeStatements')}
                  className="rounded border border-slate-200 bg-slate-50 px-2.5 py-2 text-left hover:border-blue-400 hover:bg-white"
                >
                  <div className="flex items-center justify-between font-mono text-[10px]">
                    <span className="font-semibold text-slate-800">#{b.index}</span>
                    <span
                      className={
                        b.finiteStrongCouplingStatus === 'proved'
                          ? 'font-semibold text-emerald-700'
                          : 'font-semibold text-amber-700'
                      }
                    >
                      {b.finiteStrongCouplingStatus === 'proved' ? '● PROVED' : '▲ PARTIAL'}
                    </span>
                  </div>
                  <div className="mt-0.5 truncate font-mono text-[11px] text-slate-700">
                    {b.leanName}
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Optional Slide-Over Raw Lean Peek Drawer */}
      {drawerModuleId && (
        <div className="fixed inset-0 z-50 flex justify-end bg-slate-950/50">
          <div className="flex h-full w-full max-w-2xl flex-col bg-slate-950 text-slate-100 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 px-4 py-3">
              <div className="flex items-center gap-2 font-mono text-xs">
                <Code2 className="h-4 w-4 text-blue-400" />
                <span>{drawerModuleId}.lean (First 140 lines)</span>
              </div>
              <button
                type="button"
                aria-label="Close source drawer"
                onClick={() => setDrawerModuleId(null)}
                className="rounded p-1 text-slate-400 hover:bg-slate-800 hover:text-white"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
            <div className="flex-1 overflow-auto p-4 font-mono text-[11.5px] leading-relaxed">
              {sourceLines.map((line, i) => (
                <div key={i} className="flex gap-3">
                  <span className="w-8 shrink-0 text-right text-slate-500 tabular-nums">{i + 1}</span>
                  <span className="whitespace-pre">{line}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
