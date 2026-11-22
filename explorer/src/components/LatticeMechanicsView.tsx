import { useMemo, useState } from 'react';
import {
  ALL_S16_STATES,
  auditS16State,
  checkIsingShiftObstruction,
  evaluateCanonicalWitness,
  evaluateIsingSchwinger,
  le16F,
  le16I,
  le16T,
  s16Label,
  s16ToString,
  S16State,
} from '../utils/yangMillsMath';

type MechanicsSubMode = 'witness' | 'feynman_kac' | 'ising' | 'trilattice';

export function LatticeMechanicsView() {
  const [subMode, setSubMode] = useState<MechanicsSubMode>('witness');

  // 1. Canonical Witness state
  const [suN, setSuN] = useState<number>(3);
  const [latticeL, setLatticeL] = useState<number>(4);

  // 2. Feynman-Kac Slices state
  const [ltSlices, setLtSlices] = useState<number>(4);
  const [reflectEnabled, setReflectEnabled] = useState<boolean>(true);

  // 3. Ising Obstruction state
  const [shiftA0, setShiftA0] = useState<number>(1.0);
  const [shiftSpatial, setShiftSpatial] = useState<number>(0.0);

  // 4. Trilattice S16 state
  const [selectedS16Idx, setSelectedS16Idx] = useState<number>(12); // (true, true, false, false)

  const witness = useMemo(() => evaluateCanonicalWitness(suN), [suN]);

  const isingCheck = useMemo(
    () => checkIsingShiftObstruction([shiftA0, shiftSpatial, 0, 0]),
    [shiftA0, shiftSpatial],
  );
  const isingThreePoint = useMemo(() => {
    const a: [number, number, number, number] = [shiftA0, shiftSpatial, 0, 0];
    return {
      s3Zero: evaluateIsingSchwinger([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
      ]),
      s3Shift: evaluateIsingSchwinger([a, a, a]),
    };
  }, [shiftA0, shiftSpatial]);

  const selectedS16: S16State = ALL_S16_STATES[selectedS16Idx] ?? ALL_S16_STATES[0];
  const s16Audit = useMemo(() => auditS16State(selectedS16), [selectedS16]);

  return (
    <div className="space-y-6">
      {/* Mode Switcher */}
      <section className="rounded-lg border border-slate-200 bg-white p-5">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="font-mono text-xs uppercase tracking-wider text-slate-500">
              Interactive Formal Proof Workbenches
            </p>
            <h1 className="mt-1 text-xl font-semibold text-slate-900 sm:text-2xl">
              Lattice Gauge Mechanics, Witnesses &amp; Obstructions
            </h1>
          </div>

          <div
            className="flex flex-wrap items-center gap-1.5 lg:flex-nowrap"
            role="tablist"
            aria-label="Lattice mechanics workbenches"
          >
            {(
              [
                { id: 'witness', label: 'Canonical Witness (§46W)' },
                { id: 'feynman_kac', label: 'Feynman–Kac Slices (§39–42)' },
                { id: 'ising', label: 'Ising Obstruction (§34/§37)' },
                { id: 'trilattice', label: 'Trilattice S16 (§8/§37)' },
              ] as const
            ).map((tab) => {
              const active = subMode === tab.id;
              return (
                <button
                  key={tab.id}
                  type="button"
                  role="tab"
                  aria-selected={active}
                  onClick={() => setSubMode(tab.id)}
                  className={`whitespace-nowrap shrink-0 rounded-md border px-2.5 py-1.5 text-xs font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-blue-600/30 ${
                    active
                      ? 'border-blue-600 bg-blue-600 text-white'
                      : 'border-slate-200 bg-slate-50 text-slate-700 hover:bg-white'
                  }`}
                >
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>
      </section>

      {/* SUBMODE 1: CANONICAL WITNESS */}
      {subMode === 'witness' && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
          <section className="space-y-5 rounded-lg border border-slate-200 bg-white p-5 lg:col-span-4">
            <div>
              <h2 className="font-mono text-xs font-semibold uppercase tracking-wider text-slate-700">
                Gauge Group &amp; Plaquette Witness Parameters
              </h2>
              <p className="mt-1 text-xs leading-relaxed text-slate-500">
                <span className="font-mono text-slate-700">CanonicalWitness.lean §46W</span> rules out trivial
                constant observables inside <span className="font-mono text-slate-700">LatticeSinglePointObs</span>{' '}
                by placing <span className="font-mono text-slate-700">suFlip2 = diag(-1,-1,1,…,1)</span> on
                one base link.
              </p>
            </div>

            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <label htmlFor="sun-slider" className="text-xs font-medium text-slate-700">
                  Gauge Group SU(N)
                </label>
                <span className="font-mono text-sm font-semibold text-slate-900 tabular-nums">
                  SU({suN})
                </span>
              </div>
              <input
                id="sun-slider"
                type="range"
                min={2}
                max={10}
                step={1}
                value={suN}
                onChange={(e) => setSuN(Number(e.target.value))}
                className="w-full accent-blue-600"
              />
              <div className="flex gap-1.5 pt-1">
                {[2, 3, 4, 6, 8].map((n) => (
                  <button
                    key={n}
                    type="button"
                    onClick={() => setSuN(n)}
                    className={`rounded border px-2.5 py-1 font-mono text-xs ${
                      suN === n
                        ? 'border-slate-900 bg-slate-900 text-white'
                        : 'border-slate-200 bg-slate-50 text-slate-700 hover:bg-white'
                    }`}
                  >
                    SU({n})
                  </button>
                ))}
              </div>
            </div>

            <div className="space-y-2 border-t border-slate-100 pt-4">
              <div className="flex items-center justify-between">
                <label htmlFor="witness-l-slider" className="text-xs font-medium text-slate-700">
                  Torus Size L (Theorem requires L ≥ 2)
                </label>
                <span className="font-mono text-xs font-semibold text-slate-900 tabular-nums">
                  L = {latticeL}
                </span>
              </div>
              <input
                id="witness-l-slider"
                type="range"
                min={2}
                max={8}
                step={1}
                value={latticeL}
                onChange={(e) => setLatticeL(Number(e.target.value))}
                className="w-full accent-blue-600"
              />
              <p className="text-[11px] leading-relaxed text-slate-500">
                Why <span className="font-mono text-slate-700">L ≥ 2</span>? By{' '}
                <span className="font-mono text-slate-700">tail_links_ne_base</span>, unit step in direction 2
                must yield a distinct site modulo <span className="font-mono text-slate-700">L</span> so the
                other 3 plaquette links keep identity <span className="font-mono text-slate-700">1</span>.
              </p>
            </div>

            <div className="rounded-md border border-slate-200 bg-slate-50 p-3">
              <div className="font-mono text-[11px] font-semibold uppercase tracking-wider text-slate-600">
                suFlip2 Diagonal Matrix ∈ SU({suN})
              </div>
              <div className="mt-2 flex flex-wrap gap-1.5 font-mono text-xs tabular-nums">
                {witness.diagonalEntries.map((val, idx) => (
                  <span
                    key={idx}
                    className={`rounded border px-2 py-0.5 ${
                      val === -1
                        ? 'border-rose-300 bg-rose-50 font-semibold text-rose-700'
                        : 'border-slate-200 bg-white text-slate-700'
                    }`}
                  >
                    {val === -1 ? '−1' : '+1'}
                  </span>
                ))}
              </div>
              <div className="mt-2 font-mono text-[11px] text-slate-500 tabular-nums">
                det(suFlip2) = (−1)·(−1)·1^(N−2) = +{witness.detProduct}
              </div>
            </div>
          </section>

          <section className="space-y-5 lg:col-span-8">
            {/* Value Comparison Readouts */}
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
              <div className="rounded-lg border border-slate-200 bg-white p-4">
                <div className="font-mono text-[10px] uppercase tracking-wider text-slate-500">
                  witnessFieldOne (U = 1)
                </div>
                <div className="mt-1 font-mono text-2xl font-semibold text-slate-900 tabular-nums">
                  {witness.oneNormalized.toFixed(4)}
                </div>
                <div className="mt-0.5 font-mono text-xs text-slate-500 tabular-nums">
                  Re Tr(1) / {suN} = {witness.oneTrace}/{suN}
                </div>
              </div>

              <div className="rounded-lg border border-slate-200 bg-white p-4">
                <div className="font-mono text-[10px] uppercase tracking-wider text-slate-500">
                  witnessFieldFlip (U = suFlip2)
                </div>
                <div className="mt-1 font-mono text-2xl font-semibold text-blue-700 tabular-nums">
                  {witness.flipNormalized.toFixed(4)}
                </div>
                <div className="mt-0.5 font-mono text-xs text-slate-500 tabular-nums">
                  Re Tr(suFlip2) / {suN} = ({suN}−4)/{suN} = {witness.flipTrace}/{suN}
                </div>
              </div>

              <div className="rounded-lg border border-slate-200 bg-white p-4">
                <div className="font-mono text-[10px] uppercase tracking-wider text-slate-500">
                  Separation |W₁ − W₂|
                </div>
                <div className="mt-1 font-mono text-2xl font-semibold text-emerald-700 tabular-nums">
                  {witness.difference.toFixed(4)}
                </div>
                <div className="mt-0.5 font-mono text-xs text-emerald-700">
                  ● NON-CONSTANT (4/{suN} ≠ 0)
                </div>
              </div>
            </div>

            {/* Plaquette Loop Diagram */}
            <div className="rounded-lg border border-slate-200 bg-white p-5">
              <h3 className="text-sm font-semibold text-slate-900">
                Embedded Canonical Plaquette Loop (plane d=1 × d=2 on cubicTorus4 {latticeL} {latticeL})
              </h3>
              <p className="mt-1 font-mono text-xs text-slate-500">
                pathHolonomy(witnessFieldFlip, embedLoop4DZ L (canonicalLoop4DZ x)) = suFlip2 · 1 · 1⁻¹ · 1⁻¹ = suFlip2
              </p>

              <div className="mt-4 grid grid-cols-1 items-center gap-6 md:grid-cols-2">
                <svg
                  viewBox="0 0 360 235"
                  className="w-full rounded border border-slate-100 bg-slate-50"
                  role="img"
                  aria-label="Canonical 4-link plaquette holonomy diagram showing suFlip2 on the base link"
                >
                  {/* Grid context */}
                  <line x1="95" y1="162" x2="255" y2="162" stroke="#dc2626" strokeWidth="4" />
                  <line x1="255" y1="162" x2="255" y2="56" stroke="#2563eb" strokeWidth="2.5" />
                  <line x1="255" y1="56" x2="95" y2="56" stroke="#2563eb" strokeWidth="2.5" strokeDasharray="5 3" />
                  <line x1="95" y1="56" x2="95" y2="162" stroke="#2563eb" strokeWidth="2.5" strokeDasharray="5 3" />

                  {/* Direction arrows */}
                  <polygon points="175,156 187,162 175,168" fill="#dc2626" />
                  <polygon points="249,112 255,100 261,112" fill="#2563eb" />
                  <polygon points="175,50 163,56 175,62" fill="#2563eb" />
                  <polygon points="89,106 95,118 101,106" fill="#2563eb" />

                  {/* Vertices */}
                  {[
                    { cx: 95, cy: 162, dx: -10, dy: 4, anchor: 'end' as const, label: '⌊x⌋ (base)' },
                    { cx: 255, cy: 162, dx: 10, dy: 4, anchor: 'start' as const, label: 'step +e₁' },
                    { cx: 255, cy: 56, dx: 10, dy: -6, anchor: 'start' as const, label: 'step +e₁+e₂' },
                    { cx: 95, cy: 56, dx: -10, dy: -6, anchor: 'end' as const, label: 'step +e₂' },
                  ].map((v) => (
                    <g key={v.label}>
                      <circle cx={v.cx} cy={v.cy} r="5" fill="#0f172a" />
                      <text
                        x={v.cx + v.dx}
                        y={v.cy + v.dy}
                        textAnchor={v.anchor}
                        className="fill-slate-700 font-mono text-[10px]"
                      >
                        {v.label}
                      </text>
                    </g>
                  ))}

                  <text x="175" y="196" textAnchor="middle" className="fill-rose-700 font-mono text-[11px] font-semibold">
                    Link 1 (dir=1, fwd): suFlip2
                  </text>
                  <text x="266" y="113" textAnchor="start" className="fill-blue-700 font-mono text-[10px]">
                    Link 2: 1
                  </text>
                  <text x="175" y="34" textAnchor="middle" className="fill-blue-700 font-mono text-[10px]">
                    Link 3 (bwd): 1⁻¹
                  </text>
                  <text x="84" y="113" textAnchor="end" className="fill-blue-700 font-mono text-[10px]">
                    Link 4: 1⁻¹
                  </text>
                </svg>

                <div className="space-y-3 text-xs leading-relaxed text-slate-600">
                  <div className="rounded border border-slate-200 bg-slate-50 p-3">
                    <div className="font-mono text-[11px] font-semibold text-slate-800">
                      Path A vs Path B Embeddings (ContinuumClosure.lean §46W)
                    </div>
                    <p className="mt-1">
                      <span className="font-mono text-slate-800">canonicalSContA</span> evaluates the
                      canonical plaquette at <span className="font-mono text-slate-800">x</span> with
                      fixed positive-time reflection <span className="font-mono text-slate-800">revFlip</span>,
                      while <span className="font-mono text-slate-800">canonicalSContB</span> preserves both
                      finite-volume RP and Euclidean time-reflection invariance.
                    </p>
                  </div>

                  <div className="rounded border border-slate-200 bg-white p-3">
                    <div className="font-mono text-[11px] font-semibold text-slate-800">
                      Why N = 4 gives 0 trace:
                    </div>
                    <p className="mt-1">
                      For <span className="font-mono text-slate-800">SU(4)</span>,{' '}
                      <span className="font-mono text-slate-800">suFlip2 = diag(−1,−1,1,1)</span> is
                      traceless (<span className="font-mono text-slate-800">(4−4)/4 = 0</span>), while
                      trivial field gives <span className="font-mono text-slate-800">1</span> — still
                      strictly separated by gap <span className="font-mono text-slate-800">1.0</span>!
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>
      )}

      {/* SUBMODE 2: FEYNMAN-KAC SLICES */}
      {subMode === 'feynman_kac' && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
          <section className="space-y-4 rounded-lg border border-slate-200 bg-white p-5 lg:col-span-4">
            <h2 className="font-mono text-xs font-semibold uppercase tracking-wider text-slate-700">
              Slice &amp; Transfer-Operator Controls (§39–§42)
            </h2>
            <p className="text-xs leading-relaxed text-slate-500">
              <span className="font-mono text-slate-700">slice4DFieldEquiv</span> decomposes any 4D gauge
              field into <span className="font-mono text-slate-700">Lt</span> spatial gauge slices{' '}
              <span className="font-mono text-slate-700">U_sl(t)</span> and{' '}
              <span className="font-mono text-slate-700">Lt</span> temporal gauge matrices{' '}
              <span className="font-mono text-slate-700">g_tm(t)</span>, integrating out temporal links
              to produce <span className="font-mono text-slate-700">wilson4DTransferOp</span>.
            </p>

            <div className="space-y-1.5 border-t border-slate-100 pt-3">
              <div className="flex items-center justify-between">
                <label htmlFor="lt-slider" className="text-xs font-medium text-slate-700">
                  Temporal Extent L_t (Slices)
                </label>
                <span className="font-mono text-xs font-semibold text-slate-900 tabular-nums">
                  L_t = {ltSlices}
                </span>
              </div>
              <input
                id="lt-slider"
                type="range"
                min={2}
                max={8}
                step={2}
                value={ltSlices}
                onChange={(e) => setLtSlices(Number(e.target.value))}
                className="w-full accent-blue-600"
              />
            </div>

            <div className="flex items-center justify-between border-t border-slate-100 pt-3">
              <span className="text-xs font-medium text-slate-700">
                Show Euclidean Time Reflection Θ
              </span>
              <button
                type="button"
                onClick={() => setReflectEnabled((v) => !v)}
                className={`rounded border px-3 py-1 font-mono text-xs ${
                  reflectEnabled
                    ? 'border-blue-600 bg-blue-50 text-blue-700'
                    : 'border-slate-200 bg-slate-50 text-slate-700'
                }`}
              >
                {reflectEnabled ? 'Θ ACTIVE' : 'Θ OFF'}
              </button>
            </div>

            <div className="space-y-2 border-t border-slate-100 pt-3 font-mono text-[11px] text-slate-700">
              <div className="font-semibold text-slate-900">Exact Proved Identities:</div>
              <div className="rounded border border-slate-100 bg-slate-50 p-2">
                Z_4D = Tr( T_4D^{ltSlices} )
                <div className="text-[10px] text-slate-500">cubic4PartitionFn_eq_chainTrace</div>
              </div>
              <div className="rounded border border-slate-100 bg-slate-50 p-2">
                ⟨f(t=0) g(t=k)⟩ = ⟨f, T_4D^k g⟩ / Tr(T_4D^{ltSlices})
                <div className="text-[10px] text-slate-500">cubic4Schwinger_two_slice_eq_wilson4D</div>
              </div>
              <div className="rounded border border-slate-100 bg-slate-50 p-2">
                0 ≤ ⟨ψ, T_4D ψ⟩ (Bernoulli–Taylor positivity)
                <div className="text-[10px] text-slate-500">wilson4DTransferOp_pos (§40)</div>
              </div>
            </div>
          </section>

          <section className="rounded-lg border border-slate-200 bg-white p-5 lg:col-span-8">
            <h3 className="text-sm font-semibold text-slate-900">
              Euclidean Time-Slice Factorization Diagram (L_t = {ltSlices})
            </h3>
            <p className="mt-1 font-mono text-xs text-slate-500">
              {reflectEnabled
                ? 'Reflection plane splits t ∈ {0,…,Lt/2−1} (Θ-reflected) vs {Lt/2,…,Lt−1} (positive-time)'
                : 'Periodic chain trace along Fin Lt around cubicTorus4'}
            </p>

            <div className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-4">
              {Array.from({ length: ltSlices }, (_, t) => {
                const isPosHalf = t >= ltSlices / 2;
                return (
                  <div
                    key={t}
                    className={`rounded-md border p-3 transition-colors ${
                      reflectEnabled
                        ? isPosHalf
                          ? 'border-blue-300 bg-blue-50/40'
                          : 'border-amber-300 bg-amber-50/40'
                        : 'border-slate-200 bg-slate-50'
                    }`}
                  >
                    <div className="flex items-center justify-between font-mono text-xs">
                      <span className="font-semibold text-slate-900">Slice t={t}</span>
                      {reflectEnabled && (
                        <span
                          className={`text-[10px] font-semibold ${
                            isPosHalf ? 'text-blue-700' : 'text-amber-700'
                          }`}
                        >
                          {isPosHalf ? 't ≥ 0 (pos)' : 'Θ(t) (neg)'}
                        </span>
                      )}
                    </div>
                    <div className="mt-2 space-y-1 font-mono text-[11px] text-slate-600">
                      <div>Spatial: U_sl({t})</div>
                      <div>Temporal: g_tm({t}) → t={(t + 1) % ltSlices}</div>
                      <div className="pt-1 text-slate-800">Kernel: K_4D(U_{t}, U_{(t + 1) % ltSlices})</div>
                    </div>
                  </div>
                );
              })}
            </div>
          </section>
        </div>
      )}

      {/* SUBMODE 3: ISING OBSTRUCTION */}
      {subMode === 'ising' && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
          <section className="space-y-4 rounded-lg border border-slate-200 bg-white p-5 lg:col-span-4">
            <h2 className="font-mono text-xs font-semibold uppercase tracking-wider text-slate-700">
              Origin-Anchored Toy Audit (§34 / §37)
            </h2>
            <p className="text-xs leading-relaxed text-slate-500">
              <span className="font-mono text-slate-700">isingSchwinger</span> defines{' '}
              <span className="font-mono text-slate-700">S_n(x) = ½(∏(1+g(xᵢ)) + ∏(1−g(xᵢ)))</span> with{' '}
              <span className="font-mono text-slate-700">g(x) = exp(−2‖x‖)</span>. It passes clustering
              and non-Gaussianity in <span className="font-mono text-slate-700">OS4DContinuumTheory</span>,
              but <span className="font-mono text-slate-700">OsterwalderSchrader4DStrict</span> rejects it!
            </p>

            <div className="space-y-1.5 border-t border-slate-100 pt-3">
              <div className="flex items-center justify-between">
                <label htmlFor="shift-a0" className="text-xs font-medium text-slate-700">
                  Euclidean Time Shift a₀
                </label>
                <span className="font-mono text-xs font-semibold text-slate-900 tabular-nums">
                  a₀ = {shiftA0.toFixed(2)}
                </span>
              </div>
              <input
                id="shift-a0"
                type="range"
                min={0}
                max={2.5}
                step={0.1}
                value={shiftA0}
                onChange={(e) => setShiftA0(Number(e.target.value))}
                className="w-full accent-rose-600"
              />
            </div>

            <div className="space-y-1.5">
              <div className="flex items-center justify-between">
                <label htmlFor="shift-a1" className="text-xs font-medium text-slate-700">
                  Spatial Shift a₁
                </label>
                <span className="font-mono text-xs font-semibold text-slate-900 tabular-nums">
                  a₁ = {shiftSpatial.toFixed(2)}
                </span>
              </div>
              <input
                id="shift-a1"
                type="range"
                min={0}
                max={2.5}
                step={0.1}
                value={shiftSpatial}
                onChange={(e) => setShiftSpatial(Number(e.target.value))}
                className="w-full accent-rose-600"
              />
            </div>

            <button
              type="button"
              onClick={() => {
                setShiftA0(1.0);
                setShiftSpatial(0.0);
              }}
              className="w-full rounded border border-slate-200 bg-slate-50 px-3 py-1.5 font-mono text-xs font-medium text-slate-700 hover:bg-white"
            >
              Reset to Lean Proof Witness a = ![1, 0, 0, 0]
            </button>
          </section>

          <section className="space-y-4 lg:col-span-8">
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
              <div className="rounded-lg border border-slate-200 bg-white p-4">
                <div className="font-mono text-[10px] uppercase tracking-wider text-slate-500">
                  Unshifted S₂(0, 0)
                </div>
                <div className="mt-1 font-mono text-2xl font-semibold text-slate-900 tabular-nums">
                  {isingCheck.unshiftedS2.toFixed(6)}
                </div>
                <div className="mt-0.5 font-mono text-xs text-slate-500">Exact value = 2</div>
              </div>

              <div className="rounded-lg border border-slate-200 bg-white p-4">
                <div className="font-mono text-[10px] uppercase tracking-wider text-slate-500">
                  Shifted S₂(a, a)
                </div>
                <div className="mt-1 font-mono text-2xl font-semibold text-rose-700 tabular-nums">
                  {isingCheck.shiftedS2.toFixed(6)}
                </div>
                <div className="mt-0.5 font-mono text-xs text-slate-500">
                  1 + exp(−4‖a‖)
                </div>
              </div>

              <div className="rounded-lg border border-slate-200 bg-white p-4">
                <div className="font-mono text-[10px] uppercase tracking-wider text-slate-500">
                  Violation |S₂(0,0) − S₂(a,a)|
                </div>
                <div
                  className={`mt-1 font-mono text-2xl font-semibold tabular-nums ${
                    isingCheck.translationInvariant ? 'text-emerald-700' : 'text-rose-700'
                  }`}
                >
                  {isingCheck.delta.toFixed(6)}
                </div>
                <div
                  className={`mt-0.5 font-mono text-xs font-semibold ${
                    isingCheck.translationInvariant ? 'text-emerald-700' : 'text-rose-700'
                  }`}
                >
                  {isingCheck.translationInvariant ? '● TRIVIAL SHIFT (a=0)' : '✖ FAILS trans_inv (§37)'}
                </div>
              </div>
            </div>

            <div className="rounded-lg border border-slate-200 bg-white p-5 text-sm leading-relaxed text-slate-600">
              <div className="font-mono text-xs font-semibold uppercase tracking-wider text-slate-800">
                Exact Lean Counterexample Proof (concreteOS4D_fails_trans_inv)
              </div>
              <p className="mt-2">
                Evaluating at <span className="font-mono text-slate-800">a = ![1,0,0,0]</span> shifts both
                points from origin norm <span className="font-mono text-slate-800">0</span> to norm{' '}
                <span className="font-mono text-slate-800">1</span>. Since radial coupling{' '}
                <span className="font-mono text-slate-800">g(0) = 1</span> collapses to{' '}
                <span className="font-mono text-slate-800">g(a) = e^(−2)</span>, we get{' '}
                <span className="font-mono text-slate-800">S₂(a,a) = 1 + e^(−4) ≈ 1.018316 &lt; 2</span> (and{' '}
                <span className="font-mono text-slate-800">S₃(a,a,a) = {isingThreePoint.s3Shift.toFixed(6)}</span>{' '}
                vs <span className="font-mono text-slate-800">{isingThreePoint.s3Zero.toFixed(6)}</span>). This
                proves why <span className="font-mono text-slate-800">ClayYangMillsMassGap4DStrict</span> requires{' '}
                <span className="font-mono text-slate-800">OsterwalderSchrader4DStrict.trans_inv</span>.
              </p>
            </div>
          </section>
        </div>
      )}

      {/* SUBMODE 4: TRILATTICE S16 */}
      {subMode === 'trilattice' && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
          <section className="rounded-lg border border-slate-200 bg-white p-5 lg:col-span-7">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div>
                <h2 className="text-sm font-semibold text-slate-900">
                  16-State Tesseract Carrier S16 = Bool × Bool × Bool × Bool
                </h2>
                <p className="font-mono text-xs text-slate-500">
                  Click any state to compare trilattice16 (inc16) vs trilattice16Strict (inc16Strict)
                </p>
              </div>
              <span className="font-mono text-xs text-slate-500">16 vertices</span>
            </div>

            <div className="mt-4 grid grid-cols-2 gap-2 sm:grid-cols-4">
              {ALL_S16_STATES.map((st, idx) => {
                const audit = auditS16State(st);
                const selected = idx === selectedS16Idx;
                return (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => setSelectedS16Idx(idx)}
                    className={`rounded border p-2.5 text-left font-mono text-xs transition-colors ${
                      selected
                        ? 'border-blue-600 bg-blue-50 ring-1 ring-blue-600'
                        : 'border-slate-200 bg-slate-50 hover:bg-white'
                    }`}
                  >
                    <div className="flex items-center justify-between font-semibold text-slate-900">
                      <span>{s16ToString(st)}</span>
                      <span className="text-blue-700">{s16Label(st)}</span>
                    </div>
                    <div className="mt-1 text-[10px] text-slate-500">
                      incStrict → {s16ToString(audit.incStrict)}
                    </div>
                  </button>
                );
              })}
            </div>
          </section>

          <section className="space-y-4 rounded-lg border border-slate-200 bg-white p-5 lg:col-span-5">
            <div>
              <div className="font-mono text-xs uppercase tracking-wider text-slate-500">
                Selected S16 State Inspector
              </div>
              <div className="mt-1 font-mono text-xl font-semibold text-slate-900">
                x = {s16ToString(selectedS16)} · {s16Label(selectedS16)}
              </div>
            </div>

            <div className="space-y-2 border-t border-slate-100 pt-3 font-mono text-xs">
              <div className="flex justify-between rounded bg-slate-50 px-3 py-2">
                <span className="text-slate-600">inc16 (legacy §8):</span>
                <span className="font-semibold text-slate-900">{s16ToString(s16Audit.incLegacy)}</span>
              </div>
              <div className="flex justify-between rounded bg-blue-50 px-3 py-2">
                <span className="text-blue-800">inc16Strict (§37):</span>
                <span className="font-semibold text-blue-900">{s16ToString(s16Audit.incStrict)}</span>
              </div>
              <div className="flex justify-between rounded bg-slate-50 px-3 py-2">
                <span className="text-slate-600">walk16(x):</span>
                <span className="font-semibold text-slate-900">{s16ToString(s16Audit.walkNext)}</span>
              </div>
            </div>

            <div className="space-y-1.5 border-t border-slate-100 pt-3 font-mono text-xs">
              <div className="flex justify-between">
                <span className="text-slate-600">incStrict(incStrict(x)) = incStrict(x)</span>
                <span className="font-semibold text-emerald-700">
                  ● {String(s16Audit.strictIdempotent).toUpperCase()}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-600">incStrict(x) ≠ ∅ (non-void)</span>
                <span className="font-semibold text-emerald-700">
                  ● {String(s16Audit.strictNonVoid).toUpperCase()}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-600">IncStrict ∘ W = W ∘ IncStrict</span>
                <span
                  className={`font-semibold ${
                    s16Audit.incWalkCommuteStrict ? 'text-slate-700' : 'text-amber-700'
                  }`}
                >
                  {s16Audit.incWalkCommuteStrict ? 'commutes here' : '▲ NON-COMMUTING WITNESS'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-600">le16_i(∅, x) / le16_t(∅, x) / le16_f(∅, x)</span>
                <span className="text-slate-900">
                  {String(le16I([false, false, false, false], selectedS16))} /{' '}
                  {String(le16T([false, false, false, false], selectedS16))} /{' '}
                  {String(le16F([false, false, false, false], selectedS16))}
                </span>
              </div>
            </div>
          </section>
        </div>
      )}
    </div>
  );
}
