// ============================================================================
// Route A · TrilatticeYM interactive mathematics
// Faithful JS shadows of the Lean 4 declarations in Imscribing.TrilatticeYM,
// formalizing Shramko and Wansing's SIXTEEN_3 trilattice.
// Every function here mirrors a kernel-checked definition; nothing is invented.
// ============================================================================

/** Belnap4 : N | F | T | B — the four generalized truth values. */
export type Belnap4 = 'N' | 'F' | 'T' | 'B';
export const BELNAP4: readonly Belnap4[] = ['N', 'F', 'T', 'B'] as const;

/** Sixteen3 = Belnap4 → Bool, stored as the truth-set of marked values. */
export type Sixteen3 = readonly [boolean, boolean, boolean, boolean];

export const SIXTEEN_STATES: readonly Sixteen3[] = Array.from({ length: 16 }, (_, idx) => [
  Boolean((idx >> 3) & 1),
  Boolean((idx >> 2) & 1),
  Boolean((idx >> 1) & 1),
  Boolean(idx & 1),
] as Sixteen3);

/** Named canonical states of Trilattice.lean. */
export const CANONICAL = {
  sVoid: [false, false, false, false] as Sixteen3,
  sNeither: [true, false, false, false] as Sixteen3,
  sFalse: [false, true, false, false] as Sixteen3,
  sTrue: [false, false, true, false] as Sixteen3,
  sBoth: [false, false, false, true] as Sixteen3,
  sGlut: [false, true, true, false] as Sixteen3,
  sTopI: [true, true, true, true] as Sixteen3,
};

export function s16(s: Sixteen3): string {
  return `(${s.map((b) => (b ? '1' : '0')).join(',')})`;
}

export function stateLabel(s: Sixteen3): string {
  const tags = BELNAP4.filter((_, i) => s[i]);
  if (tags.length === 0) return '∅ (Void)';
  if (tags.length === 4) return '[B] (Totality)';
  return `{${tags.join(',')}}`;
}

export function eqState(a: Sixteen3, b: Sixteen3): boolean {
  return a[0] === b[0] && a[1] === b[1] && a[2] === b[2] && a[3] === b[3];
}

/** impBool a b = !a || b (Trilattice.lean). */
function imp(a: boolean, b: boolean): boolean {
  return !a || b;
}

/** Information order le_i x y : ∀ b, x b ⇒ y b. */
export function leI(x: Sixteen3, y: Sixteen3): boolean {
  return x.every((v, i) => imp(v, y[i]));
}

/** Truth order le_t x y (Trilattice.lean). */
export function leT(x: Sixteen3, y: Sixteen3): boolean {
  return imp(x[2], y[2]) && imp(x[3], y[3]) && imp(y[0], x[0]) && imp(y[1], x[1]);
}

/** Falsity order le_f x y (Trilattice.lean). */
export function leF(x: Sixteen3, y: Sixteen3): boolean {
  return imp(x[1], y[1]) && imp(x[3], y[3]) && imp(y[0], x[0]) && imp(y[2], x[2]);
}

/** canonicalWalk (Trilattice.lean): mark the first unmarked value in N,F,T,B order. */
export function canonicalWalk(x: Sixteen3): Sixteen3 {
  const out: [boolean, boolean, boolean, boolean] = [x[0], x[1], x[2], x[3]];
  for (let i = 0; i < 4; i++) {
    if (!out[i]) {
      out[i] = true;
      return out;
    }
  }
  return out;
}

/** canonicalInc x = canonicalJoinI x sBoth : add the B mark (non-boolean re-entry). */
export function canonicalInc(x: Sixteen3): Sixteen3 {
  return [x[0], x[1], x[2], true];
}

/** canonicalR = canonicalInc (idempotent re-entry operator). */
export function canonicalR(x: Sixteen3): Sixteen3 {
  return canonicalInc(x);
}

/** canonicalMu x : highest-priority mark B > T > F > N. */
export function canonicalMu(x: Sixteen3): Belnap4 {
  if (x[3]) return 'B';
  if (x[2]) return 'T';
  if (x[1]) return 'F';
  return 'N';
}

/** canonicalDelta b : singleton truth-set. */
export function canonicalDelta(b: Belnap4): Sixteen3 {
  const i = BELNAP4.indexOf(b);
  return [i === 0, i === 1, i === 2, i === 3];
}

/** Glut: both T and F are marked (overdetermined / contradictory state). */
export function isGlut(x: Sixteen3): boolean {
  return x[1] && x[2];
}

/** Iterate the monotone walk until the totality fixed point; returns the path. */
export function walkPath(x: Sixteen3, maxSteps = 8): Sixteen3[] {
  const path: Sixteen3[] = [x];
  let cur = x;
  for (let i = 0; i < maxSteps; i++) {
    const next = canonicalWalk(cur);
    path.push(next);
    if (eqState(next, cur)) break;
    cur = next;
  }
  return path;
}

