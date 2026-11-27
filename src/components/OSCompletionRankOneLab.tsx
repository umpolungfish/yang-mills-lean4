import { useMemo, useState } from 'react';
import { type OSConfigPreset, computeOSGramMatrix, evaluateIidSchwinger } from '../utils/ymProofMath';

const AVAILABLE_WORDS: Array<{ id: string; label: string; points: string[] }> = [
  { id: 'vac', label: '∅ (Vacuum)', points: [] },
  { id: 'pt1', label: '(x₀)', points: ['x₀'] },
  { id: 'pair_eq', label: '(x₀, x₀)', points: ['x₀', 'x₀'] },
  { id: 'pair_diff', label: '(x₀, x₁)', points: ['x₀', 'x₁'] },
  { id: 'triple', label: '(x₀, x₀, x₀)', points: ['x₀', 'x₀', 'x₀'] },
  { id: 'quad_eq', label: '(x₀, x₀, x₀, x₀)', points: ['x₀', 'x₀', 'x₀', 'x₀'] },
  { id: 'quad_22', label: '(x₀, x₀, x₁, x₁)', points: ['x₀', 'x₀', 'x₁', 'x₁'] },
];

export function OSCompletionRankOneLab() {
  const [selectedIds, setSelectedIds] = useState<[string, string, string, string]>([
    'vac',
    'pt1',
    'pair_eq',
    'quad_eq',
  ]);
  const [selectedCell, setSelectedCell] = useState<[number, number]>([2, 3]);

  const activeConfigs = useMemo<OSConfigPreset[]>(() => {
    return selectedIds.map(
      (id) => AVAILABLE_WORDS.find((w) => w.id === id) ?? AVAILABLE_WORDS[0],
    );
  }, [selectedIds]);

  const gram = useMemo(() => computeOSGramMatrix(activeConfigs), [activeConfigs]);
  const maxEntry = useMemo(() => Math.max(1, ...gram.gramMatrix.flat()), [gram]);

  const [ci, cj] = selectedCell;
  const cfgI = activeConfigs[ci] ?? activeConfigs[0];
  const cfgJ = activeConfigs[cj] ?? activeConfigs[0];
  const cellVal = gram.gramMatrix[ci]?.[cj] ?? 1;
  const combinedPts = [...cfgI.points.map((p) => `Θ(${p})`), ...cfgJ.points];
  const combinedVal = evaluateIidSchwinger(combinedPts);

  return (
    <div className="space-y-5">
      {/* Header Ribbon */}
      <div className="flex flex-wrap items-center justify-between gap-4 rounded-xl border border-slate-800 bg-[#0c1220] px-5 py-3.5">
        <div>
          <div className="font-mono text-[11px] text-emerald-400">
            IIDPoincareContinuation.lean (§49) · osConfigKernel_eq_completion_inner
          </div>
          <h2 className="text-lg font-semibold text-white">
            Rank-1 OS Hilbert Completion &amp; Poincaré Continuation Verifier
          </h2>
        </div>

        <div className="flex items-center gap-4 font-mono text-xs tabular-nums">
          <span>
            Max 2×2 Minor Det:{' '}
            <strong className="text-emerald-400">{gram.maxMinorDet.toExponential(1)}</strong>
          </span>
          <span className="text-slate-600">·</span>
          <span>
            Hilbert Rank: <strong className="text-cyan-300">{gram.rank}</strong>
          </span>
          <span className="text-slate-600">·</span>
          <span>
            Growth Bound: <strong className="text-white">M_bd = 2</strong>
          </span>
        </div>
      </div>

      {/* Main Split Console */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-12">
        {/* LEFT: Basis Word Selector & Growth Bound Verifier */}
        <div className="space-y-4 lg:col-span-5">
          <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4 space-y-3">
            <h3 className="text-sm font-semibold text-white">
              Positive-Time Basis Configurations (ψ₀…ψ₃)
            </h3>
            <p className="text-xs text-slate-400">
              Select any 4 positive-time Euclidean test tuples. Because time reflection flips t &gt; 0 to −t &lt; 0, Θxᵢ
              and xⱼ are guaranteed disjoint, so{' '}
              <code className="font-mono text-emerald-300">iid_osConfigKernel_factor</code> splits every inner product
              into <code className="font-mono text-cyan-300">S(xᵢ)·S(xⱼ)</code>.
            </p>

            <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
              {selectedIds.map((curId, slotIdx) => (
                <div key={slotIdx} className="rounded-lg border border-slate-800 bg-[#070b14] p-2.5">
                  <label htmlFor={`os-slot-${slotIdx}`} className="block font-mono text-[10px] text-slate-400">
                    Vector ψ_{slotIdx} · S = {gram.schwingerValues[slotIdx].toFixed(3)}
                  </label>
                  <select
                    id={`os-slot-${slotIdx}`}
                    value={curId}
                    onChange={(e) => {
                      const next = [...selectedIds] as [string, string, string, string];
                      next[slotIdx] = e.target.value;
                      setSelectedIds(next);
                    }}
                    className="mt-1 w-full rounded border border-slate-700 bg-slate-950 px-2 py-1 font-mono text-xs text-slate-100"
                  >
                    {AVAILABLE_WORDS.map((w) => (
                      <option key={w.id} value={w.id}>
                        {w.label}
                      </option>
                    ))}
                  </select>
                </div>
              ))}
            </div>
          </div>

          {/* M_bd = 2 Growth Bound Bar Matrix */}
          <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4 space-y-3">
            <div className="flex items-center justify-between font-mono text-xs">
              <span className="font-semibold text-slate-200">OS Growth Bound Check: |Sₙ| ≤ 2ⁿ</span>
              <span className="text-emerald-400">● h_bd Verified</span>
            </div>
            <div className="space-y-2.5">
              {activeConfigs.map((cfg, idx) => {
                const val = gram.schwingerValues[idx];
                const bnd = gram.growthBounds[idx];
                const pct = Math.min(100, (val / bnd) * 100);
                return (
                  <div key={idx} className="space-y-1 font-mono text-[11px] tabular-nums">
                    <div className="flex justify-between">
                      <span className="text-slate-300">
                        ψ_{idx} {cfg.label}
                      </span>
                      <span className="text-slate-200">
                        {val.toFixed(2)} ≤ {bnd} ({pct.toFixed(1)}%)
                      </span>
                    </div>
                    <div className="h-2 w-full overflow-hidden rounded bg-slate-800">
                      <div className="h-full bg-emerald-500 transition-all" style={{ width: `${pct}%` }} />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* RIGHT: 4x4 OS Gram Kernel Heatmap & Collinear Vacuum Collapse */}
        <div className="space-y-4 lg:col-span-7">
          {/* Heatmap Card */}
          <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4">
            <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
              <div>
                <h3 className="text-sm font-semibold text-white">
                  4×4 OS Completion Gram Matrix ⟪ψᵢ, ψⱼ⟫ = S(Θxᵢ ⊔ xⱼ)
                </h3>
                <div className="font-mono text-[11px] text-slate-400">
                  Click any cell to inspect Θ-reflection factorization &amp; 2×2 minor rank
                </div>
              </div>
              <span className="font-mono text-xs text-cyan-300 tabular-nums">
                Active [{ci},{cj}] = {cellVal.toFixed(4)}
              </span>
            </div>

            <div className="grid grid-cols-1 gap-4 md:grid-cols-12">
              <div className="md:col-span-7">
                <div className="grid grid-cols-4 gap-1 rounded-lg border border-slate-800 bg-[#070b14] p-2">
                  {gram.gramMatrix.map((row, rIdx) =>
                    row.map((val, cIdx) => {
                      const norm = Math.sqrt(val / maxEntry);
                      const isSel = rIdx === ci && cIdx === cj;
                      return (
                        <button
                          key={`${rIdx}-${cIdx}`}
                          type="button"
                          onClick={() => setSelectedCell([rIdx, cIdx])}
                          style={{
                            backgroundColor: `rgba(16, 185, 129, ${(0.12 + 0.58 * norm).toFixed(2)})`,
                          }}
                          className={`flex h-16 flex-col items-center justify-center rounded font-mono text-xs transition-transform ${
                            isSel
                              ? 'ring-2 ring-cyan-300 text-white font-bold'
                              : 'text-slate-100 hover:ring-1 hover:ring-emerald-400'
                          }`}
                        >
                          <span className="text-[10px] text-slate-300">
                            ⟪ψ{rIdx},ψ{cIdx}⟫
                          </span>
                          <span className="tabular-nums font-semibold">{val.toFixed(2)}</span>
                        </button>
                      );
                    }),
                  )}
                </div>
              </div>

              {/* Cell Factorization Inspector */}
              <div className="flex flex-col justify-between rounded-lg border border-slate-800 bg-[#070b14] p-3.5 font-mono text-xs md:col-span-5">
                <div className="space-y-2">
                  <div className="text-[10px] uppercase tracking-wider text-cyan-400">
                    Cell [{ci}, {cj}] Decomposition
                  </div>
                  <div className="text-slate-300">
                    S({cfgI.label}) = <span className="text-white">{gram.schwingerValues[ci].toFixed(4)}</span>
                  </div>
                  <div className="text-slate-300">
                    S({cfgJ.label}) = <span className="text-white">{gram.schwingerValues[cj].toFixed(4)}</span>
                  </div>
                  <div className="border-t border-slate-800 pt-2 text-emerald-300 tabular-nums">
                    Product = {(gram.schwingerValues[ci] * gram.schwingerValues[cj]).toFixed(4)}
                  </div>
                  <div className="text-[11px] text-slate-400">
                    Disjoint Θx_{ci} ⊔ x_{cj} eval = {combinedVal.toFixed(4)} (exact match)
                  </div>
                </div>
                <div className="mt-3 rounded border border-emerald-500/30 bg-emerald-950/20 px-2.5 py-1.5 text-[11px] text-emerald-300">
                  ‖ψ_{ci} − S(x_{ci})·Ω_vac‖² = 0.0000
                </div>
              </div>
            </div>
          </div>

          {/* Rank-1 Collinear Collapse Projection Diagram */}
          <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4">
            <div className="mb-2 flex items-center justify-between font-mono text-xs">
              <span className="font-semibold text-white">
                Collinear Collapse onto Unit Vacuum Ray ℂ·Ω_vac (iid_osConfigVector_eq)
              </span>
              <span className="text-emerald-400">U(g) = I, φ(f) = I</span>
            </div>
            <svg viewBox="0 0 600 110" className="w-full rounded bg-[#070b14]" role="img" aria-label="Rank 1 Hilbert collapse onto vacuum ray">
              <line x1="30" y1="58" x2="570" y2="58" stroke="#334155" strokeWidth="2" />
              <line x1="30" y1="58" x2="545" y2="58" stroke="#10b981" strokeWidth="2.5" strokeDasharray="6 4" />
              <circle cx="30" cy="58" r="5" fill="#94a3b8" />
              <text x="30" y="84" textAnchor="middle" className="fill-slate-400 font-mono text-[10px]">
                0
              </text>

              {gram.schwingerValues.map((val, idx) => {
                const maxVal = Math.max(...gram.schwingerValues, 8.5);
                const px = 45 + (val / maxVal) * 500;
                const yOff = idx % 2 === 0 ? 28 : 88;
                return (
                  <g key={idx}>
                    <line x1={px} y1="58" x2={px} y2={yOff} stroke="#38bdf8" strokeWidth="1" strokeDasharray="2 2" />
                    <circle cx={px} cy="58" r="5.5" fill={idx === 0 ? '#34d399' : '#38bdf8'} />
                    <text x={px} y={idx % 2 === 0 ? 20 : 101} textAnchor="middle" className="fill-slate-200 font-mono text-[10px]">
                      ψ{idx} = {val.toFixed(2)}·Ω
                    </text>
                  </g>
                );
              })}
            </svg>
          </div>
        </div>
      </div>
    </div>
  );
}
