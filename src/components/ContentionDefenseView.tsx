import { Fragment, useMemo, useState } from 'react';
import {
  ArrowRight,
  ArrowUpRight,
  CheckCircle2,
  FileSearch,
  GitCommitHorizontal,
  Search,
  ShieldAlert,
  ShieldCheck,
} from 'lucide-react';
import {
  CONTENTIONS_CATALOG,
  LAKE_REPLAY_METRICS,
  type ContentionCategory,
  type ContentionEntry,
} from '../data/contentionsData';
import { filterContentions, getContentionStats } from '../utils/contentionTrace';
import { ContentionEvidenceLab } from './ContentionEvidenceLab';

interface ContentionDefenseViewProps {
  onOpenSourceLine: (moduleId: string, line?: number, declaration?: string) => void;
  onOpenElegantProofs?: () => void;
}

const CATEGORIES: Array<'ALL' | ContentionCategory> = [
  'ALL',
  'Kernel & Axioms',
  'Conditional Hypotheses',
  'Lattice Observables',
  'Continuum & Measure',
  'OS & Non-Gaussianity',
  'Wightman & Gap Link',
  'SU(N) Gauge Dynamics',
  'Scope Boundaries',
];

function renderInlineCode(text: string) {
  const parts = text.split(/(`[^`]+`)/g);
  return parts.map((part, idx) => {
    if (part.startsWith('`') && part.endsWith('`') && part.length >= 2) {
      return (
        <code
          key={idx}
          className="rounded bg-slate-900/95 px-1 py-0.5 font-mono text-[11px] text-cyan-300 [overflow-wrap:anywhere]"
        >
          {part.slice(1, -1)}
        </code>
      );
    }
    return <Fragment key={idx}>{part}</Fragment>;
  });
}

export function ContentionDefenseView({
  onOpenSourceLine,
  onOpenElegantProofs,
}: ContentionDefenseViewProps) {
  const [selectedId, setSelectedId] = useState<string>(CONTENTIONS_CATALOG[0].id);
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState<'ALL' | ContentionCategory>('ALL');

  const stats = useMemo(() => getContentionStats(), []);
  const filteredContentions = useMemo(
    () => filterContentions(CONTENTIONS_CATALOG, query, category),
    [query, category],
  );

  const activeContention: ContentionEntry = useMemo(
    () =>
      filteredContentions.find((c) => c.id === selectedId) ??
      filteredContentions[0] ??
      CONTENTIONS_CATALOG[0],
    [filteredContentions, selectedId],
  );

  return (
    <div className="space-y-6">
      {/* Top Referee Dossier Banner */}
      <section className="rounded-xl border border-slate-800 bg-[#0c1220] p-5 sm:p-7">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
          <div className="max-w-3xl space-y-3">
            <div className="font-mono text-xs uppercase tracking-wider text-emerald-400">
              Adversarial Referee Defense · Proof Traceability &amp; Direct Source Refutation
            </div>
            <h1 className="text-2xl font-bold tracking-tight text-white sm:text-3xl">
              Anticipated Points of Contention &amp; Kernel-Verified Refutations
            </h1>
            <p className="text-sm leading-relaxed text-slate-300">
              Every structural objection a referee, mathematical physicist, or constructivist reviewer could raise against
              the 4D <span className="font-mono text-emerald-300">SU(N)</span> Yang–Mills mass gap formalization is
              catalogued below, traced step-by-step from foundational lemmas to top-level theorems, and answered with
              clickable Lean 4.28.0 lines, <code className="font-mono text-cyan-300">#print axioms</code> replay proofs,
              and live counter-evidence checks.
            </p>
            {onOpenElegantProofs && (
              <div className="pt-1">
                <button
                  type="button"
                  onClick={onOpenElegantProofs}
                  className="inline-flex items-center gap-1.5 rounded-lg border border-cyan-500/40 bg-cyan-950/30 px-3.5 py-1.5 font-mono text-xs font-semibold text-cyan-200 transition-colors hover:bg-cyan-900/40"
                >
                  Highlight: 8 Gems of Mathematical &amp; Lean 4 Elegance
                  <ArrowRight className="h-3.5 w-3.5" aria-hidden="true" />
                </button>
              </div>
            )}
          </div>

          <div className="grid shrink-0 grid-cols-2 gap-3 sm:w-80">
            <div className="rounded-lg border border-emerald-500/30 bg-emerald-950/20 p-3">
              <div className="font-mono text-[10px] uppercase text-emerald-300">Attack Vectors Covered</div>
              <div className="mt-1 font-mono text-lg font-bold text-white tabular-nums">
                {stats.totalContentions} / {stats.totalContentions}
              </div>
              <div className="font-mono text-[10px] text-slate-400 tabular-nums">
                {stats.totalTraceSteps} traced declarations
              </div>
            </div>
            <div className="rounded-lg border border-slate-800 bg-slate-900/90 p-3">
              <div className="font-mono text-[10px] uppercase text-slate-400">Lake Replay Verified</div>
              <div className="mt-1 font-mono text-lg font-bold text-cyan-300 tabular-nums">
                {LAKE_REPLAY_METRICS.totalJobs.toLocaleString()} jobs
              </div>
              <div className="font-mono text-[10px] text-slate-400">
                0 sorry · F = 0 ELF
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Search & Category Filter Bar */}
      <section className="space-y-3 rounded-xl border border-slate-800 bg-[#0c1220] p-4">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div className="relative flex-1">
            <Search
              className="pointer-events-none absolute left-3 top-2.5 h-3.5 w-3.5 text-slate-400"
              aria-hidden="true"
            />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search any dismissal vector (e.g. sorry, Balaban, constant, torus, Gaussian, rank-1, Dobrushin, TrivialWightman)..."
              aria-label="Search anticipated points of contention"
              className="w-full rounded-md border border-slate-800 bg-[#070b14] py-2 pl-9 pr-3 text-xs text-slate-100 placeholder:text-slate-500 focus:border-emerald-500 focus:outline-none"
            />
          </div>
          <div className="font-mono text-xs text-slate-400 tabular-nums">
            Showing {filteredContentions.length} of {CONTENTIONS_CATALOG.length} contentions
          </div>
        </div>

        <div className="flex flex-wrap gap-1.5">
          {CATEGORIES.map((cat) => {
            const active = category === cat;
            return (
              <button
                key={cat}
                type="button"
                onClick={() => setCategory(cat)}
                className={`rounded border px-2.5 py-1 font-mono text-[11px] transition-colors ${
                  active
                    ? 'border-emerald-500 bg-emerald-500/15 font-semibold text-emerald-300'
                    : 'border-slate-800 bg-[#070b14] text-slate-400 hover:border-slate-700 hover:text-slate-200'
                }`}
              >
                {cat === 'ALL' ? 'All Vectors (8)' : cat}
              </button>
            );
          })}
        </div>
      </section>

      {/* Main Master-Detail Contention Workbench */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        {/* Left: Contention Index */}
        <aside className="space-y-2.5 lg:col-span-4">
          {filteredContentions.map((item) => {
            const selected = item.id === activeContention.id;
            const isScope = item.verdict === 'Scope Clarified & Proved';
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => setSelectedId(item.id)}
                className={`w-full rounded-xl border p-4 text-left transition-colors ${
                  selected
                    ? 'border-emerald-500/70 bg-emerald-950/20'
                    : 'border-slate-800 bg-[#0c1220] hover:border-slate-700 hover:bg-slate-900/70'
                }`}
              >
                <div className="flex items-center justify-between gap-2 font-mono text-[10px]">
                  <span className="font-bold text-cyan-300">
                    {item.code} · {item.category}
                  </span>
                  <span className={isScope ? 'text-amber-300' : 'text-emerald-400'}>
                    {item.verdict}
                  </span>
                </div>
                <div className="mt-1.5 text-sm font-semibold leading-snug text-white">
                  {item.title}
                </div>
                <p className="mt-1.5 line-clamp-2 text-xs leading-relaxed text-slate-400 [overflow-wrap:anywhere]">
                  {renderInlineCode(item.dismissalClaim)}
                </p>
                <div className="mt-2.5 flex items-center justify-between font-mono text-[10px] text-slate-500 tabular-nums">
                  <span>
                    {item.trace.length} trace steps · {item.exhibits.length} exhibits
                  </span>
                  {selected && (
                    <span className="inline-flex items-center gap-0.5 text-emerald-300">
                      Active <ArrowRight className="h-3 w-3" />
                    </span>
                  )}
                </div>
              </button>
            );
          })}

          {filteredContentions.length === 0 && (
            <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-6 text-center font-mono text-xs text-slate-400">
              No contention matched &ldquo;{query}&rdquo;. Clear filters to inspect all 8 attack vectors.
            </div>
          )}
        </aside>

        {/* Right: Active Contention Proof Trace & Evidence Dossier */}
        <section className="min-w-0 space-y-6 lg:col-span-8">
          {/* 1. Dismissal Claim vs Kernel Refutation */}
          <div className="min-w-0 rounded-xl border border-slate-800 bg-[#0c1220] p-5 sm:p-6">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <span className="font-mono text-xs font-semibold uppercase tracking-wider text-cyan-300">
                {activeContention.code} · {activeContention.category}
              </span>
              <span
                className={`inline-flex items-center gap-1.5 font-mono text-xs font-semibold ${
                  activeContention.verdict === 'Scope Clarified & Proved'
                    ? 'text-amber-300'
                    : 'text-emerald-400'
                }`}
              >
                <ShieldCheck className="h-4 w-4" aria-hidden="true" />
                {activeContention.verdict}
              </span>
            </div>

            <h2 className="mt-2 text-xl font-bold text-white">{activeContention.title}</h2>

            <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
              <div className="min-w-0 rounded-lg border border-rose-500/30 bg-rose-950/15 p-4">
                <div className="flex items-center gap-1.5 font-mono text-[11px] font-semibold uppercase text-rose-300">
                  <ShieldAlert className="h-3.5 w-3.5" aria-hidden="true" />
                  Anticipated Point of Contention
                </div>
                <p className="mt-2 text-xs leading-relaxed text-slate-200 [overflow-wrap:anywhere]">
                  {renderInlineCode(activeContention.dismissalClaim)}
                </p>
              </div>

              <div className="min-w-0 rounded-lg border border-emerald-500/35 bg-emerald-950/15 p-4">
                <div className="flex items-center gap-1.5 font-mono text-[11px] font-semibold uppercase text-emerald-300">
                  <CheckCircle2 className="h-3.5 w-3.5" aria-hidden="true" />
                  Formal Refutation &amp; Resolution
                </div>
                <p className="mt-2 text-xs leading-relaxed text-slate-200 [overflow-wrap:anywhere]">
                  {renderInlineCode(activeContention.refutationSummary)}
                </p>
              </div>
            </div>
          </div>

          {/* 2. Step-by-Step Formal Proof Trace */}
          <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-5 sm:p-6">
            <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
              <div>
                <h3 className="flex items-center gap-2 text-base font-semibold text-white">
                  <GitCommitHorizontal className="h-4 w-4 text-emerald-400" aria-hidden="true" />
                  Deductive Proof Trace (Click any step to jump directly to Lean line)
                </h3>
                <p className="mt-0.5 text-xs text-slate-400">
                  Ordered kernel-verified path from foundational definitions to the headline discharge.
                </p>
              </div>
              <span className="font-mono text-[11px] text-emerald-400 tabular-nums">
                {activeContention.trace.length} Verified Steps
              </span>
            </div>

            <div className="space-y-3">
              {activeContention.trace.map((node) => (
                <button
                  key={`${activeContention.id}-step-${node.step}`}
                  type="button"
                  onClick={() => onOpenSourceLine(node.moduleId, node.line, node.declaration)}
                  className="group w-full rounded-lg border border-slate-800 bg-[#070b14] p-4 text-left transition-colors hover:border-cyan-500/60 hover:bg-slate-900/70"
                >
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div className="flex items-center gap-2">
                      <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded border border-emerald-500/40 bg-emerald-500/10 font-mono text-xs font-bold text-emerald-300 tabular-nums">
                        {node.step}
                      </span>
                      <span className="font-mono text-[11px] uppercase tracking-wider text-slate-400">
                        {node.role}
                      </span>
                    </div>
                    <span className="inline-flex items-center gap-1 font-mono text-xs text-cyan-300 tabular-nums group-hover:text-cyan-200">
                      {node.moduleId}.lean:{node.line}
                      <ArrowUpRight className="h-3.5 w-3.5" aria-hidden="true" />
                    </span>
                  </div>

                  <div className="mt-2 font-mono text-xs font-semibold text-emerald-300 [overflow-wrap:anywhere]">
                    {node.declaration}
                  </div>
                  <p className="mt-1 text-xs leading-relaxed text-slate-300 [overflow-wrap:anywhere]">{node.claim}</p>

                  <div className="mt-2.5 flex flex-wrap items-center justify-between gap-2 border-t border-slate-800/80 pt-2 font-mono text-[10.5px]">
                    <span className="text-slate-400 [overflow-wrap:anywhere]">{node.signature}</span>
                    <span className="shrink-0 text-emerald-400">
                      [{node.axioms.join(', ')}]
                    </span>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* 3. Counter-Evidence Exhibits */}
          <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-5 sm:p-6">
            <h3 className="flex items-center gap-2 text-base font-semibold text-white">
              <FileSearch className="h-4 w-4 text-cyan-400" aria-hidden="true" />
              Exhibited Primary Evidence ({activeContention.exhibits.length} Verifiable Artifacts)
            </h3>
            <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2">
              {activeContention.exhibits.map((ex) => (
                <button
                  key={ex.id}
                  type="button"
                  onClick={() => onOpenSourceLine(ex.moduleId, ex.line, ex.declaration)}
                  className="flex flex-col justify-between rounded-lg border border-slate-800 bg-[#070b14] p-4 text-left transition-colors hover:border-emerald-500/60 hover:bg-slate-900/70"
                >
                  <div>
                    <div className="flex items-baseline justify-between gap-2">
                      <span className="text-xs font-semibold text-white">{ex.label}</span>
                      <span className="shrink-0 font-mono text-xs font-bold text-emerald-400 tabular-nums">
                        {ex.metric}
                      </span>
                    </div>
                    <p className="mt-1.5 text-xs leading-relaxed text-slate-300">{ex.explanation}</p>
                  </div>
                  <div className="mt-3 flex items-center justify-between border-t border-slate-800/80 pt-2 font-mono text-[10.5px] text-cyan-300 tabular-nums">
                    <span>
                      {ex.moduleId}.lean{ex.line ? `:${ex.line}` : ''}
                    </span>
                    <span className="inline-flex items-center gap-0.5">
                      Open source <ArrowUpRight className="h-3 w-3" />
                    </span>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* 4. Interactive Counter-Evidence Verifier */}
          <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-5 sm:p-6">
            <div className="mb-3">
              <div className="font-mono text-[10.5px] uppercase tracking-wider text-cyan-400">
                Interactive Quantitative &amp; Audit Counter-Check
              </div>
              <h3 className="mt-0.5 text-base font-semibold text-white">
                Live Verification Bench for {activeContention.code}
              </h3>
            </div>
            <ContentionEvidenceLab
              labKind={activeContention.labKind}
              onOpenSourceLine={onOpenSourceLine}
            />
          </div>
        </section>
      </div>
    </div>
  );
}