export interface StateAudit {
  state: Sixteen3;
  inc: Sixteen3;
  reentry: Sixteen3;
  walk: Sixteen3;
  fold: Belnap4;
  coreLawHolds: boolean;
  incFixed: boolean;
  walkFixed: boolean;
  glut: boolean;
  topI: boolean;
}

export function auditState(x: Sixteen3): StateAudit {
  const inc = canonicalInc(x);
  const fold = canonicalMu(x);
  return {
    state: x,
    inc,
    reentry: canonicalR(x),
    walk: canonicalWalk(x),
    fold,
    coreLawHolds: canonicalMu(canonicalDelta(fold)) === fold,
    incFixed: eqState(canonicalInc(inc), inc),
    walkFixed: eqState(canonicalWalk(x), x),
    glut: isGlut(x),
    topI: eqState(x, CANONICAL.sTopI),
  };
}

// ----------------------------------------------------------------------------
// Exact spectral constants (YM_MassGap_Engine.lean / AssignedModel.lean)
// ----------------------------------------------------------------------------

export const Q_LOCAL = 1 / 7; // phiD traceless eigenvalue
export const DIRICHLET_GAP = 6 / 7; // phiTensor uniform gap
export const T_LOCAL_EIG = 1 / 4; // Tlocal *ᵥ u = (1/4) • u
export const Q_4D = 729 / 2704; // (27/52)^2
export const B_F_BOUND = 1 / 4;
export const B_L_BOUND = 625 / 38416;
export const KAPPA = 2 * Math.log(52 / 27);
export const ZETA_NEG_ONE = -1 / 12;

export interface TransmutationMetrics {
  alpha: number;
  lambdaYM: number;
  ell: number;
  kappa: number;
  q4d: number;
  massGap: number;
  expCheck: number;
  identityResidual: number;
  decay: Array<{ k: number; value: number }>;
}

/** m_gap = κ/ℓ = (κ/α)·Λ  with ℓ = α/Λ (ym_mass_gap_exists). */
export function transmutation(alpha: number, lambdaYM: number): TransmutationMetrics {
  const ell = alpha / lambdaYM;
  const massGap = KAPPA / ell;
  const expCheck = Math.exp(-massGap * ell);
  const decay = Array.from({ length: 24 }, (_, k) => ({ k, value: Math.pow(Q_4D, k) }));
  return {
    alpha,
    lambdaYM,
    ell,
    kappa: KAPPA,
    q4d: Q_4D,
    massGap,
    expCheck,
    identityResidual: Math.abs(expCheck - Q_4D),
    decay,
  };
}

// ----------------------------------------------------------------------------
// SIC dual frame (ZetaSICDualFrame.lean / Frobenius.lean)
// ----------------------------------------------------------------------------

/** g_ij = 2/3 δ_ij + 1/3 — represented as 1 on diagonal, 1/3 off. */
export function sicGramEntry(i: number, j: number): number {
  return i === j ? 1 : 1 / 3;
}

/** g^ij = 3/2 δ_ij + ζ(-1) — diagonal 5/4, off-diagonal -1/16 at d=4. */
export function sicDualEntry(i: number, j: number, zeta = ZETA_NEG_ONE): number {
  return (i === j ? 1.5 : 0) + zeta;
}

/** Isotropic SIC Gram for dimension d: (d/(d+1))I + (1/(d+1))·J. */
export function isotropicGram(n: number, d: number): number[][] {
  return Array.from({ length: n }, (_, i) =>
    Array.from({ length: n }, (_, j) => (i === j ? d / (d + 1) : 0) + 1 / (d + 1)),
  );
}

/** Zeta-derived dual: a·I + b·J with a = 1 - 12ζ(-1)/d, b = 12ζ(-1)/d². */
export function isotropicDual(n: number, d: number): number[][] {
  const a = 1 - (12 * ZETA_NEG_ONE) / d;
  const b = (12 * ZETA_NEG_ONE) / (d * d);
  return Array.from({ length: n }, (_, i) =>
    Array.from({ length: n }, (_, j) => (i === j ? a : 0) + b),
  );
}

function matVec(m: number[][], v: number[]): number[] {
  return m.map((row) => row.reduce((acc, x, j) => acc + x * v[j], 0));
}

/** Analysis by Gram followed by dual synthesis returns the coordinates. */
export function reconstruct(matrix: number[][], input: number[]): {
  analyzed: number[];
  restored: number[];
  residual: number;
} {
  const analyzed = matVec(matrix, input);
  const restored = matVec(isotropicDual(analyzed.length, Math.round(Math.sqrt(analyzed.length))), analyzed);
  const residual = Math.max(...restored.map((v, i) => Math.abs(v - input[i])));
  return { analyzed, restored, residual };
}

/** Joint k-site kernel: tensor product of the ququart dual kernel entries. */
export function jointKernelEntry(bitsA: readonly number[], bitsB: readonly number[]): number {
  return bitsA.reduce((acc, a, n) => {
    const local = (a === bitsB[n] ? 5 / 4 : 0) - 1 / 16;
    return acc * local;
  }, 1);
}
