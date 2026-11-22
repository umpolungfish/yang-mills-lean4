export type ProofStatus = 'proved' | 'obstruction' | 'open_hypothesis';

export interface CorpusModule {
  id: string;
  title: string;
  fileName: string;
  assetPath: string;
  sections: string;
  lineCount: number;
  layer: 'foundation' | 'lattice_4d' | 'os_hilbert' | 'feynman_kac' | 'strong_coupling' | 'bridge_closure';
  status: ProofStatus;
  summary: string;
  imports: string[];
  keyDefinitions: string[];
  keyTheorems: string[];
}

export interface ArchitectureEdge {
  from: string;
  to: string;
  label: string;
  kind: 'depends' | 'rejects' | 'open_gap';
}

export interface BridgeStatementItem {
  index: number;
  id: string;
  leanName: string;
  title: string;
  finiteStrongCouplingStatus: 'proved' | 'partial';
  weakContinuumStatus: 'open';
  leanTargetSignature: string;
  finiteVolumeLemma: string;
  remainingContinuumGap: string;
}

export interface TheoremEntry {
  name: string;
  section: string;
  moduleId: string;
  kind: 'theorem' | 'def' | 'structure' | 'inductive';
  status: ProofStatus;
  statement: string;
}

export const CORPUS_MODULES: CorpusModule[] = [
  {
    id: 'Core',
    title: 'Core Axiomatics, Spectral Clustering & Concrete Realizations',
    fileName: 'Core.lean',
    assetPath: 'assets/aistudio/Core_ea76d0a5.txt',
    sections: '§§1–21',
    lineCount: 5040,
    layer: 'foundation',
    status: 'proved',
    summary:
      'Establishes gauge invariance of path holonomies and Wilson loops, spectral clustering on infinite-dimensional Hilbert spaces, Källén–Lehmann bounds, S16 trilattice models, connected 4-point cumulants (IsGaussian4), Hamiltonian phase space, and the origin-anchored isingSchwinger example.',
    imports: ['Mathlib'],
    keyDefinitions: [
      'LatticeGaugeSetup',
      'TrilatticeModel / trilattice16 / tesseractLattice',
      'connected4 / IsGaussian4',
      'OS4DContinuumTheory',
      'isingSchwinger',
    ],
    keyTheorems: [
      'wilsonLoop_gauge_invariant',
      'clustering',
      'kl_decay',
      'trilattice16_properties',
      'isGaussian4_connected4_zero',
      'unconditional_os_hilbert_completion_and_wightman_reconstruction',
    ],
  },
  {
    id: 'CubicHaar4D',
    title: '3D/4D Cubic Torus, SU(N) Haar Measure & Reflection Positivity',
    fileName: 'CubicHaar4D.lean',
    assetPath: 'assets/aistudio/CubicHaar4D_d22af2f2.txt',
    sections: '§§23–26, 28, 32–33, 36',
    lineCount: 8156,
    layer: 'lattice_4d',
    status: 'proved',
    summary:
      'Constructs cubicTorus3 and cubicTorus4 with genuine compact SU(N) Haar product probability measures, Kogut–Susskind Hamiltonian with canonical non-commuting electric-link shift suFlip2, full-rank Wilson integral operator with Perron–Frobenius spectral gap, and 4D OS reflection positivity and S4 symmetries.',
    imports: ['Mathlib', 'Core'],
    keyDefinitions: [
      'cubicTorus3 / cubicTorus4',
      'suHaar / spacetimeHaarMeasure',
      'cubic4Schwinger',
      'suFlip2',
      'wilsonIntegralOp',
    ],
    keyTheorems: [
      'ks_electric_link_noncommute',
      'wilsonIntegral_perron_frobenius',
      'fullRankCubicNonAbelianWilsonSetup_exact_gap',
      'cubic4Schwinger_refl_pos_n',
      'cubic4Schwinger_trans_inv',
      'cubic4Schwinger_axis_perm_inv',
    ],
  },
  {
    id: 'OSCompletion',
    title: 'True OS Completion, Poincaré Group, Obstructions & Hardened Interfaces',
    fileName: 'OSCompletion.lean',
    assetPath: 'assets/aistudio/OSCompletion_eb19a235.txt',
    sections: '§§22, 27, 29–31, 34–35, 37–38',
    lineCount: 3043,
    layer: 'os_hilbert',
    status: 'obstruction',
    summary:
      'Builds genuine OSHilbertSpace completion, Poincare4 = ℝ⁴ ⋊ O(1,3), Glimm–Jaffe semigroup contraction, and Euclidean cluster → semigroup gap (§38). Critically proves isingSchwinger fails time translation invariance (§34/§37) and hardens the Clay target into ClayYangMillsMassGap4DStrict.',
    imports: ['Mathlib', 'Core', 'CubicHaar4D'],
    keyDefinitions: [
      'OSHilbertSpace / osCompletionMap',
      'Poincare4',
      'OsterwalderSchrader4DStrict',
      'WightmanQFT4DStrict',
      'LatticeSinglePointObs',
      'ClayYangMillsMassGap4DStrict',
      'trilattice16Strict',
    ],
    keyTheorems: [
      'os_semigroup_contraction_of_bounded',
      'isingSchwinger_not_time_trans_inv',
      'concreteOS4D_fails_trans_inv',
      'clay_yang_mills_from_rg_estimates',
      'trilattice16Strict_global_axioms',
      'os_cluster_implies_semigroup_gap',
    ],
  },
  {
    id: 'Wilson4DOp',
    title: 'Exact 4D Temporal-Gauge Transfer Operator & Positivity',
    fileName: 'Wilson4DOp.lean',
    assetPath: 'assets/aistudio/Wilson4DOp_72156458.txt',
    sections: '§§39–40',
    lineCount: 1876,
    layer: 'feynman_kac',
    status: 'proved',
    summary:
      'Defines the exact 4D Wilson temporal-link-integrated transfer kernel wilson4DKernel between adjacent cubicTorus3 slices, proves self-adjointness, compactness, gauge projection, strict operator positivity (via Bernoulli–Taylor evalSepList), and Perron–Frobenius spectral gap.',
    imports: ['Mathlib', 'OSCompletion'],
    keyDefinitions: [
      'GaugeGrp3',
      'temporalPlaqFactor',
      'wilson4DKernel',
      'wilson4DTransferOp',
      'wilson4DLatticeGaugeSetup',
    ],
    keyTheorems: [
      'wilson4DKernel_gauge_inv_two_sided',
      'wilson4DTransferOp_sa',
      'wilson4DTransferOp_compact',
      'wilson4DTransferOp_pos',
      'wilson4DNonAbelianSetup',
    ],
  },
  {
    id: 'FeynmanKac',
    title: '4D Slice Decomposition & Exact Transfer-Matrix Trace Equivalence',
    fileName: 'FeynmanKac.lean',
    assetPath: 'assets/aistudio/FeynmanKac_cd5e0e8b.txt',
    sections: '§§41–42',
    lineCount: 2115,
    layer: 'feynman_kac',
    status: 'proved',
    summary:
      'Constructs the slice bijection slice4DFieldEquiv separating Lt spatial slices from Lt temporal gauge links, proves measure-preserving Haar factorization spacetimeHaarMeasure_slice_mp, chain kernel composition, and exact equality between 4D lattice Schwinger two-slice correlators and wilson4DTransferOp powers.',
    imports: ['Mathlib', 'OSCompletion', 'Wilson4DOp'],
    keyDefinitions: [
      'slice4DFieldEquiv',
      'polyakovLoop3 / polyakovObs3',
      'osSpaceTransOp',
      'wilson4DChainKernel',
    ],
    keyTheorems: [
      'polyakovObs3_nonconst',
      'osSpaceTransOp_comm_time',
      'spacetimeHaarMeasure_slice_mp',
      'cubic4WilsonWeight_slice_factor',
      'cubic4PartitionFn_eq_chainTrace',
      'cubic4Schwinger_two_slice_eq_wilson4D',
    ],
  },
  {
    id: 'StrongCouplingDobrushin',
    title: 'Volume-Independent Strong-Coupling Gap via Dobrushin Expansion',
    fileName: 'StrongCouplingDobrushin.lean',
    assetPath: 'assets/aistudio/StrongCouplingDobrushin_1b2ac8bc.txt',
    sections: '§43',
    lineCount: 2339,
    layer: 'strong_coupling',
    status: 'proved',
    summary:
      'Proves that in 4D every link touches at most 6 plaquettes and has at most 18 plaquette-neighbors (SharesPlaq4). Derives single-link conditional Gibbs TV contraction c = 1 − exp(−12β) and Lyapunov potential greedy elimination, yielding volume-independent exponential clustering whenever α = 18(1 − e^(−12β)) < 1.',
    imports: ['Mathlib', 'OSCompletion', 'Wilson4DOp', 'FeynmanKac'],
    keyDefinitions: [
      'plaqsTouching',
      'SharesPlaq4',
      'PlaqWalk',
      'dobrushinPhiExt / dobrushinPsiSharp',
    ],
    keyTheorems: [
      'plaqsTouching_length_le',
      'sharesPlaq4_card_le',
      'condDensity_tv_bound',
      'condGibbsExp_osc_bound',
      'cubic4Schwinger_strong_coupling_clustering',
    ],
  },
  {
    id: 'StrongCouplingInfVol',
    title: 'Plaquette Connectivity & Infinite-Volume Strong-Coupling Lattice OS',
    fileName: 'StrongCouplingInfVol.lean',
    assetPath: 'assets/aistudio/StrongCouplingInfVol_b0fe0390.txt',
    sections: '§44',
    lineCount: 864,
    layer: 'strong_coupling',
    status: 'proved',
    summary:
      'Establishes periodic Lee metric torusDist1, proves full connectivity of cubic4_plaqWalk_connected, proves time-slice clustering at strongCouplingClusterRate β = -½ log α, and extracts an infinite-volume strong-coupling SU(N) lattice theory along L_m = 2(φ m + 1) for all Loop4DZ loops.',
    imports: ['Mathlib', 'OSCompletion', 'Wilson4DOp', 'FeynmanKac', 'StrongCouplingDobrushin'],
    keyDefinitions: [
      'torusDist1',
      'strongCouplingClusterRate',
      'Loop4DZ / embedLoop4DZ',
      'decLoop4DZ / decQuery',
    ],
    keyTheorems: [
      'cubic4_plaqWalk_connected',
      'strongCoupling_time_slice_clustering',
      'embedLoop4DZ_isPath',
      'strongCoupling_infinite_volume_lattice_os',
    ],
  },
  {
    id: 'FeynmanKacAndStrongCoupling',
    title: 'Aggregator Module (§§39–44)',
    fileName: 'FeynmanKacAndStrongCoupling.lean',
    assetPath: 'assets/aistudio/FeynmanKacAndStrongCoupling_349de8da.txt',
    sections: '§§39–44 (Agg)',
    lineCount: 9,
    layer: 'strong_coupling',
    status: 'proved',
    summary:
      'Lightweight cached-layer aggregator re-exporting Wilson4DOp, FeynmanKac, StrongCouplingDobrushin, and StrongCouplingInfVol into ContinuumClosure.',
    imports: ['Wilson4DOp', 'FeynmanKac', 'StrongCouplingDobrushin', 'StrongCouplingInfVol'],
    keyDefinitions: [],
    keyTheorems: [],
  },
  {
    id: 'ContinuumClosure',
    title: 'Balaban RG / OS Continuation Bridge & Axiom Verification',
    fileName: 'ContinuumClosure.lean',
    assetPath: 'assets/aistudio/ContinuumClosure_627682d9.txt',
    sections: '§§45–46W',
    lineCount: 1221,
    layer: 'bridge_closure',
    status: 'open_hypothesis',
    summary:
      'Isolates the open weak-coupling BalabanRGContinuumHypothesis and OSPoincareContinuationHypothesis structures and proves unconditionally that combining them yields ClayYangMillsMassGap4DStrict. Also extracts canonical thermodynamic data at standardBeta0 = 1/300 and runs a complete #print axioms audit.',
    imports: ['Mathlib', 'Core', 'CubicHaar4D', 'OSCompletion', 'FeynmanKacAndStrongCoupling'],
    keyDefinitions: [
      'BalabanRGContinuumHypothesis',
      'OSPoincareContinuationHypothesis',
      'standardBeta0 (1/300)',
      'standardDeltaPhys',
      'canonicalSContA / canonicalSContB',
    ],
    keyTheorems: [
      'buildStrictWightmanFromOS',
      'clay_yang_mills_strict_from_balaban_and_os',
      'standardBeta0_dobrushin',
      'canonicalS_inf_conv',
      'canonicalWildcard_nonconstW',
    ],
  },
  {
    id: 'CanonicalWitness',
    title: 'Canonical Observable Non-Constancy Witness',
    fileName: 'CanonicalWitness.lean',
    assetPath: 'assets/aistudio/CanonicalWitness_96d8e111.txt',
    sections: '§46W',
    lineCount: 162,
    layer: 'bridge_closure',
    status: 'proved',
    summary:
      'Self-contained unconditional witness proving that normWilsonLoop4 on the embedded canonical elementary plaquette takes distinct values 1 (on witnessFieldOne) and (N − 4)/N (on witnessFieldFlip using suFlip2) for every L ≥ 2 and N ≥ 2.',
    imports: ['Mathlib', 'ContinuumClosure'],
    keyDefinitions: ['witnessFieldOne', 'witnessFieldFlip'],
    keyTheorems: [
      'embedLoop4DZ_canonicalPlaq',
      'witnessFieldOne_hol',
      'tail_links_ne_base',
      'witnessFieldFlip_hol',
      'canonicalWildcard_nonconst',
    ],
  },
  {
    id: 'BridgeStatements',
    title: 'Nine Formal Target Properties for the Infinite-Volume Bridge',
    fileName: 'BridgeStatements.lean',
    assetPath: 'assets/aistudio/BridgeStatements_67faba65.txt',
    sections: 'Target Spec',
    lineCount: 98,
    layer: 'bridge_closure',
    status: 'open_hypothesis',
    summary:
      'Records the exact schematic Prop signatures of the nine Osterwalder–Schrader and continuum target axioms required to discharge the infinite-volume bridge into Wightman QFT.',
    imports: ['Mathlib'],
    keyDefinitions: [
      'SO4RotationInvariance',
      'TranslationInvariance',
      'ClusterProperty',
      'OSReflectionPositivity',
      'NonvanishingConnectedFourPoint',
      'NontrivialitySchwinger',
      'KernelHermitian',
      'LatticeContinuumLimit',
      'VacuumCyclicity',
    ],
    keyTheorems: [],
  },
];

