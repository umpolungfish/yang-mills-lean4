import { useEffect, useMemo, useRef, useState } from 'react';
import { Pause, Play } from 'lucide-react';
import {
  type ContinuumPoint4D,
  analyzeStageTupleInjectivity,
  plaquetteCDFQuantile,
  stageScalingParams,
  suClosureGapErrorMetrics,
} from '../utils/ymProofMath';

type TrajectoryMode = 'balaban' | 'suclosure';

interface TuplePreset {
  id: string;
  label: string;
  note: string;
  pts: [ContinuumPoint4D, ContinuumPoint4D, ContinuumPoint4D, ContinuumPoint4D];
}

const CONTINUUM_PRESETS: TuplePreset[] = [
  {
    id: 'near_cluster',
    label: 'Near-Coincident Pair',
    note: 'x₀ and x₁ differ by Δ = 0.08; they collide at m = 0..10 before separating at m* = 11.',
    pts: [
      [0.42, 0.55, 0, 0],
      [0.5, 0.55, 0, 0],
      [1.35, 1.4, 0, 0],
      [2.1, 0.85, 0, 0],
    ],
  },
  {
    id: 'two_pairs',
    label: 'Two Exact Pairs',
    note: 'x₀ = x₁ and x₂ = x₃: equality classes [2, 2] factorize to iidMom(2)² = 25/4 = 6.25.',
    pts: [
      [0.6, 0.6, 0, 0],
      [0.6, 0.6, 0, 0],
      [1.6, 1.5, 0, 0],
      [1.6, 1.5, 0, 0],
    ],
  },
  {
    id: 'all_coincident',
    label: '4-Point Coincident',
    note: 'All 4 insertions coincide at x₀: witnesses non-Gaussian connected cumulant S₄ᶜ = -1/8.',
    pts: [
      [0.9, 0.9, 0, 0],
      [0.9, 0.9, 0, 0],
      [0.9, 0.9, 0, 0],
      [0.9, 0.9, 0, 0],
    ],
  },
  {
    id: 'generic_four',
    label: '4 Distinct Insertions',
    note: 'All 4 distinct points separate into distinct wrapped sites with zero finite-volume error for m ≥ m*.',
    pts: [
      [0.3, 0.4, 0, 0],
      [0.85, 1.45, 0, 0],
      [1.65, 0.55, 0, 0],
      [1.8, 1.7, 0, 0],
    ],
  },
];

const PT_COLORS = ['#34d399', '#38bdf8', '#fbbf24', '#fb7185'] as const;

