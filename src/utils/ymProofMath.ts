export const STANDARD_BETA0 = 1 / 300; // ContinuumClosure.lean §45 standardBeta0
export const DOBRUSHIN_CRITICAL_BETA = -Math.log(17 / 18) / 12; // 18 * (1 - exp(-12 * β)) = 1

export type DobrushinRegime = 'contractive' | 'boundary' | 'supercritical' | 'zero_coupling';

export interface DobrushinMetrics {
  beta: number;
  alpha: number;
  rho: number;
  cSingleLink: number;
  clusterRate: number | null;
  prefactor: number | null;
  regime: DobrushinRegime;
}

export function dobrushinAlpha(beta: number): number {
  const safeBeta = Math.max(0, beta);
  return 18 * (1 - Math.exp(-12 * safeBeta));
}

export function dobrushinMetrics(beta: number): DobrushinMetrics {
  const safeBeta = Math.max(0, beta);
  const cSingleLink = 1 - Math.exp(-12 * safeBeta);
  const alpha = 18 * cSingleLink;
  const rho = Math.sqrt(Math.max(0, alpha));

  if (safeBeta === 0) {
    return {
      beta: 0,
      alpha: 0,
      rho: 0,
      cSingleLink: 0,
      clusterRate: Number.POSITIVE_INFINITY,
      prefactor: 0,
      regime: 'zero_coupling',
    };
  }

  if (alpha < 1 - 1e-12) {
    const clusterRate = -0.5 * Math.log(alpha);
    const prefactor = (2 * cSingleLink) / (rho * (1 - rho));
    return {
      beta: safeBeta,
      alpha,
      rho,
      cSingleLink,
      clusterRate,
      prefactor,
      regime: 'contractive',
    };
  }

  if (Math.abs(alpha - 1) <= 1e-12) {
    return {
      beta: safeBeta,
      alpha: 1,
      rho: 1,
      cSingleLink,
      clusterRate: 0,
      prefactor: null,
      regime: 'boundary',
    };
  }

  return {
    beta: safeBeta,
    alpha,
    rho,
    cSingleLink,
    clusterRate: null,
    prefactor: null,
    regime: 'supercritical',
  };
}

export function dobrushinClusterBound(
  beta: number,
  distanceD: number,
  supportSizeSg = 4,
  mF = 1,
  mG = 1,
): number | null {
  const m = dobrushinMetrics(beta);
  if (m.regime === 'zero_coupling') {
    return 0;
  }
  if (m.prefactor === null || !Number.isFinite(m.prefactor)) {
    return null;
  }
  return m.prefactor * supportSizeSg * mF * mG * Math.pow(m.rho, distanceD);
}

export interface DecayPoint {
  d: number;
  bound: number;
  expDecay: number;
}

export function generateDobrushinDecayCurve(
  beta: number,
  maxD: number,
  supportSizeSg = 4,
): DecayPoint[] {
  const m = dobrushinMetrics(beta);
  const points: DecayPoint[] = [];
  const rate = m.clusterRate && Number.isFinite(m.clusterRate) ? m.clusterRate : 0;

  for (let d = 1; d <= maxD; d++) {
    const expDecay = m.regime === 'zero_coupling' ? 0 : Math.exp(-rate * d);
    const bound =
      m.prefactor !== null
        ? m.prefactor * supportSizeSg * Math.pow(m.rho, d)
        : Number.NaN;
    points.push({ d, bound, expDecay });
  }
  return points;
}

// Stage-limit scaling (BalabanFromStage.lean / SchwingerConv.lean)
export interface StageScalingParams {
  m: number;
  shiftedStage: number; // m + 1 in BalabanFromStage.lean
  periodicSide: number; // (m + 2)^2 sites per side
  latticeSpacing: number; // 1 / (m + 2)
  physicalSide: number; // periodicSide * latticeSpacing = m + 2
  beta: number; // m + 1
  bareCouplingSq: number; // 1 / beta
  totalSites4D: number; // periodicSide^4
}

export function stageScalingParams(m: number): StageScalingParams {
  const safeM = Math.max(0, Math.floor(m));
  const base = safeM + 2;
  const periodicSide = base * base;
  const latticeSpacing = 1 / base;
  const physicalSide = periodicSide * latticeSpacing;
  const beta = safeM + 1;
  return {
    m: safeM,
    shiftedStage: safeM + 1,
    periodicSide,
    latticeSpacing,
    physicalSide,
    beta,
    bareCouplingSq: 1 / beta,
    totalSites4D: Math.pow(periodicSide, 4),
  };
}

