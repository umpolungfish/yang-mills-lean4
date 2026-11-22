import { useEffect, useMemo, useRef, useState } from 'react';
import { Pause, Play } from 'lucide-react';
import { checkIsingShiftObstruction, radialCoupling4D } from '../utils/yangMillsMath';

export function FeynmanKacIsingLab() {
  const [ltSlices, setLtSlices] = useState<number>(6);
  const [showMirror, setShowMirror] = useState<boolean>(true);
  const [playing, setPlaying] = useState<boolean>(true);
  const [phase, setPhase] = useState<number>(0);

  // Ising 2D heatmap interactive probe point (a0, a1)
  const [probeA0, setProbeA0] = useState<number>(1.0);
  const [probeA1, setProbeA1] = useState<number>(0.0);
  const [autoSweep, setAutoSweep] = useState<boolean>(false);

  const heatmapCanvasRef = useRef<HTMLCanvasElement | null>(null);
  const rafRef = useRef<number>(0);
  const phaseRef = useRef<number>(0);

  useEffect(() => {
    let last = performance.now();
    const tick = (now: number) => {
      const dt = Math.max(0, Math.min(0.05, (now - last) / 1000));
      last = now;
      if (playing) {
        const next = phaseRef.current + dt;
        phaseRef.current = next;
        setPhase(next);
        if (autoSweep) {
          const rad = 1.15 * (0.5 + 0.5 * Math.sin(next * 1.4));
          const ang = next * 0.9;
          setProbeA0(Number((rad * Math.cos(ang)).toFixed(2)));
          setProbeA1(Number((rad * Math.sin(ang)).toFixed(2)));
        }
      }
      rafRef.current = requestAnimationFrame(tick);
    };
    rafRef.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(rafRef.current);
  }, [playing, autoSweep]);

  const isingCheck = useMemo(
    () => checkIsingShiftObstruction([probeA0, probeA1, 0, 0]),
    [probeA0, probeA1],
  );

  // Draw 2D Ising radial coupling heatmap
  useEffect(() => {
    const canvas = heatmapCanvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const w = 320;
    const h = 260;
    if (canvas.width !== w || canvas.height !== h) {
      canvas.width = w;
      canvas.height = h;
    }

    const img = ctx.createImageData(w, h);
    const maxCoord = 2.2;
    for (let py = 0; py < h; py++) {
      const x1 = ((h / 2 - py) / (h / 2)) * maxCoord;
      for (let px = 0; px < w; px++) {
        const x0 = ((px - w / 2) / (w / 2)) * maxCoord;
        const g = radialCoupling4D([x0, x1, 0, 0]);
        const s2 = 1 + g * g; // 1 .. 2
        const t = Math.max(0, Math.min(1, s2 - 1)); // 0 .. 1
        const idx = (py * w + px) * 4;
        // Obsidian slate (#0b1120) -> Emerald/Cyan (#06b6d4 -> #34d399) at origin peak
        img.data[idx] = Math.round(11 + t * 40);
        img.data[idx + 1] = Math.round(17 + t * 200);
        img.data[idx + 2] = Math.round(32 + t * 195);
        img.data[idx + 3] = 255;
      }
    }
    ctx.putImageData(img, 0, 0);

    // Axes
    ctx.strokeStyle = 'rgba(226, 232, 240, 0.25)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(w / 2, 0);
    ctx.lineTo(w / 2, h);
    ctx.moveTo(0, h / 2);
    ctx.lineTo(w, h / 2);
    ctx.stroke();

    // Origin marker
    ctx.beginPath();
    ctx.arc(w / 2, h / 2, 5, 0, Math.PI * 2);
    ctx.strokeStyle = '#34d399';
    ctx.lineWidth = 1.8;
    ctx.stroke();

    // Probe marker (a0, a1)
    const px = w / 2 + (probeA0 / maxCoord) * (w / 2);
    const py = h / 2 - (probeA1 / maxCoord) * (h / 2);
    ctx.beginPath();
    ctx.arc(px, py, 6, 0, Math.PI * 2);
    ctx.fillStyle = isingCheck.translationInvariant ? '#34d399' : '#f43f5e';
    ctx.fill();
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.fillStyle = 'rgba(226, 232, 240, 0.72)';
    ctx.font = '600 10px "Fira Code", monospace';
    ctx.fillText('a₀ →', w - 34, h / 2 - 6);
    ctx.fillText('a₁ ↑', w / 2 + 6, 14);
  }, [probeA0, probeA1, isingCheck.translationInvariant]);

  const handleHeatmapClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const nx = (e.clientX - rect.left) / rect.width;
    const ny = (e.clientY - rect.top) / rect.height;
    setAutoSweep(false);
    setProbeA0(Number(((nx * 2 - 1) * 2.2).toFixed(2)));
    setProbeA1(Number(((1 - ny * 2) * 2.2).toFixed(2)));
  };

  // Slice coordinates around a vertical Euclidean time-slice ring
  const sliceNodes = useMemo(() => {
    const cx = 165;
    const cy = 128;
    const rx = 105;
    const ry = 76;
    return Array.from({ length: ltSlices }, (_, t) => {
      const ang = -Math.PI / 2 + (t / ltSlices) * Math.PI * 2;
      const isPos = t < ltSlices / 2;
      return {
        t,
        x: cx + rx * Math.cos(ang),
        y: cy + ry * Math.sin(ang),
        isPos,
      };
    });
  }, [ltSlices]);

  const pulseSlicePos = useMemo(() => {
    const len = Math.max(1, sliceNodes.length);
    const safePhase = ((phase * 0.75) % 1 + 1) % 1;
    const idxFloat = safePhase * len;
    const i0 = Math.floor(idxFloat) % len;
    const i1 = (i0 + 1) % len;
    const f = idxFloat - Math.floor(idxFloat);
    const a = sliceNodes[i0];
    const b = sliceNodes[i1];
    if (!a || !b) {
      return { x: 165, y: 128 };
    }
    return {
      x: a.x + (b.x - a.x) * f,
      y: a.y + (b.y - a.y) * f,
    };
  }, [phase, sliceNodes]);

  return (
    <div className="space-y-5">
      {/* Header Controls */}
      <div className="flex flex-wrap items-center justify-between gap-4 rounded-lg border border-slate-800 bg-slate-900 px-5 py-3.5">
        <div>
          <div className="font-mono text-[11px] uppercase tracking-wider text-slate-400">
            §§39–42 Feynman–Kac Slice Transfer · §§34/37 Ising Toy Obstruction
          </div>
          <h1 className="text-lg font-semibold text-slate-100">
            Euclidean Transfer Cylinder, Reflection Plane Θ &amp; Radial Peak Collapse
          </h1>
        </div>

        <button
          type="button"
          onClick={() => setPlaying((p) => !p)}
          className="inline-flex items-center gap-1.5 rounded border border-slate-800 bg-slate-800 px-3 py-1.5 font-mono text-xs text-slate-200 hover:bg-slate-700"
        >
          {playing ? <Pause className="h-3.5 w-3.5" /> : <Play className="h-3.5 w-3.5" />}
          {playing ? 'Pause Motion' : 'Play Motion'}
        </button>
      </div>

      {/* Dual Visual Figures */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-12">
        {/* LEFT FIGURE: Feynman-Kac Time-Slice Ring + Reflection Mirror */}
        <div className="rounded-lg border border-slate-800 bg-slate-900 p-5 lg:col-span-6">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div>
              <h2 className="text-sm font-semibold text-slate-100">
                Feynman–Kac Transfer Chain: Z = Tr(T_4D^L_t)
              </h2>
              <div className="font-mono text-[11px] text-slate-400">
                slice4DFieldEquiv: U_sl(t) + temporal g_tm(t)
              </div>
            </div>
            <div className="flex items-center gap-2">
              <div className="flex rounded border border-slate-800 bg-slate-800 p-0.5 font-mono text-xs">
                {[2, 4, 6, 8].map((lt) => (
                  <button
                    key={lt}
                    type="button"
                    onClick={() => setLtSlices(lt)}
                    className={`rounded px-2 py-0.5 ${
                      ltSlices === lt ? 'bg-slate-900 text-white' : 'text-slate-300'
                    }`}
                  >
                    L_t={lt}
                  </button>
                ))}
              </div>
              <button
                type="button"
                onClick={() => setShowMirror((m) => !m)}
                className={`rounded border px-2 py-1 font-mono text-xs ${
                  showMirror
                    ? 'border-emerald-500 bg-emerald-500/10 text-emerald-400'
                    : 'border-slate-800 bg-slate-900 text-slate-400'
                }`}
              >
                Mirror Θ
              </button>
            </div>
          </div>

          <svg viewBox="0 0 330 260" className="mt-3 w-full rounded bg-slate-950" role="img" aria-label="Animated Feynman-Kac transfer chain">
            {/* Periodic ring */}
            <ellipse
              cx="165"
              cy="128"
              rx="105"
              ry="76"
              fill="none"
              stroke="#334155"
              strokeWidth="2"
              strokeDasharray="4 4"
            />

            {/* Reflection plane bisecting vertical axis */}
            {showMirror && (
              <>
                <line
                  x1="165"
                  y1="20"
                  x2="165"
                  y2="236"
                  stroke="#fbbf24"
                  strokeWidth="2"
                  strokeDasharray="6 4"
                />
                <text x="165" y="15" textAnchor="middle" className="fill-amber-400 font-mono text-[10px] font-semibold">
                  Θ Time-Reflection Plane
                </text>

                {/* Symmetric RP pairing arcs */}
                {sliceNodes
                  .filter((_, idx) => idx > 0 && idx < ltSlices / 2)
                  .map((posNode) => {
                    const negNode = sliceNodes[ltSlices - posNode.t];
                    if (!negNode) return null;
                    return (
                      <line
                        key={`pair-${posNode.t}`}
                        x1={negNode.x}
                        y1={negNode.y}
                        x2={posNode.x}
                        y2={posNode.y}
                        stroke="rgba(251, 191, 36, 0.35)"
                        strokeWidth="1.5"
                        strokeDasharray="3 3"
                      />
                    );
                  })}
              </>
            )}

            {/* Transfer pulse */}
            <circle cx={pulseSlicePos.x} cy={pulseSlicePos.y} r="8" fill="#38bdf8" opacity="0.28" />
            <circle cx={pulseSlicePos.x} cy={pulseSlicePos.y} r="4.5" fill="#38bdf8" />

            {/* Slice nodes */}
            {sliceNodes.map((n) => (
              <g key={n.t}>
                <rect
                  x={n.x - 19}
                  y={n.y - 12}
                  width="38"
                  height="24"
                  rx="4"
                  fill={showMirror ? (n.isPos ? '#1e3a8a' : '#78350f') : '#0f172a'}
                  stroke={showMirror ? (n.isPos ? '#60a5fa' : '#fbbf24') : '#64748b'}
                  strokeWidth="1.5"
                />
                <text
                  x={n.x}
                  y={n.y + 4}
                  textAnchor="middle"
                  className="fill-white font-mono text-[10px] font-semibold"
                >
                  U({n.t})
                </text>
              </g>
            ))}

            <text x="165" y="250" textAnchor="middle" className="fill-slate-400 font-mono text-[9.5px]">
              K_4D(U_t, U_t+1) · temporal Haar links g_tm(t)
            </text>
          </svg>
        </div>

        {/* RIGHT FIGURE: Interactive Ising Radial Obstruction Heatmap */}
        <div className="rounded-lg border border-slate-800 bg-slate-900 p-5 lg:col-span-6">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div>
              <h2 className="text-sm font-semibold text-slate-100">
                Ising Toy Translation Obstruction (§34/§37)
              </h2>
              <div className="font-mono text-[11px] text-slate-400">
                Click spacetime heatmap or animate shift a = (a₀, a₁, 0, 0)
              </div>
            </div>

            <div className="flex items-center gap-1.5">
              <button
                type="button"
                onClick={() => setAutoSweep((s) => !s)}
                className={`rounded border px-2.5 py-1 font-mono text-xs ${
                  autoSweep
                    ? 'border-emerald-500 bg-emerald-500/10 text-emerald-400'
                    : 'border-slate-800 bg-slate-800 text-slate-300'
                }`}
              >
                {autoSweep ? 'Orbiting a' : 'Auto Sweep'}
              </button>
              <button
                type="button"
                onClick={() => {
                  setAutoSweep(false);
                  setProbeA0(1.0);
                  setProbeA1(0.0);
                }}
                className="rounded border border-slate-800 bg-slate-900 px-2.5 py-1 font-mono text-xs text-slate-300 hover:bg-slate-700"
              >
                a=(1,0)
              </button>
            </div>
          </div>

          <div className="mt-3 grid grid-cols-1 items-center gap-4 sm:grid-cols-12">
            <div className="sm:col-span-7">
              <canvas
                ref={heatmapCanvasRef}
                onClick={handleHeatmapClick}
                className="w-full cursor-crosshair rounded border border-slate-800"
              />
            </div>

            <div className="space-y-3 sm:col-span-5">
              <div className="rounded border border-slate-800 bg-slate-800 p-3">
                <div className="font-mono text-[10px] uppercase tracking-wider text-slate-400">
                  Origin S₂(0, 0)
                </div>
                <div className="font-mono text-xl font-semibold text-emerald-400 tabular-nums">
                  {isingCheck.unshiftedS2.toFixed(4)}
                </div>
              </div>

              <div className="rounded border border-slate-800 bg-slate-800 p-3">
                <div className="font-mono text-[10px] uppercase tracking-wider text-slate-400">
                  Shifted S₂({probeA0}, {probeA1})
                </div>
                <div
                  className={`font-mono text-xl font-semibold tabular-nums ${
                    isingCheck.translationInvariant ? 'text-emerald-400' : 'text-rose-400'
                  }`}
                >
                  {isingCheck.shiftedS2.toFixed(4)}
                </div>
                <div className="mt-1 h-2 w-full overflow-hidden rounded bg-slate-200">
                  <div
                    className={`h-full transition-all ${
                      isingCheck.translationInvariant ? 'bg-emerald-600' : 'bg-rose-600'
                    }`}
                    style={{ width: `${Math.max(5, (isingCheck.shiftedS2 - 1) * 100)}%` }}
                  />
                </div>
              </div>

              <div
                className={`font-mono text-xs font-semibold ${
                  isingCheck.translationInvariant ? 'text-emerald-400' : 'text-rose-400'
                }`}
              >
                {isingCheck.translationInvariant
                  ? '● At origin (a = 0)'
                  : `✖ ΔS₂ = ${isingCheck.delta.toFixed(4)} ≠ 0`}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
