import corpusIndexRaw from './corpusIndex.json';

export type CorpusCategory =
  | 'Unconditional Closure'
  | 'Analytic Rungs (R1–R4)'
  | 'OS & Wightman Reconstruction'
  | 'Dobrushin & Strong Coupling'
  | 'Lattice & Gauge Core'
  | 'Finite Witnesses';

export interface CorpusDeclaration {
  kind: 'theorem' | 'lemma' | 'def' | 'structure' | 'abbrev' | 'instance' | 'inductive';
  name: string;
  line: number;
}

export interface CorpusModuleIndex {
  id: string;
  fileName: string;
  assetPath: string;
  lineCount: number;
  category: CorpusCategory;
  summary: string;
  imports: string[];
  importedBy: string[];
  declarations: CorpusDeclaration[];
}

export interface LinkedTheoremAudit {
  section: string;
  name: string;
  axioms: string[];
  status: string;
  module: string | null;
  line: number | null;
}

interface CorpusIndexPayload {
  modules: CorpusModuleIndex[];
  theorems: LinkedTheoremAudit[];
}

const corpusIndex = corpusIndexRaw as CorpusIndexPayload;

export const ALL_106_MODULES: CorpusModuleIndex[] = corpusIndex.modules;

export const LINKED_THEOREMS: LinkedTheoremAudit[] = corpusIndex.theorems;

// Backward-compatible alias consumed across components
export type AuditedTheoremEntry = LinkedTheoremAudit;
export const AUDITED_THEOREMS: LinkedTheoremAudit[] = LINKED_THEOREMS;

export const TOTAL_CORPUS_LINES: number = ALL_106_MODULES.reduce(
  (acc, mod) => acc + mod.lineCount,
  0,
);

export const CORPUS_CATEGORIES: CorpusCategory[] = [
  'Unconditional Closure',
  'Analytic Rungs (R1–R4)',
  'OS & Wightman Reconstruction',
  'Dobrushin & Strong Coupling',
  'Lattice & Gauge Core',
  'Finite Witnesses',
];

export const MODULE_BY_ID: Record<string, CorpusModuleIndex> = Object.fromEntries(
  ALL_106_MODULES.map((m) => [m.id, m]),
);
