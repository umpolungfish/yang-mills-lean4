import { Fragment, useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowUpRight,
  CheckCircle2,
  FileCode2,
  FolderGit2,
  GitBranch,
  Search,
} from 'lucide-react';
import {
  ALL_106_MODULES,
  AUDITED_THEOREMS,
  CORPUS_CATEGORIES,
  MODULE_BY_ID,
  TOTAL_CORPUS_LINES,
  type CorpusCategory,
  type LinkedTheoremAudit,
} from '../data/theoremsCatalog';
import { CORPUS_MODULES } from '../data/proofData';

export interface SourceJumpTarget {
  moduleId: string;
  line?: number;
  theoremName?: string;
  nonce: number;
}

interface AxiomSourceExplorerProps {
  selectedModuleId: string;
  onSelectModule: (moduleId: string) => void;
  jumpTarget?: SourceJumpTarget | null;
}

interface ParsedSectionAnchor {
  lineNumber: number;
  title: string;
}

const LEAN_KEYWORDS = new Set([
  'theorem',
  'lemma',
  'def',
  'structure',
  'abbrev',
  'instance',
  'inductive',
  'class',
  'noncomputable',
  'private',
  'protected',
  'import',
  'namespace',
  'end',
  'section',
  'open',
  'variable',
  'universe',
  'where',
  'extends',
  'by',
  'have',
  'let',
  'show',
  'exact',
  'rw',
  'calc',
  'intro',
  'intros',
  'apply',
  'refine',
  'simp',
  'ring',
  'linarith',
  'norm_num',
  'fun',
  'match',
  'with',
  'if',
  'then',
  'else',
  'for',
  'in',
  'do',
  'return',
]);

const LEAN_TYPES_AND_QUANTIFIERS = new Set([
  'Type',
  'Prop',
  'Sort',
  'ℝ',
  'ℂ',
  'ℕ',
  'ℤ',
  '∀',
  '∃',
  'Fin',
  'ENNReal',
  'NNReal',
  'Matrix',
  'Measure',
  'True',
  'False',
]);

function renderLeanLineTokens(line: string, inBlockComment: boolean) {
  if (inBlockComment) {
    return <span className="italic text-slate-500">{line}</span>;
  }

  const trimmed = line.trim();
  if (trimmed.startsWith('--')) {
    return <span className="italic text-slate-500">{line}</span>;
  }
  if (trimmed.startsWith('/-!') || trimmed.startsWith('/--')) {
    return <span className="italic text-emerald-300/75">{line}</span>;
  }
  if (trimmed.startsWith('/-')) {
    return <span className="italic text-slate-500">{line}</span>;
  }

  // Split trailing `--` comment if not inside quotes
  let codePart = line;
  let commentPart = '';
  const commentIdx = line.indexOf(' --');
  if (commentIdx >= 0) {
    codePart = line.slice(0, commentIdx);
    commentPart = line.slice(commentIdx);
  } else if (trimmed.startsWith('--')) {
    return <span className="italic text-slate-500">{line}</span>;
  }

  // Tokenize words, delimiters, strings, numbers
  const tokenRegex = /("(?:[^"\\]|\\.)*"|\b[A-Za-z_][A-Za-z0-9_']*\b|[∀∃ℝℂℕℤ]+|\b\d+(?:\.\d+)?\b|:=|=>|->|<-|≤|≥|≠)/g;
  const parts: Array<{ text: string; cls?: string }> = [];
  let lastIndex = 0;
  let match: RegExpExecArray | null = tokenRegex.exec(codePart);

  while (match !== null) {
    if (match.index > lastIndex) {
      parts.push({ text: codePart.slice(lastIndex, match.index) });
    }
    const tok = match[0];
    let cls: string | undefined;
    if (tok.startsWith('"')) {
      cls = 'text-amber-300';
    } else if (LEAN_KEYWORDS.has(tok)) {
      cls = 'font-semibold text-sky-300';
    } else if (LEAN_TYPES_AND_QUANTIFIERS.has(tok)) {
      cls = 'text-emerald-300';
    } else if (/^\d/.test(tok)) {
      cls = 'text-violet-300';
    } else if (tok === ':=' || tok === '=>' || tok === '->' || tok === '<-' || tok === '≤' || tok === '≥' || tok === '≠') {
      cls = 'text-cyan-400';
    }
    parts.push({ text: tok, cls });
    lastIndex = match.index + tok.length;
    match = tokenRegex.exec(codePart);
  }

  if (lastIndex < codePart.length) {
    parts.push({ text: codePart.slice(lastIndex) });
  }

  return (
    <Fragment>
      {parts.map((p, idx) =>
        p.cls ? (
          <span key={idx} className={p.cls}>
            {p.text}
          </span>
        ) : (
          <Fragment key={idx}>{p.text}</Fragment>
        ),
      )}
      {commentPart && <span className="italic text-slate-500">{commentPart}</span>}
    </Fragment>
  );
}

