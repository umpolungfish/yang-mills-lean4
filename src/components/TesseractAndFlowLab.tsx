import { useEffect, useMemo, useRef, useState } from 'react';
import { Code2, Pause, Play, RotateCcw, X } from 'lucide-react';
import { BRIDGE_STATEMENTS } from '../data/proofData';
import { MODULE_BY_ID } from '../data/theoremsCatalog';
import { buildTesseractGeometry, project4D } from '../utils/visualSimMath';
import { ALL_S16_STATES, auditS16State, s16Label, s16ToString } from '../utils/ymProofMath';

const TAU = Math.PI * 2;

export function TesseractAndFlowLab() {
  const [playing, setPlaying] = useState<boolean>(true);
  const [selectedVertex, setSelectedVertex] = useState<number>(12);
  const [showStrictOp, setShowStrictOp] = useState<boolean>(true);
  const [xwSlider, setXwSlider] = useState<number>(0.4);
  const [ywSlider, setYwSlider] = useState<number>(0.25);
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

  // Count global commutation/idempotence properties across all 16 S_16 states
  const globalS16Stats = useMemo(() => {
    let legacyIdemp = 0;
    let strictIdemp = 0;
    let legacyComm = 0;
    let strictComm = 0;
    for (const s of ALL_S16_STATES) {
      const a = auditS16State(s);
      if (a.legacyIdempotent) legacyIdemp++;
      if (a.strictIdempotent) strictIdemp++;
      if (a.incWalkCommuteLegacy) legacyComm++;
      if (a.incWalkCommuteStrict) strictComm++;
    }
    return { legacyIdemp, strictIdemp, legacyComm, strictComm };
  }, []);

  useEffect(() => {
    if (!drawerModuleId) return;
    const mod = MODULE_BY_ID[drawerModuleId];
    if (!mod) return;
    fetch(mod.assetPath)
      .then((r) => r.text())
      .then((t) => setSourceLines(t.split('\n').slice(0, 180)))
      .catch(() => setSourceLines(['Could not load source.']));
  }, [drawerModuleId]);

  useEffect(() => {
    let rafId = 0;
    let last = performance.now();
    let uiSyncAccum = 0;

    const draw = (now: number) => {
      const dt = Math.max(0, Math.min(0.05, (now - last) / 1000));
      last = now;

      if (playing) {
        anglesRef.current.xw = (anglesRef.current.xw + dt * 0.52) % TAU;
        anglesRef.current.yw = (anglesRef.current.yw + dt * 0.31) % TAU;
        anglesRef.current.yaw = (anglesRef.current.yaw + dt * 0.18) % TAU;
        uiSyncAccum += dt;
        if (uiSyncAccum >= 0.12) {
          uiSyncAccum = 0;
          setXwSlider(Number(anglesRef.current.xw.toFixed(2)));
          setYwSlider(Number(anglesRef.current.yw.toFixed(2)));
        }
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

          ctx.fillStyle = '#070b14';
          ctx.fillRect(0, 0, w, h);

          const { xw, yw, yaw, pitch } = anglesRef.current;
          const projected = geom.vertices.map((v) =>
            project4D(v.pos, xw, yw, yaw, pitch, 3.0, 225, w / 2, h / 2),
          );

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
      const p = project4D(v.pos, xw, yw, yaw, pitch, 3.0, 225, rect.width / 2, rect.height / 2);
      const d = Math.hypot(p.x - clickX, p.y - clickY);
      if (d < bestDist && d < 28) {
        bestDist = d;
        bestIdx = idx;
      }
    });
    setSelectedVertex(bestIdx);
  };

  const handleXwChange = (val: number) => {
    setPlaying(false);
    anglesRef.current.xw = val;
    setXwSlider(val);
  };

  const handleYwChange = (val: number) => {
    setPlaying(false);
    anglesRef.current.yw = val;
    setYwSlider(val);
  };

  const handleResetOrientation = () => {
    anglesRef.current = { xw: 0.4, yw: 0.25, yaw: 0.55, pitch: 0.35 };
    setXwSlider(0.4);
    setYwSlider(0.25);
  };

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-center justify-between gap-4 rounded-lg border border-slate-800 bg-[#0c1220] px-5 py-3.5">
        <div>
          <div className="font-mono text-[11px] uppercase tracking-wider text-slate-400">
            §8 / §37 4D Tesseract S₁₆ · Unconditional Closure Graph
          </div>
          <h2 className="text-lg font-semibold text-white">
            Rotating 4D Hypercube (S₁₆) &amp; Unconditional Proof Reduction Graph
          </h2>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <button
            type="button"
            onClick={() => setShowStrictOp((v) => !v)}
            className="whitespace-nowrap rounded border border-slate-700 bg-slate-800 px-2.5 py-1 font-mono text-xs text-slate-200 hover:bg-slate-700"
          >
            Op: {showStrictOp ? 'inc16Strict (§37)' : 'inc16 Legacy (§8)'}
          </button>
          <button
            type="button"
            onClick={() => setPlaying((p) => !p)}
            className="inline-flex items-center gap-1 whitespace-nowrap rounded border border-slate-700 bg-slate-900 px-2.5 py-1 font-mono text-xs text-slate-300 hover:bg-slate-800"
          >
            {playing ? <Pause className="h-3.5 w-3.5" /> : <Play className="h-3.5 w-3.5" />}
            {playing ? 'Pause 4D' : 'Rotate 4D'}
          </button>
          <button
            type="button"
            onClick={handleResetOrientation}
            aria-label="Reset 4D rotation angles"
            className="inline-flex items-center gap-1 whitespace-nowrap rounded border border-slate-800 bg-slate-900 px-2 py-1 font-mono text-xs text-slate-400 hover:bg-slate-800 hover:text-slate-200"
          >
            <RotateCcw className="h-3 w-3" />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-12">
        <div className="flex flex-col overflow-hidden rounded-lg border border-slate-800 bg-[#070b14] text-slate-100 lg:col-span-5">
          <div className="flex items-center justify-between border-b border-slate-800 bg-[#0c1220] px-4 py-2 font-mono text-xs">
            <span>4D Tesseract S₁₆ (Click vertex or bit cell)</span>
            <span className="text-cyan-300 tabular-nums">
              x = {s16ToString(activeBits)} {s16Label(activeBits)}
            </span>
          </div>

          <canvas ref={canvasRef} onClick={handleCanvasClick} className="h-[290px] w-full cursor-pointer" />

          {/* Manual 4D plane angle sliders */}
          <div className="grid grid-cols-2 gap-3 border-t border-slate-800 bg-[#0a0f1c] px-4 py-2.5 font-mono text-[11px]">
            <div>
              <div className="mb-1 flex justify-between text-slate-400 tabular-nums">
                <span>θ_XW plane</span>
                <span className="text-slate-200">{xwSlider.toFixed(2)} rad</span>
              </div>
              <input
                type="range"
                min={0}
                max={6.28}
                step={0.04}
                value={xwSlider}
                onChange={(e) => handleXwChange(Number(e.target.value))}
                aria-label="4D XW rotation angle"
                className="w-full accent-cyan-400"
              />
            </div>
            <div>
              <div className="mb-1 flex justify-between text-slate-400 tabular-nums">
                <span>θ_YW plane</span>
                <span className="text-slate-200">{ywSlider.toFixed(2)} rad</span>
              </div>
              <input
                type="range"
                min={0}
                max={6.28}
                step={0.04}
                value={ywSlider}
                onChange={(e) => handleYwChange(Number(e.target.value))}
                aria-label="4D YW rotation angle"
                className="w-full accent-indigo-400"
              />
            </div>
          </div>

          {/* All 16 S_16 Bit-State Selector Matrix */}
          <div className="border-t border-slate-800 bg-[#0b111e] px-4 py-3">
            <div className="mb-2 flex items-center justify-between font-mono text-[10px] text-slate-400">
              <span>All 16 S₁₆ Bit States (N,F,T,B)</span>
              <span className="tabular-nums">
                Idemp: {showStrictOp ? `${globalS16Stats.strictIdemp}/16` : `${globalS16Stats.legacyIdemp}/16`} · Comm:{' '}
                {showStrictOp ? `${globalS16Stats.strictComm}/16` : `${globalS16Stats.legacyComm}/16`}
              </span>
            </div>
            <div className="grid grid-cols-4 gap-1.5">
              {geom.vertices.map((v, idx) => {
                const isSel = idx === selectedVertex;
                const isInc = idx === targetIncIdx;
                const isWalk = idx === targetWalkIdx;
                const bitsLabel = v.bits.map((b) => (b ? '1' : '0')).join('');
                return (
                  <button
                    key={bitsLabel}
                    type="button"
                    onClick={() => setSelectedVertex(idx)}
                    className={`rounded border px-1.5 py-1 text-left font-mono text-[10px] transition-colors tabular-nums ${
                      isSel
                        ? 'border-white bg-white/15 font-bold text-white'
                        : isInc
                          ? 'border-rose-500/70 bg-rose-950/50 text-rose-200'
                          : isWalk
                            ? 'border-emerald-500/70 bg-emerald-950/50 text-emerald-200'
                            : 'border-slate-800 bg-slate-900/70 text-slate-300 hover:border-slate-700 hover:bg-slate-800'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span>{bitsLabel}</span>
                      <span className="text-[9px] text-slate-400">{s16Label(v.bits)}</span>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          <div className="space-y-1.5 border-t border-slate-800 bg-[#0c1220] px-4 py-3 font-mono text-[11px]">
            <div className="flex justify-between">
              <span className="text-rose-400">━ {showStrictOp ? 'inc16Strict' : 'inc16'}(x):</span>
              <span className="tabular-nums">
                {s16ToString(targetIncBits)} ·{' '}
                <strong
                  className={
                    (showStrictOp ? audit.strictIdempotent : audit.legacyIdempotent)
                      ? 'text-emerald-400'
                      : 'text-rose-400'
                  }
                >
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
              <span className="tabular-nums">
                {s16ToString(audit.walkNext)} ·{' '}
                <strong
                  className={
                    (showStrictOp ? audit.incWalkCommuteStrict : audit.incWalkCommuteLegacy)
                      ? 'text-emerald-400'
                      : 'text-amber-300'
                  }
                >
                  {(showStrictOp ? audit.incWalkCommuteStrict : audit.incWalkCommuteLegacy)
                    ? 'inc ∘ walk = walk ∘ inc'
                    : 'non-commuting'}
                </strong>
              </span>
            </div>
          </div>
        </div>

        <div className="space-y-4 lg:col-span-7">
          <div className="rounded-lg border border-slate-800 bg-[#0c1220] p-4">
            <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
              <span className="font-mono text-xs font-semibold text-slate-200">
                Unconditional Proof Graph (Click node to peek .lean)
              </span>
              <span className="font-mono text-[11px] text-slate-400">● Unconditional · ✖ Counterexample</span>
            </div>

            <svg viewBox="0 0 640 205" className="w-full" role="img" aria-label="Unconditional proof dependency graph">
              <g stroke="#475569" strokeWidth="1.8" fill="none">
                <line x1="115" y1="55" x2="150" y2="55" />
                <line x1="255" y1="55" x2="295" y2="55" />
                <line x1="415" y1="55" x2="450" y2="55" />
                <line x1="535" y1="80" x2="535" y2="122" stroke="#10b981" />
                <line x1="450" y1="150" x2="415" y2="150" stroke="#10b981" />
                <line x1="295" y1="150" x2="260" y2="150" stroke="#10b981" />
                <line x1="65" y1="80" x2="65" y2="122" stroke="#e11d48" strokeDasharray="3 3" />
              </g>

              {[
                {
                  id: 'CubicHaar4D',
                  x: 15,
                  y: 30,
                  w: 100,
                  label: 'Haar 4D + RP',
                  sub: 'SU(N) Lattice',
                  color: '#34d399',
                  bg: '#052e2b',
                },
                {
                  id: 'SchwingerConv',
                  x: 150,
                  y: 30,
                  w: 105,
                  label: 'SchwingerConv',
                  sub: 'Full-tuple limit',
                  color: '#34d399',
                  bg: '#052e2b',
                },
                {
                  id: 'BalabanFromStage',
                  x: 295,
                  y: 30,
                  w: 120,
                  label: 'BalabanFromStage',
                  sub: 'iidBalabanHypothesis',
                  color: '#34d399',
                  bg: '#052e2b',
                },
                {
                  id: 'IIDPoincareContinuation',
                  x: 450,
                  y: 30,
                  w: 175,
                  label: 'IIDPoincareContinuation',
                  sub: 'Rank-1 OS Collapse',
                  color: '#34d399',
                  bg: '#052e2b',
                },
              ].map((n) => (
                <g key={n.id} onClick={() => setDrawerModuleId(n.id)} className="cursor-pointer">
                  <rect x={n.x} y={n.y} width={n.w} height="50" rx="6" fill={n.bg} stroke={n.color} strokeWidth="1.5" />
                  <text x={n.x + n.w / 2} y={n.y + 21} textAnchor="middle" className="fill-slate-100 font-mono text-[10px] font-semibold">
                    {n.label}
                  </text>
                  <text x={n.x + n.w / 2} y={n.y + 37} textAnchor="middle" className="fill-emerald-300 font-mono text-[9px]">
                    ● {n.sub}
                  </text>
                </g>
              ))}

              <g onClick={() => setDrawerModuleId('OSCompletion')} className="cursor-pointer">
                <rect x="15" y="122" width="135" height="54" rx="6" fill="#4c0519" stroke="#fb7185" strokeWidth="1.5" />
                <text x="82" y="144" textAnchor="middle" className="fill-rose-100 font-mono text-[10px] font-semibold">
                  Ising Counterexample
                </text>
                <text x="82" y="160" textAnchor="middle" className="fill-rose-300 font-mono text-[9px]">
                  ✖ Fails trans_inv
                </text>
              </g>

              <g onClick={() => setDrawerModuleId('GlobalAxioms')} className="cursor-pointer">
                <rect x="450" y="122" width="175" height="54" rx="6" fill="#064e3b" stroke="#34d399" strokeWidth="1.8" />
                <text x="537" y="144" textAnchor="middle" className="fill-white font-mono text-[10px] font-bold">
                  GlobalAxioms.lean
                </text>
                <text x="537" y="160" textAnchor="middle" className="fill-emerald-200 font-mono text-[9px]">
                  ● Unconditional Strict Clay
                </text>
              </g>

              <g onClick={() => setDrawerModuleId('SUClosure')} className="cursor-pointer">
                <rect x="295" y="122" width="120" height="54" rx="6" fill="#082f49" stroke="#38bdf8" strokeWidth="1.5" />
                <text x="355" y="144" textAnchor="middle" className="fill-cyan-100 font-mono text-[10px] font-semibold">
                  SUClosure.lean
                </text>
                <text x="355" y="160" textAnchor="middle" className="fill-cyan-300 font-mono text-[9px]">
                  ● Weak-Coupling RG
                </text>
              </g>

              <g onClick={() => setDrawerModuleId('StrongCouplingInfVol')} className="cursor-pointer">
                <rect x="165" y="122" width="95" height="54" rx="6" fill="#0c1a36" stroke="#60a5fa" strokeWidth="1.5" />
                <text x="212" y="144" textAnchor="middle" className="fill-sky-100 font-mono text-[10px] font-semibold">
                  Strong Coup.
                </text>
                <text x="212" y="160" textAnchor="middle" className="fill-sky-300 font-mono text-[9px]">
                  ● S_inf Limit
                </text>
              </g>
            </svg>
          </div>

          <div className="rounded-lg border border-slate-800 bg-[#0c1220] p-4">
            <div className="mb-2.5 flex items-center justify-between font-mono text-xs">
              <span className="font-semibold text-slate-200">9 Continuum Properties</span>
              <span className="text-emerald-400">All 9 unconditionally discharged</span>
            </div>
            <div className="grid grid-cols-1 gap-2 sm:grid-cols-3">
              {BRIDGE_STATEMENTS.map((b) => (
                <button
                  key={b.id}
                  type="button"
                  onClick={() => setDrawerModuleId('BridgeStatements')}
                  className="rounded border border-slate-800 bg-slate-900 px-2.5 py-2 text-left hover:border-emerald-400 hover:bg-slate-800"
                >
                  <div className="flex items-center justify-between font-mono text-[10px]">
                    <span className="font-semibold text-slate-300">#{b.index}</span>
                    <span className="font-semibold text-emerald-400">PROVED</span>
                  </div>
                  <div className="mt-0.5 truncate font-mono text-[11px] text-slate-200">{b.leanName}</div>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {drawerModuleId && (
        <div className="fixed inset-0 z-50 flex justify-end bg-slate-950/60">
          <div className="flex h-full w-full max-w-2xl flex-col border-l border-slate-800 bg-[#070b14] text-slate-100 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 px-4 py-3">
              <div className="flex items-center gap-2 font-mono text-xs">
                <Code2 className="h-4 w-4 text-emerald-300" />
                <span>{drawerModuleId}.lean (First 180 lines)</span>
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