// SUClosure.lean weak-coupling trajectory (β_m = exp((m+1)^4), L_m = m+1)
export interface SUClosureStageParams {
  m: number;
  sideSites: number; // m + 1
  logBeta: number; // (m + 1)^4
  betaLabel: string;
}

export function suClosureStageParams(m: number): SUClosureStageParams {
  const safeM = Math.max(0, Math.floor(m));
  const x = safeM + 1;
  const logBeta = Math.pow(x, 4);
  return {
    m: safeM,
    sideSites: x,
    logBeta,
    betaLabel: `exp(${logBeta})`,
  };
}

// Equality-class IID Schwinger functional & cumulants (IIDSchwinger.lean / Core.lean)
export function iidMom(k: number): number {
  const safeK = Math.max(0, Math.floor(k));
  if (safeK === 0) return 1;
  return (1 + Math.pow(2, safeK)) / 2;
}

export function equalityClassSizes(labels: readonly string[]): number[] {
  const counts = new Map<string, number>();
  for (const l of labels) {
    counts.set(l, (counts.get(l) ?? 0) + 1);
  }
  return Array.from(counts.values());
}

export function evaluateIidSchwinger(labels: readonly string[]): number {
  if (labels.length === 0) return 1;
  return equalityClassSizes(labels).reduce((acc, size) => acc * iidMom(size), 1);
}

export function connected2Iid(x0: string, x1: string): number {
  return evaluateIidSchwinger([x0, x1]) - evaluateIidSchwinger([x0]) * evaluateIidSchwinger([x1]);
}

export function connected4Iid(xs: readonly [string, string, string, string]): number {
  const s1 = (i: number) => evaluateIidSchwinger([xs[i]]);
  const s2 = (i: number, j: number) => evaluateIidSchwinger([xs[i], xs[j]]);
  const s3 = (i: number, j: number, k: number) => evaluateIidSchwinger([xs[i], xs[j], xs[k]]);
  const s4 = evaluateIidSchwinger(xs);

  return (
    s4 -
    (s1(0) * s3(1, 2, 3) + s1(1) * s3(0, 2, 3) + s1(2) * s3(0, 1, 3) + s1(3) * s3(0, 1, 2)) -
    (s2(0, 1) * s2(2, 3) + s2(0, 2) * s2(1, 3) + s2(0, 3) * s2(1, 2)) +
    2 *
      (s1(0) * s1(1) * s2(2, 3) +
        s1(0) * s1(2) * s2(1, 3) +
        s1(0) * s1(3) * s2(1, 2) +
        s1(1) * s1(2) * s2(0, 3) +
        s1(1) * s1(3) * s2(0, 2) +
        s1(2) * s1(3) * s2(0, 1)) -
    6 * (s1(0) * s1(1) * s1(2) * s1(3))
  );
}

export type Site4D = [number, number, number, number];
export interface Link4D {
  site: Site4D;
  dir: 0 | 1 | 2 | 3;
}

export function mod(a: number, m: number): number {
  return ((a % m) + m) % m;
}

export function shiftSite4(site: Site4D, dir: 0 | 1 | 2 | 3, delta: 1 | -1, L: number): Site4D {
  const next: Site4D = [...site] as Site4D;
  next[dir] = mod(next[dir] + delta, L);
  return next;
}

export function linkKey(link: Link4D): string {
  return `(${link.site.join(',')};d=${link.dir})`;
}

export interface Plaquette4D {
  id: string;
  base: Site4D;
  plane: [0 | 1 | 2 | 3, 0 | 1 | 2 | 3];
  links: Link4D[];
}

