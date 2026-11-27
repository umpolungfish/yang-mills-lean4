import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { CONTENTIONS_CATALOG, REPLAY_AXIOM_SAMPLES } from '../data/contentionsData';
import { MODULE_BY_ID } from '../data/theoremsCatalog';
import { ELEGANT_PROOFS } from '../data/elegantProofsData';
import {
  filterContentions,
  filterElegantProofs,
  filterReplaySamples,
  getContentionStats,
  getScopeComparisonMatrix,
  isStandardAxiomSetOnly,
  validateContentionTraceModules,
  validateElegantProofGems,
  verifyObservableVarianceWitness,
} from './contentionTrace';

test('Every trace step and exhibit in CONTENTIONS_CATALOG resolves to an existing Lean module and valid line range', () => {
  const result = validateContentionTraceModules(CONTENTIONS_CATALOG, MODULE_BY_ID);
  assert.equal(result.valid, true, `Validation errors: ${JSON.stringify(result)}`);
  assert.equal(result.missingModules.length, 0);
  assert.equal(result.outOfBoundsLines.length, 0);
  assert.ok(result.totalTraceSteps >= 28);
  assert.ok(result.totalExhibits >= 24);
});

test('All audited axioms across traces and replay samples contain strictly standard Lean 4 axioms', () => {
  const stats = getContentionStats();
  assert.equal(stats.totalContentions, 8);
  assert.equal(stats.allAxiomsValid, true);
  assert.equal(stats.sampleAxiomsValid, true);
  assert.equal(isStandardAxiomSetOnly(['propext', 'Classical.choice', 'Quot.sound']), true);
  assert.equal(isStandardAxiomSetOnly(['propext', 'sorryAx']), false);
  assert.equal(isStandardAxiomSetOnly([]), false);
});

test('filterContentions matches keywords, categories, declarations, and claims accurately', () => {
  const rankOneHits = filterContentions(CONTENTIONS_CATALOG, 'rank-1', 'ALL');
  assert.ok(rankOneHits.some((c) => c.id === 'c8-scope-honesty'));

  const isingHits = filterContentions(CONTENTIONS_CATALOG, 'Ising', 'OS & Non-Gaussianity');
  assert.equal(isingHits.length, 1);
  assert.equal(isingHits[0].code, 'C5');

  const emptyHits = filterContentions(CONTENTIONS_CATALOG, 'nonexistent_token_xyz', 'ALL');
  assert.equal(emptyHits.length, 0);
});

test('filterReplaySamples finds matching #print axioms replay entries', () => {
  const globalHits = filterReplaySamples(REPLAY_AXIOM_SAMPLES, 'GlobalAxioms');
  assert.ok(globalHits.length >= 4);
  const allSamples = filterReplaySamples(REPLAY_AXIOM_SAMPLES, '');
  assert.equal(allSamples.length, REPLAY_AXIOM_SAMPLES.length);
});

test('verifyObservableVarianceWitness confirms non-constancy (3/2)^2 != 5/2 and non-Gaussianity -1/8 != 0', () => {
  const witness = verifyObservableVarianceWitness(5);
  assert.equal(witness.moment1, 1.5);
  assert.equal(witness.moment2, 2.5);
  assert.equal(witness.moment1Squared, 2.25);
  assert.equal(witness.variance, 0.25);
  assert.equal(witness.connected4Coincident, -0.125);
  assert.equal(witness.nonConstantAe, true);
  assert.equal(witness.nonGaussian, true);
  assert.equal(witness.canonicalWitnessN2.distinct, true);
  assert.ok(Math.abs(witness.canonicalWitnessN2.flipNormalized - 1 / 5) < 1e-12);
});

test('getScopeComparisonMatrix exposes valid module references for all 5 targets', () => {
  const rows = getScopeComparisonMatrix();
  assert.equal(rows.length, 5);
  for (const row of rows) {
    const mod = MODULE_BY_ID[row.moduleId];
    assert.ok(mod, `Missing module ${row.moduleId}`);
    assert.ok(row.line >= 1 && row.line <= mod.lineCount, `Out of range line ${row.line} for ${row.moduleId}`);
  }
});

test('ELEGANT_PROOFS gems resolve to valid Lean modules and lines and filter cleanly', () => {
  const res = validateElegantProofGems(ELEGANT_PROOFS, MODULE_BY_ID);
  assert.equal(res.valid, true, `Validation errors: ${JSON.stringify(res)}`);
  assert.equal(ELEGANT_PROOFS.length, 8);
  const symHits = filterElegantProofs(ELEGANT_PROOFS, '', 'Symmetry & Functoriality');
  assert.equal(symHits.length, 2);
  const slopeHits = filterElegantProofs(ELEGANT_PROOFS, 'HasDerivAt', 'ALL');
  assert.equal(slopeHits.length, 1);
  assert.equal(slopeHits[0].code, 'E4');
});

test('scripts/site_showcase.json stays in sync with contentionsData & elegantProofsData', () => {
  const raw = fs.readFileSync(path.resolve(process.cwd(), 'scripts/site_showcase.json'), 'utf8');
  const parsed = JSON.parse(raw);
  assert.deepEqual(parsed.contentions, CONTENTIONS_CATALOG);
  assert.deepEqual(parsed.elegantProofs, ELEGANT_PROOFS);
  assert.deepEqual(parsed.scopeMatrix, getScopeComparisonMatrix());
});
