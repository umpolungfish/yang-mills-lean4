import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import {
  ALL_S16_STATES,
  DOBRUSHIN_CRITICAL_BETA,
  STANDARD_BETA0,
  auditS16State,
  checkIsingShiftObstruction,
  dobrushinAlpha,
  dobrushinClusterBound,
  dobrushinMetrics,
  enumerateTouchingPlaquettes4D,
  evaluateCanonicalWitness,
  evaluateIsingSchwinger,
  generateDobrushinDecayCurve,
  le16F,
  le16I,
  le16T,
} from './yangMillsMath.ts';

describe('Dobrushin strong-coupling contraction (§43–§45)', () => {
  it('standardBeta0 = 1/300 strictly satisfies the Dobrushin condition 0 < alpha < 1', () => {
    const m = dobrushinMetrics(STANDARD_BETA0);
    assert.equal(m.regime, 'contractive');
    assert.ok(m.alpha > 0 && m.alpha < 1, `Expected 0 < alpha < 1, got ${m.alpha}`);
    assert.ok(Math.abs(m.alpha - 18 * (1 - Math.exp(-12 / 300))) < 1e-12);
    assert.ok(m.clusterRate !== null && m.clusterRate > 0);
    assert.ok(m.prefactor !== null && m.prefactor > 0);
  });

  it('transitions from contractive below critical beta to supercritical above critical beta', () => {
    const below = dobrushinMetrics(DOBRUSHIN_CRITICAL_BETA * 0.9);
    const atCrit = dobrushinAlpha(DOBRUSHIN_CRITICAL_BETA);
    const above = dobrushinMetrics(DOBRUSHIN_CRITICAL_BETA * 1.15);

    assert.equal(below.regime, 'contractive');
    assert.ok(Math.abs(atCrit - 1) < 1e-12);
    assert.equal(above.regime, 'supercritical');
    assert.equal(above.clusterRate, null);
  });

  it('produces strictly decreasing positive cluster bounds with distance D', () => {
    const curve = generateDobrushinDecayCurve(STANDARD_BETA0, 8, 4);
    assert.equal(curve.length, 8);
    for (let i = 1; i < curve.length; i++) {
      assert.ok(curve[i].bound < curve[i - 1].bound);
      assert.ok(curve[i].expDecay < curve[i - 1].expDecay);
    }
    const b4 = dobrushinClusterBound(STANDARD_BETA0, 4, 4, 1, 1);
    assert.ok(b4 !== null && Math.abs(b4 - curve[3].bound) < 1e-12);
  });

  it('enumerates exact 4D torus bounds: plaqsTouching <= 6 and sharesPlaq4 <= 18', () => {
    for (const L of [2, 3, 4]) {
      for (const dir of [0, 1, 2, 3] as const) {
        const res = enumerateTouchingPlaquettes4D(L, { site: [0, 1 % L, 0, 0], dir });
        assert.equal(res.plaquettes.length, 6);
        assert.ok(
          res.uniqueNeighbors.length <= 18,
          `Expected <= 18 unique neighbors for L=${L}, got ${res.uniqueNeighbors.length}`,
        );
        if (L >= 3) {
          assert.equal(res.uniqueNeighbors.length, 18);
        }
      }
    }
  });
});

describe('Canonical Witness suFlip2 (§46W)', () => {
  it('computes 1 vs (N - 4) / N for N >= 2 and preserves SU(N) unit determinant', () => {
    for (const N of [2, 3, 4, 5, 8]) {
      const w = evaluateCanonicalWitness(N);
      assert.equal(w.oneNormalized, 1);
      assert.equal(w.flipTrace, N - 4);
      assert.ok(Math.abs(w.flipNormalized - (N - 4) / N) < 1e-12);
      assert.equal(w.distinct, true);
      assert.equal(w.detProduct, 1);
    }
  });
});

describe('Ising Schwinger obstruction (§34 & §37)', () => {
  it('matches exact Lean proof: S2(0,0) = 2 while S2(a,a) = 1 + exp(-4)', () => {
    const sZero = evaluateIsingSchwinger([
      [0, 0, 0, 0],
      [0, 0, 0, 0],
    ]);
    assert.ok(Math.abs(sZero - 2) < 1e-12);

    const obs = checkIsingShiftObstruction([1, 0, 0, 0]);
    assert.ok(Math.abs(obs.unshiftedS2 - 2) < 1e-12);
    assert.ok(Math.abs(obs.shiftedS2 - (1 + Math.exp(-4))) < 1e-12);
    assert.equal(obs.translationInvariant, false);
  });
});

describe('S16 Trilattice axioms (§8 & §37)', () => {
  it('verifies trilattice16Strict is globally idempotent and non-void across all 16 states', () => {
    assert.equal(ALL_S16_STATES.length, 16);
    for (const st of ALL_S16_STATES) {
      const audit = auditS16State(st);
      assert.equal(audit.strictIdempotent, true);
      assert.equal(audit.strictNonVoid, true);
    }

    // Legacy inc16 is non-commutative with walk16 on (true, true, false, false)
    const witnessLegacy = auditS16State([true, true, false, false]);
    assert.equal(witnessLegacy.incWalkCommuteLegacy, false);

    // Strict inc16Strict is non-commutative with walk16 on (false, false, true, false)
    const witnessStrict = auditS16State([false, false, true, false]);
    assert.equal(witnessStrict.incWalkCommuteStrict, false);

    // Order independence matches Core.lean trilattice16_properties
    assert.equal(le16I([false, false, false, false], [false, true, false, false]), true);
    assert.equal(le16T([false, false, false, false], [false, true, false, false]), false);
    assert.equal(le16T([false, true, false, false], [false, false, true, false]), true);
    assert.equal(le16F([false, true, false, false], [false, false, true, false]), false);
  });
});
