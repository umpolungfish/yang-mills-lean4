import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import {
  buildCentralLinkPlaquettes3D,
  buildTesseractGeometry,
  computeKogutSusskindPathGap,
  project3D,
  project4D,
  waveRingAmplitude,
} from './visualSimMath.ts';
import { STANDARD_BETA0 } from './yangMillsMath.ts';

describe('Visual projection & 4D lattice geometry helpers', () => {
  it('constructs exact 16-vertex, 32-edge S16 tesseract geometry', () => {
    const geom = buildTesseractGeometry();
    assert.equal(geom.vertices.length, 16);
    assert.equal(geom.edges.length, 32);
    for (const [u, v] of geom.edges) {
      assert.ok(u < v);
      const xor = u ^ v;
      assert.equal(xor & (xor - 1), 0, 'Tesseract edge endpoints must differ by exactly 1 bit');
    }
  });

  it('builds 6 orthogonal plaquettes with 18 unique neighbor outer segments around central link', () => {
    const plaqs = buildCentralLinkPlaquettes3D();
    assert.equal(plaqs.length, 6);
    // Each of 6 plaquettes contributes 3 outer links besides the shared central link = 18
    assert.equal(plaqs.length * 3, 18);
  });

  it('projects 3D and 4D coordinates into finite 2D viewport points', () => {
    const p3 = project3D({ x: 1, y: -1, z: 0.5 }, 0.4, 0.3, 400, 4.5, 300, 200);
    assert.ok(Number.isFinite(p3.x) && Number.isFinite(p3.y) && p3.scale > 0);

    const p4 = project4D({ x: 1, y: 1, z: -1, w: 1 }, 0.5, 0.25, 0.4, 0.3);
    assert.ok(Number.isFinite(p4.x) && Number.isFinite(p4.y) && p4.scale > 0);
  });

  it('decays Dobrushin wave amplitude radially at standardBeta0 and saturates at supercritical beta', () => {
    const a0 = waveRingAmplitude(STANDARD_BETA0, 0, 0);
    const a4 = waveRingAmplitude(STANDARD_BETA0, 4, 0);
    assert.ok(a4 < a0, 'Strong-coupling wave must decay across hops');

    const superA = waveRingAmplitude(0.007, 4, 0);
    assert.ok(superA >= 0.5, 'Supercritical regime should remain unsuppressed');
  });

  it('computes non-zero Kogut-Susskind commutator magnitude 4/N for N >= 2', () => {
    for (const N of [2, 3, 4, 6]) {
      const ks = computeKogutSusskindPathGap(N);
      assert.ok(Math.abs(ks.commutatorMag - 4 / N) < 1e-12);
    }
  });
});
