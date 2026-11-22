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

    // Positive & negative orthogonal shifts yield up to 6 incident plaquettes (for L >= 2)
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

// S16 SIXTEEN_3 Trilattice from Core.txt (§8) & OSCompletion.txt (§37)
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

export function le16I(x: S16State, y: S16State): boolean {
  return (
    (!x[0] || y[0]) &&
    (!x[1] || y[1]) &&
    (!x[2] || y[2]) &&
    (!x[3] || y[3])
  );
}

export function le16T(x: S16State, y: S16State): boolean {
  return (
    (!y[0] || x[0]) &&
    (!y[1] || x[1]) &&
    (!x[2] || y[2]) &&
    (!x[3] || y[3])
  );
}

export function le16F(x: S16State, y: S16State): boolean {
  return (
    (!y[0] || x[0]) &&
    (!x[1] || y[1]) &&
    (!y[2] || x[2]) &&
    (!y[3] || x[3])
  );
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