export function enumerateTouchingPlaquettes4D(
  L: number,
  target: Link4D,
): {
  plaquettes: Plaquette4D[];
  uniqueNeighbors: Link4D[];
  expectedMaxPlaquettes: number;
  expectedMaxNeighbors: number;
} {
  const plaquettes: Plaquette4D[] = [];
  const neighborMap = new Map<string, Link4D>();
  const targetKey = linkKey(target);
  const d0 = target.dir;

  for (let dOtherNum = 0; dOtherNum < 4; dOtherNum++) {
    const dOther = dOtherNum as 0 | 1 | 2 | 3;
    if (dOther === d0) continue;

    const d1 = d0 < dOther ? d0 : dOther;
    const d2 = d0 < dOther ? dOther : d0;

    for (const polarity of ['fwd', 'bwd'] as const) {
      const base =
        polarity === 'fwd'
          ? target.site
          : shiftSite4(target.site, dOther, -1, L);

      const s1 = shiftSite4(base, d1, 1, L);
      const s2 = shiftSite4(base, d2, 1, L);

      const links: Link4D[] = [
        { site: base, dir: d1 },
        { site: s1, dir: d2 },
        { site: s2, dir: d1 },
        { site: base, dir: d2 },
      ];

      plaquettes.push({
        id: `P[${base.join(',')}](${d1},${d2})`,
        base,
        plane: [d1, d2],
        links,
      });

      for (const l of links) {
        const k = linkKey(l);
        if (k !== targetKey && !neighborMap.has(k)) {
          neighborMap.set(k, l);
        }
      }
    }
  }

  return {
    plaquettes,
    uniqueNeighbors: Array.from(neighborMap.values()),
    expectedMaxPlaquettes: 6,
    expectedMaxNeighbors: 18,
  };
}

export interface CanonicalWitnessResult {
  N: number;
  diagonalEntries: number[];
  oneTrace: number;
  flipTrace: number;
  oneNormalized: number;
  flipNormalized: number;
  difference: number;
  distinct: boolean;
  detProduct: number;
}

export function evaluateCanonicalWitness(N: number): CanonicalWitnessResult {
  const safeN = Math.max(2, Math.floor(N));
  const diagonalEntries: number[] = Array.from({ length: safeN }, (_, i) => (i < 2 ? -1 : 1));
  const flipTrace = diagonalEntries.reduce((acc, v) => acc + v, 0);
  const detProduct = diagonalEntries.reduce((acc, v) => acc * v, 1);
  const oneTrace = safeN;
  const oneNormalized = 1;
  const flipNormalized = flipTrace / safeN;

  return {
    N: safeN,
    diagonalEntries,
    oneTrace,
    flipTrace,
    oneNormalized,
    flipNormalized,
    difference: Math.abs(oneNormalized - flipNormalized),
    distinct: oneNormalized !== flipNormalized,
    detProduct,
  };
}

export function radialCoupling4D(x: Site4D): number {
  const norm = Math.sqrt(x[0] * x[0] + x[1] * x[1] + x[2] * x[2] + x[3] * x[3]);
  return Math.exp(-2 * norm);
}

export function evaluateIsingSchwinger(points: Site4D[]): number {
  let prodPlus = 1;
  let prodMinus = 1;
  for (const pt of points) {
    const g = radialCoupling4D(pt);
    prodPlus *= 1 + g;
    prodMinus *= 1 - g;
  }
  return 0.5 * (prodPlus + prodMinus);
}

export function checkIsingShiftObstruction(shift: Site4D): {
  unshiftedS2: number;
  shiftedS2: number;
  delta: number;
  translationInvariant: boolean;
} {
  const zero: Site4D = [0, 0, 0, 0];
  const unshiftedS2 = evaluateIsingSchwinger([zero, zero]);
  const shiftedS2 = evaluateIsingSchwinger([shift, shift]);
  const delta = Math.abs(unshiftedS2 - shiftedS2);
  return {
    unshiftedS2,
    shiftedS2,
    delta,
    translationInvariant: delta < 1e-12,
  };
}

export type S16State = [boolean, boolean, boolean, boolean];

export const ALL_S16_STATES: S16State[] = Array.from({ length: 16 }, (_, idx) => [
  Boolean((idx >> 3) & 1),
  Boolean((idx >> 2) & 1),
  Boolean((idx >> 1) & 1),
  Boolean(idx & 1),
]);

export function s16ToString(s: S16State): string {
  return `(${s[0] ? '1' : '0'},${s[1] ? '1' : '0'},${s[2] ? '1' : '0'},${s[3] ? '1' : '0'})`;
}

export function s16Label(s: S16State): string {
  const tags: string[] = [];
  if (s[0]) tags.push('N');
  if (s[1]) tags.push('F');
  if (s[2]) tags.push('T');
  if (s[3]) tags.push('B');
  return tags.length === 0 ? '∅' : `{${tags.join(',')}}`;
}

export function walk16(x: S16State): S16State {
  const [b0, b1, b2, b3] = x;
  if (!b0) return [true, b1, b2, b3];
  if (!b1) return [true, true, b2, b3];
  if (!b2) return [true, true, true, b3];
  if (!b3) return [true, true, true, true];
  return [true, true, true, true];
}

export function inc16(x: S16State): S16State {
  const [b0, b1, b2, b3] = x;
  return [b0 && b3, b2, b1, b3];
}

