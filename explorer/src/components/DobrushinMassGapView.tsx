import { useMemo, useState } from 'react';
import {
  DOBRUSHIN_CRITICAL_BETA,
  STANDARD_BETA0,
  dobrushinClusterBound,
  dobrushinMetrics,
  enumerateTouchingPlaquettes4D,
  generateDobrushinDecayCurve,
  linkKey,
} from '../utils/yangMillsMath';

const DIR_LABELS = ['t (0)', 'x (1)', 'y (2)', 'z (3)'] as const;

export function DobrushinMassGapView() {
  const [beta, setBeta] = useState<number>(STANDARD_BETA0);
  const [distanceD, setDistanceD] = useState<number>(6);
  const [supportSize, setSupportSize] = useState<number>(4);
  const [latticeL, setLatticeL] = useState<number>(3);
  const [targetDir, setTargetDir] = useState<0 | 1 | 2 | 3>(1);
  const [hoverD, setHoverD] = useState<number | null>(null);

  const metrics = useMemo(() => dobrushinMetrics(beta), [beta]);
  const curve = useMemo(
    () => generateDobrushinDecayCurve(beta, 14, supportSize),
    [beta, supportSize],
  );
  const boundAtD = useMemo(
    () => dobrushinClusterBound(beta, distanceD, supportSize, 1, 1),
    [beta, distanceD, supportSize],
  );

  const neighborhood = useMemo(
    () => enumerateTouchingPlaquettes4D(latticeL, { site: [0, 0, 0, 0], dir: targetDir }),
    [latticeL, targetDir],
  );

  // SVG chart dimensions
  const svgW = 680;
  const svgH = 260;
  const padL = 54;
  const padR = 20;
  const padT = 22;
  const padB = 36;
  const plotW = svgW - padL - padR;
  const plotH = svgH - padT - padB;

  const maxLogY = 2; // 10^2 upper visual ceiling
  const minLogY = -6; // 10^-6 floor

  const yForValue = (val: number) => {
    if (!Number.isFinite(val) || val <= 0) return padT + plotH;
    const log10 = Math.log10(val);
    const clamped = Math.max(minLogY, Math.min(maxLogY, log10));
    const frac = (clamped - minLogY) / (maxLogY - minLogY);
    return padT + plotH * (1 - frac);
  };

  const xForD = (d: number) => padL + ((d - 1) / 13) * plotW;

  const expPath = useMemo(() => {
    if (metrics.regime === 'supercritical' || metrics.regime === 'boundary') return '';
    return curve
      .map((pt, idx) => `${idx === 0 ? 'M' : 'L'} ${xForD(pt.d).toFixed(1)} ${yForValue(pt.expDecay).toFixed(1)}`)
      .join(' ');
  }, [curve, metrics.regime]);

  const boundPath = useMemo(() => {
    if (metrics.regime !== 'contractive') return '';
    return curve
      .filter((pt) => Number.isFinite(pt.bound) && pt.bound > 0)
      .map((pt, idx) => `${idx === 0 ? 'M' : 'L'} ${xForD(pt.d).toFixed(1)} ${yForValue(pt.bound).toFixed(1)}`)
      .join(' ');
  }, [curve, metrics.regime]);

  const activePoint = curve[(hoverD ?? distanceD) - 1] ?? curve[0];

  return (
    <div className="space-y-6">
      {/* Header Telemetry Bar */}
      <section className="rounded-lg border border-slate-200 bg-white p-5">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="font-mono text-xs uppercase tracking-wider text-slate-500">
              StrongCouplingDobrushin.lean §43 · StrongCouplingInfVol.lean §44
            </p>
            <h1 className="mt-1 text-xl font-semibold text-slate-900 sm:text-2xl">
              Dobrushin Contraction &amp; Volume-Independent Mass Gap
            </h1>
            <p className="mt-1 text-sm text-slate-600">
              Every 4D link touches at most 6 plaquettes and 18 neighbor links. When{' '}
              <span className="font-mono text-slate-800">α = 18(1 − e^(−12β)) &lt; 1</span>, greedy
              conditional-expectation elimination yields an exact volume-independent exponential mass gap{' '}
              <span className="font-mono text-slate-800">m(β) = −½ log α &gt; 0</span>.
            </p>
          </div>

          <div className="shrink-0 border-t border-slate-200 pt-3 lg:border-l lg:border-t-0 lg:pl-6 lg:pt-0">
            <div className="font-mono text-[11px] uppercase tracking-wider text-slate-500">
              Theorem Regime
            </div>
            {metrics.regime === 'contractive' && (
              <div className="mt-1 font-mono text-sm font-semibold text-emerald-700">
                ● CONTRACTIVE (α &lt; 1)
              </div>
            )}
            {metrics.regime === 'zero_coupling' && (
              <div className="mt-1 font-mono text-sm font-semibold text-sky-700">
                ● FREE HAAR LIMIT (β = 0)
              </div>
            )}
            {metrics.regime === 'boundary' && (
              <div className="mt-1 font-mono text-sm font-semibold text-amber-700">
                ▲ CRITICAL BOUNDARY (α = 1)
              </div>
            )}
            {metrics.regime === 'supercritical' && (
              <div className="mt-1 font-mono text-sm font-semibold text-rose-700">
                ✖ DOBRUSHIN BREAKDOWN (α ≥ 1)
              </div>
            )}
            <div className="mt-0.5 font-mono text-xs text-slate-500 tabular-nums">
              β_crit ≈ {DOBRUSHIN_CRITICAL_BETA.toFixed(6)}
            </div>
          </div>
        </div>
      </section>

      {/* Two-zone Split Console: Left Parameters (360px), Right Visualizations */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        {/* Control Column */}
        <section className="space-y-5 rounded-lg border border-slate-200 bg-white p-5 lg:col-span-4">
          <div>
            <h2 className="font-mono text-xs font-semibold uppercase tracking-wider text-slate-700">
              Coupling &amp; Observable Controls
            </h2>
            <p className="mt-1 text-xs text-slate-500">
              Tune inverse coupling β and plaquette-graph distance D to inspect the exact Lean bound.
            </p>
          </div>

          {/* Presets */}
          <div className="space-y-1.5">
            <div className="font-mono text-[11px] uppercase tracking-wider text-slate-500">
              Verified Corpus Presets
            </div>
            <div className="grid grid-cols-2 gap-1.5">
              <button
                type="button"
                onClick={() => setBeta(STANDARD_BETA0)}
                className={`rounded border px-2.5 py-1.5 text-left text-xs font-medium transition-colors ${
                  Math.abs(beta - STANDARD_BETA0) < 1e-6
                    ? 'border-blue-600 bg-blue-50 text-blue-800'
                    : 'border-slate-200 bg-slate-50 text-slate-700 hover:bg-white'
                }`}
              >
                <div className="font-mono font-semibold">standardBeta0</div>
                <div className="text-[11px] text-slate-500">1/300 ≈ 0.00333</div>
              </button>
              <button
                type="button"
                onClick={() => setBeta(0.0015)}
                className="rounded border border-slate-200 bg-slate-50 px-2.5 py-1.5 text-left text-xs font-medium text-slate-700 hover:bg-white"
              >
                <div className="font-mono font-semibold">Deep Strong</div>
                <div className="text-[11px] text-slate-500">β = 0.00150</div>
              </button>
              <button
                type="button"
                onClick={() => setBeta(0.0046)}
                className="rounded border border-slate-200 bg-slate-50 px-2.5 py-1.5 text-left text-xs font-medium text-slate-700 hover:bg-white"
              >
                <div className="font-mono font-semibold">Near Threshold</div>
                <div className="text-[11px] text-slate-500">β = 0.00460</div>
              </button>
              <button
                type="button"
                onClick={() => setBeta(0.0062)}
                className="rounded border border-slate-200 bg-slate-50 px-2.5 py-1.5 text-left text-xs font-medium text-slate-700 hover:bg-white"
              >
                <div className="font-mono font-semibold">Above α = 1</div>
                <div className="text-[11px] text-slate-500">β = 0.00620</div>
              </button>
            </div>
          </div>

          {/* Beta Slider */}
          <div className="space-y-1.5 border-t border-slate-100 pt-4">
            <div className="flex items-center justify-between">
              <label htmlFor="beta-slider" className="text-xs font-medium text-slate-700">
                Inverse Coupling β
              </label>
              <span className="font-mono text-xs font-semibold text-slate-900 tabular-nums">
                {beta.toFixed(5)}
              </span>
            </div>
            <input
              id="beta-slider"
              type="range"
              min={0}
              max={0.008}
              step={0.00005}
              value={beta}
              onChange={(e) => setBeta(Number(e.target.value))}
              className="w-full accent-blue-600"
            />
            <div className="flex justify-between font-mono text-[10px] text-slate-400">
              <span>0.0000</span>
              <span>β₀=0.00333</span>
              <span>β_c=0.00477</span>
              <span>0.0080</span>
            </div>
          </div>

          {/* Distance D Slider */}
          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <label htmlFor="dist-slider" className="text-xs font-medium text-slate-700">
                Plaquette Separation D
              </label>
              <span className="font-mono text-xs font-semibold text-slate-900 tabular-nums">
                {distanceD} links
              </span>
            </div>
            <input
              id="dist-slider"
              type="range"
              min={1}
              max={14}
              step={1}
              value={distanceD}
              onChange={(e) => setDistanceD(Number(e.target.value))}
              className="w-full accent-blue-600"
            />
          </div>

          {/* Support Size |S_g| */}
          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <label htmlFor="support-slider" className="text-xs font-medium text-slate-700">
                Observable Support |S_g|
              </label>
              <span className="font-mono text-xs font-semibold text-slate-900 tabular-nums">
                {supportSize} links
              </span>
            </div>
            <input
              id="support-slider"
              type="range"
              min={1}
              max={12}
              step={1}
              value={supportSize}
              onChange={(e) => setSupportSize(Number(e.target.value))}
              className="w-full accent-blue-600"
            />
          </div>

          {/* Torus & Target Link Geometry */}
          <div className="space-y-3 border-t border-slate-100 pt-4">
            <div className="font-mono text-[11px] font-semibold uppercase tracking-wider text-slate-500">
              4D Plaquette-Graph Geometry (cubicTorus4)
            </div>
            <div className="flex items-center justify-between gap-2">
              <span className="text-xs text-slate-700">Torus Side L</span>
              <div className="flex gap-1">
                {[2, 3, 4].map((L) => (
                  <button
                    key={L}
                    type="button"
                    onClick={() => setLatticeL(L)}
                    className={`rounded border px-2.5 py-1 font-mono text-xs ${
                      latticeL === L
                        ? 'border-slate-900 bg-slate-900 text-white'
                        : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
                    }`}
                  >
                    L={L}
                  </button>
                ))}
              </div>
            </div>

            <div className="flex items-center justify-between gap-2">
              <span className="text-xs text-slate-700">Target Link Axis</span>
              <div className="flex gap-1">
                {([0, 1, 2, 3] as const).map((d) => (
                  <button
                    key={d}
                    type="button"
                    onClick={() => setTargetDir(d)}
                    className={`rounded border px-2 py-1 font-mono text-xs ${
                      targetDir === d
                        ? 'border-blue-600 bg-blue-50 text-blue-700'
                        : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
                    }`}
                  >
                    {DIR_LABELS[d]}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Main Viewport Stage */}
        <section className="space-y-5 lg:col-span-8">
          {/* 4 Metric Readouts */}
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            <div className="rounded-lg border border-slate-200 bg-white p-3.5">
              <div className="font-mono text-[10px] uppercase tracking-wider text-slate-500">
                Dobrushin α(β)
              </div>
              <div
                className={`mt-1 font-mono text-xl font-semibold tabular-nums ${
                  metrics.alpha < 1 ? 'text-emerald-700' : 'text-rose-700'
                }`}
              >
                {metrics.alpha.toFixed(4)}
              </div>
              <div className="mt-0.5 font-mono text-[11px] text-slate-500">18(1 − e^(−12β))</div>
            </div>

            <div className="rounded-lg border border-slate-200 bg-white p-3.5">
              <div className="font-mono text-[10px] uppercase tracking-wider text-slate-500">
                Decay Base ρ = √α
              </div>
              <div className="mt-1 font-mono text-xl font-semibold text-slate-900 tabular-nums">
                {metrics.rho.toFixed(4)}
              </div>
              <div className="mt-0.5 font-mono text-[11px] text-slate-500">
                TV coeff c = {metrics.cSingleLink.toFixed(4)}
              </div>
            </div>

            <div className="rounded-lg border border-slate-200 bg-white p-3.5">
              <div className="font-mono text-[10px] uppercase tracking-wider text-slate-500">
                Cluster Rate m(β)
              </div>
              <div className="mt-1 font-mono text-xl font-semibold text-blue-700 tabular-nums">
                {metrics.clusterRate === null
                  ? '—'
                  : Number.isFinite(metrics.clusterRate)
                    ? metrics.clusterRate.toFixed(4)
                    : '∞'}
              </div>
              <div className="mt-0.5 font-mono text-[11px] text-slate-500">−½ log α (lattice⁻¹)</div>
            </div>

            <div className="rounded-lg border border-slate-200 bg-white p-3.5">
              <div className="font-mono text-[10px] uppercase tracking-wider text-slate-500">
                Bound at D={distanceD}
              </div>
              <div className="mt-1 font-mono text-xl font-semibold text-slate-900 tabular-nums">
                {boundAtD === null
                  ? 'Unbounded'
                  : boundAtD < 0.001 && boundAtD > 0
                    ? boundAtD.toExponential(2)
                    : boundAtD.toFixed(4)}
              </div>
              <div className="mt-0.5 font-mono text-[11px] text-slate-500">
                C(β)·|S_g|·ρ^D
              </div>
            </div>
          </div>

          {/* Decay Curve SVG Chart */}
          <div className="rounded-lg border border-slate-200 bg-white p-4">
            <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
              <div>
                <h3 className="text-sm font-semibold text-slate-900">
                  Exponential Clustering Upper Bound (Log₁₀ Scale)
                </h3>
                <p className="font-mono text-xs text-slate-500">
                  Solid cobalt: Theorem §43 bound C(β)|S_g|ρ^D · Dashed cyan: Unit rate e^(−m(β)D)
                </p>
              </div>
              <div className="rounded border border-slate-200 bg-slate-50 px-2.5 py-1 font-mono text-xs text-slate-700 tabular-nums">
                D={activePoint.d}:{' '}
                {Number.isFinite(activePoint.bound)
                  ? `bound=${activePoint.bound.toExponential(2)}`
                  : 'α ≥ 1 (no Dobrushin contraction)'}
              </div>
            </div>

            <div className="overflow-x-auto">
              <svg
                viewBox={`0 0 ${svgW} ${svgH}`}
                className="h-60 w-full min-w-[500px] cursor-crosshair select-none"
                role="img"
                aria-label="Log-scale exponential clustering decay curve across graph distance D"
              >
                {/* Horizontal grid ticks */}
                {[-6, -4, -2, 0, 2].map((exp) => {
                  const y = yForValue(Math.pow(10, exp));
                  return (
                    <g key={exp}>
                      <line
                        x1={padL}
                        x2={svgW - padR}
                        y1={y}
                        y2={y}
                        stroke={exp === 0 ? '#cbd5e1' : '#e2e8f0'}
                        strokeDasharray={exp === 0 ? undefined : '3 3'}
                      />
                      <text
                        x={padL - 8}
                        y={y + 4}
                        textAnchor="end"
                        className="fill-slate-500 font-mono text-[10px]"
                      >
                        10^{exp}
                      </text>
                    </g>
                  );
                })}

                {/* X-axis distance ticks */}
                {curve.map((pt) => {
                  const x = xForD(pt.d);
                  return (
                    <g key={pt.d}>
                      <line
                        x1={x}
                        x2={x}
                        y1={padT}
                        y2={svgH - padB}
                        stroke={pt.d === distanceD ? '#93c5fd' : '#f1f5f9'}
                      />
                      <text
                        x={x}
                        y={svgH - 14}
                        textAnchor="middle"
                        className="fill-slate-500 font-mono text-[10px]"
                      >
                        {pt.d}
                      </text>
                    </g>
                  );
                })}

                <text
                  x={padL + plotW / 2}
                  y={svgH - 2}
                  textAnchor="middle"
                  className="fill-slate-500 font-mono text-[10px]"
                >
                  Plaquette Graph Distance D = plaqDist4(S_f, S_g)
                </text>

                {metrics.regime === 'contractive' ? (
                  <>
                    <path
                      d={expPath}
                      fill="none"
                      stroke="#0284c7"
                      strokeWidth={2}
                      strokeDasharray="5 4"
                    />
                    <path d={boundPath} fill="none" stroke="#2563eb" strokeWidth={2.5} />
                    {curve.map((pt) => {
                      const x = xForD(pt.d);
                      const y = yForValue(pt.bound);
                      const isTarget = pt.d === distanceD;
                      return (
                        <g
                          key={pt.d}
                          onMouseEnter={() => setHoverD(pt.d)}
                          onMouseLeave={() => setHoverD(null)}
                        >
                          <rect
                            x={x - 14}
                            y={padT}
                            width={28}
                            height={plotH}
                            fill="transparent"
                          />
                          <circle
                            cx={x}
                            cy={y}
                            r={isTarget ? 5.5 : 3.5}
                            className={
                              isTarget
                                ? 'fill-blue-600 stroke-white stroke-2'
                                : 'fill-white stroke-blue-600 stroke-2'
                            }
                          />
                        </g>
                      );
                    })}
                  </>
                ) : (
                  <text
                    x={padL + plotW / 2}
                    y={padT + plotH / 2}
                    textAnchor="middle"
                    className="fill-rose-600 font-mono text-xs font-medium"
                  >
                    α = {metrics.alpha.toFixed(3)} ≥ 1 · Single-link Dobrushin condition violated
                  </text>
                )}
              </svg>
            </div>
          </div>

          {/* 4D Plaquette-Adjacency Combinatorial Proof Inspector */}
          <div className="rounded-lg border border-slate-200 bg-white p-4">
            <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3">
              <div>
                <h3 className="text-sm font-semibold text-slate-900">
                  4D Plaquette-Neighbor Verification (plaqsTouching_length_le &amp; sharesPlaq4_card_le)
                </h3>
                <p className="text-xs text-slate-500">
                  Inspecting target link <span className="font-mono text-slate-800">(0,0,0,0; dir={DIR_LABELS[targetDir]})</span>{' '}
                  on <span className="font-mono text-slate-800">cubicTorus4 {latticeL} {latticeL}</span>
                </p>
              </div>
              <div className="font-mono text-xs text-slate-700 tabular-nums">
                Touching Plaquettes: <strong>{neighborhood.plaquettes.length}</strong> / 6 · Unique Neighbors:{' '}
                <strong className="text-blue-700">{neighborhood.uniqueNeighbors.length}</strong> / 18
              </div>
            </div>

            <div className="mt-3 grid grid-cols-1 gap-3 md:grid-cols-2">
              {/* 6 Plaquettes list */}
              <div className="space-y-1.5">
                <div className="font-mono text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                  6 Incident 2D Plaquettes (3 orthogonal axes × ±1)
                </div>
                <div className="grid grid-cols-1 gap-1.5">
                  {neighborhood.plaquettes.map((p) => (
                    <div
                      key={p.id}
                      className="flex items-center justify-between rounded border border-slate-100 bg-slate-50 px-2.5 py-1.5 font-mono text-[11px] text-slate-700"
                    >
                      <span>{p.id}</span>
                      <span className="text-slate-500">
                        plane ({p.plane[0]},{p.plane[1]})
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Unique Neighbor Links Grid */}
              <div className="space-y-1.5">
                <div className="font-mono text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                  Distinct SharesPlaq4 Neighbors ({neighborhood.uniqueNeighbors.length})
                </div>
                <div className="grid max-h-44 grid-cols-2 gap-1 overflow-y-auto pr-1">
                  {neighborhood.uniqueNeighbors.map((nbr) => (
                    <div
                      key={linkKey(nbr)}
                      className="rounded border border-slate-100 bg-white px-2 py-1 font-mono text-[11px] text-slate-700 tabular-nums"
                    >
                      {linkKey(nbr)}
                    </div>
                  ))}
                </div>
                {latticeL === 2 && (
                  <p className="text-[11px] text-amber-700">
                    Note: At L=2 periodic wraparound causes opposing plaquette links to coincide (12 unique neighbors ≤ 18); for all L ≥ 3, degree is exactly 18.
                  </p>
                )}
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