export function ContinuumStageLab() {
  const [mode, setMode] = useState<TrajectoryMode>('balaban');
  const [stageM, setStageM] = useState<number>(6);
  const [suMExp, setSuMExp] = useState<number>(18); // slider index 0..30 mapped to exponential scale up to ~2*M0
  const [suN, setSuN] = useState<number>(3);
  const [presetId, setPresetId] = useState<string>('near_cluster');
  const [x1Offset, setX1Offset] = useState<number>(0.5);
  const [playing, setPlaying] = useState<boolean>(false);
  const [traceNorm, setTraceNorm] = useState<number>(0.25);
  const [hoverCell, setHoverCell] = useState<{ gx: number; gy: number } | null>(null);
  const [hoverCurveIdx, setHoverCurveIdx] = useState<number | null>(null);

  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  const activePreset = useMemo(
    () => CONTINUUM_PRESETS.find((p) => p.id === presetId) ?? CONTINUUM_PRESETS[0],
    [presetId],
  );

  const activePoints = useMemo<ContinuumPoint4D[]>(() => {
    const pts = activePreset.pts.map((p) => [...p] as ContinuumPoint4D);
    if (presetId === 'near_cluster') {
      pts[1][0] = x1Offset;
    }
    return pts;
  }, [activePreset, presetId, x1Offset]);

  // Mapped SUClosure stage m from slider 0..30
  const suClosureM = useMemo(() => {
    const baseMetrics = suClosureGapErrorMetrics(suN, 0);
    if (suMExp <= 10) return suMExp * 25;
    const frac = (suMExp - 10) / 20;
    return Math.round(250 + frac * (baseMetrics.m0Threshold * 1.4 - 250));
  }, [suMExp, suN]);

  useEffect(() => {
    if (!playing) return;
    const id = window.setInterval(() => {
      if (mode === 'balaban') {
        setStageM((m) => (m >= 24 ? 0 : m + 1));
      } else {
        setSuMExp((idx) => (idx >= 30 ? 0 : idx + 1));
      }
    }, 520);
    return () => window.clearInterval(id);
  }, [playing, mode]);

  const balabanScaling = useMemo(() => stageScalingParams(stageM), [stageM]);
  const tupleAnalysis = useMemo(
    () => analyzeStageTupleInjectivity(activePoints, stageM, 36),
    [activePoints, stageM],
  );
  const suMetrics = useMemo(() => suClosureGapErrorMetrics(suN, suClosureM), [suN, suClosureM]);
  const cdfReadout = useMemo(
    () => plaquetteCDFQuantile(traceNorm, balabanScaling.beta),
    [traceNorm, balabanScaling.beta],
  );

  // Dual-curve telemetry samples
  const curveSamples = useMemo(() => {
    if (mode === 'balaban') {
      return Array.from({ length: 25 }, (_, m) => {
        const sc = stageScalingParams(m);
        const tup = analyzeStageTupleInjectivity(activePoints, m, 36);
        return {
          idx: m,
          label: `m=${m}`,
          primary: sc.latticeSpacing, // a_m = 1/(m+2)
          secondary: tup.finiteVolumeError, // |S_m - S_iid|
          extra: `L=${sc.periodicSide} · collisions=${tup.collisionCount}`,
        };
      });
    }
    const base = suClosureGapErrorMetrics(suN, 0);
    return Array.from({ length: 25 }, (_, i) => {
      const mVal = Math.max(10, Math.round(((i + 1) / 25) * base.m0Threshold * 1.4));
      const met = suClosureGapErrorMetrics(suN, mVal);
      return {
        idx: mVal,
        label: `m=${mVal.toLocaleString()}`,
        primary: Math.min(2.5, met.errorEnvelope),
        secondary: 0.5, // contractive threshold err <= 1/2
        extra: `err=${met.errorEnvelope.toFixed(3)} · ${met.contractiveRegion ? 'err ≤ 1/2' : 'pre-M₀'}`,
      };
    });
  }, [mode, activePoints, suN]);

  // Draw 2D periodic torus slice (Z / L_m Z)^2
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    const tw = Math.max(320, Math.floor(rect.width * dpr));
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

    const pad = 34;
    const boxSize = Math.min(w - pad * 2, h - pad * 2);
    const ox = (w - boxSize) / 2;
    const oy = (h - pad - boxSize) / 2 + 6;

    const L = mode === 'balaban' ? tupleAnalysis.L : Math.min(36, Math.max(4, Math.round(Math.sqrt(suMetrics.L))));

    // Draw lattice grid (decimate lines cleanly when L is large)
    const step = L <= 24 ? 1 : Math.ceil(L / 24);
    ctx.strokeStyle = 'rgba(148, 163, 184, 0.14)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= L; i += step) {
      const px = ox + (i / L) * boxSize;
      const py = oy + (i / L) * boxSize;
      ctx.beginPath();
      ctx.moveTo(px, oy);
      ctx.lineTo(px, oy + boxSize);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(ox, py);
      ctx.lineTo(ox + boxSize, py);
      ctx.stroke();
    }

    // Outer torus boundary
    ctx.strokeStyle = mode === 'balaban' ? '#10b981' : '#06b6d4';
    ctx.lineWidth = 1.6;
    ctx.strokeRect(ox, oy, boxSize, boxSize);

    // Highlight hovered lattice cell
    if (hoverCell && hoverCell.gx >= 0 && hoverCell.gx < L && hoverCell.gy >= 0 && hoverCell.gy < L) {
      const cw = boxSize / L;
      const cx = ox + hoverCell.gx * cw;
      const cy = oy + (L - 1 - hoverCell.gy) * cw;
      ctx.fillStyle = 'rgba(6, 182, 212, 0.22)';
      ctx.fillRect(cx, cy, Math.max(4, cw), Math.max(4, cw));
    }

    if (mode === 'balaban') {
      // Group wrapped lattice coordinates to detect distinct continuum points colliding at finite m
      const cellCounts = new Map<string, number[]>();
      tupleAnalysis.wrappedSites.forEach((ws, idx) => {
        const key = `${ws.latticeCoords[0]},${ws.latticeCoords[1]}`;
        const arr = cellCounts.get(key) ?? [];
        arr.push(idx);
        cellCounts.set(key, arr);
      });

      const cw = boxSize / L;
      tupleAnalysis.wrappedSites.forEach((ws, idx) => {
        const gx = ws.latticeCoords[0];
        const gy = ws.latticeCoords[1];
        const key = `${gx},${gy}`;
        const occupants = cellCounts.get(key) ?? [idx];
        const distinctContInSameCell = new Set(
          occupants.map((oIdx) => activePoints[oIdx].map((v) => v.toFixed(4)).join(',')),
        ).size > 1;

        const cx = ox + (gx + 0.5) * cw;
        const cy = oy + (L - 1 - gy + 0.5) * cw;

        // Cell highlight
        ctx.fillStyle = distinctContInSameCell ? 'rgba(244, 63, 94, 0.28)' : 'rgba(16, 185, 129, 0.20)';
        ctx.fillRect(ox + gx * cw, oy + (L - 1 - gy) * cw, Math.max(5, cw), Math.max(5, cw));

        if (distinctContInSameCell) {
          ctx.beginPath();
          ctx.arc(cx, cy, 13, 0, Math.PI * 2);
          ctx.strokeStyle = '#fb7185';
          ctx.lineWidth = 1.6;
          ctx.setLineDash([3, 2]);
          ctx.stroke();
          ctx.setLineDash([]);
        }

        // Offset marker slightly if multiple points share site
        const rankInCell = occupants.indexOf(idx);
        const angle = (rankInCell / Math.max(1, occupants.length)) * Math.PI * 2;
        const spread = occupants.length > 1 ? 6 : 0;
        const px = cx + Math.cos(angle) * spread;
        const py = cy + Math.sin(angle) * spread;

        ctx.beginPath();
        ctx.arc(px, py, 5.2, 0, Math.PI * 2);
        ctx.fillStyle = PT_COLORS[idx % PT_COLORS.length];
        ctx.fill();
        ctx.strokeStyle = '#070b14';
        ctx.lineWidth = 1.4;
        ctx.stroke();

        if (rankInCell === 0) {
          const combinedNames = occupants.map((oIdx) => `x${oIdx}`).join(',');
          const label = `${combinedNames} (${gx},${gy})`;
          const clearance = occupants.length > 1 ? 16 : 10;
          const labelX = Math.min(w - 96, cx + clearance);
          const labelY = Math.max(oy + 14, Math.min(oy + boxSize - 6, cy - (gy === 0 ? 6 : 0) + 3));
          ctx.font = '600 10px "IBM Plex Mono", monospace';
          const tw = ctx.measureText(label).width;
          ctx.fillStyle = 'rgba(7, 11, 20, 0.82)';
          ctx.fillRect(labelX - 3, labelY - 10, tw + 6, 13);
          ctx.fillStyle = distinctContInSameCell ? '#fda4af' : '#e2e8f0';
          ctx.textAlign = 'left';
          ctx.fillText(label, labelX, labelY);
        }
      });
    } else {
      // SUClosure weak-coupling field alignment visualization
      const cw = boxSize / L;
      const alignOrder = suMetrics.contractiveRegion
        ? Math.max(0.05, Math.min(0.45, suMetrics.errorEnvelope * 0.4))
        : 0.9;
      for (let gx = 0; gx < L; gx++) {
        for (let gy = 0; gy < L; gy++) {
          const cx = ox + (gx + 0.5) * cw;
          const cy = oy + (gy + 0.5) * cw;
          const jitter = Math.sin(gx * 12.9898 + gy * 78.233 + suClosureM) * alignOrder;
          const len = Math.max(3, cw * 0.34);
          ctx.strokeStyle = suMetrics.contractiveRegion ? 'rgba(34, 211, 238, 0.72)' : 'rgba(245, 158, 11, 0.65)';
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.moveTo(cx, cy);
          ctx.lineTo(cx + Math.cos(jitter) * len, cy - Math.sin(jitter) * len);
          ctx.stroke();
        }
      }
    }

    ctx.font = '500 10px "IBM Plex Mono", monospace';
    ctx.fillStyle = '#94a3b8';
    ctx.textAlign = 'left';
    ctx.fillText(
      mode === 'balaban'
        ? `(ℤ/${tupleAnalysis.L}ℤ)² slice · a_m = 1/${stageM + 2} · phys box = ${stageM + 2}`
        : `SU(${suN}) Cubic Torus L_m=${suMetrics.L} · β_m = exp(${suMetrics.logBeta.toLocaleString()})`,
      ox,
      oy - 10,
    );

    ctx.restore();
  }, [mode, tupleAnalysis, activePoints, stageM, suMetrics, suN, suClosureM, hoverCell]);

  const handleCanvasMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const w = rect.width;
    const h = rect.height;
    const pad = 34;
    const boxSize = Math.min(w - pad * 2, h - pad * 2);
    const ox = (w - boxSize) / 2;
    const oy = (h - pad - boxSize) / 2 + 6;
    const L = mode === 'balaban' ? tupleAnalysis.L : Math.min(36, Math.max(4, Math.round(Math.sqrt(suMetrics.L))));

    const nx = (e.clientX - rect.left - ox) / boxSize;
    const ny = (e.clientY - rect.top - oy) / boxSize;
    if (nx >= 0 && nx < 1 && ny >= 0 && ny < 1) {
      setHoverCell({
        gx: Math.floor(nx * L),
        gy: L - 1 - Math.floor(ny * L),
      });
    } else {
      setHoverCell(null);
    }
  };

  // Dual-curve SVG dimensions
  const svgW = 540;
  const svgH = 185;
  const pL = 44;
  const pR = 16;
  const pT = 16;
  const pB = 26;
  const plotW = svgW - pL - pR;
  const plotH = svgH - pT - pB;

  const maxY = mode === 'balaban' ? 2.5 : 2.5;
  const xForI = (i: number) => pL + (i / (curveSamples.length - 1)) * plotW;
  const yForV = (v: number) => pT + plotH * (1 - Math.max(0, Math.min(maxY, v)) / maxY);

  const primaryPath = curveSamples
    .map((s, i) => `${i === 0 ? 'M' : 'L'} ${xForI(i).toFixed(1)} ${yForV(s.primary).toFixed(1)}`)
    .join(' ');
  const secondaryPath = curveSamples
    .map((s, i) => `${i === 0 ? 'M' : 'L'} ${xForI(i).toFixed(1)} ${yForV(s.secondary).toFixed(1)}`)
    .join(' ');

  return (
    <div className="space-y-5">
      {/* Top Calibration Ribbon */}
      <div className="flex flex-wrap items-center justify-between gap-4 rounded-xl border border-slate-800 bg-[#0c1220] px-5 py-3.5">
        <div>
          <div className="font-mono text-[11px] text-emerald-400">
            SchwingerConv.lean (§47) · BalabanFromStage.lean (§48) · SUClosure.lean (§51)
          </div>
          <h2 className="text-lg font-semibold text-white">
            Continuum Stage Scaling, Torus Injectivity &amp; Plaquette-CDF Simulator
          </h2>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <div className="flex rounded-lg border border-slate-800 bg-slate-900 p-0.5 font-mono text-xs">
            <button
              type="button"
              onClick={() => setMode('balaban')}
              className={`rounded-md px-3 py-1 transition-colors ${
                mode === 'balaban' ? 'bg-emerald-600 text-white' : 'text-slate-300 hover:text-white'
              }`}
            >
              Balaban Stage (aₘ=1/(m+2))
            </button>
            <button
              type="button"
              onClick={() => setMode('suclosure')}
              className={`rounded-md px-3 py-1 transition-colors ${
                mode === 'suclosure' ? 'bg-cyan-600 text-white' : 'text-slate-300 hover:text-white'
              }`}
            >
              SUClosure (βₘ=exp((m+1)⁴))
            </button>
          </div>

          <button
            type="button"
            onClick={() => setPlaying((p) => !p)}
            aria-label={playing ? 'Pause stage sweep' : 'Auto-advance stage sweep'}
            className="inline-flex items-center gap-1.5 rounded-lg border border-slate-700 bg-slate-900 px-3 py-1 font-mono text-xs text-slate-200 hover:bg-slate-800"
          >
            {playing ? <Pause className="h-3.5 w-3.5" /> : <Play className="h-3.5 w-3.5" />}
            {playing ? 'Pause Sweep' : 'Sweep Stages'}
          </button>
        </div>
      </div>

      {/* Asymmetric Split Scientific Console */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-12">
        {/* LEFT: Parameter & Probe Deck */}
        <div className="space-y-4 lg:col-span-5">
          {mode === 'balaban' ? (
            <>
              {/* Stage Scrubber */}
              <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4 space-y-3">
                <div className="flex items-center justify-between font-mono text-xs">
                  <label htmlFor="stage-lab-m" className="text-slate-300">
                    Stage Index m (shifted m+1 = {stageM + 1})
                  </label>
                  <span className="font-semibold text-emerald-400 tabular-nums">
                    m = {stageM} · L = {balabanScaling.periodicSide}
                  </span>
                </div>
                <input
                  id="stage-lab-m"
                  type="range"
                  min={0}
                  max={24}
                  step={1}
                  value={stageM}
                  onChange={(e) => setStageM(Number(e.target.value))}
                  className="w-full accent-emerald-500"
                />

                <div className="grid grid-cols-2 gap-2 pt-1 font-mono text-xs tabular-nums">
                  <div className="rounded-lg border border-slate-800 bg-[#070b14] p-2.5">
                    <div className="text-[10px] text-slate-400">Spacing aₘ = 1/(m+2)</div>
                    <div className="mt-0.5 text-base font-bold text-white">
                      {balabanScaling.latticeSpacing.toFixed(4)}
                    </div>
                  </div>
                  <div className="rounded-lg border border-slate-800 bg-[#070b14] p-2.5">
                    <div className="text-[10px] text-slate-400">Injective Threshold m*</div>
                    <div
                      className={`mt-0.5 text-base font-bold ${
                        tupleAnalysis.injectiveOnDistinct ? 'text-emerald-400' : 'text-rose-400'
                      }`}
                    >
                      m* = {tupleAnalysis.firstInjectiveStage}
                    </div>
                  </div>
                </div>
              </div>

              {/* Continuum Tuple & Collision Probe */}
              <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-semibold text-slate-200">
                    Continuum Tuple (x₀, x₁, x₂, x₃)
                  </span>
                  <span
                    className={`font-mono text-[11px] font-semibold ${
                      tupleAnalysis.injectiveOnDistinct ? 'text-emerald-400' : 'text-rose-400'
                    }`}
                  >
                    {tupleAnalysis.injectiveOnDistinct
                      ? '● Injective on distinct pts'
                      : `▲ ${tupleAnalysis.collisionCount} collision(s)`}
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-1.5">
                  {CONTINUUM_PRESETS.map((p) => (
                    <button
                      key={p.id}
                      type="button"
                      onClick={() => setPresetId(p.id)}
                      className={`rounded border px-2 py-1.5 text-left font-mono text-[11px] transition-colors ${
                        presetId === p.id
                          ? 'border-emerald-500 bg-emerald-500/15 text-emerald-300'
                          : 'border-slate-800 bg-[#070b14] text-slate-300 hover:bg-slate-800'
                      }`}
                    >
                      {p.label}
                    </button>
                  ))}
                </div>

                {presetId === 'near_cluster' && (
                  <div>
                    <div className="flex justify-between font-mono text-[11px] text-slate-400 tabular-nums">
                      <label htmlFor="x1-coord-slider">Move x₁₀ relative to x₀₀ = 0.42</label>
                      <span className="text-cyan-300">x₁₀ = {x1Offset.toFixed(2)}</span>
                    </div>
                    <input
                      id="x1-coord-slider"
                      type="range"
                      min={0.44}
                      max={1.15}
                      step={0.01}
                      value={x1Offset}
                      onChange={(e) => setX1Offset(Number(e.target.value))}
                      className="mt-1 w-full accent-cyan-400"
                    />
                  </div>
                )}

                <div className="rounded-lg border border-slate-800 bg-[#070b14] p-2.5 font-mono text-[11px] tabular-nums space-y-1">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Wrapped S_m(x):</span>
                    <span className="font-semibold text-white">{tupleAnalysis.wrappedSchwinger.toFixed(4)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Target iidSchwinger(x):</span>
                    <span className="font-semibold text-emerald-400">
                      {tupleAnalysis.continuumSchwinger.toFixed(4)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">|S_m − S_iid| finite error:</span>
                    <span
                      className={tupleAnalysis.finiteVolumeError > 1e-9 ? 'text-rose-400' : 'text-emerald-400'}
                    >
                      {tupleAnalysis.finiteVolumeError.toFixed(4)}
                    </span>
                  </div>
                </div>
              </div>
            </>
          ) : (
            /* SUClosure Weak-Coupling Mode Controls */
            <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4 space-y-3">
              <div>
                <div className="flex justify-between font-mono text-xs tabular-nums">
                  <label htmlFor="su-rank-slider" className="text-slate-300">
                    Gauge Rank SU(N)
                  </label>
                  <span className="font-semibold text-cyan-300">N = {suN}</span>
                </div>
                <input
                  id="su-rank-slider"
                  type="range"
                  min={2}
                  max={8}
                  step={1}
                  value={suN}
                  onChange={(e) => setSuN(Number(e.target.value))}
                  className="mt-1 w-full accent-cyan-500"
                />
              </div>

              <div>
                <div className="flex justify-between font-mono text-xs tabular-nums">
                  <label htmlFor="su-stage-slider" className="text-slate-300">
                    SUClosure Stage m
                  </label>
                  <span className="font-semibold text-cyan-300">
                    m = {suClosureM.toLocaleString()} (M₀ = {suMetrics.m0Threshold.toLocaleString()})
                  </span>
                </div>
                <input
                  id="su-stage-slider"
                  type="range"
                  min={0}
                  max={30}
                  step={1}
                  value={suMExp}
                  onChange={(e) => setSuMExp(Number(e.target.value))}
                  className="mt-1 w-full accent-cyan-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-2 font-mono text-xs tabular-nums">
                <div className="rounded-lg border border-slate-800 bg-[#070b14] p-2.5">
                  <div className="text-[10px] text-slate-400">cubicGapErr ≤ C_err/x</div>
                  <div
                    className={`mt-0.5 text-base font-bold ${
                      suMetrics.contractiveRegion ? 'text-emerald-400' : 'text-amber-400'
                    }`}
                  >
                    {suMetrics.errorEnvelope.toFixed(4)}
                  </div>
                </div>
                <div className="rounded-lg border border-slate-800 bg-[#070b14] p-2.5">
                  <div className="text-[10px] text-slate-400">−log(1 − err) Upper Bound</div>
                  <div className="mt-0.5 text-base font-bold text-cyan-300">
                    {suMetrics.gapUpperBound !== null ? suMetrics.gapUpperBound.toFixed(4) : 'err ≥ 1'}
                  </div>
                </div>
              </div>
              <div className="rounded border border-slate-800 bg-[#070b14] px-3 py-2 font-mono text-[11px] text-slate-300 tabular-nums">
                C_err({suN}) = {suMetrics.cErr.toLocaleString()} ·{' '}
                {suMetrics.contractiveRegion
                  ? `● m ≥ M₀: 2·C_err/x = ${suMetrics.rescaledBound?.toFixed(4)} → 0`
                  : `▲ Below M₀ threshold (${suMetrics.m0Threshold.toLocaleString()})`}
              </div>
            </div>
          )}

          {/* Plaquette-CDF Quantile Mapper */}
          <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4 space-y-2.5">
            <div className="flex items-center justify-between font-mono text-xs">
              <span className="font-semibold text-slate-200">Plaquette-CDF Rademacher Pushforward</span>
              <span className="text-emerald-400 tabular-nums">O(U) = {cdfReadout.rademacherVal}</span>
            </div>
            <div>
              <div className="flex justify-between font-mono text-[11px] text-slate-400 tabular-nums">
                <label htmlFor="cdf-trace-slider">Normalized Plaquette Trace (Re Tr U_P)/N</label>
                <span className="text-slate-200">{traceNorm.toFixed(2)}</span>
              </div>
              <input
                id="cdf-trace-slider"
                type="range"
                min={-1}
                max={1}
                step={0.01}
                value={traceNorm}
                onChange={(e) => setTraceNorm(Number(e.target.value))}
                className="mt-1 w-full accent-emerald-500"
              />
            </div>
            <div className="grid grid-cols-3 gap-2 font-mono text-[11px] tabular-nums">
              <div className="rounded border border-slate-800 bg-[#070b14] p-2">
                <div className="text-[10px] text-slate-400">CDF F_β(w)</div>
                <div className="font-bold text-cyan-300">{cdfReadout.cdfValue.toFixed(3)}</div>
              </div>
              <div className="rounded border border-slate-800 bg-[#070b14] p-2">
                <div className="text-[10px] text-slate-400">Uniform → &#123;1,2&#125;</div>
                <div className="font-bold text-emerald-400">{cdfReadout.rademacherVal}</div>
              </div>
              <div className="rounded border border-slate-800 bg-[#070b14] p-2">
                <div className="text-[10px] text-slate-400">E[O^k] Moment</div>
                <div className="font-bold text-white">(1+2^k)/2</div>
              </div>
            </div>
          </div>
        </div>

        {/* RIGHT: Main Interactive Torus Canvas + Crosshair Telemetry Chart */}
        <div className="space-y-4 lg:col-span-7">
          <div className="relative overflow-hidden rounded-xl border border-slate-800 bg-[#070b14]">
            <canvas
              ref={canvasRef}
              onMouseMove={handleCanvasMove}
              onMouseLeave={() => setHoverCell(null)}
              className="h-[310px] w-full cursor-crosshair"
            />
            <div className="flex flex-wrap items-center justify-between gap-2 border-t border-slate-800 bg-[#0c1220] px-4 py-2 font-mono text-[11px] text-slate-300 tabular-nums">
              <span>
                {hoverCell
                  ? `Probe site: (${hoverCell.gx}, ${hoverCell.gy}, 0, 0)`
                  : 'Hover lattice slice to inspect coordinates'}
              </span>
              <span className="text-slate-400">
                {mode === 'balaban' ? activePreset.note : 'SU(N) link deviations shrink as O(β^{-1/2})'}
              </span>
            </div>
          </div>

          {/* Interactive Dual-Curve Crosshair Chart */}
          <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4">
            <div className="mb-1.5 flex flex-wrap items-center justify-between gap-2 font-mono text-[11px]">
              <span className="text-slate-200 font-semibold">
                {mode === 'balaban'
                  ? 'Lattice Spacing aₘ (solid) vs Finite-Volume Error |Sₘ − S_iid| (dashed)'
                  : `SUClosure Error Envelope C_err/x (solid) vs 1/2 Threshold at M₀=${suMetrics.m0Threshold.toLocaleString()}`}
              </span>
              <span className="text-cyan-300 tabular-nums">
                {hoverCurveIdx !== null && curveSamples[hoverCurveIdx]
                  ? `${curveSamples[hoverCurveIdx].label} · ${curveSamples[hoverCurveIdx].extra}`
                  : 'Hover curve to inspect stage'}
              </span>
            </div>

            <svg
              viewBox={`0 0 ${svgW} ${svgH}`}
              className="w-full cursor-crosshair"
              role="img"
              aria-label="Asymptotic stage convergence chart"
              onMouseLeave={() => setHoverCurveIdx(null)}
              onMouseMove={(e) => {
                const rect = e.currentTarget.getBoundingClientRect();
                const relX = ((e.clientX - rect.left) / rect.width) * svgW;
                const frac = Math.max(0, Math.min(1, (relX - pL) / plotW));
                setHoverCurveIdx(Math.round(frac * (curveSamples.length - 1)));
              }}
            >
              {[0, 0.5, 1, 1.5, 2].map((val) => {
                const y = yForV(val);
                return (
                  <g key={val}>
                    <line x1={pL} x2={svgW - pR} y1={y} y2={y} stroke="#1e293b" strokeDasharray="3 3" />
                    <text x={pL - 6} y={y + 3} textAnchor="end" className="fill-slate-400 font-mono text-[9px]">
                      {val.toFixed(1)}
                    </text>
                  </g>
                );
              })}

              <path d={primaryPath} fill="none" stroke="#10b981" strokeWidth="2.4" />
              <path
                d={secondaryPath}
                fill="none"
                stroke={mode === 'balaban' ? '#f59e0b' : '#38bdf8'}
                strokeWidth="2"
                strokeDasharray="5 3"
              />

              {hoverCurveIdx !== null && curveSamples[hoverCurveIdx] && (
                <>
                  <line
                    x1={xForI(hoverCurveIdx)}
                    x2={xForI(hoverCurveIdx)}
                    y1={pT}
                    y2={pT + plotH}
                    stroke="#38bdf8"
                    strokeWidth="1"
                  />
                  <circle
                    cx={xForI(hoverCurveIdx)}
                    cy={yForV(curveSamples[hoverCurveIdx].primary)}
                    r="4.5"
                    className="fill-emerald-400 stroke-slate-950 stroke-2"
                  />
                  <circle
                    cx={xForI(hoverCurveIdx)}
                    cy={yForV(curveSamples[hoverCurveIdx].secondary)}
                    r="4"
                    className="fill-amber-400 stroke-slate-950 stroke-2"
                  />
                </>
              )}

              <text x={pL} y={svgH - 6} className="fill-slate-400 font-mono text-[9px]">
                {curveSamples[0]?.label}
              </text>
              <text x={svgW - pR} y={svgH - 6} textAnchor="end" className="fill-slate-400 font-mono text-[9px]">
                {curveSamples[curveSamples.length - 1]?.label}
              </text>
            </svg>
          </div>
        </div>
      </div>
    </div>
  );
}