const HEADLINE_QUICK_MODULES = [
  'GlobalAxioms',
  'BalabanFromStage',
  'IIDPoincareContinuation',
  'SUClosure',
  'SchwingerConv',
  'CubicHaar4D',
];

export function AxiomSourceExplorer({
  selectedModuleId,
  onSelectModule,
  jumpTarget,
}: AxiomSourceExplorerProps) {
  const [leftTab, setLeftTab] = useState<'theorems' | 'modules'>('theorems');
  const [theoremQuery, setTheoremQuery] = useState('');
  const [layerFilter, setLayerFilter] = useState<'all' | 'unconditional'>('all');
  const [moduleQuery, setModuleQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState<'all' | CorpusCategory>('all');

  const [sourceLines, setSourceLines] = useState<string[]>([]);
  const [loadingSource, setLoadingSource] = useState(false);
  const [sourceError, setSourceError] = useState<string | null>(null);
  const [sourceSearch, setSourceSearch] = useState('');
  const [startLine, setStartLine] = useState(1);
  const [highlightedLine, setHighlightedLine] = useState<number | null>(null);
  const [activeTheoremName, setActiveTheoremName] = useState<string | null>(null);

  // Ref preserves target jump line when switching modules asynchronously
  const pendingJumpRef = useRef<{ moduleId: string; line: number; theoremName?: string } | null>(null);
  const highlightedRowRef = useRef<HTMLDivElement | null>(null);

  const selectedModule = useMemo(
    () => MODULE_BY_ID[selectedModuleId] ?? MODULE_BY_ID.GlobalAxioms ?? ALL_106_MODULES[0],
    [selectedModuleId],
  );

  const displaySummary = useMemo(() => {
    const curated = CORPUS_MODULES.find((c) => c.id === selectedModule.id)?.summary;
    if (curated) return curated;
    const raw = selectedModule.summary.trim();
    if (!raw || /[.!?)`]$/.test(raw) || raw.length < 210) return raw;
    const cut = raw.lastIndexOf(' ');
    return `${cut > 40 ? raw.slice(0, cut) : raw}…`;
  }, [selectedModule]);

  useEffect(() => {
    if (highlightedLine !== null && highlightedRowRef.current) {
      highlightedRowRef.current.scrollIntoView({ block: 'center', behavior: 'smooth' });
    }
  }, [highlightedLine, sourceLines]);

  useEffect(() => {
    let cancelled = false;
    setLoadingSource(true);
    setSourceError(null);

    const initialPending = pendingJumpRef.current;
    const isInitialTargetedJump = initialPending && initialPending.moduleId === selectedModule.id;
    if (!isInitialTargetedJump && !(jumpTarget && jumpTarget.moduleId === selectedModule.id && jumpTarget.line)) {
      setStartLine(1);
      setHighlightedLine(null);
      setActiveTheoremName(null);
    }

    fetch(selectedModule.assetPath)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.text();
      })
      .then((text) => {
        if (!cancelled) {
          const lines = text.split('\n');
          setSourceLines(lines);
          setLoadingSource(false);

          const activePending = pendingJumpRef.current;
          if (activePending && activePending.moduleId === selectedModule.id) {
            const clampedLine = Math.max(1, Math.min(lines.length, activePending.line));
            setStartLine(Math.max(1, clampedLine - 14));
            setHighlightedLine(clampedLine);
            setActiveTheoremName(activePending.theoremName ?? null);
            pendingJumpRef.current = null;
          }
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setSourceError(err instanceof Error ? err.message : 'Failed to load Lean source');
          setLoadingSource(false);
          pendingJumpRef.current = null;
        }
      });

    return () => {
      cancelled = true;
    };
  }, [selectedModule.assetPath, selectedModule.id]);

  const jumpToModuleLine = (moduleId: string, line: number, theoremName?: string) => {
    setSourceSearch('');
    if (moduleId === selectedModule.id && !loadingSource && sourceLines.length > 0) {
      const clampedLine = Math.max(1, Math.min(sourceLines.length, line));
      setStartLine(Math.max(1, clampedLine - 14));
      setHighlightedLine(clampedLine);
      setActiveTheoremName(theoremName ?? null);
    } else {
      pendingJumpRef.current = { moduleId, line, theoremName };
      onSelectModule(moduleId);
    }
  };

  useEffect(() => {
    if (!jumpTarget) return;
    if (jumpTarget.line && jumpTarget.line > 0) {
      jumpToModuleLine(jumpTarget.moduleId, jumpTarget.line, jumpTarget.theoremName);
    } else {
      setSourceSearch('');
      pendingJumpRef.current = null;
      onSelectModule(jumpTarget.moduleId);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [jumpTarget?.nonce]);

  const handleClickTheorem = (thm: LinkedTheoremAudit) => {
    if (!thm.module || !thm.line) return;
    jumpToModuleLine(thm.module, thm.line, thm.name);
  };

  const sectionAnchors = useMemo<ParsedSectionAnchor[]>(() => {
    const anchors: ParsedSectionAnchor[] = [];
    sourceLines.forEach((line, idx) => {
      const trimmed = line.trim();
      if (trimmed.startsWith('/-! ##') || trimmed.startsWith('/-!')) {
        const clean = trimmed.replace(/^\/-!\s*(##\s*)?/, '').replace(/\s*-\/$/, '').trim();
        if (clean.length > 0 && clean.length <= 72) {
          anchors.push({ lineNumber: idx + 1, title: clean });
        }
      }
    });
    return anchors;
  }, [sourceLines]);

  const filteredTheorems = useMemo(() => {
    const q = theoremQuery.trim().toLowerCase();
    return AUDITED_THEOREMS.filter((t) => {
      if (layerFilter === 'unconditional') {
        const sec = t.section.toLowerCase();
        const nm = t.name.toLowerCase();
        const isUncond =
          sec.includes('§47') ||
          sec.includes('§48') ||
          sec.includes('§49') ||
          sec.includes('§50') ||
          sec.includes('§51') ||
          sec.includes('§52') ||
          nm.includes('unconditional') ||
          nm.includes('strictclay') ||
          nm.includes('balaban') ||
          nm.includes('poincarecontinuation') ||
          nm.includes('suclosure');
        if (!isUncond) return false;
      }
      if (!q) return true;
      return (
        t.name.toLowerCase().includes(q) ||
        t.section.toLowerCase().includes(q) ||
        (t.module?.toLowerCase().includes(q) ?? false) ||
        t.axioms.some((a) => a.toLowerCase().includes(q))
      );
    });
  }, [theoremQuery, layerFilter]);

  const filteredModules = useMemo(() => {
    const q = moduleQuery.trim().toLowerCase();
    return ALL_106_MODULES.filter((m) => {
      if (categoryFilter !== 'all' && m.category !== categoryFilter) return false;
      if (!q) return true;
      return (
        m.fileName.toLowerCase().includes(q) ||
        m.summary.toLowerCase().includes(q) ||
        m.declarations.some((d) => d.name.toLowerCase().includes(q))
      );
    });
  }, [moduleQuery, categoryFilter]);

  const visibleWindowLines = useMemo(() => {
    const q = sourceSearch.trim().toLowerCase();
    if (q) {
      const matches: Array<{ lineNum: number; text: string; inBlockComment: boolean }> = [];
      for (let i = 0; i < sourceLines.length; i++) {
        if (sourceLines[i].toLowerCase().includes(q)) {
          matches.push({ lineNum: i + 1, text: sourceLines[i], inBlockComment: false });
          if (matches.length >= 160) break;
        }
      }
      return matches;
    }

    const sliceStart = Math.max(0, startLine - 1);
    const sliceEnd = Math.min(sourceLines.length, sliceStart + 140);

    // Track multi-line `/- ... -/` comment state up to sliceEnd
    let blockDepth = 0;
    const rows: Array<{ lineNum: number; text: string; inBlockComment: boolean }> = [];
    for (let i = 0; i < sliceEnd; i++) {
      const line = sourceLines[i];
      const wasInBlock = blockDepth > 0;
      const opens = (line.match(/\/-(?!-)/g) || []).length;
      const closes = (line.match(/-\//g) || []).length;
      if (i >= sliceStart) {
        rows.push({
          lineNum: i + 1,
          text: line,
          inBlockComment: wasInBlock && !line.trim().startsWith('/-'),
        });
      }
      blockDepth = Math.max(0, blockDepth + opens - closes);
    }
    return rows;
  }, [sourceLines, sourceSearch, startLine]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <section className="rounded-xl border border-slate-800 bg-[#0c1220] p-5">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="font-mono text-xs uppercase tracking-wider text-emerald-400">
              Lean 4.28.0 Kernel Audit &amp; Complete {ALL_106_MODULES.length}-Module Corpus Workbench
            </div>
            <h1 className="mt-1 text-xl font-bold text-white">
              {AUDITED_THEOREMS.length} Audited Declarations · {ALL_106_MODULES.length} Lean Source Files ·{' '}
              {TOTAL_CORPUS_LINES.toLocaleString()} Lines
            </h1>
            <p className="mt-1 text-xs text-slate-400">
              Every theorem passes Lean&apos;s kernel check with 0 <code className="font-mono">sorry</code> and only
              standard axioms (<code className="font-mono">propext</code>,{' '}
              <code className="font-mono">Classical.choice</code>, <code className="font-mono">Quot.sound</code>).
            </p>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {HEADLINE_QUICK_MODULES.map((quickId) => (
              <button
                key={quickId}
                type="button"
                onClick={() => {
                  setSourceSearch('');
                  onSelectModule(quickId);
                }}
                className={`whitespace-nowrap rounded border px-2.5 py-1 font-mono text-xs transition-colors ${
                  selectedModule.id === quickId
                    ? 'border-emerald-500 bg-emerald-500/15 text-emerald-300'
                    : 'border-slate-800 bg-slate-900 text-slate-300 hover:bg-slate-800'
                }`}
              >
                {quickId}.lean
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Split Layout: Kernel Audit + 106-Module Directory | Live Lean Source IDE */}
      <div className="grid grid-cols-1 gap-6 xl:grid-cols-12">
        {/* Left: Switchable Audited Theorem Index vs All 106 Modules */}
        <section className="flex min-w-0 flex-col space-y-3 rounded-xl border border-slate-800 bg-[#0c1220] p-5 xl:col-span-5">
          {/* Primary Left Panel Mode Switcher */}
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div className="flex rounded-lg border border-slate-800 bg-slate-950 p-0.5 font-mono text-xs">
              <button
                type="button"
                onClick={() => setLeftTab('theorems')}
                className={`whitespace-nowrap rounded-md px-2.5 py-1 transition-colors ${
                  leftTab === 'theorems'
                    ? 'bg-emerald-500/15 font-semibold text-emerald-300'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                Audited Theorems ({AUDITED_THEOREMS.length})
              </button>
              <button
                type="button"
                onClick={() => setLeftTab('modules')}
                className={`whitespace-nowrap rounded-md px-2.5 py-1 transition-colors ${
                  leftTab === 'modules'
                    ? 'bg-sky-500/15 font-semibold text-sky-300'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                All Modules ({ALL_106_MODULES.length})
              </button>
            </div>

            {leftTab === 'theorems' && (
              <div className="flex rounded border border-slate-800 bg-slate-900 p-0.5 font-mono text-[11px]">
                <button
                  type="button"
                  onClick={() => setLayerFilter('all')}
                  className={`rounded px-2 py-0.5 ${
                    layerFilter === 'all' ? 'bg-slate-800 text-white' : 'text-slate-400'
                  }`}
                >
                  All
                </button>
                <button
                  type="button"
                  onClick={() => setLayerFilter('unconditional')}
                  className={`rounded px-2 py-0.5 ${
                    layerFilter === 'unconditional' ? 'bg-emerald-600 text-white' : 'text-slate-400'
                  }`}
                >
                  §§47–52
                </button>
              </div>
            )}
          </div>

          {leftTab === 'theorems' ? (
            <>
              <div className="relative">
                <Search
                  className="pointer-events-none absolute left-2.5 top-2.5 h-3.5 w-3.5 text-slate-400"
                  aria-hidden="true"
                />
                <input
                  type="text"
                  value={theoremQuery}
                  onChange={(e) => setTheoremQuery(e.target.value)}
                  placeholder="Search theorems or modules (click any card to jump to line)..."
                  aria-label="Search audited theorems"
                  className="w-full rounded-md border border-slate-800 bg-slate-900 py-1.5 pl-8 pr-3 text-xs text-slate-100 placeholder:text-slate-500 focus:border-emerald-500 focus:outline-none"
                />
              </div>

              <div className="max-h-[580px] space-y-2 overflow-y-auto pr-1">
                {filteredTheorems.map((thm) => {
                  const canJump = Boolean(thm.module && thm.line);
                  const isActiveTarget =
                    canJump &&
                    thm.module === selectedModule.id &&
                    thm.line === highlightedLine;

                  return (
                    <button
                      key={`${thm.section}-${thm.name}`}
                      type="button"
                      disabled={!canJump}
                      onClick={() => handleClickTheorem(thm)}
                      className={`w-full rounded-md border p-2.5 text-left transition-colors ${
                        isActiveTarget
                          ? 'border-cyan-400 bg-cyan-950/35'
                          : canJump
                            ? 'border-slate-800/90 bg-slate-900/70 hover:border-emerald-500/60 hover:bg-slate-900'
                            : 'border-slate-800/60 bg-slate-900/40 opacity-85'
                      }`}
                    >
                      <div className="flex items-center justify-between gap-2">
                        <span className="truncate font-mono text-xs font-semibold text-emerald-300">
                          {thm.name}
                        </span>
                        <span className="inline-flex shrink-0 items-center gap-1 font-mono text-[10px] font-semibold text-emerald-400">
                          <CheckCircle2 className="h-3 w-3" aria-hidden="true" />
                          {thm.status}
                        </span>
                      </div>
                      <div className="mt-1 flex flex-wrap items-center justify-between gap-2 text-[11px] text-slate-400">
                        <span>{thm.section}</span>
                        {canJump && (
                          <span className="inline-flex items-center gap-0.5 font-mono text-[10px] text-cyan-300 tabular-nums">
                            {thm.module}.lean:{thm.line}
                            <ArrowUpRight className="h-2.5 w-2.5" />
                          </span>
                        )}
                      </div>
                      <div className="mt-1.5 flex flex-wrap gap-1 font-mono text-[10px] text-slate-400">
                        {thm.axioms.map((ax) => (
                          <span key={ax} className="rounded border border-slate-800 bg-slate-950 px-1.5 py-0.5">
                            {ax}
                          </span>
                        ))}
                      </div>
                    </button>
                  );
                })}
                {filteredTheorems.length === 0 && (
                  <div className="py-8 text-center font-mono text-xs text-slate-500">
                    No theorems matched &ldquo;{theoremQuery}&rdquo;.
                  </div>
                )}
              </div>
              <div className="font-mono text-[11px] text-slate-500 tabular-nums">
                Showing {filteredTheorems.length} of {AUDITED_THEOREMS.length} kernel-audited declarations
              </div>
            </>
          ) : (
            <>
              <div className="relative">
                <Search
                  className="pointer-events-none absolute left-2.5 top-2.5 h-3.5 w-3.5 text-slate-400"
                  aria-hidden="true"
                />
                <input
                  type="text"
                  value={moduleQuery}
                  onChange={(e) => setModuleQuery(e.target.value)}
                  placeholder="Filter 106 modules by filename, summary, or declaration..."
                  aria-label="Search 106 Lean modules"
                  className="w-full rounded-md border border-slate-800 bg-slate-900 py-1.5 pl-8 pr-3 text-xs text-slate-100 placeholder:text-slate-500 focus:border-sky-500 focus:outline-none"
                />
              </div>

              {/* Category Filter Chips */}
              <div className="flex flex-wrap gap-1 font-mono text-[10px]">
                <button
                  type="button"
                  onClick={() => setCategoryFilter('all')}
                  className={`rounded border px-2 py-0.5 ${
                    categoryFilter === 'all'
                      ? 'border-sky-500 bg-sky-500/15 text-sky-300'
                      : 'border-slate-800 bg-slate-900 text-slate-400 hover:text-slate-200'
                  }`}
                >
                  All ({ALL_106_MODULES.length})
                </button>
                {CORPUS_CATEGORIES.map((cat) => (
                  <button
                    key={cat}
                    type="button"
                    onClick={() => setCategoryFilter(cat)}
                    className={`rounded border px-2 py-0.5 ${
                      categoryFilter === cat
                        ? 'border-sky-500 bg-sky-500/15 text-sky-300'
                        : 'border-slate-800 bg-slate-900 text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    {cat}
                  </button>
                ))}
              </div>

              <div className="max-h-[530px] space-y-2 overflow-y-auto pr-1">
                {filteredModules.map((mod) => {
                  const isActive = mod.id === selectedModule.id;
                  return (
                    <button
                      key={mod.id}
                      type="button"
                      onClick={() => {
                        setSourceSearch('');
                        onSelectModule(mod.id);
                      }}
                      className={`w-full rounded-md border p-2.5 text-left transition-colors ${
                        isActive
                          ? 'border-sky-400 bg-sky-950/35'
                          : 'border-slate-800/90 bg-slate-900/70 hover:border-sky-500/50 hover:bg-slate-900'
                      }`}
                    >
                      <div className="flex items-center justify-between gap-2">
                        <span className="truncate font-mono text-xs font-semibold text-white">
                          {mod.fileName}
                        </span>
                        <span className="shrink-0 font-mono text-[10px] text-slate-400 tabular-nums">
                          {mod.lineCount.toLocaleString()} L · {mod.declarations.length} decls
                        </span>
                      </div>
                      <div className="mt-1 font-mono text-[10px] text-sky-300/90">
                        {mod.category}
                      </div>
                      <p className="mt-1 line-clamp-2 text-[11px] leading-snug text-slate-400">
                        {mod.summary}
                      </p>
                    </button>
                  );
                })}
                {filteredModules.length === 0 && (
                  <div className="py-8 text-center font-mono text-xs text-slate-500">
                    No modules matched &ldquo;{moduleQuery}&rdquo;.
                  </div>
                )}
              </div>
              <div className="font-mono text-[11px] text-slate-500 tabular-nums">
                Showing {filteredModules.length} of {ALL_106_MODULES.length} Lean source modules
              </div>
            </>
          )}
        </section>

        {/* Right: Genuine Lean Source Viewer with Syntax Highlighting & Dependency Traversal */}
        <section className="flex min-w-0 flex-col rounded-xl border border-slate-800 bg-[#0c1220] p-5 xl:col-span-7">
          <div className="flex flex-col gap-3 border-b border-slate-800 pb-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-center gap-2.5">
              <FileCode2 className="h-4 w-4 shrink-0 text-emerald-400" aria-hidden="true" />
              <div>
                <h2 className="font-mono text-sm font-semibold text-white">
                  {selectedModule.fileName}
                </h2>
                <div className="font-mono text-[11px] text-slate-400 tabular-nums">
                  {sourceLines.length.toLocaleString()} lines · {selectedModule.category} ·{' '}
                  {selectedModule.declarations.length} indexed declarations
                </div>
              </div>
            </div>

            <div>
              <label htmlFor="module-select" className="sr-only">
                Select Lean source module
              </label>
              <select
                id="module-select"
                value={selectedModule.id}
                onChange={(e) => {
                  setSourceSearch('');
                  onSelectModule(e.target.value);
                }}
                className="w-full max-w-full rounded border border-slate-700 bg-slate-900 px-2.5 py-1.5 font-mono text-xs text-slate-200 focus:border-emerald-500 focus:outline-none sm:max-w-[260px]"
              >
                {ALL_106_MODULES.map((m) => (
                  <option key={m.id} value={m.id}>
                    {m.fileName} ({m.lineCount} L)
                  </option>
                ))}
              </select>
            </div>
          </div>

          <p className="mt-3 text-xs leading-relaxed text-slate-300">{displaySummary}</p>

          {/* Module Import / Imported-By Dependency Traversal Bar */}
          {(selectedModule.imports.length > 0 || selectedModule.importedBy.length > 0) && (
            <div className="mt-3 space-y-1.5 rounded-lg border border-slate-800/80 bg-[#080d18] p-3 font-mono text-[10px]">
              {selectedModule.imports.length > 0 && (
                <div className="flex flex-wrap items-center gap-1.5">
                  <span className="inline-flex items-center gap-1 text-slate-400">
                    <GitBranch className="h-3 w-3 text-sky-400" />
                    Imports:
                  </span>
                  {selectedModule.imports.map((imp) => (
                    <button
                      key={imp}
                      type="button"
                      onClick={() => {
                        setSourceSearch('');
                        onSelectModule(imp);
                      }}
                      className="rounded border border-slate-800 bg-slate-900 px-1.5 py-0.5 text-sky-300 hover:border-sky-500/60 hover:bg-slate-800"
                    >
                      {imp}
                    </button>
                  ))}
                </div>
              )}
              {selectedModule.importedBy.length > 0 && (
                <div className="flex flex-wrap items-center gap-1.5">
                  <span className="inline-flex items-center gap-1 text-slate-400">
                    <FolderGit2 className="h-3 w-3 text-emerald-400" />
                    Used by:
                  </span>
                  {selectedModule.importedBy.map((rev) => (
                    <button
                      key={rev}
                      type="button"
                      onClick={() => {
                        setSourceSearch('');
                        onSelectModule(rev);
                      }}
                      className="rounded border border-slate-800 bg-slate-900 px-1.5 py-0.5 text-emerald-300 hover:border-emerald-500/60 hover:bg-slate-800"
                    >
                      {rev}
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Grep + Declaration Outline + Section Jump */}
          <div className="mt-3 flex flex-wrap items-center gap-2 border-b border-slate-800 pb-3">
            <input
              type="text"
              value={sourceSearch}
              onChange={(e) => setSourceSearch(e.target.value)}
              placeholder="Grep inside active file..."
              aria-label="Filter lines within active Lean source file"
              className="min-w-[160px] flex-1 rounded border border-slate-800 bg-slate-900 px-2.5 py-1.5 font-mono text-xs text-slate-200 placeholder:text-slate-500 focus:border-emerald-500 focus:outline-none"
            />
            {selectedModule.declarations.length > 0 && (
              <select
                aria-label="Jump to Lean declaration in active file"
                value=""
                onChange={(e) => {
                  const line = Number(e.target.value);
                  if (line > 0) {
                    const decl = selectedModule.declarations.find((d) => d.line === line);
                    jumpToModuleLine(selectedModule.id, line, decl?.name);
                  }
                }}
                className="max-w-[230px] rounded border border-slate-800 bg-slate-900 px-2.5 py-1.5 font-mono text-xs text-cyan-300"
              >
                <option value="">
                  Declarations ({selectedModule.declarations.length})…
                </option>
                {selectedModule.declarations.map((d) => (
                  <option key={`${d.name}-${d.line}`} value={d.line}>
                    L{d.line} [{d.kind}] {d.name}
                  </option>
                ))}
              </select>
            )}
            {sectionAnchors.length > 0 && (
              <select
                aria-label="Jump to section in active Lean file"
                value=""
                onChange={(e) => {
                  const line = Number(e.target.value);
                  if (line > 0) {
                    jumpToModuleLine(selectedModule.id, line);
                  }
                }}
                className="max-w-[210px] rounded border border-slate-800 bg-slate-900 px-2.5 py-1.5 font-mono text-xs text-slate-300"
              >
                <option value="">Sections ({sectionAnchors.length})…</option>
                {sectionAnchors.map((a) => (
                  <option key={a.lineNumber} value={a.lineNumber}>
                    L{a.lineNumber}: {a.title.slice(0, 36)}
                  </option>
                ))}
              </select>
            )}
          </div>

          {/* Active Jump Indicator */}
          {highlightedLine !== null && !sourceSearch && (
            <div className="mt-2.5 flex items-center justify-between rounded border border-cyan-500/30 bg-cyan-950/30 px-3 py-1.5 font-mono text-[11px] text-cyan-200 tabular-nums">
              <span>
                Focused line {highlightedLine}
                {activeTheoremName ? ` · ${activeTheoremName}` : ''}
              </span>
              <button
                type="button"
                onClick={() => {
                  setHighlightedLine(null);
                  setActiveTheoremName(null);
                }}
                className="text-cyan-400 hover:text-white"
              >
                Clear highlight
              </button>
            </div>
          )}

          {/* Code Viewer */}
          <div className="mt-3 min-w-0 flex-1 overflow-hidden rounded-lg border border-slate-800 bg-[#070b14]">
            {loadingSource ? (
              <div className="p-6 font-mono text-xs text-slate-400">
                Loading {selectedModule.fileName}…
              </div>
            ) : sourceError ? (
              <div className="p-6 font-mono text-xs text-rose-400">
                Could not load source: {sourceError}
              </div>
            ) : (
              <div className="max-h-[480px] overflow-auto py-2.5 font-mono text-[11.5px] leading-relaxed">
                {visibleWindowLines.map((row) => {
                  const isHighlighted = highlightedLine === row.lineNum;
                  return (
                    <div
                      key={row.lineNum}
                      ref={isHighlighted ? highlightedRowRef : undefined}
                      className={`flex gap-3 px-3 ${
                        isHighlighted
                          ? 'bg-cyan-500/15 ring-1 ring-inset ring-cyan-500/40'
                          : 'hover:bg-slate-900/70'
                      }`}
                    >
                      <span
                        className={`w-10 shrink-0 select-none text-right tabular-nums ${
                          isHighlighted ? 'font-bold text-cyan-300' : 'text-slate-600'
                        }`}
                      >
                        {row.lineNum}
                      </span>
                      <span className="whitespace-pre text-slate-200">
                        {renderLeanLineTokens(row.text, row.inBlockComment)}
                      </span>
                    </div>
                  );
                })}
                {visibleWindowLines.length === 0 && (
                  <div className="p-4 text-slate-400">
                    No lines matching &ldquo;{sourceSearch}&rdquo; in {selectedModule.fileName}.
                  </div>
                )}
              </div>
            )}
          </div>

          {!sourceSearch && sourceLines.length > 140 && (
            <div className="mt-3 flex flex-wrap items-center justify-between gap-2 font-mono text-xs text-slate-400 tabular-nums">
              <span>
                Lines {startLine}–{Math.min(sourceLines.length, startLine + 139)} of{' '}
                {sourceLines.length.toLocaleString()}
              </span>
              <div className="flex flex-wrap gap-1.5">
                <button
                  type="button"
                  disabled={startLine <= 1}
                  onClick={() => setStartLine(1)}
                  className="rounded border border-slate-800 bg-slate-900 px-2 py-1 hover:bg-slate-800 disabled:opacity-40"
                >
                  Top
                </button>
                <button
                  type="button"
                  disabled={startLine <= 1}
                  onClick={() => setStartLine((s) => Math.max(1, s - 120))}
                  className="rounded border border-slate-800 bg-slate-900 px-2.5 py-1 hover:bg-slate-800 disabled:opacity-40"
                >
                  Prev 120
                </button>
                <button
                  type="button"
                  disabled={startLine + 140 > sourceLines.length}
                  onClick={() => setStartLine((s) => Math.min(Math.max(1, sourceLines.length - 100), s + 120))}
                  className="rounded border border-slate-800 bg-slate-900 px-2.5 py-1 hover:bg-slate-800 disabled:opacity-40"
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
