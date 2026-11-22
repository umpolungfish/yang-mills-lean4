import { useEffect, useMemo, useRef, useState } from 'react';
import { Pause, Play, RotateCcw } from 'lucide-react';
import {
  DOBRUSHIN_CRITICAL_BETA,
  STANDARD_BETA0,
  dobrushinClusterBound,
  dobrushinMetrics,
  generateDobrushinDecayCurve,
} from '../utils/yangMillsMath';
import {
  buildCentralLinkPlaquettes3D,
  project3D,
  waveRingAmplitude,
} from '../utils/visualSimMath';

type VisualSceneMode = 'plaquette_star' | 'wave_lattice';

const PLANE_COLORS = [
  { fill: 'rgba(37, 99, 235, 0.14)', stroke: '#2563eb', name: 'x–y plane (±2)' },
  { fill: 'rgba(2, 132, 199, 0.14)', stroke: '#0284c7', name: 'x–z plane (±2)' },
  { fill: 'rgba(217, 119, 6, 0.14)', stroke: '#d97706', name: 'x–t 4th axis (±2)' },
] as const;

export function DobrushinVisualLab() {
  const [beta, setBeta] = useState<number>(STANDARD_BETA0);
  const [distanceD, setDistanceD] = useState<number>(6);
  const [sceneMode, setSceneMode] = useState<VisualSceneMode>('plaquette_star');
  const [playing, setPlaying] = useState<boolean>(true);
  const [autoRotate, setAutoRotate] = useState<boolean>(true);
  const [yaw, setYaw] = useState<number>(0.58);
  const [pitch, setPitch] = useState<number>(0.42);
  const [dragOrigin, setDragOrigin] = useState<{ x: number; y: number } | null>(null);

  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const phaseRef = useRef<number>(0);

  const metrics = useMemo(() => dobrushinMetrics(beta), [beta]);
  const curve = useMemo(() => generateDobrushinDecayCurve(beta, 12, 4), [beta]);
  const boundAtD = useMemo(() => dobrushinClusterBound(beta, distanceD, 4, 1, 1), [beta, distanceD]);
  const plaquettes = useMemo(() => buildCentralLinkPlaquettes3D(), []);

  // 60fps animation loop for Canvas
  useEffect(() => {
    let rafId = 0;
    let lastTime = performance.now();

    const renderFrame = (now: number) => {
      const dt = Math.max(0, Math.min(0.05, (now - lastTime) / 1000));
      lastTime = now;

      if (playing) {
        phaseRef.current += dt * 1.6;
        if (autoRotate && !dragOrigin && sceneMode === 'plaquette_star') {
          setYaw((y) => y + dt * 0.32);
        }
      }

      const canvas = canvasRef.current;
      if (canvas) {
        const ctx = canvas.getContext('2d');
        if (ctx) {
          const dpr = window.devicePixelRatio || 1;
          const rect = canvas.getBoundingClientRect();
          const targetW = Math.max(320, Math.floor(rect.width * dpr));
          const targetH = Math.max(260, Math.floor(rect.height * dpr));
          if (canvas.width !== targetW || canvas.height !== targetH) {
            canvas.width = targetW;
            canvas.height = targetH;
          }
          ctx.save();
          ctx.scale(dpr, dpr);
          const w = rect.width;
          const h = rect.height;

          // Clear clean studio backdrop
          ctx.fillStyle = '#0b1120';
          ctx.fillRect(0, 0, w, h);

          // Subtle coordinate grid
          ctx.strokeStyle = 'rgba(148, 163, 184, 0.08)';
          ctx.lineWidth = 1;
          for (let gx = 0; gx < w; gx += 32) {
            ctx.beginPath();
            ctx.moveTo(gx, 0);
            ctx.lineTo(gx, h);
            ctx.stroke();
          }
          for (let gy = 0; gy < h; gy += 32) {
            ctx.beginPath();
            ctx.moveTo(0, gy);
            ctx.lineTo(w, gy);
            ctx.stroke();
          }

          if (sceneMode === 'plaquette_star') {
            drawPlaquetteStar(ctx, w, h, yaw, pitch, phaseRef.current, beta, plaquettes);
          } else {
            drawWaveLattice(ctx, w, h, phaseRef.current, beta, distanceD);
          }

          ctx.restore();
        }
      }

      rafId = requestAnimationFrame(renderFrame);
    };

    rafId = requestAnimationFrame(renderFrame);
    return () => cancelAnimationFrame(rafId);
  }, [playing, autoRotate, dragOrigin, sceneMode, yaw, pitch, beta, distanceD, plaquettes]);

  // SVG decay figure coordinates
  const svgW = 540;
  const svgH = 210;
  const padL = 48;
  const padR = 16;
  const padT = 18;
  const padB = 30;
  const plotW = svgW - padL - padR;
  const plotH = svgH - padT - padB;

  const yForLog = (val: number) => {
    if (!Number.isFinite(val) || val <= 0) return padT + plotH;
    const l = Math.max(-5, Math.min(2, Math.log10(val)));
    return padT + plotH * (1 - (l + 5) / 7);
  };
  const xForD = (d: number) => padL + ((d - 1) / 11) * plotW;

  const boundPath =
    metrics.regime === 'contractive'
      ? curve
          .filter((p) => Number.isFinite(p.bound) && p.bound > 0)
          .map((p, i) => `${i === 0 ? 'M' : 'L'} ${xForD(p.d).toFixed(1)} ${yForLog(p.bound).toFixed(1)}`)
          .join(' ')
      : '';

  const areaPath =
    boundPath && metrics.regime === 'contractive'
      ? `${boundPath} L ${xForD(12).toFixed(1)} ${(padT + plotH).toFixed(1)} L ${xForD(1).toFixed(1)} ${(padT + plotH).toFixed(1)} Z`
      : '';

  return (
    <div className="space-y-5">
      {/* Compact Visual Header + Quick Presets */}
      <div className="flex flex-wrap items-center justify-between gap-4 rounded-lg border border-slate-800 bg-slate-900 px-5 py-3.5">
        <div>
          <div className="font-mono text-[11px] uppercase tracking-wider text-slate-400">
            §43–§44 · 4D Plaquette Neighborhood &amp; Dobrushin Contraction
          </div>
          <h1 className="text-lg font-semibold text-slate-100">
            6 Plaquettes · 18 Neighbors · Exponential Mass Gap Wave
          </h1>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <button
            type="button"
            onClick={() => setBeta(STANDARD_BETA0)}
            className={`rounded border px-2.5 py-1 font-mono text-xs ${
              Math.abs(beta - STANDARD_BETA0) < 1e-6
                ? 'border-emerald-500 bg-emerald-500/10 font-semibold text-emerald-300'
                : 'border-slate-800 bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            β₀ = 1/300 (Proved)
          </button>
          <button
            type="button"
            onClick={() => setBeta(0.0018)}
            className="rounded border border-slate-800 bg-slate-800 px-2.5 py-1 font-mono text-xs text-slate-300 hover:bg-slate-700"
          >
            Deep Strong (0.0018)
          </button>
          <button
            type="button"
            onClick={() => setBeta(0.0046)}
            className="rounded border border-slate-800 bg-slate-800 px-2.5 py-1 font-mono text-xs text-slate-300 hover:bg-slate-700"
          >
            Near Critical (0.0046)
          </button>
          <button
            type="button"
            onClick={() => setBeta(0.0064)}
            className="rounded border border-slate-800 bg-slate-800 px-2.5 py-1 font-mono text-xs text-rose-400 hover:bg-rose-500/10"
          >
            Supercritical α&gt;1 (0.0064)
          </button>
        </div>
      </div>

      {/* Main Split: Animated 3D/4D Canvas (7 cols) + Live Controls & Curve Figure (5 cols) */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-12">
        {/* LEFT: 60fps Animated Canvas Stage */}
        <div className="flex flex-col overflow-hidden rounded-lg border border-slate-800 bg-slate-950 lg:col-span-7">
          {/* Canvas Toolbar */}
          <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 bg-slate-900 px-4 py-2.5">
            <div className="flex items-center gap-1.5">
              <button
                type="button"
                onClick={() => setSceneMode('plaquette_star')}
                className={`rounded px-2.5 py-1 font-mono text-xs transition-colors ${
                  sceneMode === 'plaquette_star'
                    ? 'bg-emerald-600 text-white'
                    : 'bg-slate-800 text-slate-300 hover:text-white'
                }`}
              >
                3D+t Plaquette Star (1→6→18)
              </button>
              <button
                type="button"
                onClick={() => setSceneMode('wave_lattice')}
                className={`rounded px-2.5 py-1 font-mono text-xs transition-colors ${
                  sceneMode === 'wave_lattice'
                    ? 'bg-emerald-600 text-white'
                    : 'bg-slate-800 text-slate-300 hover:text-white'
                }`}
              >
                Dobrushin Correlation Wave
              </button>
            </div>

            <div className="flex items-center gap-1.5">
              <button
                type="button"
                onClick={() => setPlaying((p) => !p)}
                aria-label={playing ? 'Pause animation' : 'Play animation'}
                className="inline-flex items-center gap-1 rounded border border-slate-700 bg-slate-800 px-2.5 py-1 font-mono text-xs text-slate-200 hover:bg-slate-700"
              >
                {playing ? <Pause className="h-3.5 w-3.5" /> : <Play className="h-3.5 w-3.5" />}
                {playing ? 'Pause' : 'Play'}
              </button>
              {sceneMode === 'plaquette_star' && (
                <>
                  <button
                    type="button"
                    onClick={() => setAutoRotate((r) => !r)}
                    className={`rounded border px-2 py-1 font-mono text-xs ${
                      autoRotate
                        ? 'border-cyan-600/60 bg-cyan-950/60 text-cyan-300'
                        : 'border-slate-700 bg-slate-800 text-slate-300'
                    }`}
                  >
                    Orbit
                  </button>
                  <button
                    type="button"
                    aria-label="Reset camera"
                    onClick={() => {
                      setYaw(0.58);
                      setPitch(0.42);
                    }}
                    className="rounded border border-slate-700 bg-slate-800 p-1.5 text-slate-300 hover:text-white"
                  >
                    <RotateCcw className="h-3.5 w-3.5" />
                  </button>
                </>
              )}
            </div>
          </div>

          {/* Interactive Canvas */}
          <div className="relative flex-1">
            <canvas
              ref={canvasRef}
              onPointerDown={(e) => setDragOrigin({ x: e.clientX, y: e.clientY })}
              onPointerMove={(e) => {
                if (!dragOrigin || sceneMode !== 'plaquette_star') return;
                const dx = e.clientX - dragOrigin.x;
                const dy = e.clientY - dragOrigin.y;
                setYaw((v) => v + dx * 0.009);
                setPitch((v) => Math.max(-1.2, Math.min(1.2, v + dy * 0.009)));
                setDragOrigin({ x: e.clientX, y: e.clientY });
              }}
              onPointerUp={() => setDragOrigin(null)}
              onPointerLeave={() => setDragOrigin(null)}
              className={`h-[390px] w-full ${
                sceneMode === 'plaquette_star' ? 'cursor-grab active:cursor-grabbing' : 'cursor-crosshair'
              }`}
            />

            {/* Floating HUD Legend */}
            <div className="pointer-events-none absolute bottom-3 left-3 right-3 flex flex-wrap items-center justify-between gap-2 rounded bg-slate-900/80 px-3 py-2 font-mono text-[11px] text-slate-300 backdrop-blur-xs">
              {sceneMode === 'plaquette_star' ? (
                <>
                  <div className="flex flex-wrap items-center gap-3">
                    <span className="text-rose-400">━ Target Link e</span>
                    {PLANE_COLORS.map((pl) => (
                      <span key={pl.name} style={{ color: pl.stroke }}>
                        ■ {pl.name}
                      </span>
                    ))}
                  </div>
                  <span className="text-slate-400">Drag to rotate 3D+t star · 18 outer links</span>
                </>
              ) : (
                <>
                  <span>Source S_f (hop 0) → Target S_g (hop D={distanceD})</span>
                  <span className={metrics.alpha < 1 ? 'text-emerald-400' : 'text-rose-400'}>
                    {metrics.alpha < 1
                      ? `Wave damped by ρ^D = ${Math.pow(metrics.rho, distanceD).toFixed(4)}`
                      : 'α ≥ 1: Fluctuations percolate (bound lost)'}
                  </span>
                </>
              )}
            </div>
          </div>
        </div>

        {/* RIGHT: Live Parameter Deck + Animated Clustering Curve */}
        <div className="space-y-4 lg:col-span-5">
          {/* Live Numerical Telemetry Strip */}
          <div className="grid grid-cols-3 gap-2.5">
            <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
              <div className="font-mono text-[10px] uppercase tracking-wider text-slate-400">
                α = 18(1−e⁻¹²ᵝ)
              </div>
              <div
                className={`mt-1 font-mono text-xl font-semibold tabular-nums ${
                  metrics.alpha < 1 ? 'text-emerald-400' : 'text-rose-400'
                }`}
              >
                {metrics.alpha.toFixed(4)}
              </div>
              <div className="font-mono text-[10px] text-slate-400">
                {metrics.alpha < 1 ? '● α < 1 Contractive' : '✖ α ≥ 1 Breakdown'}
              </div>
            </div>

            <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
              <div className="font-mono text-[10px] uppercase tracking-wider text-slate-400">
                Mass Gap m(β)
              </div>
              <div className="mt-1 font-mono text-xl font-semibold text-emerald-400 tabular-nums">
                {metrics.clusterRate && Number.isFinite(metrics.clusterRate)
                  ? metrics.clusterRate.toFixed(4)
                  : '—'}
              </div>
              <div className="font-mono text-[10px] text-slate-400">−½ log α</div>
            </div>

            <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
              <div className="font-mono text-[10px] uppercase tracking-wider text-slate-400">
                Bound (D={distanceD})
              </div>
              <div className="mt-1 font-mono text-xl font-semibold text-slate-100 tabular-nums">
                {boundAtD === null ? '∞' : boundAtD.toFixed(3)}
              </div>
              <div className="font-mono text-[10px] text-slate-400">
                ρ = {metrics.rho.toFixed(3)}
              </div>
            </div>
          </div>

          {/* Sliders */}
          <div className="space-y-3.5 rounded-lg border border-slate-800 bg-slate-900 p-4">
            <div>
              <div className="flex justify-between text-xs font-medium">
                <label htmlFor="dob-beta" className="text-slate-300">
                  Inverse Coupling β
                </label>
                <span className="font-mono font-semibold text-slate-100 tabular-nums">
                  {beta.toFixed(5)} (β_crit ≈ {DOBRUSHIN_CRITICAL_BETA.toFixed(5)})
                </span>
              </div>
              <input
                id="dob-beta"
                type="range"
                min={0}
                max={0.008}
                step={0.00005}
                value={beta}
                onChange={(e) => setBeta(Number(e.target.value))}
                className="mt-1.5 w-full accent-emerald-500"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs font-medium">
                <label htmlFor="dob-dist" className="text-slate-300">
                  Graph Separation D
                </label>
                <span className="font-mono font-semibold text-slate-100 tabular-nums">
                  {distanceD} hops
                </span>
              </div>
              <input
                id="dob-dist"
                type="range"
                min={1}
                max={12}
                step={1}
                value={distanceD}
                onChange={(e) => setDistanceD(Number(e.target.value))}
                className="mt-1.5 w-full accent-emerald-500"
              />
            </div>
          </div>

          {/* SVG Decay Curve Figure */}
          <div className="rounded-lg border border-slate-800 bg-slate-900 p-3.5">
            <div className="mb-1 flex items-center justify-between font-mono text-[11px] text-slate-400">
              <span>|S²(f,g) − S¹(f)S¹(g)| ≤ C(β)·4·ρ^D</span>
              <span className="tabular-nums">D = 1…12</span>
            </div>
            <svg
              viewBox={`0 0 ${svgW} ${svgH}`}
              className="w-full"
              role="img"
              aria-label="Exponential clustering upper bound curve"
            >
              {[-5, -3, -1, 1].map((exp) => {
                const y = yForLog(Math.pow(10, exp));
                return (
                  <g key={exp}>
                    <line
                      x1={padL}
                      x2={svgW - padR}
                      y1={y}
                      y2={y}
                      stroke="#334155"
                      strokeDasharray="3 3"
                    />
                    <text x={padL - 6} y={y + 3} textAnchor="end" className="fill-slate-400 font-mono text-[9px]">
                      10^{exp}
                    </text>
                  </g>
                );
              })}

              {curve.map((pt) => (
                <text
                  key={pt.d}
                  x={xForD(pt.d)}
                  y={svgH - 8}
                  textAnchor="middle"
                  className="fill-slate-400 font-mono text-[9px]"
                >
                  {pt.d}
                </text>
              ))}

              {metrics.regime === 'contractive' ? (
                <>
                  <path d={areaPath} fill="rgba(16, 185, 129, 0.12)" />
                  <path d={boundPath} fill="none" stroke="#34d399" strokeWidth={2.5} />
                  <line
                    x1={xForD(distanceD)}
                    x2={xForD(distanceD)}
                    y1={padT}
                    y2={padT + plotH}
                    stroke="#22d3ee"
                    strokeDasharray="3 3"
                  />
                  {curve.map((pt) => (
                    <circle
                      key={pt.d}
                      cx={xForD(pt.d)}
                      cy={yForLog(pt.bound)}
                      r={pt.d === distanceD ? 5 : 2.5}
                      className={
                        pt.d === distanceD
                          ? 'fill-cyan-500 stroke-white stroke-2'
                          : 'fill-emerald-400'
                      }
                    />
                  ))}
                </>
              ) : (
                <text
                  x={padL + plotW / 2}
                  y={padT + plotH / 2}
                  textAnchor="middle"
                  className="fill-rose-600 font-mono text-xs font-semibold"
                >
                  α = {metrics.alpha.toFixed(3)} ≥ 1 · Dobrushin contraction fails
                </text>
              )}
            </svg>
          </div>
        </div>
      </div>
    </div>
  );
}

function drawPlaquetteStar(
  ctx: CanvasRenderingContext2D,
  w: number,
  h: number,
  yaw: number,
  pitch: number,
  phase: number,
  beta: number,
  plaquettes: ReturnType<typeof buildCentralLinkPlaquettes3D>,
) {
  const cx = w / 2;
  const cy = h / 2;
  const m = dobrushinMetrics(beta);
  const waveAmp = 0.45 + 0.55 * Math.sin(phase * 2.5);

  // Project and draw the 6 semi-transparent orthogonal plaquettes + their 18 outer links
  for (const pl of plaquettes) {
    const style = PLANE_COLORS[pl.planeIndex];
    const pts = pl.corners.map((c) => project3D(c, yaw, pitch, 520, 4.4, cx, cy));

    // Fill plaquette sheet
    ctx.beginPath();
    ctx.moveTo(pts[0].x, pts[0].y);
    ctx.lineTo(pts[1].x, pts[1].y);
    ctx.lineTo(pts[2].x, pts[2].y);
    ctx.lineTo(pts[3].x, pts[3].y);
    ctx.closePath();
    ctx.fillStyle = style.fill;
    ctx.fill();

    // Draw the 3 outer neighbor links (edges 1-2, 2-3, 3-0)
    const neighborAlpha = m.regime === 'contractive' ? 0.35 + 0.5 * m.rho * waveAmp : 0.9;
    ctx.strokeStyle = style.stroke;
    ctx.globalAlpha = neighborAlpha;
    ctx.lineWidth = 2.2;
    for (const [a, b] of [
      [1, 2],
      [2, 3],
      [3, 0],
    ]) {
      ctx.beginPath();
      ctx.moveTo(pts[a].x, pts[a].y);
      ctx.lineTo(pts[b].x, pts[b].y);
      ctx.stroke();

      // Traveling pulse particle along neighbor link
      const t = ((phase * 0.45 + a * 0.25) % 1 + 1) % 1;
      const px = pts[a].x + (pts[b].x - pts[a].x) * t;
      const py = pts[a].y + (pts[b].y - pts[a].y) * t;
      ctx.beginPath();
      ctx.arc(px, py, 2.8, 0, Math.PI * 2);
      ctx.fillStyle = style.stroke;
      ctx.fill();
    }
    ctx.globalAlpha = 1;

    // Draw corner vertices
    for (let i = 2; i <= 3; i++) {
      ctx.beginPath();
      ctx.arc(pts[i].x, pts[i].y, 3.5, 0, Math.PI * 2);
      ctx.fillStyle = '#e2e8f0';
      ctx.fill();
    }
  }

  // Draw glowing central target link e from (-0.5, 0, 0) to (+0.5, 0, 0)
  const pA = project3D({ x: -0.5, y: 0, z: 0 }, yaw, pitch, 520, 4.4, cx, cy);
  const pB = project3D({ x: 0.5, y: 0, z: 0 }, yaw, pitch, 520, 4.4, cx, cy);

  ctx.shadowColor = '#f43f5e';
  ctx.shadowBlur = 14;
  ctx.strokeStyle = '#fb7185';
  ctx.lineWidth = 5;
  ctx.beginPath();
  ctx.moveTo(pA.x, pA.y);
  ctx.lineTo(pB.x, pB.y);
  ctx.stroke();
  ctx.shadowBlur = 0;

  for (const endPt of [pA, pB]) {
    ctx.beginPath();
    ctx.arc(endPt.x, endPt.y, 5.5, 0, Math.PI * 2);
    ctx.fillStyle = '#fff1f2';
    ctx.fill();
  }
}

function drawWaveLattice(
  ctx: CanvasRenderingContext2D,
  w: number,
  h: number,
  phase: number,
  beta: number,
  targetD: number,
) {
  const cols = 13;
  const rows = 9;
  const marginX = 48;
  const marginY = 46;
  const cellW = (w - marginX * 2) / (cols - 1);
  const cellH = (h - marginY * 2) / (rows - 1);

  const srcR = 4;
  const srcC = 1;
  const m = dobrushinMetrics(beta);

  // Draw links on 2D slice colored by waveRingAmplitude(beta, manhattanHop, phase)
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const x = marginX + c * cellW;
      const y = marginY + r * cellH;
      const hop = Math.abs(r - srcR) + Math.abs(c - srcC);
      const amp = waveRingAmplitude(beta, hop, phase);

      const color =
        m.regime === 'supercritical' || m.regime === 'boundary'
          ? `rgba(244, 63, 94, ${0.25 + 0.75 * amp})`
          : `rgba(56, 189, 248, ${0.15 + 0.85 * amp})`;

      // Horizontal link to right
      if (c + 1 < cols) {
        ctx.strokeStyle = color;
        ctx.lineWidth = 1.5 + 3.2 * amp;
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x + cellW, y);
        ctx.stroke();
      }
      // Vertical link downward
      if (r + 1 < rows) {
        ctx.strokeStyle = color;
        ctx.lineWidth = 1.5 + 3.2 * amp;
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x, y + cellH);
        ctx.stroke();
      }
    }
  }

  // Highlight source S_f and target S_g at hop D
  const sx = marginX + srcC * cellW;
  const sy = marginY + srcR * cellH;
  ctx.beginPath();
  ctx.arc(sx, sy, 8, 0, Math.PI * 2);
  ctx.fillStyle = '#34d399';
  ctx.fill();

  const targetC = Math.min(cols - 1, srcC + targetD);
  const tx = marginX + targetC * cellW;
  const ty = marginY + srcR * cellH;
  ctx.beginPath();
  ctx.arc(tx, ty, 8, 0, Math.PI * 2);
  ctx.fillStyle = m.alpha < 1 ? '#38bdf8' : '#f43f5e';
  ctx.fill();

  ctx.font = '600 11px "Fira Code", monospace';
  ctx.fillStyle = '#a7f3d0';
  ctx.textAlign = 'center';
  ctx.fillText('S_f', sx, sy - 14);
  ctx.fillStyle = m.alpha < 1 ? '#bae6fd' : '#fecdd3';
  ctx.fillText(`S_g (D=${targetD})`, tx, ty - 14);
}