export const ARCHITECTURE_EDGES: ArchitectureEdge[] = [
  { from: 'Core', to: 'CubicHaar4D', label: 'Lattice setup & Wilson action', kind: 'depends' },
  { from: 'Core', to: 'OSCompletion', label: 'isingSchwinger toy & OS4D interfaces', kind: 'rejects' },
  { from: 'CubicHaar4D', to: 'OSCompletion', label: 'Haar 4D Schwinger + suFlip2 + RP', kind: 'depends' },
  { from: 'OSCompletion', to: 'Wilson4DOp', label: 'OSHilbertSpace & strict gap', kind: 'depends' },
  { from: 'Wilson4DOp', to: 'FeynmanKac', label: 'wilson4DTransferOp positivity', kind: 'depends' },
  { from: 'FeynmanKac', to: 'StrongCouplingDobrushin', label: 'Slice factorization & traces', kind: 'depends' },
  { from: 'StrongCouplingDobrushin', to: 'StrongCouplingInfVol', label: 'α < 1 Dobrushin clustering', kind: 'depends' },
  { from: 'StrongCouplingInfVol', to: 'FeynmanKacAndStrongCoupling', label: 'Exports §§39–44', kind: 'depends' },
  { from: 'FeynmanKacAndStrongCoupling', to: 'ContinuumClosure', label: 'Strong-coupling S_inf (β = 1/300)', kind: 'depends' },
  { from: 'ContinuumClosure', to: 'CanonicalWitness', label: 'Plaquette embedding lemmas', kind: 'depends' },
  { from: 'BridgeStatements', to: 'ContinuumClosure', label: '9 target bridge Props', kind: 'open_gap' },
];