export function inc16Strict(x: S16State): S16State {
  const [b0, b1, b2] = x;
  return [b0 || b2, b1, b2, true];
}

export function s16Equal(a: S16State, b: S16State): boolean {
  return a[0] === b[0] && a[1] === b[1] && a[2] === b[2] && a[3] === b[3];
}

export interface S16Audit {
  state: S16State;
  incLegacy: S16State;
  incStrict: S16State;
  walkNext: S16State;
  legacyIdempotent: boolean;
  strictIdempotent: boolean;
  strictNonVoid: boolean;
  incWalkCommuteLegacy: boolean;
  incWalkCommuteStrict: boolean;
}

export function auditS16State(s: S16State): S16Audit {
  const voidState: S16State = [false, false, false, false];
  const incL = inc16(s);
  const incS = inc16Strict(s);
  return {
    state: s,
    incLegacy: incL,
    incStrict: incS,
    walkNext: walk16(s),
    legacyIdempotent: s16Equal(inc16(incL), incL),
    strictIdempotent: s16Equal(inc16Strict(incS), incS),
    strictNonVoid: !s16Equal(incS, voidState),
    incWalkCommuteLegacy: s16Equal(inc16(walk16(s)), walk16(incL)),
    incWalkCommuteStrict: s16Equal(inc16Strict(walk16(s)), walk16(incS)),
  };
}

// ============================================================================
// Stage Torus Wraparound, Injective Threshold & Plaquette-CDF Engine (§47-§48)
// ============================================================================

export type ContinuumPoint4D = [number, number, number, number];

export interface WrappedStageSite {
  index: number;
  label: string;
  continuum: ContinuumPoint4D;
  latticeCoords: Site4D;
  siteKey: string;
}

export interface StageTupleAnalysis {
  m: number;
  L: number;
  a: number;
  wrappedSites: WrappedStageSite[];
  collisionCount: number;
  injectiveOnDistinct: boolean;
  firstInjectiveStage: number;
  wrappedSchwinger: number;
  continuumSchwinger: number;
  finiteVolumeError: number;
}

export function wrapContinuumPointAtStage(pt: ContinuumPoint4D, m: number): Site4D {
  const { periodicSide: L, latticeSpacing: a } = stageScalingParams(m);
  return [
    mod(Math.floor(pt[0] / a), L),
    mod(Math.floor(pt[1] / a), L),
    mod(Math.floor(pt[2] / a), L),
    mod(Math.floor(pt[3] / a), L),
  ];
}

function point4DKey(pt: ContinuumPoint4D): string {
  return `${pt[0].toFixed(6)},${pt[1].toFixed(6)},${pt[2].toFixed(6)},${pt[3].toFixed(6)}`;
}

export function analyzeStageTupleInjectivity(
  points: readonly ContinuumPoint4D[],
  m: number,
  maxSearchStage = 64,
): StageTupleAnalysis {
  const { periodicSide: L, latticeSpacing: a } = stageScalingParams(m);
  const wrappedSites: WrappedStageSite[] = points.map((pt, index) => {
    const latticeCoords = wrapContinuumPointAtStage(pt, m);
    return {
      index,
      label: `x_${index}`,
      continuum: pt,
      latticeCoords,
      siteKey: `(${latticeCoords.join(',')})`,
    };
  });

  const contKeys = points.map(point4DKey);
  const latticeKeys = wrappedSites.map((s) => s.siteKey);

  let collisionCount = 0;
  for (let i = 0; i < points.length; i++) {
    for (let j = i + 1; j < points.length; j++) {
      if (contKeys[i] !== contKeys[j] && latticeKeys[i] === latticeKeys[j]) {
        collisionCount++;
      }
    }
  }

  let firstInjectiveStage = maxSearchStage;
  for (let cand = 0; cand <= maxSearchStage; cand++) {
    const candKeys = points.map((p) => `(${wrapContinuumPointAtStage(p, cand).join(',')})`);
    let collides = false;
    for (let i = 0; i < points.length; i++) {
      for (let j = i + 1; j < points.length; j++) {
        if (contKeys[i] !== contKeys[j] && candKeys[i] === candKeys[j]) {
          collides = true;
          break;
        }
      }
      if (collides) break;
    }
    if (!collides) {
      firstInjectiveStage = cand;
      break;
    }
  }

  const wrappedSchwinger = evaluateIidSchwinger(latticeKeys);
  const continuumSchwinger = evaluateIidSchwinger(contKeys);
  return {
    m,
    L,
    a,
    wrappedSites,
    collisionCount,
    injectiveOnDistinct: collisionCount === 0,
    firstInjectiveStage,
    wrappedSchwinger,
    continuumSchwinger,
    finiteVolumeError: Math.abs(wrappedSchwinger - continuumSchwinger),
  };
}

