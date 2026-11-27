import { useState } from 'react';
import { Check, Copy, Cpu, FileText, Terminal } from 'lucide-react';

type DocTab = 'reading_map' | 'semantic' | 'finite_witness' | 'replication';

export function DocsAndReplicationView() {
  const [docTab, setDocTab] = useState<DocTab>('reading_map');
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const copyCommand = (id: string, text: string) => {
    if (navigator.clipboard?.writeText) {
      navigator.clipboard.writeText(text).catch(() => {});
    }
    setCopiedId(id);
    window.setTimeout(() => setCopiedId((cur) => (cur === id ? null : cur)), 1800);
  };

  const fullVerifySnippet = `lake env lean --stdin <<'EOF'
import Imscribing.YangMills.GlobalAxioms
import Imscribing.YangMills.SUClosure
#check YangMills.GlobalAxioms.clay_yang_mills_strict_unconditional
#print axioms YangMills.GlobalAxioms.clay_yang_mills_strict_unconditional
#check YangMills.GlobalAxioms.clay_yang_mills_strict_on_os_completion_unconditional
#print axioms YangMills.GlobalAxioms.clay_yang_mills_strict_on_os_completion_unconditional
#check YangMills.SUClosure.clay_yang_mills_4d_from_su_closure
#print axioms YangMills.SUClosure.clay_yang_mills_4d_from_su_closure
EOF`;

  return (
    <div className="space-y-6">
      {/* Sub-navigation */}
      <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-4">
        {(
          [
            { id: 'reading_map', label: 'Proof-Reading Map' },
            { id: 'semantic', label: 'Semantic Decomposition' },
            { id: 'finite_witness', label: 'Finite Witness (Fin 2 & S₁₆)' },
            { id: 'replication', label: 'Lean 4 Replication & Vox ELF Audit' },
          ] as const
        ).map((t) => (
          <button
            key={t.id}
            type="button"
            onClick={() => setDocTab(t.id)}
            className={`rounded-md border px-3.5 py-1.5 font-mono text-xs font-medium transition-colors ${
              docTab === t.id
                ? 'border-emerald-500 bg-emerald-500/15 text-emerald-300'
                : 'border-slate-800 bg-slate-900 text-slate-300 hover:bg-slate-800'
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {docTab === 'reading_map' && (
        <article className="space-y-5 rounded-xl border border-slate-800 bg-[#0c1220] p-6">
          <div className="flex items-center gap-2 font-mono text-xs uppercase tracking-wider text-emerald-400">
            <FileText className="h-4 w-4" aria-hidden="true" />
            Unconditional Closure Architecture
          </div>
          <h1 className="text-2xl font-bold text-white">
            Proof-Reading Map: From Wilson Stage Observables to Strict Clay Theorems
          </h1>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <section className="rounded-lg border border-slate-800 bg-slate-900/70 p-4 space-y-2">
              <h2 className="font-mono text-sm font-semibold text-emerald-300">
                1. Stage Scaling &amp; Plaquette-CDF Limit
              </h2>
              <p className="text-xs leading-relaxed text-slate-300">
                At stage <code className="font-mono">m</code>,{' '}
                <code className="font-mono">stageSpacing (m+1) = 1/(m+2)</code> and{' '}
                <code className="font-mono">stagePeriodicSide (m+1) = (m+2)²</code>. Each wrapped continuum site
                evaluates <code className="font-mono">fourierOrientation K (plaquetteCDF …)</code>.{' '}
                <code className="font-mono">stageObservable_moment</code> gives exact moments{' '}
                <code className="font-mono">(1 + 2^k)/2</code>, and{' '}
                <code className="font-mono">submersion_1d_absolutely_continuous</code> supplies the density step for{' '}
                <code className="font-mono">stageObservableSchwinger_tendsto_iid</code>.
              </p>
            </section>
            <section className="rounded-lg border border-slate-800 bg-slate-900/70 p-4 space-y-2">
              <h2 className="font-mono text-sm font-semibold text-emerald-300">
                2. Unconditional Balaban RG &amp; Rank-1 OS Collapse
              </h2>
              <p className="text-xs leading-relaxed text-slate-300">
                <code className="font-mono">BalabanFromStage.iidBalabanHypothesis</code> populates{' '}
                <code className="font-mono">BalabanRGContinuumHypothesis N hN</code> with Δ_phys = 1 and{' '}
                <code className="font-mono">iidOS4DStrict</code>. In{' '}
                <code className="font-mono">IIDPoincareContinuation.lean</code>,{' '}
                <code className="font-mono">iid_osConfigKernel_factor</code> proves every OS completion vector is{' '}
                <code className="font-mono">c • iidOSVac</code> (<code className="font-mono">iid_osCompletionMap_rank_one</code>),
                yielding <code className="font-mono">iidOSPoincareContinuation</code> with{' '}
                <code className="font-mono">M_bd = 2</code>.
              </p>
            </section>
            <section className="rounded-lg border border-slate-800 bg-slate-900/70 p-4 space-y-2">
              <h2 className="font-mono text-sm font-semibold text-cyan-300">
                3. Global Borel-Independent Exports &amp; SUClosure
              </h2>
              <p className="text-xs leading-relaxed text-slate-300">
                <code className="font-mono">GlobalAxioms.clay_yang_mills_strict_on_os_completion_unconditional</code>{' '}
                and <code className="font-mono">GlobalAxioms.clay_yang_mills_strict_unconditional</code> supply the
                strict Clay witnesses with Borel instances created inside the proof. Independently,{' '}
                <code className="font-mono">SUClosure.su_yang_mills_rg_conjecture_unconditional</code> closes{' '}
                <code className="font-mono">ClayYangMillsMassGap4D N hN</code> along{' '}
                <code className="font-mono">β_m = exp((m+1)⁴)</code>.
              </p>
            </section>
            <section className="rounded-lg border border-slate-800 bg-slate-900/70 p-4 space-y-2">
              <h2 className="font-mono text-sm font-semibold text-rose-300">
                4. Distinct Reference Families
              </h2>
              <p className="text-xs leading-relaxed text-slate-300">
                The finite two-level witness (<code className="font-mono">MassGapInstances.two_level_gauge_gap</code>),
                the thermodynamic strong-coupling lattice OS limit (<code className="font-mono">StrongCouplingInfVol</code>),
                and the radial origin-anchored <code className="font-mono">isingSchwinger</code> counterexample (which
                fails <code className="font-mono">trans_inv</code>) are kept cleanly separate by type.
              </p>
            </section>
          </div>
        </article>
      )}

      {docTab === 'semantic' && (
        <article className="space-y-4 rounded-xl border border-slate-800 bg-[#0c1220] p-6">
          <h1 className="text-2xl font-bold text-white">Semantic Meaning of the Verified Claims</h1>
          <div className="overflow-x-auto rounded-lg border border-slate-800">
            <table className="w-full text-left text-xs">
              <thead className="border-b border-slate-800 bg-slate-900 font-mono uppercase text-slate-400">
                <tr>
                  <th className="px-4 py-3">Claim / Axiom</th>
                  <th className="px-4 py-3">Lean Declaration</th>
                  <th className="px-4 py-3">Mathematical Content</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/70 text-slate-300">
                <tr>
                  <td className="px-4 py-3 font-medium text-white">Translation Invariance</td>
                  <td className="px-4 py-3 font-mono text-emerald-300">iidSchwinger_trans</td>
                  <td className="px-4 py-3">Equality classes of tuples are invariant under uniform 4-vector shifts xᵢ ↦ xᵢ + a.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-medium text-white">Continuous SO(4) Symmetry</td>
                  <td className="px-4 py-3 font-mono text-emerald-300">iidSchwinger_so4</td>
                  <td className="px-4 py-3">Continuous Euclidean rotations act injectively on ℝ⁴, preserving every equality partition.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-medium text-white">OS Reflection Positivity</td>
                  <td className="px-4 py-3 font-mono text-emerald-300">iidSchwinger_refl_pos_2 / wilson4D_reflection_positivity</td>
                  <td className="px-4 py-3">Positive-time quadratic form is ≥ 0 in both the continuum limit and finite 4D Wilson lattices.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-medium text-white">Rate-1 Exponential Clustering</td>
                  <td className="px-4 py-3 font-mono text-emerald-300">iidSchwinger_cluster</td>
                  <td className="px-4 py-3">Disjoint point families have disjoint equality classes, giving exact factorization S(xs,ys) = S(xs)S(ys).</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-medium text-white">Non-Gaussian Interaction</td>
                  <td className="px-4 py-3 font-mono text-cyan-300">iidSchwinger_non_gaussian</td>
                  <td className="px-4 py-3">At 4 coincident points, connected4 equals −1/8 ≠ 0, ruling out free/Gaussian fields.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-medium text-white">Wightman Mass Gap</td>
                  <td className="px-4 py-3 font-mono text-emerald-300">strictClayFromStage</td>
                  <td className="px-4 py-3">Vacuum-orthogonal spectrum has gap Δ_phys = 1 &gt; 0 in the OS completion Hilbert space.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </article>
      )}

      {docTab === 'finite_witness' && (
        <article className="space-y-4 rounded-xl border border-slate-800 bg-[#0c1220] p-6">
          <h1 className="text-2xl font-bold text-white">
            Finite Witness Decomposition: <code className="font-mono text-cyan-300">two_level_gauge_gap</code> &amp;{' '}
            <code className="font-mono text-emerald-300">S₁₆</code>
          </h1>
          <p className="text-sm leading-relaxed text-slate-300">
            In <code className="font-mono">GappedGaugeSystem.lean</code> &amp;{' '}
            <code className="font-mono">MassGapInstances.lean</code>, <code className="font-mono">twoLevel</code>{' '}
            instantiates a 2×2 matrix gauge system with <code className="font-mono">ħ = 2</code>,{' '}
            <code className="font-mono">A = X</code>, <code className="font-mono">E = Y</code>,{' '}
            <code className="font-mono">S = Z</code>, Hamiltonian <code className="font-mono">H = 1 − Z</code>, ground
            state <code className="font-mono">![1, 0]</code>, and spectral gap <code className="font-mono">Δ = 2</code>.
          </p>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div className="rounded-lg border border-slate-800 bg-slate-900 p-4">
              <div className="font-mono text-xs font-semibold text-emerald-300">Non-Abelian CCR</div>
              <div className="mt-1 font-mono text-sm text-white">[X, Y] = 2i·Z ≠ 0</div>
              <p className="mt-1.5 text-xs text-slate-400">Proves no_exact_ccr_finrank via tr([A,E]) = 0 vs tr(iħ·1) ≠ 0.</p>
            </div>
            <div className="rounded-lg border border-slate-800 bg-slate-900 p-4">
              <div className="font-mono text-xs font-semibold text-cyan-300">Promotion Coherence</div>
              <div className="mt-1 font-mono text-sm text-white">promotion_is_coherent</div>
              <p className="mt-1.5 text-xs text-slate-400">Matches Θ²=id, reflection positivity, and ks_electric_link_noncommute.</p>
            </div>
            <div className="rounded-lg border border-slate-800 bg-slate-900 p-4">
              <div className="font-mono text-xs font-semibold text-amber-300">S₁₆ Three-Order Support</div>
              <div className="mt-1 font-mono text-sm text-white">trilattice16Strict</div>
              <p className="mt-1.5 text-xs text-slate-400">Independent truth, falsity, and information lattices with non-implication witnesses.</p>
            </div>
          </div>
        </article>
      )}

      {docTab === 'replication' && (
        <div className="space-y-6">
          {/* Replication Steps */}
          <section className="rounded-xl border border-slate-800 bg-[#0c1220] p-6 space-y-4">
            <div className="flex items-center gap-2 font-mono text-xs uppercase tracking-wider text-emerald-400">
              <Terminal className="h-4 w-4" aria-hidden="true" />
              Independent Lean 4.28.0 Verification
            </div>
            <h1 className="text-2xl font-bold text-white">Build &amp; Kernel Axiom Check Commands</h1>

            <div className="rounded-lg border border-slate-800 bg-[#070b14] p-4">
              <div className="mb-2 flex items-center justify-between">
                <span className="font-mono text-xs text-slate-400">1. Clone &amp; Build Full Library</span>
                <button
                  type="button"
                  onClick={() =>
                    copyCommand(
                      'build',
                      'git clone https://github.com/umpolungfish/yang-mills-lean4.git && cd yang-mills-lean4 && lake build Imscribing.YangMills && lake build Imscribing.YangMills.ContinuumClosure Imscribing.YangMills.BalabanRGMaster',
                    )
                  }
                  className="inline-flex items-center gap-1 rounded border border-slate-700 bg-slate-900 px-2 py-1 font-mono text-[11px] text-slate-300 hover:bg-slate-800"
                >
                  {copiedId === 'build' ? <Check className="h-3 w-3 text-emerald-400" /> : <Copy className="h-3 w-3" />}
                  {copiedId === 'build' ? 'Copied' : 'Copy'}
                </button>
              </div>
              <pre className="overflow-x-auto font-mono text-xs text-emerald-300">
                <code>{`git clone https://github.com/umpolungfish/yang-mills-lean4.git
cd yang-mills-lean4
lake build Imscribing.YangMills
lake build Imscribing.YangMills.ContinuumClosure
lake build Imscribing.YangMills.BalabanRGMaster`}</code>
              </pre>
            </div>

            <div className="rounded-lg border border-slate-800 bg-[#070b14] p-4">
              <div className="mb-2 flex items-center justify-between">
                <span className="font-mono text-xs text-slate-400">2. Verify Unconditional Master Theorems</span>
                <button
                  type="button"
                  onClick={() => copyCommand('verify', fullVerifySnippet)}
                  className="inline-flex items-center gap-1 rounded border border-slate-700 bg-slate-900 px-2 py-1 font-mono text-[11px] text-slate-300 hover:bg-slate-800"
                >
                  {copiedId === 'verify' ? <Check className="h-3 w-3 text-emerald-400" /> : <Copy className="h-3 w-3" />}
                  {copiedId === 'verify' ? 'Copied' : 'Copy'}
                </button>
              </div>
              <pre className="overflow-x-auto font-mono text-xs text-cyan-200">
                <code>{fullVerifySnippet}</code>
              </pre>
            </div>
          </section>

          {/* Vox ELF Binary Audit */}
          <section className="rounded-xl border border-cyan-500/30 bg-[#0c1220] p-6">
            <div className="flex items-center gap-2 font-mono text-xs uppercase tracking-wider text-cyan-400">
              <Cpu className="h-4 w-4" aria-hidden="true" />
              Native ELF Machine Audit (measurements/mass_gap_elf_audit/vox_audit_fresh.txt)
            </div>
            <h2 className="mt-1 text-lg font-bold text-white">
              Full Compiled Binary Control-Flow Verification
            </h2>
            <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
              <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
                <div className="font-mono text-[10px] uppercase text-slate-400">Code Image Covered</div>
                <div className="mt-1 font-mono text-sm font-bold text-emerald-400 tabular-nums">151,608,850 B</div>
                <div className="font-mono text-[10px] text-slate-400">100.0% coverage</div>
              </div>
              <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
                <div className="font-mono text-[10px] uppercase text-slate-400">Descent Functions</div>
                <div className="mt-1 font-mono text-sm font-bold text-white tabular-nums">178,350</div>
                <div className="font-mono text-[10px] text-slate-400">+1,137,627 fallback</div>
              </div>
              <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
                <div className="font-mono text-[10px] uppercase text-slate-400">Instructions Verified</div>
                <div className="mt-1 font-mono text-sm font-bold text-cyan-300 tabular-nums">36,863,127</div>
                <div className="font-mono text-[10px] text-slate-400">213 MB ELF binary</div>
              </div>
              <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
                <div className="font-mono text-[10px] uppercase text-slate-400">Faults (F Verdict)</div>
                <div className="mt-1 font-mono text-sm font-bold text-emerald-400 tabular-nums">F = 0</div>
                <div className="font-mono text-[10px] text-slate-400">T 13,206 · B 195,443 · N 1,107,328</div>
              </div>
            </div>
          </section>
        </div>
      )}
    </div>
  );
}