export const BRIDGE_STATEMENTS: BridgeStatementItem[] = [
  {
    index: 1,
    id: 'so4',
    leanName: 'SO4RotationInvariance',
    title: 'SO(4) Euclidean Rotation Invariance',
    finiteStrongCouplingStatus: 'partial',
    weakContinuumStatus: 'open',
    leanTargetSignature:
      '∀ n R x, BridgeS n (fun i => R.mulVec (x i)) = BridgeS n x',
    finiteVolumeLemma:
      'cubic4Schwinger_axis_perm_inv (§36) & S_inf hypercubic S₄ invariance (§44) proved unconditionally on Z⁴ lattices.',
    remainingContinuumGap:
      'Full continuous SO(4) restoration in the a → 0⁺, β → ∞ scaling limit requires weak-coupling RG rotational symmetry control.',
  },
  {
    index: 2,
    id: 'trans',
    leanName: 'TranslationInvariance',
    title: 'Euclidean Translation Invariance',
    finiteStrongCouplingStatus: 'proved',
    weakContinuumStatus: 'open',
    leanTargetSignature:
      '∀ n a x, BridgeS n (fun i => x i + a) = BridgeS n x',
    finiteVolumeLemma:
      'cubic4Schwinger_trans_inv (§36) and Z⁴ shift invariance of S_inf (§44) are proved; isingSchwinger explicitly fails this (§37).',
    remainingContinuumGap:
      'Extending discrete Z⁴ shift invariance to full ℝ⁴ continuous translation invariance of the scaling limit.',
  },
  {
    index: 3,
    id: 'cluster',
    leanName: 'ClusterProperty',
    title: 'Exponential Clustering Property',
    finiteStrongCouplingStatus: 'proved',
    weakContinuumStatus: 'open',
    leanTargetSignature:
      '∃ Δ > 0, |S(n+m)(x ++ y) − S(n)(x)·S(m)(y)| ≤ C · exp(−Δ·R)',
    finiteVolumeLemma:
      'cubic4Schwinger_strong_coupling_clustering (§43) & strongCoupling_time_slice_clustering (§44) give rate -½ log α > 0 for α < 1.',
    remainingContinuumGap:
      'Uniform mass gap lower bound Δ_latt / a ≥ Δ₀ > 0 as β → ∞ (outside the α < 1 Dobrushin radius).',
  },
  {
    index: 4,
    id: 'rp',
    leanName: 'OSReflectionPositivity',
    title: 'Osterwalder–Schrader Reflection Positivity',
    finiteStrongCouplingStatus: 'proved',
    weakContinuumStatus: 'open',
    leanTargetSignature:
      '0 ≤ Re (∑ i j, cᵢ c̄ⱼ S(nᵢ + nⱼ)(Θ(xᵢ) ++ xⱼ))',
    finiteVolumeLemma:
      'cubic4Schwinger_refl_pos_n (§36) and time-reflection invariance revFlip (§46W) proved unconditionally for SU(N) Haar measures.',
    remainingContinuumGap:
      'Preservation of n-point reflection positivity under weak-coupling distributional test-function smearing in the scaling limit.',
  },
  {
    index: 5,
    id: 'conn4',
    leanName: 'NonvanishingConnectedFourPoint',
    title: 'Non-Gaussian Connected 4-Point Function',
    finiteStrongCouplingStatus: 'partial',
    weakContinuumStatus: 'open',
    leanTargetSignature: '∃ x : BridgeConfig 4, BridgeSconn x ≠ 0',
    finiteVolumeLemma:
      'connected4 cumulant formalism (§9) and canonicalWildcard_nonconst (§46W) prove single-point observables are non-constant (1 vs (N−4)/N).',
    remainingContinuumGap:
      'Proving ¬ IsGaussian4 (non-vanishing 4-point connected cumulant) survives the continuum scaling renormalization limit.',
  },
  {
    index: 6,
    id: 'nontriv',
    leanName: 'NontrivialitySchwinger',
    title: 'Schwinger Function Nontriviality',
    finiteStrongCouplingStatus: 'proved',
    weakContinuumStatus: 'open',
    leanTargetSignature: '∀ n ≥ 1, ∃ x : BridgeConfig n, BridgeS n x ≠ 0',
    finiteVolumeLemma:
      'Unitary non-constancy of normWilsonLoop4 proved in CanonicalWitness (§46W) and strict positivity of partition function (§25).',
    remainingContinuumGap:
      'Ensuring renormalized field insertions in BalabanRGContinuumHypothesis remain non-trivial at infinite β.',
  },
  {
    index: 7,
    id: 'herm',
    leanName: 'KernelHermitian',
    title: 'Reflection Kernel Hermiticity',
    finiteStrongCouplingStatus: 'proved',
    weakContinuumStatus: 'open',
    leanTargetSignature: 'reflectionKernel x y = starRingEnd ℂ (reflectionKernel y x)',
    finiteVolumeLemma:
      'osConfigForm Hermiticity & wilson4DKernel_symm (§39) and cubic4Schwinger_timeReflect_inv (§36) proved.',
    remainingContinuumGap:
      'Automatic once continuum Schwinger functions inherit time-reflection + permutation symmetry from lattice approximations.',
  },
  {
    index: 8,
    id: 'limit',
    leanName: 'LatticeContinuumLimit',
    title: 'Lattice-to-Continuum Convergence',
    finiteStrongCouplingStatus: 'proved',
    weakContinuumStatus: 'open',
    leanTargetSignature:
      '∀ n ε > 0, ∃ M, ∀ β ≥ M, |BridgeSlatt β n x − BridgeSinf n x| < ε',
    finiteVolumeLemma:
      'strongCoupling_infinite_volume_lattice_os (§44) constructs thermodynamic convergence L_m → ∞ at fixed β = 1/300.',
    remainingContinuumGap:
      'Simultaneous weak-coupling asymptotic freedom trajectory (a_m → 0⁺, β_m → ∞, Ls_m → ∞) in BalabanRGContinuumHypothesis.',
  },
  {
    index: 9,
    id: 'cyclic',
    leanName: 'VacuumCyclicity',
    title: 'Vacuum Cyclicity on Physical Hilbert Space',
    finiteStrongCouplingStatus: 'partial',
    weakContinuumStatus: 'open',
    leanTargetSignature: 'closure (span ℂ { U_g (φ n x Ω) }) = Set.univ',
    finiteVolumeLemma:
      'osCompletionMap_dense (§22) constructs cyclic vacuum Ω on OSHilbertSpace and lifts T_E (§31/§38).',
    remainingContinuumGap:
      'Analytic continuation from Euclidean T_E to full Poincare4 = ℝ⁴ ⋊ O(1,3) unitary representation and local commutativity (OSPoincareContinuationHypothesis).',
  },
];