export function plaquetteCDFQuantile(traceNorm: number, beta: number): {
  traceNorm: number;
  cdfValue: number;
  rademacherVal: 1 | 2;
  boltzmannDensity: number;
} {
  const clamped = Math.max(-1, Math.min(1, traceNorm));
  // Smooth monotone bijection F_β : [-1, 1] -> [0, 1] induced by Wilson weight exp(β w)
  const k = Math.max(0.05, Math.min(6, beta * 0.35 + 0.15));
  const num = Math.exp(k * clamped) - Math.exp(-k);
  const den = Math.exp(k) - Math.exp(-k);
  const cdfValue = Math.max(0, Math.min(1, num / den));
  const rademacherVal: 1 | 2 = cdfValue <= 0.5 ? 1 : 2;
  const boltzmannDensity = Math.exp(beta * clamped);
  return {
    traceNorm: clamped,
    cdfValue,
    rademacherVal,
    boltzmannDensity,
  };
}

// ============================================================================
// SUClosure Exponential Weak-Coupling Error Envelope (§51)
// ============================================================================

export interface SUClosureErrorMetrics {
  N: number;
  m: number;
  x: number;
  L: number;
  logBeta: number;
  cErr: number;
  m0Threshold: number;
  errorEnvelope: number;
  contractiveRegion: boolean;
  gapUpperBound: number | null;
  rescaledBound: number | null;
}

export function suClosureGapErrorMetrics(N: number, m: number): SUClosureErrorMetrics {
  const safeN = Math.max(2, Math.floor(N));
  const safeM = Math.max(0, Math.floor(m));
  const x = safeM + 1;
  const L = x;
  const logBeta = Math.pow(x, 4);
  const cErr = 216 * (18 * safeN * safeN + 2) + 8;
  const m0Threshold = Math.ceil(Math.max(15, Math.log(4 * safeN + 2), 2 * cErr + 1));
  const errorEnvelope = cErr / x;
  const contractiveRegion = x >= m0Threshold && errorEnvelope < 1;
  const gapUpperBound = errorEnvelope < 1 ? -Math.log(1 - errorEnvelope) : null;
  const rescaledBound = contractiveRegion ? (2 * cErr) / x : null;

  return {
    N: safeN,
    m: safeM,
    x,
    L,
    logBeta,
    cErr,
    m0Threshold,
    errorEnvelope,
    contractiveRegion,
    gapUpperBound,
    rescaledBound,
  };
}

// ============================================================================
// Rank-1 OS Hilbert Completion & Poincaré Projection Kernel (§49)
// ============================================================================

export interface OSConfigPreset {
  id: string;
  label: string;
  points: string[];
}

export interface OSGramAnalysis {
  configs: OSConfigPreset[];
  schwingerValues: number[];
  gramMatrix: number[][];
  maxMinorDet: number;
  rank: 1;
  growthBounds: number[];
  growthRatio: number[];
}

export function computeOSGramMatrix(configs: readonly OSConfigPreset[]): OSGramAnalysis {
  const schwingerValues = configs.map((c) => evaluateIidSchwinger(c.points));
  const n = configs.length;
  const gramMatrix: number[][] = Array.from({ length: n }, (_, i) =>
    Array.from({ length: n }, (_, j) => schwingerValues[i] * schwingerValues[j]),
  );

  let maxMinorDet = 0;
  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      for (let k = 0; k < n; k++) {
        for (let l = k + 1; l < n; l++) {
          const det = Math.abs(gramMatrix[i][k] * gramMatrix[j][l] - gramMatrix[i][l] * gramMatrix[j][k]);
          if (det > maxMinorDet) maxMinorDet = det;
        }
      }
    }
  }

  // Growth bound: |S_n| <= M_bd^n with M_bd = 2 (IIDPoincareContinuation.lean line 136)
  const growthBounds = configs.map((c) => Math.pow(2, c.points.length));
  const growthRatio = schwingerValues.map((s, idx) => Math.abs(s) / growthBounds[idx]);

  return {
    configs: [...configs],
    schwingerValues,
    gramMatrix,
    maxMinorDet,
    rank: 1,
    growthBounds,
    growthRatio,
  };
}

