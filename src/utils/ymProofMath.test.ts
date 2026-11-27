import assert from 'node:assert/strict';
import test from 'node:test';
import {
  ALL_S16_STATES,
  STANDARD_BETA0,
  analyzeStageTupleInjectivity,
  auditS16State,
  checkIsingShiftObstruction,
  computeOSGramMatrix,
  connected2Iid,
  connected4Iid,
  dobrushinMetrics,
  enumerateTouchingPlaquettes4D,
  evaluateCanonicalWitness,
  evaluateIidSchwinger,
  iidMom,
  plaquetteCDFQuantile,
  stageScalingParams,
  suClosureGapErrorMetrics,
  suClosureStageParams,
} from './ymProofMath';

test('stageScalingParams matches BalabanFromStage & SchwingerConv formulas', () => {
  const m0 = stageScalingParams(0);
  assert.equal(m0.periodicSide, 4);
  assert.equal(m0.latticeSpacing, 0.5);
  assert.equal(m0.physicalSide, 2);
  assert.equal(m0.beta, 1);

  const m8 = stageScalingParams(8);
  assert.equal(m8.periodicSide, 100);
  assert.equal(m8.latticeSpacing, 0.1);
  assert.equal(m8.physicalSide, 10);
  assert.equal(m8.beta, 9);
  assert.ok(Math.abs(m8.bareCouplingSq - 1 / 9) < 1e-12);
});

test('suClosureStageParams matches SUClosure exponential trajectory', () => {
  const s = suClosureStageParams(2);
  assert.equal(s.sideSites, 3);
  assert.equal(s.logBeta, 81);
});

test('iidMom and connected4Iid prove exact non-Gaussianity -1/8 and clustering', () => {
  assert.equal(iidMom(0), 1);
  assert.equal(iidMom(1), 1.5);
  assert.equal(iidMom(2), 2.5);
  assert.equal(iidMom(3), 4.5);
  assert.equal(iidMom(4), 8.5);

  assert.equal(connected2Iid('x', 'x'), 0.25);
  assert.equal(connected2Iid('x', 'y'), 0);

  assert.equal(evaluateIidSchwinger(['x', 'y']), 2.25);
  assert.equal(connected4Iid(['x', 'x', 'x', 'x']), -0.125);
  assert.equal(connected4Iid(['x', 'x', 'y', 'y']), 0);
  assert.equal(connected4Iid(['x', 'y', 'z', 'w']), 0);
});

test('Dobrushin β₀ = 1/300 lies strictly in contractive regime with positive mass gap', () => {
  const m = dobrushinMetrics(STANDARD_BETA0);
  assert.equal(m.regime, 'contractive');
  assert.ok(m.alpha < 1);
  assert.ok(m.clusterRate !== null && m.clusterRate > 0);
});

test('4D plaquette star has 6 plaquettes and 18 unique neighbor links for L >= 3', () => {
  const res = enumerateTouchingPlaquettes4D(4, { site: [0, 0, 0, 0], dir: 0 });
  assert.equal(res.plaquettes.length, 6);
  assert.equal(res.uniqueNeighbors.length, 18);
});

test('Canonical witness suFlip2 satisfies det=1 and distinguishes 1 from (N-4)/N', () => {
  for (let N = 2; N <= 8; N++) {
    const w = evaluateCanonicalWitness(N);
    assert.equal(w.detProduct, 1);
    assert.equal(w.oneNormalized, 1);
    assert.ok(Math.abs(w.flipNormalized - (N - 4) / N) < 1e-12);
    assert.equal(w.distinct, true);
  }
});

test('Ising radial Schwinger fails time translation invariance', () => {
  const zeroShift = checkIsingShiftObstruction([0, 0, 0, 0]);
  assert.equal(zeroShift.translationInvariant, true);
  const unitShift = checkIsingShiftObstruction([1, 0, 0, 0]);
  assert.equal(unitShift.translationInvariant, false);
  assert.ok(unitShift.delta > 0.5);
});

test('S16 inc16Strict fixes idempotency & void collapse over all 16 states', () => {
  for (const s of ALL_S16_STATES) {
    const audit = auditS16State(s);
    assert.equal(audit.strictIdempotent, true);
    assert.equal(audit.strictNonVoid, true);
  }
});

test('analyzeStageTupleInjectivity separates nearby points above finite threshold m*', () => {
  const pts: [number, number, number, number][] = [
    [0.1, 0.2, 0, 0],
    [0.25, 0.2, 0, 0],
  ];
  const lowStage = analyzeStageTupleInjectivity(pts, 0); // a=0.5 => both floor(0.1/0.5)=0, floor(0.25/0.5)=0
  assert.equal(lowStage.collisionCount, 1);
  assert.equal(lowStage.injectiveOnDistinct, false);

  const highStage = analyzeStageTupleInjectivity(pts, lowStage.firstInjectiveStage);
  assert.equal(highStage.collisionCount, 0);
  assert.equal(highStage.injectiveOnDistinct, true);
  assert.equal(highStage.finiteVolumeError, 0);
});

test('plaquetteCDFQuantile maps traces monotonically to [0,1] and {1,2}', () => {
  const lo = plaquetteCDFQuantile(-1, 4);
  const hi = plaquetteCDFQuantile(1, 4);
  assert.equal(lo.cdfValue, 0);
  assert.equal(lo.rademacherVal, 1);
  assert.equal(hi.cdfValue, 1);
  assert.equal(hi.rademacherVal, 2);
});

test('suClosureGapErrorMetrics reaches contractive error <= 1/2 past M0 threshold', () => {
  const pre = suClosureGapErrorMetrics(3, 5);
  assert.equal(pre.contractiveRegion, false);
  const post = suClosureGapErrorMetrics(3, pre.m0Threshold);
  assert.equal(post.contractiveRegion, true);
  assert.ok(post.errorEnvelope <= 0.5);
  assert.ok(post.gapUpperBound !== null && post.gapUpperBound > 0);
});

test('computeOSGramMatrix proves rank-1 (all 2x2 minors = 0) and M_bd = 2 growth bound', () => {
  const analysis = computeOSGramMatrix([
    { id: 'vac', label: '∅ (Vacuum)', points: [] },
    { id: 's1', label: '(x₀)', points: ['x₀'] },
    { id: 's2', label: '(x₀, x₀)', points: ['x₀', 'x₀'] },
    { id: 's3', label: '(x₀, x₁, x₂)', points: ['x₀', 'x₁', 'x₂'] },
  ]);
  assert.equal(analysis.rank, 1);
  assert.ok(analysis.maxMinorDet < 1e-12);
  for (const ratio of analysis.growthRatio) {
    assert.ok(ratio <= 1 + 1e-12);
  }
});