export const THEOREM_CATALOG: TheoremEntry[] = [
  {
    name: 'wilsonLoop_gauge_invariant',
    section: '§1',
    moduleId: 'Core',
    kind: 'theorem',
    status: 'proved',
    statement: 'Normalized trace of closed path holonomy is invariant under arbitrary local gauge transformations g : Site → G.',
  },
  {
    name: 'trilattice16_properties',
    section: '§8',
    moduleId: 'Core',
    kind: 'theorem',
    status: 'proved',
    statement: 'Establishes independence of le16_i, le16_t, le16_f and non-commutativity of legacy inc16 with walk16.',
  },
  {
    name: 'ks_electric_link_noncommute',
    section: '§28',
    moduleId: 'CubicHaar4D',
    kind: 'theorem',
    status: 'proved',
    statement: 'Proves [ksLinkShiftOp(suFlip2), ksLinkTraceOp] ≠ 0 for N ≥ 2, establishing non-Abelian canonical conjugate link algebra.',
  },
  {
    name: 'fullRankCubicNonAbelianWilsonSetup_exact_gap',
    section: '§33',
    moduleId: 'CubicHaar4D',
    kind: 'theorem',
    status: 'proved',
    statement: 'Extracts finite-volume Perron–Frobenius ground state and strictly positive spectral gap for wilsonIntegralOp.',
  },
  {
    name: 'cubic4Schwinger_refl_pos_n',
    section: '§36',
    moduleId: 'CubicHaar4D',
    kind: 'theorem',
    status: 'proved',
    statement: 'Proves full n-point Osterwalder–Schrader reflection positivity for 4D SU(N) Haar Schwinger correlators.',
  },
  {
    name: 'isingSchwinger_not_time_trans_inv',
    section: '§34',
    moduleId: 'OSCompletion',
    kind: 'theorem',
    status: 'obstruction',
    statement: 'Counterexample showing the origin-anchored radial Ising toy fails Euclidean time-translation invariance.',
  },
  {
    name: 'concreteOS4D_fails_trans_inv',
    section: '§37',
    moduleId: 'OSCompletion',
    kind: 'theorem',
    status: 'obstruction',
    statement: 'Hardened OsterwalderSchrader4DStrict interface immediately rejects concreteOS4DContinuumTheory (S₂(0,0)=2 vs S₂(a,a)=1+e⁻⁴).',
  },
  {
    name: 'trilattice16Strict_global_axioms',
    section: '§37',
    moduleId: 'OSCompletion',
    kind: 'theorem',
    status: 'proved',
    statement: 'Proves inc16Strict is globally idempotent, globally non-void, and non-commutative with walk16.',
  },
  {
    name: 'os_cluster_implies_semigroup_gap',
    section: '§38',
    moduleId: 'OSCompletion',
    kind: 'theorem',
    status: 'proved',
    statement: 'Derives Euclidean OS transfer semigroup decay ‖T_E(t)v‖ ≤ exp(-Δ·t)‖v‖ on Ω_phys⊥ directly from Schwinger clustering + translation invariance.',
  },
  {
    name: 'wilson4DTransferOp_pos',
    section: '§40',
    moduleId: 'Wilson4DOp',
    kind: 'theorem',
    status: 'proved',
    statement: 'Uses Bernoulli–Taylor polynomial factorization (evalSepList) to prove strict positivity ⟨ψ, T_4D ψ⟩ ≥ 0.',
  },
  {
    name: 'cubic4Schwinger_two_slice_eq_wilson4D',
    section: '§42',
    moduleId: 'FeynmanKac',
    kind: 'theorem',
    status: 'proved',
    statement: 'Exact Feynman–Kac identity equating 4D Euclidean 2-slice Schwinger expectations to powers of wilson4DTransferOp.',
  },
  {
    name: 'sharesPlaq4_card_le',
    section: '§43',
    moduleId: 'StrongCouplingDobrushin',
    kind: 'theorem',
    status: 'proved',
    statement: 'Combinatorial proof that every link on cubicTorus4 belongs to ≤ 6 plaquettes and shares a plaquette with ≤ 18 neighbor links.',
  },
  {
    name: 'cubic4Schwinger_strong_coupling_clustering',
    section: '§43',
    moduleId: 'StrongCouplingDobrushin',
    kind: 'theorem',
    status: 'proved',
    statement: 'Volume-independent exponential clustering at rate -½ log α for all α = 18(1 − e^(-12β)) < 1 via Dobrushin greedy elimination.',
  },
  {
    name: 'strongCoupling_infinite_volume_lattice_os',
    section: '§44',
    moduleId: 'StrongCouplingInfVol',
    kind: 'theorem',
    status: 'proved',
    statement: 'Subsequence thermodynamic limit along L_m = 2(φ m + 1) preserving Z⁴ translations, S₄ axis permutations, RP, and positive mass gap.',
  },
  {
    name: 'clay_yang_mills_strict_from_balaban_and_os',
    section: '§45',
    moduleId: 'ContinuumClosure',
    kind: 'theorem',
    status: 'open_hypothesis',
    statement: 'Unconditional Lean implication: BalabanRGContinuumHypothesis ∧ OSPoincareContinuationHypothesis → ClayYangMillsMassGap4DStrict.',
  },
  {
    name: 'standardBeta0_dobrushin',
    section: '§45',
    moduleId: 'ContinuumClosure',
    kind: 'theorem',
    status: 'proved',
    statement: 'Proves β₀ = 1/300 strictly satisfies the Dobrushin contraction bound 18(1 − exp(-12/300)) < 1.',
  },
  {
    name: 'canonicalWildcard_nonconst',
    section: '§46W',
    moduleId: 'CanonicalWitness',
    kind: 'theorem',
    status: 'proved',
    statement: 'Constructs witnessFieldOne (value 1) and witnessFieldFlip (value (N−4)/N via suFlip2) proving canonical plaquette non-constancy for all N, L ≥ 2.',
  },
];
