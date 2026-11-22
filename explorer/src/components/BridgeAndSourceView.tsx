import { useEffect, useMemo, useState } from 'react';
import { CheckCircle2, FileCode2, HelpCircle, Search } from 'lucide-react';
import {
  BRIDGE_STATEMENTS,
  CORPUS_MODULES,
  THEOREM_CATALOG,
} from '../data/corpusData';

interface BridgeAndSourceViewProps {
  selectedModuleId: string;
  onSelectModule: (moduleId: string) => void;
}

interface ParsedSectionAnchor {
  lineNumber: number;
  title: string;
}

export function BridgeAndSourceView({
  selectedModuleId,
  onSelectModule,
}: BridgeAndSourceViewProps) {
  const [theoremQuery, setTheoremQuery] = useState('');
  const [bridgeFilter, setBridgeFilter] = useState<'all' | 'proved' | 'partial'>('all');
  const [sourceLines, setSourceLines] = useState<string[]>([]);
  const [loadingSource, setLoadingSource] = useState(false);
  const [sourceError, setSourceError] = useState<string | null>(null);
  const [sourceSearch, setSourceSearch] = useState('');
  const [startLine, setStartLine] = useState(1);

  const selectedModule = useMemo(
    () => CORPUS_MODULES.find((m) => m.id === selectedModuleId) ?? CORPUS_MODULES[0],
    [selectedModuleId],
  );

  useEffect(() => {
    let cancelled = false;
    setLoadingSource(true);
    setSourceError(null);
    setStartLine(1);

    fetch(selectedModule.assetPath)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.text();
      })
      .then((text) => {
        if (!cancelled) {
          setSourceLines(text.split('\n'));
          setLoadingSource(false);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setSourceError(err instanceof Error ? err.message : 'Failed to load file');
          setLoadingSource(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [selectedModule.assetPath]);

  const sectionAnchors = useMemo<ParsedSectionAnchor[]>(() => {
    const anchors: ParsedSectionAnchor[] = [];
    sourceLines.forEach((line, idx) => {
      const trimmed = line.trim();
      if (trimmed.startsWith('/-! ##')) {
        anchors.push({
          lineNumber: idx + 1,
          title: trimmed.replace(/^\/-!\s*##\s*/, '').replace(/\s*-\/$/, ''),
        });
      }
    });
    return anchors;
  }, [sourceLines]);

  const filteredBridge = useMemo(() => {
    if (bridgeFilter === 'all') return BRIDGE_STATEMENTS;
    return BRIDGE_STATEMENTS.filter((b) => b.finiteStrongCouplingStatus === bridgeFilter);
  }, [bridgeFilter]);

  const filteredTheorems = useMemo(() => {
    const q = theoremQuery.trim().toLowerCase();
    if (!q) return THEOREM_CATALOG;
    return THEOREM_CATALOG.filter(
      (t) =>
        t.name.toLowerCase().includes(q) ||
        t.statement.toLowerCase().includes(q) ||
        t.moduleId.toLowerCase().includes(q) ||
        t.section.toLowerCase().includes(q),
    );
  }, [theoremQuery]);

  const visibleWindowLines = useMemo(() => {
    const q = sourceSearch.trim().toLowerCase();
    if (q) {
      const matches: Array<{ lineNum: number; text: string }> = [];
      for (let i = 0; i < sourceLines.length; i++) {
        if (sourceLines[i].toLowerCase().includes(q)) {
          matches.push({ lineNum: i + 1, text: sourceLines[i] });
          if (matches.length >= 160) break;
        }
      }
      return matches;
    }

    const sliceStart = Math.max(0, startLine - 1);
    const sliceEnd = Math.min(sourceLines.length, sliceStart + 140);
    return sourceLines.slice(sliceStart, sliceEnd).map((text, idx) => ({
      lineNum: sliceStart + idx + 1,
      text,
    }));
  }, [sourceLines, sourceSearch, startLine]);

  return (
    <div className="space-y-6">
      {/* 9 BridgeStatements Matrix */}
      <section className="rounded-lg border border-slate-800 bg-slate-900 p-5">
        <div className="flex flex-col gap-3 border-b border-slate-800 pb-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="font-mono text-xs uppercase tracking-wider text-slate-400">
              BridgeStatements.lean · Infinite-Volume &amp; Continuum Target Matrix
            </p>
            <h1 className="mt-1 text-xl font-semibold text-slate-100">
              The 9 Formal Bridge Properties: Proved Lattice Core vs Weak-Coupling Gap
            </h1>
          </div>

          <div className="flex items-center gap-1.5">
            {(
              [
                { id: 'all', label: 'All 9 Props' },
                { id: 'proved', label: '● Discharged at Strong Coupling' },
                { id: 'partial', label: '▲ Partial on Z⁴' },
              ] as const
            ).map((f) => (
              <button
                key={f.id}
                type="button"
                onClick={() => setBridgeFilter(f.id)}
                className={`rounded border px-2.5 py-1 text-xs font-medium ${
                  bridgeFilter === f.id
                    ? 'border-slate-700 bg-slate-900 text-white'
                    : 'border-slate-800 bg-slate-800 text-slate-300 hover:bg-slate-700'
                }`}
              >
                {f.label}
              </button>
            ))}
          </div>
        </div>

        <div className="mt-4 grid grid-cols-1 gap-3 md:grid-cols-3">
          {filteredBridge.map((item) => (
            <div
              key={item.id}
              className="flex flex-col justify-between rounded-md border border-slate-800 bg-slate-800/50 p-3.5"
            >
              <div>
                <div className="flex items-center justify-between gap-2">
                  <span className="font-mono text-xs font-semibold text-slate-100">
                    {item.index}. {item.leanName}
                  </span>
                  {item.finiteStrongCouplingStatus === 'proved' ? (
                    <span className="inline-flex items-center gap-1 font-mono text-[11px] font-medium text-emerald-400">
                      <CheckCircle2 className="h-3 w-3" aria-hidden="true" />
                      LATTICE PROVED
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 font-mono text-[11px] font-medium text-amber-400">
                      <HelpCircle className="h-3 w-3" aria-hidden="true" />
                      PARTIAL ON Z⁴
                    </span>
                  )}
                </div>
                <h2 className="mt-1 text-sm font-medium text-slate-200">{item.title}</h2>
                <pre className="mt-2 whitespace-pre-wrap break-words rounded border border-slate-800 bg-slate-900 px-2.5 py-1.5 font-mono text-[11px] leading-snug text-slate-300">
                  {item.leanTargetSignature}
                </pre>
              </div>

              <div className="mt-3 space-y-1.5 border-t border-slate-800 pt-2.5 text-xs leading-relaxed">
                <p className="text-slate-300">
                  <strong className="font-semibold text-emerald-300">Finite / β=1/300:</strong>{' '}
                  {item.finiteVolumeLemma}
                </p>
                <p className="text-slate-400">
                  <strong className="font-semibold text-amber-300">Open a→0⁺, β→∞:</strong>{' '}
                  {item.remainingContinuumGap}
                </p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Theorem Search + Live Source Reader Split */}
      <div className="grid grid-cols-1 gap-6 xl:grid-cols-12">
        {/* Left: Theorem & Module Index */}
        <section className="space-y-4 rounded-lg border border-slate-800 bg-slate-900 p-5 xl:col-span-5">
          <div>
            <h2 className="text-sm font-semibold text-slate-100">
              Verified Theorem &amp; Obstruction Index
            </h2>
            <p className="mt-0.5 text-xs text-slate-400">
              Filter key theorems and click any entry to load its module source on the right.
            </p>
          </div>

          <div className="relative">
            <Search
              className="pointer-events-none absolute left-2.5 top-2.5 h-3.5 w-3.5 text-slate-400"
              aria-hidden="true"
            />
            <input
              type="text"
              value={theoremQuery}
              onChange={(e) => setTheoremQuery(e.target.value)}
              placeholder="Search theorems (e.g. dobrushin, suFlip2, ising, §38)..."
              aria-label="Search theorems"
              className="w-full rounded-md border border-slate-800 bg-slate-800 py-1.5 pl-8 pr-3 text-xs text-slate-100 placeholder:text-slate-400 focus:border-emerald-500 focus:bg-slate-900 focus:outline-none"
            />
          </div>

          <div className="max-h-[540px] space-y-2 overflow-y-auto pr-1">
            {filteredTheorems.map((thm) => {
              const activeMod = thm.moduleId === selectedModule.id;
              return (
                <button
                  key={thm.name}
                  type="button"
                  onClick={() => {
                    onSelectModule(thm.moduleId);
                    setSourceSearch(thm.name);
                  }}
                  className={`w-full rounded-md border p-3 text-left transition-colors ${
                    activeMod
                      ? 'border-emerald-500/40 bg-emerald-500/10'
                      : 'border-slate-800 bg-slate-900 hover:border-slate-600 hover:bg-slate-700'
                  }`}
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="truncate font-mono text-xs font-semibold text-slate-100">
                      {thm.name}
                    </span>
                    <span className="shrink-0 font-mono text-[11px] text-slate-400">
                      {thm.moduleId} · {thm.section}
                    </span>
                  </div>
                  <p className="mt-1 text-xs leading-relaxed text-slate-400">{thm.statement}</p>
                </button>
              );
            })}
            {filteredTheorems.length === 0 && (
              <p className="py-6 text-center text-xs text-slate-400">
                No theorem matched "{theoremQuery}".
              </p>
            )}
          </div>
        </section>

        {/* Right: Genuine Lean Source File Viewer */}
        <section className="flex flex-col rounded-lg border border-slate-800 bg-slate-900 p-5 xl:col-span-7">
          <div className="flex flex-col gap-3 border-b border-slate-800 pb-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-center gap-2">
              <FileCode2 className="h-4 w-4 text-emerald-400" aria-hidden="true" />
              <div>
                <h2 className="font-mono text-sm font-semibold text-slate-100">
                  {selectedModule.fileName} ({selectedModule.sections})
                </h2>
                <div className="font-mono text-[11px] text-slate-400 tabular-nums">
                  {sourceLines.length.toLocaleString()} lines · loaded directly from corpus asset
                </div>
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-2">
              <label htmlFor="module-select" className="sr-only">
                Select Lean Corpus Module
              </label>
              <select
                id="module-select"
                value={selectedModule.id}
                onChange={(e) => {
                  setSourceSearch('');
                  onSelectModule(e.target.value);
                }}
                className="rounded border border-slate-800 bg-slate-800 px-2.5 py-1.5 font-mono text-xs text-slate-200 focus:border-emerald-500 focus:outline-none"
              >
                {CORPUS_MODULES.map((m) => (
                  <option key={m.id} value={m.id}>
                    {m.fileName} ({m.sections})
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Section quick-jump & source filter */}
          <div className="mt-3 flex flex-wrap items-center gap-2 border-b border-slate-800 pb-3">
            <input
              type="text"
              value={sourceSearch}
              onChange={(e) => setSourceSearch(e.target.value)}
              placeholder="Grep within active file..."
              aria-label="Filter lines within active Lean source file"
              className="min-w-[200px] flex-1 rounded border border-slate-800 bg-slate-800 px-2.5 py-1 font-mono text-xs text-slate-200 placeholder:text-slate-400 focus:border-emerald-500 focus:bg-slate-900 focus:outline-none"
            />
            {sectionAnchors.length > 0 && (
              <select
                aria-label="Jump to section in active file"
                value=""
                onChange={(e) => {
                  const line = Number(e.target.value);
                  if (line > 0) {
                    setSourceSearch('');
                    setStartLine(line);
                  }
                }}
                className="max-w-[260px] rounded border border-slate-800 bg-slate-900 px-2.5 py-1 font-mono text-xs text-slate-300"
              >
                <option value="">Jump to § section ({sectionAnchors.length})…</option>
                {sectionAnchors.map((a) => (
                  <option key={a.lineNumber} value={a.lineNumber}>
                    L{a.lineNumber}: {a.title.slice(0, 44)}
                  </option>
                ))}
              </select>
            )}
          </div>

          {/* Source Code Window */}
          <div className="mt-3 flex-1 overflow-hidden rounded-md border border-slate-800 bg-slate-950 text-slate-100">
            {loadingSource ? (
              <div className="p-6 font-mono text-xs text-slate-400">Loading {selectedModule.fileName}…</div>
            ) : sourceError ? (
              <div className="p-6 font-mono text-xs text-rose-400">
                Could not load source: {sourceError}
              </div>
            ) : (
              <div className="max-h-[480px] overflow-auto p-3 font-mono text-[11.5px] leading-relaxed">
                {visibleWindowLines.map((row) => (
                  <div key={row.lineNum} className="flex gap-3 hover:bg-slate-900">
                    <span className="w-11 shrink-0 select-none text-right text-slate-400 tabular-nums">
                      {row.lineNum}
                    </span>
                    <span className="whitespace-pre text-slate-100">{row.text}</span>
                  </div>
                ))}
                {visibleWindowLines.length === 0 && (
                  <div className="p-4 text-slate-400">
                    No lines matching "{sourceSearch}" in {selectedModule.fileName}.
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Pagination when not searching */}
          {!sourceSearch && sourceLines.length > 140 && (
            <div className="mt-3 flex items-center justify-between font-mono text-xs text-slate-400 tabular-nums">
              <span>
                Showing lines {startLine}–{Math.min(sourceLines.length, startLine + 139)} of{' '}
                {sourceLines.length}
              </span>
              <div className="flex gap-1.5">
                <button
                  type="button"
                  disabled={startLine <= 1}
                  onClick={() => setStartLine((s) => Math.max(1, s - 120))}
                  className="rounded border border-slate-800 bg-slate-900 px-2.5 py-1 hover:bg-slate-700 disabled:opacity-40"
                >
                  Prev 120
                </button>
                <button
                  type="button"
                  disabled={startLine + 140 > sourceLines.length}
                  onClick={() => setStartLine((s) => Math.min(sourceLines.length, s + 120))}
                  className="rounded border border-slate-800 bg-slate-900 px-2.5 py-1 hover:bg-slate-700 disabled:opacity-40"
                >
                  Next 120
                </button>
              </div>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
