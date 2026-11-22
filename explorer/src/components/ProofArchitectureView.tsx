import { useMemo, useState } from 'react';
import {
  ArrowRight,
  BookOpen,
  CheckCircle2,
  ExternalLink,
  FlaskConical,
  GitBranch,
  HelpCircle,
  XCircle,
} from 'lucide-react';
import {
  ARCHITECTURE_EDGES,
  CORPUS_MODULES,
  CorpusModule,
  ProofStatus,
} from '../data/corpusData';

interface ProofArchitectureViewProps {
  selectedModuleId: string;
  onSelectModule: (moduleId: string) => void;
  onOpenSource: (moduleId: string) => void;
  onJumpToLab: (tab: 'dobrushin' | 'mechanics' | 'bridge') => void;
}

const LAYER_ORDER: Array<{
  layer: CorpusModule['layer'];
  label: string;
  sublabel: string;
}> = [
  { layer: 'foundation', label: '01 · Core Axiomatics', sublabel: '§§1–21 · Core.lean' },
  { layer: 'lattice_4d', label: '02 · 4D SU(N) Haar & RP', sublabel: '§§23–36 · CubicHaar4D.lean' },
  { layer: 'os_hilbert', label: '03 · OS Completion & Hardening', sublabel: '§§22–38 · OSCompletion.lean' },
  { layer: 'feynman_kac', label: '04 · Transfer Op & Slice FK', sublabel: '§§39–42 · Wilson4DOp + FeynmanKac' },
  { layer: 'strong_coupling', label: '05 · Dobrushin & Inf-Vol', sublabel: '§§43–44 · Strong Coupling' },
  { layer: 'bridge_closure', label: '06 · Clay Bridge & Witness', sublabel: '§§45–46W · Closure + 9 Props' },
  { layer: 'analytic_rungs', label: '07 · Analytic Rungs & Schwinger Bridge', sublabel: 'R1–R4 · Haar, PIT, Rademacher, Density, Bridge' },
];

