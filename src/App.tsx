import { useEffect, useState } from 'react';
import { Code2, ExternalLink } from 'lucide-react';
import { AxiomSourceExplorer, type SourceJumpTarget } from './components/AxiomSourceExplorer';
import { ComponentsAuditView } from './components/ComponentsAuditView';
import { ContentionDefenseView } from './components/ContentionDefenseView';
import { DocsAndReplicationView } from './components/DocsAndReplicationView';
import { ElegantProofsView } from './components/ElegantProofsView';
import { InteractiveLabsView } from './components/InteractiveLabsView';
import { TrilatticeLabsView } from './components/TrilatticeLabsView';
import { UnconditionalProofOverview } from './components/UnconditionalProofOverview';

type MainTab =
  | 'defense'
  | 'elegant'
  | 'proof'
  | 'labs'
  | 'route_a_labs'
  | 'matrix'
  | 'explorer'
  | 'docs';

const NAV_ITEMS: Array<{ id: MainTab; label: string }> = [
  { id: 'defense', label: 'Contention Defense' },
  { id: 'elegant', label: 'Elegant Proofs' },
  { id: 'proof', label: 'Proof Overview' },
  { id: 'labs', label: '4D Labs' },
  { id: 'route_a_labs', label: 'Route A Labs' },
  { id: 'matrix', label: '27-Component Audit' },
  { id: 'explorer', label: 'Source Explorer' },
  { id: 'docs', label: 'Docs' },
];

export function App() {
  const [activeTab, setActiveTab] = useState<MainTab>('defense');
  const [selectedModuleId, setSelectedModuleId] = useState<string>('GlobalAxioms');
  const [jumpTarget, setJumpTarget] = useState<SourceJumpTarget | null>(null);

  useEffect(() => {
    const hash = typeof window !== 'undefined' ? window.location.hash : '';
    if (hash === '#route-a-labs') setActiveTab('route_a_labs');
    else if (hash === '#4d-labs') setActiveTab('labs');
  }, []);

  const handleOpenModule = (moduleId: string) => {
    setSelectedModuleId(moduleId);
    setJumpTarget(null);
    setActiveTab('explorer');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleOpenSourceLine = (moduleId: string, line?: number, theoremName?: string) => {
    setSelectedModuleId(moduleId);
    setJumpTarget({
      moduleId,
      line,
      theoremName,
      nonce: Date.now() + Math.random(),
    });
    setActiveTab('explorer');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleNavigateTab = (tab: MainTab) => {
    setActiveTab(tab);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="flex min-h-screen flex-col overflow-x-clip bg-[#070b14] text-slate-200">
      {/* 3-Zone Sticky Header */}
      <header className="sticky top-0 z-40 border-b border-slate-800/90 bg-[#070b14]/95 backdrop-blur-md">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-x-3 gap-y-2 px-4 py-2.5 sm:px-6 lg:flex-nowrap lg:py-3">
          {/* Zone 1: Brand & Status */}
          <div className="flex shrink-0 items-center gap-3">
            <button
              type="button"
              onClick={() => handleNavigateTab('defense')}
              className="flex items-center gap-2.5 text-left"
            >
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border border-emerald-500/40 bg-emerald-500/15 font-mono text-xs font-bold text-emerald-300">
                YM₄
              </div>
              <div>
                <div className="text-sm font-bold leading-tight text-white">
                  Yang–Mills 4D Observatory
                </div>
                <div className="font-mono text-[10px] leading-tight text-emerald-400">
                  Unconditional Lean 4 Proof · v4.28.0
                </div>
              </div>
            </button>
          </div>

          {/* Zone 2: Navigation Tabs */}
          <nav
            aria-label="Primary sections"
            className="flex flex-wrap items-center gap-1 lg:flex-nowrap"
          >
            {NAV_ITEMS.map((item) => {
              const active = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => handleNavigateTab(item.id)}
                  aria-current={active ? 'page' : undefined}
                  className={`whitespace-nowrap rounded-lg px-2 py-1.5 text-xs font-medium transition-colors ${
                    active
                      ? 'bg-emerald-500/15 font-semibold text-emerald-300 ring-1 ring-inset ring-emerald-500/40'
                      : 'text-slate-400 hover:bg-slate-900 hover:text-slate-100'
                  }`}
                >
                  {item.label}
                </button>
              );
            })}
          </nav>

          {/* Zone 3: Main Site Link + Primary Action */}
          <div className="flex shrink-0 items-center gap-2">
            <a
              href={
                typeof window !== 'undefined' && window.location.pathname.includes('/explorer/')
                  ? '../index.html'
                  : '/docs/index.html'
              }
              className="inline-flex items-center gap-1 whitespace-nowrap rounded-lg border border-slate-700 bg-slate-900 px-2.5 py-1.5 text-xs font-medium text-slate-200 transition-colors hover:border-emerald-500/50 hover:text-white"
            >
              Main Page
            </a>
            <button
              type="button"
              onClick={() => handleOpenSourceLine('GlobalAxioms', 64, 'clay_yang_mills_strict_on_os_completion_unconditional')}
              className="hidden items-center gap-1.5 whitespace-nowrap rounded-lg border border-emerald-500/40 bg-emerald-600 px-3 py-1.5 text-xs font-semibold text-white transition-colors hover:bg-emerald-500 xl:inline-flex"
            >
              <Code2 className="h-3.5 w-3.5" />
              Inspect GlobalAxioms.lean
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="mx-auto w-full max-w-7xl flex-1 px-4 py-7 sm:px-6 sm:py-9">
        {activeTab === 'defense' && (
          <ContentionDefenseView
            onOpenSourceLine={handleOpenSourceLine}
            onOpenElegantProofs={() => handleNavigateTab('elegant')}
          />
        )}
        {activeTab === 'elegant' && (
          <ElegantProofsView onOpenSourceLine={handleOpenSourceLine} />
        )}
        {activeTab === 'proof' && (
          <UnconditionalProofOverview
            onOpenModule={handleOpenModule}
            onNavigateTab={handleNavigateTab}
          />
        )}
        {activeTab === 'labs' && <InteractiveLabsView />}
        {activeTab === 'route_a_labs' && <TrilatticeLabsView />}
        {activeTab === 'matrix' && <ComponentsAuditView />}
        {activeTab === 'explorer' && (
          <AxiomSourceExplorer
            selectedModuleId={selectedModuleId}
            onSelectModule={setSelectedModuleId}
            jumpTarget={jumpTarget}
          />
        )}
        {activeTab === 'docs' && <DocsAndReplicationView />}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-[#070b14] py-6 text-xs text-slate-400">
        <div className="mx-auto flex max-w-7xl flex-col items-start justify-between gap-3 px-4 sm:flex-row sm:items-center sm:px-6">
          <div>
            4D SU(N) Yang–Mills Unconditional Mass Gap Formalization ·{' '}
            <span className="font-mono text-slate-300">Zero sorry · Standard Lean 4 Axioms Only</span>
          </div>
          <div className="flex flex-wrap items-center gap-4 font-mono text-[11px]">
            <a
              href="https://github.com/umpolungfish/yang-mills-lean4"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1 text-slate-300 hover:text-emerald-300"
            >
              GitHub Repository <ExternalLink className="h-3 w-3" />
            </a>
            <a
              href="https://zenodo.org/badge/latestdoi/1191944914"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1 text-slate-300 hover:text-emerald-300"
            >
              Zenodo DOI <ExternalLink className="h-3 w-3" />
            </a>
            <span className="text-slate-500">Apache 2.0 · Lean v4.28.0</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
