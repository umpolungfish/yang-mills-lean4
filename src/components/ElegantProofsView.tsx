import { useMemo, useState } from 'react';
import { ArrowUpRight, Compass, Search, Sparkles } from 'lucide-react';
import { ELEGANT_PROOFS, type EleganceTheme } from '../data/elegantProofsData';
import { filterElegantProofs } from '../utils/contentionTrace';

interface ElegantProofsViewProps {
  onOpenSourceLine: (moduleId: string, line?: number, declaration?: string) => void;
}

const THEMES: Array<'ALL' | EleganceTheme> = [
  'ALL',
  'Symmetry & Functoriality',
  'Hilbert & Operator Theory',
  'Measure & Probability',
  'Gauge Algebra & Lean Craft',
];

export function ElegantProofsView({ onOpenSourceLine }: ElegantProofsViewProps) {
  const [selectedTheme, setSelectedTheme] = useState<'ALL' | EleganceTheme>('ALL');
  const [query, setQuery] = useState('');

  const filteredGems = useMemo(
    () => filterElegantProofs(ELEGANT_PROOFS, query, selectedTheme),
    [query, selectedTheme],
  );

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <section className="rounded-xl border border-slate-800 bg-[#0c1220] p-5 sm:p-7">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
          <div className="max-w-3xl space-y-3">
            <div className="font-mono text-xs uppercase tracking-wider text-cyan-300">
              Architectural Highlights · Minimal Machinery, Maximum Reach
            </div>
            <h1 className="text-2xl font-bold tracking-tight text-white sm:text-3xl">
              Eight Gems of Mathematical &amp; Formal Elegance in the Lean 4 Corpus
            </h1>
            <p className="text-sm leading-relaxed text-slate-300">
              Beyond verifying the mass-gap endpoints, several proofs in the repository turn seemingly intractable
              non-Abelian, infinite-dimensional, or analytic steps into crisp algebraic and functorial compressions.
              Select any card&apos;s source link to read the full Lean 4.28.0 derivation in context.
            </p>
          </div>

          <div className="grid shrink-0 grid-cols-2 gap-3 sm:w-72">
            <div className="rounded-lg border border-cyan-500/30 bg-cyan-950/20 p-3">
              <div className="font-mono text-[10px] uppercase text-cyan-300">Curated Proofs</div>
              <div className="mt-1 font-mono text-lg font-bold text-white tabular-nums">
                {ELEGANT_PROOFS.length} Gems
              </div>
              <div className="font-mono text-[10px] text-slate-400">4 thematic pillars</div>
            </div>
            <div className="rounded-lg border border-slate-800 bg-slate-900/90 p-3">
              <div className="font-mono text-[10px] uppercase text-slate-400">Axiom Footprint</div>
              <div className="mt-1 font-mono text-lg font-bold text-emerald-400">Std Only</div>
              <div className="font-mono text-[10px] text-slate-400">0 sorry · direct source</div>
            </div>
          </div>
        </div>
      </section>

      {/* Filter & Search Bar */}
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
              placeholder="Search insights or techniques (e.g. injective, normSq, HasDerivAt, suFlip2, BorelSpace)..."
              aria-label="Search curated elegant proofs"
              className="w-full rounded-md border border-slate-800 bg-[#070b14] py-2 pl-9 pr-3 text-xs text-slate-100 placeholder:text-slate-500 focus:border-cyan-500 focus:outline-none"
            />
          </div>
          <div className="font-mono text-xs text-slate-400 tabular-nums">
            Showing {filteredGems.length} of {ELEGANT_PROOFS.length} highlights
          </div>
        </div>

        <div className="flex flex-wrap gap-1.5">
          {THEMES.map((theme) => {
            const active = selectedTheme === theme;
            return (
              <button
                key={theme}
                type="button"
                onClick={() => setSelectedTheme(theme)}
                className={`rounded border px-2.5 py-1 font-mono text-[11px] transition-colors ${
                  active
                    ? 'border-cyan-500 bg-cyan-500/15 font-semibold text-cyan-200'
                    : 'border-slate-800 bg-[#070b14] text-slate-400 hover:border-slate-700 hover:text-slate-200'
                }`}
              >
                {theme === 'ALL' ? 'All Pillars (8)' : theme}
              </button>
            );
          })}
        </div>
      </section>

      {/* Gems Grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {filteredGems.map((gem) => (
          <article
            key={gem.id}
            className="flex min-w-0 flex-col justify-between rounded-xl border border-slate-800 bg-[#0c1220] p-5 sm:p-6"
          >
            <div className="min-w-0 space-y-4">
              {/* Card Header */}
              <div className="flex flex-wrap items-center justify-between gap-2">
                <span className="font-mono text-[11px] font-semibold uppercase tracking-wider text-cyan-300">
                  {gem.code} · {gem.theme}
                </span>
                <button
                  type="button"
                  onClick={() => onOpenSourceLine(gem.moduleId, gem.line, gem.declaration)}
                  className="inline-flex items-center gap-1 font-mono text-xs text-emerald-300 hover:text-emerald-200"
                >
                  {gem.moduleId}.lean:{gem.line} ({gem.lineSpan})
                  <ArrowUpRight className="h-3.5 w-3.5" aria-hidden="true" />
                </button>
              </div>

              <div>
                <h2 className="text-lg font-bold leading-snug text-white">{gem.title}</h2>
                <div className="mt-1 font-mono text-xs text-emerald-400 [overflow-wrap:anywhere]">
                  {gem.declaration}
                </div>
              </div>

              {/* Core Insight */}
              <div className="rounded-lg border border-cyan-500/30 bg-cyan-950/15 p-3.5">
                <div className="flex items-center gap-1.5 font-mono text-[10.5px] font-semibold uppercase text-cyan-300">
                  <Sparkles className="h-3.5 w-3.5" aria-hidden="true" />
                  Key Compression Insight
                </div>
                <p className="mt-1.5 text-xs leading-relaxed text-slate-200 [overflow-wrap:anywhere]">
                  {gem.coreInsight}
                </p>
              </div>

              {/* Why It's Elegant */}
              <div className="space-y-1.5">
                <div className="flex items-center gap-1.5 font-mono text-[10.5px] font-semibold uppercase text-slate-400">
                  <Compass className="h-3.5 w-3.5 text-emerald-400" aria-hidden="true" />
                  Why This Avoids Brute Force
                </div>
                <p className="text-xs leading-relaxed text-slate-300 [overflow-wrap:anywhere]">
                  {gem.contrastWithBruteForce}
                </p>
              </div>

              {/* Lean Excerpt */}
              <div className="overflow-x-auto rounded-lg border border-slate-800 bg-[#070b14] p-3.5">
                <pre className="font-mono text-[11px] leading-relaxed text-slate-200">
                  <code>{gem.leanExcerpt}</code>
                </pre>
              </div>
            </div>

            {/* Footer Payoff + Deep Link */}
            <div className="mt-4 flex flex-wrap items-center justify-between gap-3 border-t border-slate-800/80 pt-3">
              <span className="min-w-0 flex-1 text-xs font-medium text-emerald-300 [overflow-wrap:anywhere]">
                Payoff: {gem.payoff}
              </span>
              <button
                type="button"
                onClick={() => onOpenSourceLine(gem.moduleId, gem.line, gem.declaration)}
                className="inline-flex shrink-0 items-center gap-1 rounded-md border border-slate-700 bg-slate-900 px-3 py-1.5 font-mono text-[11px] font-semibold text-cyan-200 transition-colors hover:border-cyan-500/60 hover:bg-slate-800"
              >
                Inspect line {gem.line}
                <ArrowUpRight className="h-3 w-3" aria-hidden="true" />
              </button>
            </div>
          </article>
        ))}
      </div>

      {filteredGems.length === 0 && (
        <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-8 text-center font-mono text-xs text-slate-400">
          No elegant proof gems matched &ldquo;{query}&rdquo;.
        </div>
      )}
    </div>
  );
}
