import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {
  ARCHITECTURE_EDGES,
  BRIDGE_STATEMENTS,
  CORPUS_MODULES,
  THEOREM_CATALOG,
} from './corpusData.ts';

describe('Lean 4 Corpus Metadata Integrity', () => {
  it('references all 11 existing asset files in public/assets/aistudio/', () => {
    assert.equal(CORPUS_MODULES.length, 11);
    const ids = new Set(CORPUS_MODULES.map((m) => m.id));
    assert.equal(ids.size, 11);

    for (const mod of CORPUS_MODULES) {
      const diskPath = path.join(process.cwd(), 'public', mod.assetPath.replace(/^\//, ''));
      assert.ok(fs.existsSync(diskPath), `Missing corpus file at ${diskPath}`);
      const content = fs.readFileSync(diskPath, 'utf8');
      const actualLines = content.split('\n').length;
      assert.equal(
        mod.lineCount,
        actualLines,
        `Line count mismatch for ${mod.id}: expected ${actualLines}, got ${mod.lineCount}`,
      );
    }
  });

  it('has valid module references in all DAG edges and theorem catalog entries', () => {
    const ids = new Set(CORPUS_MODULES.map((m) => m.id));
    for (const edge of ARCHITECTURE_EDGES) {
      assert.ok(ids.has(edge.from), `Unknown edge.from ${edge.from}`);
      assert.ok(ids.has(edge.to), `Unknown edge.to ${edge.to}`);
    }
    for (const thm of THEOREM_CATALOG) {
      assert.ok(ids.has(thm.moduleId), `Unknown theorem moduleId ${thm.moduleId}`);
    }
  });

  it('records all 9 BridgeStatements in sequential order', () => {
    assert.equal(BRIDGE_STATEMENTS.length, 9);
    BRIDGE_STATEMENTS.forEach((b, idx) => {
      assert.equal(b.index, idx + 1);
      assert.ok(b.leanName.length > 0);
      assert.ok(b.finiteVolumeLemma.length > 0);
      assert.ok(b.remainingContinuumGap.length > 0);
    });
  });
});