function StatusMark({ status }: { status: ProofStatus }) {
  if (status === 'proved') {
    return (
      <span className="inline-flex items-center gap-1.5 font-mono text-xs font-medium text-emerald-700">
        <CheckCircle2 className="h-3.5 w-3.5 shrink-0" aria-hidden="true" />
        PROVED UNCONDITIONALLY
      </span>
    );
  }
  if (status === 'obstruction') {
    return (
      <span className="inline-flex items-center gap-1.5 font-mono text-xs font-medium text-rose-700">
        <XCircle className="h-3.5 w-3.5 shrink-0" aria-hidden="true" />
        PROVED + OBSTRUCTION AUDIT
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1.5 font-mono text-xs font-medium text-amber-700">
      <HelpCircle className="h-3.5 w-3.5 shrink-0" aria-hidden="true" />
      EXPLICIT OPEN BRIDGE
    </span>
  );
}

export function ProofArchitectureView({
  selectedModuleId,
  onSelectModule,
  onOpenSource,
  onJumpToLab,
}: ProofArchitectureViewProps) {
  const [statusFilter, setStatusFilter] = useState<'all' | ProofStatus>('all');

  const selectedModule = useMemo(
    () => CORPUS_MODULES.find((m) => m.id === selectedModuleId) ?? CORPUS_MODULES[0],
    [selectedModuleId],
  );

  const incomingEdges = useMemo(
    () => ARCHITECTURE_EDGES.filter((e) => e.to === selectedModule.id),
    [selectedModule.id],
  );

  const outgoingEdges = useMemo(
    () => ARCHITECTURE_EDGES.filter((e) => e.from === selectedModule.id),
    [selectedModule.id],
  );

  const totalLines = useMemo(
    () => CORPUS_MODULES.reduce((acc, m) => acc + m.lineCount, 0),
    [],
  );

  return (
    <div className="space-y-6">
      {/* Top scientific thesis summary strip */}
      <section className="rounded-lg border border-slate-200 bg-white p-5">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div className="max-w-3xl space-y-1.5">
            <p className="font-mono text-xs uppercase tracking-wider text-slate-500">
              4D SU(N) Yang–Mills &amp; Mass Gap · Formalization Map
            </p>
            <h1 className="text-xl font-semibold tracking-tight text-slate-900 sm:text-2xl">
              From Compact SU(N) Haar Lattices to the Clay Weak-Coupling Interface
            </h1>
            <p className="text-sm leading-relaxed text-slate-600">
              This Lean 4 corpus separates unconditionally proved finite-volume &amp; strong-coupling
              theorems ({totalLines.toLocaleString()} lines across 11 modules) from toy-model
              counterexamples and the two explicitly isolated open analytic hypotheses.
            </p>
          </div>

          <div className="grid grid-cols-3 gap-4 border-t border-slate-200 pt-4 lg:border-l lg:border-t-0 lg:pl-6 lg:pt-0">
            <div>
              <div className="font-mono text-[11px] uppercase tracking-wider text-slate-500">
                Strong Coupling
              </div>
              <div className="mt-1 font-mono text-lg font-semibold text-emerald-700 tabular-nums">
                α &lt; 1
              </div>
              <div className="text-xs text-slate-500">Proved Inf-Vol Gap</div>
            </div>
            <div>
              <div className="font-mono text-[11px] uppercase tracking-wider text-slate-500">
                Toy Filter
              </div>
              <div className="mt-1 font-mono text-lg font-semibold text-rose-700 tabular-nums">
                ΔS₂ ≠ 0
              </div>
              <div className="text-xs text-slate-500">Ising Rejected (§37)</div>
            </div>
            <div>
              <div className="font-mono text-[11px] uppercase tracking-wider text-slate-500">
                Clay Reduction
              </div>
              <div className="mt-1 font-mono text-lg font-semibold text-amber-700 tabular-nums">
                2 Hyps
              </div>
              <div className="text-xs text-slate-500">RG + OS Continuation</div>
            </div>
          </div>
        </div>
      </section>

      {/* Filter & quick lab jump controls */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-wrap items-center gap-1.5" role="group" aria-label="Filter proof status">
          {(
            [
              { id: 'all', label: 'All 11 Modules' },
              { id: 'proved', label: '● Proved Core' },
              { id: 'obstruction', label: '✖ Obstruction Audit' },
              { id: 'open_hypothesis', label: '▲ Open Clay Bridge' },
            ] as const
          ).map((f) => {
            const active = statusFilter === f.id;
            return (
              <button
                key={f.id}
                type="button"
                onClick={() => setStatusFilter(f.id)}
                className={`rounded-md border px-3 py-1.5 text-xs font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-blue-600/30 ${
                  active
                    ? 'border-slate-900 bg-slate-900 text-white'
                    : 'border-slate-200 bg-white text-slate-700 hover:border-slate-300 hover:bg-slate-50'
                }`}
              >
                {f.label}
              </button>
            );
          })}
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <button
            type="button"
            onClick={() => onJumpToLab('dobrushin')}
            className="inline-flex items-center gap-1.5 rounded-md border border-blue-200 bg-blue-50 px-3 py-1.5 text-xs font-medium text-blue-700 hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-blue-600/30"
          >
            <FlaskConical className="h-3.5 w-3.5" aria-hidden="true" />
            Explore Dobrushin Mass Gap (§43–44)
          </button>
          <button
            type="button"
            onClick={() => onJumpToLab('mechanics')}
            className="inline-flex items-center gap-1.5 rounded-md border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-blue-600/30"
          >
            Canonical Witness &amp; Slices (§46W)
          </button>
        </div>
      </div>

      {/* Main Split: Layered Module DAG (Left 7/12) + Selected Module Inspector (Right 5/12) */}
      <div className="grid grid-cols-1 gap-6 xl:grid-cols-12">
        <div className="space-y-4 xl:col-span-7">
          {LAYER_ORDER.map((strata) => {
            const modules = CORPUS_MODULES.filter((m) => m.layer === strata.layer);
            return (
              <div
                key={strata.layer}
                className="rounded-lg border border-slate-200 bg-white p-4"
              >
                <div className="mb-3 flex items-baseline justify-between gap-2 border-b border-slate-100 pb-2">
                  <h2 className="text-xs font-semibold uppercase tracking-wider text-slate-800">
                    {strata.label}
                  </h2>
                  <span className="font-mono text-xs text-slate-500">{strata.sublabel}</span>
                </div>

                <div
                  className={`grid grid-cols-1 gap-3 ${
                    modules.length > 1 ? 'sm:grid-cols-2' : ''
                  }`}
                >
                  {modules.map((mod) => {
                    const isSelected = mod.id === selectedModule.id;
                    const dimmed = statusFilter !== 'all' && mod.status !== statusFilter;
                    const accentRing =
                      mod.status === 'proved'
                        ? 'border-emerald-300'
                        : mod.status === 'obstruction'
                          ? 'border-rose-300'
                          : 'border-amber-300';

                    return (
                      <button
                        key={mod.id}
                        type="button"
                        onClick={() => onSelectModule(mod.id)}
                        className={`group flex flex-col justify-between rounded-md border p-3.5 text-left transition-all focus:outline-none focus:ring-2 focus:ring-blue-600/40 ${
                          isSelected
                            ? `border-blue-600 bg-blue-50/40 ring-1 ring-blue-600`
                            : `border-slate-200 bg-slate-50/40 hover:border-slate-300 hover:bg-white`
                        } ${dimmed ? 'opacity-40' : 'opacity-100'}`}
                      >
                        <div>
                          <div className="flex items-center justify-between gap-2">
                            <span className="font-mono text-xs font-semibold text-slate-900">
                              {mod.fileName}
                            </span>
                            <span className="font-mono text-[11px] text-slate-500 tabular-nums">
                              {mod.sections}
                            </span>
                          </div>
                          <p className="mt-1 text-sm font-medium text-slate-800">
                            {mod.title}
                          </p>
                        </div>

                        <div className={`mt-3 flex items-center justify-between border-t pt-2 ${accentRing}`}>
                          <StatusMark status={mod.status} />
                          <span className="font-mono text-[11px] text-slate-500 tabular-nums">
                            {mod.lineCount.toLocaleString()} lines
                          </span>
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>

        {/* Right Inspector Column */}
        <aside className="space-y-4 xl:col-span-5">
          <div className="sticky top-20 rounded-lg border border-slate-200 bg-white p-5">
            <div className="flex items-start justify-between gap-3 border-b border-slate-100 pb-4">
              <div>
                <div className="font-mono text-xs text-slate-500">
                  {selectedModule.fileName} · {selectedModule.sections} ·{' '}
                  <span className="tabular-nums">{selectedModule.lineCount.toLocaleString()}</span> lines
                </div>
                <h2 className="mt-1 text-lg font-semibold text-slate-900">
                  {selectedModule.title}
                </h2>
                <div className="mt-2">
                  <StatusMark status={selectedModule.status} />
                </div>
              </div>
              <button
                type="button"
                onClick={() => onOpenSource(selectedModule.id)}
                className="inline-flex shrink-0 items-center gap-1.5 rounded-md bg-slate-900 px-3 py-1.5 text-xs font-medium text-white hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-600/40"
              >
                <BookOpen className="h-3.5 w-3.5" aria-hidden="true" />
                Read Source
              </button>
            </div>

            <p className="mt-4 text-sm leading-relaxed text-slate-600">
              {selectedModule.summary}
            </p>

            {/* Dependencies in / out */}
            <div className="mt-5 grid grid-cols-1 gap-3">
              <div className="rounded-md border border-slate-200 bg-slate-50 p-3">
                <div className="flex items-center gap-1.5 font-mono text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                  <GitBranch className="h-3 w-3" aria-hidden="true" />
                  Incoming Feeds ({incomingEdges.length})
                </div>
                {incomingEdges.length === 0 ? (
                  <p className="mt-2 text-xs text-slate-500">Root Mathlib axiomatics only.</p>
                ) : (
                  <ul className="mt-2 space-y-2">
                    {incomingEdges.map((edge) => (
                      <li key={`${edge.from}-${edge.to}`}>
                        <button
                          type="button"
                          onClick={() => onSelectModule(edge.from)}
                          className="flex w-full flex-col items-start gap-0.5 text-left text-xs text-slate-700 hover:text-blue-700"
                        >
                          <span className="font-mono font-semibold">{edge.from}</span>
                          <span className="text-[11px] text-slate-500">{edge.label}</span>
                        </button>
                      </li>
                    ))}
                  </ul>
                )}
              </div>

              <div className="rounded-md border border-slate-200 bg-slate-50 p-3">
                <div className="flex items-center gap-1.5 font-mono text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                  <ArrowRight className="h-3 w-3" aria-hidden="true" />
                  Downstream Targets ({outgoingEdges.length})
                </div>
                {outgoingEdges.length === 0 ? (
                  <p className="mt-2 text-xs text-slate-500">Terminal witness / closure artifact.</p>
                ) : (
                  <ul className="mt-2 space-y-2">
                    {outgoingEdges.map((edge) => (
                      <li key={`${edge.from}-${edge.to}`}>
                        <button
                          type="button"
                          onClick={() => onSelectModule(edge.to)}
                          className="flex w-full flex-col items-start gap-0.5 text-left text-xs text-slate-700 hover:text-blue-700"
                        >
                          <span className="font-mono font-semibold">{edge.to}</span>
                          <span className="text-[11px] text-slate-500">{edge.label}</span>
                        </button>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>

            {/* Key Definitions */}
            {selectedModule.keyDefinitions.length > 0 && (
              <div className="mt-5">
                <h3 className="font-mono text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                  Key Structures &amp; Definitions
                </h3>
                <ul className="mt-2 space-y-1">
                  {selectedModule.keyDefinitions.map((defName) => (
                    <li
                      key={defName}
                      className="rounded border border-slate-100 bg-slate-50 px-2.5 py-1.5 font-mono text-xs text-slate-800"
                    >
                      {defName}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Key Theorems */}
            {selectedModule.keyTheorems.length > 0 && (
              <div className="mt-5">
                <h3 className="font-mono text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                  Verified Theorems &amp; Reductions
                </h3>
                <ul className="mt-2 space-y-1">
                  {selectedModule.keyTheorems.map((thmName) => (
                    <li
                      key={thmName}
                      className="flex items-center justify-between rounded border border-slate-100 bg-white px-2.5 py-1.5 font-mono text-xs text-slate-800"
                    >
                      <span className="truncate">{thmName}</span>
                      <button
                        type="button"
                        onClick={() => onOpenSource(selectedModule.id)}
                        className="ml-2 inline-flex shrink-0 items-center gap-1 text-[11px] text-blue-600 hover:underline"
                      >
                        view <ExternalLink className="h-3 w-3" aria-hidden="true" />
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Honest Scope Note */}
            <div className="mt-5 rounded-md border border-slate-200 bg-slate-50 p-3.5 text-xs leading-relaxed text-slate-600">
              <span className="font-semibold text-slate-900">Honesty Boundary:</span> In{' '}
              <span className="font-mono text-slate-800">ContinuumClosure.lean §45</span>,{' '}
              <span className="font-mono text-slate-800">clay_yang_mills_strict_from_balaban_and_os</span>{' '}
              is a proved conditional reduction — the strong-coupling infinite-volume gap at{' '}
              <span className="font-mono text-slate-800">β₀ = 1/300</span> is unconditional, while weak-coupling{' '}
              <span className="font-mono text-slate-800">β → ∞</span> RG scaling remains isolated as an explicit hypothesis.
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}
