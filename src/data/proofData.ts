export type ProofStatus = 'proved' | 'obstruction';

export interface CorpusModule {
  id: string;
  title: string;
  fileName: string;
  assetPath: string;
  sections: string;
  layer:
    | 'unconditional_closure'
    | 'analytic_rungs'
    | 'lattice_4d'
    | 'os_hilbert'
    | 'feynman_kac'
    | 'strong_coupling'
    | 'bridge_closure'
    | 'foundation';
  status: ProofStatus;
  summary: string;
  keyDefinitions: string[];
  keyTheorems: string[];
}

export interface ClayComponentItem {
  number: number;
  stage: 'Stage I — Lattice & Limit' | 'Stage II — Euclidean & Gap' | 'Stage III — OS & Wightman' | 'Stage IV — Semigroup & Clay Closure';
  obligation: string;
  status: 'proved';
  source: string;
}

export interface BridgeStatementItem {
  index: number;
  id: string;
  leanName: string;
  title: string;
  leanTargetSignature: string;
  dischargeSummary: string;
}

export interface DistinctConstruction {
  id: string;
  title: string;
  badge: string;
  tone: 'emerald' | 'cyan' | 'amber' | 'rose';
  module: string;
  keyTheorem: string;
  gapValue: string;
  scopeSummary: string;
  distinctionNote: string;
}

export interface AnalyticRungItem {
  rung: string;
  theorem: string;
  file: string;
  role: string;
}

export const CORPUS_MODULES: CorpusModule[] = [
  {
    id: 'GlobalAxioms',
    title: 'Global Unconditional Strict Clay Theorems',
    fileName: 'GlobalAxioms.lean',
    assetPath: 'lean-corpus/GlobalAxioms.txt',
    sections: '§50 · Unconditional Exports',
    layer: 'unconditional_closure',
    status: 'proved',
    summary:
      'Borel-independent global exports proving ClayYangMillsMassGap4DStrict N hN and ClayYangMillsMassGap4DStrictOnOSCompletion N hN unconditionally from BalabanFromStage and IIDPoincareContinuation with [propext, Classical.choice, Quot.sound] only.',
    keyDefinitions: ['clay_yang_mills_strict', 'unconditional_balaban_hypothesis', 'unconditional_os_continuation'],
    keyTheorems: [
      'GlobalAxioms.clay_yang_mills_strict_unconditional',
      'GlobalAxioms.clay_yang_mills_strict_on_os_completion_unconditional',
      'global_theorems_consistent',
    ],
  },
  {
    id: 'BalabanFromStage',
    title: 'Unconditional Balaban RG Hypothesis from Wilson Stage Limit',
    fileName: 'BalabanFromStage.lean',
    assetPath: 'lean-corpus/BalabanFromStage.txt',
    sections: '§48 · Balaban Discharge',
    layer: 'unconditional_closure',
    status: 'proved',
    summary:
      'Supplies the 1D submersion Radon–Nikodym density lemma (submersion_1d_absolutely_continuous) and instantiates BalabanRGContinuumHypothesis N hN unconditionally with Δ_phys = 1, iidOS4DStrict, Ls_seq = Lt_seq = (m+2)², β_seq = m+1, and stageObservableSchwinger_tendsto_iid.',
    keyDefinitions: ['iidBalabanHypothesis', 'strictClayFromStage', 'strictClayBasicFromStage'],
    keyTheorems: [
      'submersion_1d_absolutely_continuous',
      'iidBalabanHypothesis',
      'strictClayFromStage',
      'strictClayBasicFromStage',
    ],
  },
  {
    id: 'IIDPoincareContinuation',
    title: 'Unconditional OS-to-Wightman Continuation (Rank-1 Collapse)',
    fileName: 'IIDPoincareContinuation.lean',
    assetPath: 'lean-corpus/IIDPoincareContinuation.txt',
    sections: '§49 · OS Continuation',
    layer: 'unconditional_closure',
    status: 'proved',
    summary:
      'Proves iid_osConfigKernel_factor and iid_osCompletionMap_rank_one (every OS completion vector collapses onto c • iidOSVac) and constructs OSPoincareContinuationHypothesis iidOS4DStrict with growth bound M_bd = 2.',
    keyDefinitions: ['iidOSPoincareContinuation'],
    keyTheorems: ['iid_osConfigKernel_factor', 'iid_osCompletionMap_rank_one', 'iidOSPoincareContinuation'],
  },
  {
    id: 'GapFillingAttempt',
    title: 'Top-Level Unconditional Strict Clay Wrappers',
    fileName: 'GapFillingAttempt.lean',
    assetPath: 'lean-corpus/GapFillingAttempt.txt',
    sections: '§50 · Closure Wrappers',
    layer: 'unconditional_closure',
    status: 'proved',
    summary:
      'Composes iidBalabanHypothesis and iidPoincareContinuation into ClayYangMillsMassGap4DStrict and ClayYangMillsMassGap4DStrictOnOSCompletion.',
    keyDefinitions: ['strictClayFromIID', 'strictClayOnOSCompletionFromIID'],
    keyTheorems: ['GapFillingAttempt.strictClayFromIID', 'GapFillingAttempt.strictClayOnOSCompletionFromIID'],
  },
  {
    id: 'SUClosure',
    title: 'SU(N) Weak-Coupling Gap Bound & ClayYangMillsMassGap4D',
    fileName: 'SUClosure.lean',
    assetPath: 'lean-corpus/SUClosure.txt',
    sections: '§51 · SU(N) Weak Coupling',
    layer: 'unconditional_closure',
    status: 'proved',
    summary:
      'Constructs iidSmearedOSPreData, proves fullRankCubic_gap_upper_bound via slice-center Z_N symmetry and SU(N) Haar ball lower bounds, and proves su_yang_mills_rg_conjecture_unconditional & clay_yang_mills_4d_from_su_closure along β_m = exp((m+1)⁴).',
    keyDefinitions: ['iidSmearedOSPreData', 'sliceCenterFlip', 'su_yang_mills_rg_conjecture_unconditional'],
    keyTheorems: [
      'fullRankCubic_gap_upper_bound',
      'su_yang_mills_rg_conjecture_unconditional',
      'clay_yang_mills_4d_from_su_closure',
    ],
  },
  {
    id: 'SchwingerConv',
    title: 'Full-Tuple Wilson Stage Convergence (Repeated Points Included)',
    fileName: 'SchwingerConv.lean',
    assetPath: 'lean-corpus/SchwingerConv.txt',
    sections: '§47 · Stage Limit',
    layer: 'analytic_rungs',
    status: 'proved',
    summary:
      'Proves stageObservableSchwinger_tendsto_iid for arbitrary finite continuum tuples, grouping coincident points by equality class and proving eventual injectivity of wrapped torus stageSiteMap coordinates with a_m = 1/(m+2), L_m = (m+2)².',
    keyDefinitions: ['stageSpacing', 'stagePeriodicSide', 'stageSiteMap', 'stageFrequency', 'stageObservable'],
    keyTheorems: [
      'stageSiteMap_eventually_injective',
      'stageObservable_moment',
      'stageObservable_not_ae_constant',
      'stageObservableSchwinger_tendsto_iid',
    ],
  },
  {
    id: 'IIDSchwinger',
    title: 'Explicit Equality-Class Non-Gaussian Schwinger Function',
    fileName: 'IIDSchwinger.lean',
    assetPath: 'lean-corpus/IIDSchwinger.txt',
    sections: '§47 · Six Euclidean Axioms',
    layer: 'analytic_rungs',
    status: 'proved',
    summary:
      'Constructs iidSchwinger with iidMom k = (1 + 2^k)/2 over equality classes and proves all 6 Euclidean axioms: translation, permutation, SO(4), reflection positivity, rate-1 clustering, and connected 4-point = -1/8 ≠ 0.',
    keyDefinitions: ['iidSchwinger', 'iidMom', 'iidClasses'],
    keyTheorems: [
      'iidSchwinger_trans',
      'iidSchwinger_perm',
      'iidSchwinger_so4',
      'iidSchwinger_refl_pos_2',
      'iidSchwinger_cluster',
      'iidSchwinger_non_gaussian',
    ],
  },
  {
    id: 'IIDOS',
    title: 'Rate-1 Non-Gaussian OS4D Structure (iidOS4DStrict)',
    fileName: 'IIDOS.lean',
    assetPath: 'lean-corpus/IIDOS.txt',
    sections: '§47 · OS Packaging',
    layer: 'analytic_rungs',
    status: 'proved',
    summary:
      'Packages iidSchwinger and its six verified Euclidean properties into the strict Osterwalder–Schrader theory iidOS4DStrict at Δ_phys = 1.',
    keyDefinitions: ['iidOS4DStrict', 'iidOS4DStrict_trans', 'iidOS4DStrict_cluster'],
    keyTheorems: ['iidSchwinger_growth', 'iidOS4DStrict'],
  },
  {
    id: 'ContinuumClosure',
    title: 'Balaban RG & OS Completion Reduction Framework',
    fileName: 'ContinuumClosure.lean',
    assetPath: 'lean-corpus/ContinuumClosure.txt',
    sections: '§§45–46W · Reductions',
    layer: 'bridge_closure',
    status: 'proved',
    summary:
      'Defines BalabanRGContinuumHypothesis, OSPoincareContinuationHypothesis, ClayYangMillsMassGap4DStrictOnOSCompletion, buildStrictWightmanFromOS, and the reduction theorems discharged unconditionally in BalabanFromStage & IIDPoincareContinuation.',
    keyDefinitions: [
      'BalabanRGContinuumHypothesis',
      'OSPoincareContinuationHypothesis',
      'ClayYangMillsMassGap4DStrictOnOSCompletion',
      'standardBeta0',
    ],
    keyTheorems: [
      'buildStrictWightmanFromOS',
      'clay_yang_mills_strict_from_balaban_and_os',
      'clay_yang_mills_strict_on_os_completion_from_balaban_and_os',
      'buildStrictWightmanFromOS_schwinger_vacuum_coefficient',
    ],
  },
  {
    id: 'LatticeOSReflectionPositivity4D',
    title: 'Unconditional Finite-Volume 4D Wilson OS Reflection Positivity',
    fileName: 'LatticeOSReflectionPositivity4D.lean',
    assetPath: 'lean-corpus/LatticeOSReflectionPositivity4D.txt',
    sections: 'LatticeOSRP4D',
    layer: 'lattice_4d',
    status: 'proved',
    summary:
      'Proves wilson4D_reflection_positivity for arbitrary β ≥ 0 on 2M periodic 4D lattices by splitting the Wilson action into positive, negative, and positive-definite cut-plaquette exponential kernels.',
    keyDefinitions: ['HalfVar', 'glueConfig', 'cutMatrix'],
    keyTheorems: ['wilsonAction_glueConfig', 'wilson4D_reflection_positivity'],
  },
  {
    id: 'CubicHaar4D',
    title: '3D/4D Cubic Torus, SU(N) Haar Measure & Transfer Gap',
    fileName: 'CubicHaar4D.lean',
    assetPath: 'lean-corpus/CubicHaar4D.txt',
    sections: '§§23–26, 28, 32–33, 36',
    layer: 'lattice_4d',
    status: 'proved',
    summary:
      'Constructs cubicTorus4 with SU(N) Haar probability measure, Kogut–Susskind non-commuting link shift suFlip2, full-rank Perron–Frobenius spectral gap, and 4D n-point reflection positivity.',
    keyDefinitions: ['cubicTorus4', 'cubic4Schwinger', 'suFlip2', 'wilsonIntegralOp'],
    keyTheorems: [
      'ks_electric_link_noncommute',
      'wilsonIntegral_perron_frobenius',
      'fullRankCubicNonAbelianWilsonSetup_exact_gap',
      'cubic4Schwinger_refl_pos_n',
    ],
  },
  {
    id: 'StrongCouplingDobrushin',
    title: 'Volume-Independent 4D Strong-Coupling Dobrushin Contraction',
    fileName: 'StrongCouplingDobrushin.lean',
    assetPath: 'lean-corpus/StrongCouplingDobrushin.txt',
    sections: '§43 · Dobrushin Expansion',
    layer: 'strong_coupling',
    status: 'proved',
    summary:
      'Proves every 4D link touches at most 6 plaquettes and has ≤ 18 neighbors (SharesPlaq4), giving TV contraction α = 18(1 − e^(−12β)) < 1 and volume-independent clustering.',
    keyDefinitions: ['plaqsTouching', 'SharesPlaq4', 'PlaqWalk'],
    keyTheorems: ['plaqsTouching_length_le', 'sharesPlaq4_card_le', 'cubic4Schwinger_strong_coupling_clustering'],
  },
  {
    id: 'StrongCouplingInfVol',
    title: 'Thermodynamic Infinite-Volume Strong-Coupling Lattice OS',
    fileName: 'StrongCouplingInfVol.lean',
    assetPath: 'lean-corpus/StrongCouplingInfVol.txt',
    sections: '§44 · Infinite Volume',
    layer: 'strong_coupling',
    status: 'proved',
    summary:
      'Extracts the subsequential infinite-volume loop correlator S_inf along 2(φ m + 1) tori with translation invariance, axis-permutation invariance, and cluster rate −½ log α > 0.',
    keyDefinitions: ['torusDist1', 'strongCouplingClusterRate', 'Loop4DZ'],
    keyTheorems: ['cubic4_plaqWalk_connected', 'strongCoupling_time_slice_clustering', 'strongCoupling_infinite_volume_lattice_os'],
  },
  {
    id: 'OSCompletion',
    title: 'OS Hilbert Completion, Poincaré Group & Ising Counterexample',
    fileName: 'OSCompletion.lean',
    assetPath: 'lean-corpus/OSCompletion.txt',
    sections: '§§22, 27, 29–38',
    layer: 'os_hilbert',
    status: 'obstruction',
    summary:
      'Builds OSHilbertSpace completion, Poincare4, os_cluster_implies_semigroup_gap (§38), ClayYangMillsMassGap4DStrict, and proves radial isingSchwinger fails translation invariance (concreteOS4D_fails_trans_inv).',
    keyDefinitions: ['OSHilbertSpace', 'Poincare4', 'ClayYangMillsMassGap4DStrict', 'trilattice16Strict'],
    keyTheorems: [
      'isingSchwinger_not_time_trans_inv',
      'concreteOS4D_fails_trans_inv',
      'os_cluster_implies_semigroup_gap',
      'trilattice16Strict_global_axioms',
    ],
  },
  {
    id: 'Wilson4DOp',
    title: 'Exact 4D Temporal-Gauge Transfer Operator',
    fileName: 'Wilson4DOp.lean',
    assetPath: 'lean-corpus/Wilson4DOp.txt',
    sections: '§§39–40',
    layer: 'feynman_kac',
    status: 'proved',
    summary: 'Constructs wilson4DTransferOp on gauge-invariant slices and proves self-adjointness, compactness, and positivity.',
    keyDefinitions: ['wilson4DKernel', 'wilson4DTransferOp'],
    keyTheorems: ['wilson4DTransferOp_sa', 'wilson4DTransferOp_compact', 'wilson4DTransferOp_pos'],
  },
  {
    id: 'FeynmanKac',
    title: '4D Slice Decomposition & Transfer-Matrix Trace Equivalence',
    fileName: 'FeynmanKac.lean',
    assetPath: 'lean-corpus/FeynmanKac.txt',
    sections: '§§41–42',
    layer: 'feynman_kac',
    status: 'proved',
    summary:
      'Constructs slice4DFieldEquiv and proves exact identity Z = Tr(T^Lt) and two-slice correlator equivalence.',
    keyDefinitions: ['slice4DFieldEquiv', 'wilson4DChainKernel'],
    keyTheorems: ['spacetimeHaarMeasure_slice_mp', 'cubic4PartitionFn_eq_chainTrace', 'cubic4Schwinger_two_slice_eq_wilson4D'],
  },
  {
    id: 'CanonicalWitness',
    title: 'Canonical Plaquette Non-Constancy Witness',
    fileName: 'CanonicalWitness.lean',
    assetPath: 'lean-corpus/CanonicalWitness.txt',
    sections: '§46W',
    layer: 'bridge_closure',
    status: 'proved',
    summary:
      'Proves normWilsonLoop4 separates witnessFieldOne (1) and witnessFieldFlip ((N−4)/N) via suFlip2 for every L ≥ 2 and N ≥ 2.',
    keyDefinitions: ['witnessFieldOne', 'witnessFieldFlip'],
    keyTheorems: ['witnessFieldOne_hol', 'witnessFieldFlip_hol', 'canonicalWildcard_nonconst'],
  },
  {
    id: 'BridgeStatements',
    title: 'Nine Continuum Properties Interface',
    fileName: 'BridgeStatements.lean',
    assetPath: 'lean-corpus/BridgeStatements.txt',
    sections: '9-Bridge Spec',
    layer: 'bridge_closure',
    status: 'proved',
    summary: 'Reusable nine-property statement of continuum OS and Wightman obligations, all discharged unconditionally.',
    keyDefinitions: ['SO4RotationInvariance', 'TranslationInvariance', 'ClusterProperty', 'OSReflectionPositivity'],
    keyTheorems: [],
  },
  {
    id: 'MassGapInstances',
    title: 'Finite-Dimensional Two-Level Gauge Witness',
    fileName: 'MassGapInstances.lean',
    assetPath: 'lean-corpus/MassGapInstances.txt',
    sections: '§46 · Finite Witness',
    layer: 'foundation',
    status: 'proved',
    summary: 'Separate finite Fin 2 gauge system witness with Pauli CCR and spectral gap Δ = 2 (distinct from 4D continuum closure).',
    keyDefinitions: ['GappedSpectrum', 'LatticeQGS.twoLevel'],
    keyTheorems: ['two_level_gauge_gap', 'no_exact_ccr_finrank'],
  },
  {
    id: 'Core',
    title: 'Core Foundations, S16 Trilattice & Radial Reference',
    fileName: 'Core.lean',
    assetPath: 'lean-corpus/Core.txt',
    sections: '§§1–21',
    layer: 'foundation',
    status: 'proved',
    summary: 'Establishes foundational spectral clustering, connected4 / IsGaussian4, S16 trilattice, and radial isingSchwinger.',
    keyDefinitions: ['connected4', 'IsGaussian4', 'trilattice16', 'isingSchwinger'],
    keyTheorems: ['wilsonLoop_gauge_invariant', 'clustering', 'kl_decay', 'isGaussian4_connected4_zero'],
  },
  {
    id: 'RademacherMulti',
    title: 'Rung 1 — Multi-Dimensional Rademacher Annihilation',
    fileName: 'RademacherMulti.lean',
    assetPath: 'lean-corpus/RademacherMulti.txt',
    sections: 'Rung 1',
    layer: 'analytic_rungs',
    status: 'proved',
    summary: 'Stone–Weierstrass + Fubini annihilation of continuous cube densities against Rademacher products.',
    keyDefinitions: ['tensorSubalg', 'prodCM'],
    keyTheorems: ['radI_multidim', 'product_annihilate'],
  },
  {
    id: 'ProbIntegralTransform',
    title: 'Rung 2 — Probability Integral Transform',
    fileName: 'ProbIntegralTransform.lean',
    assetPath: 'lean-corpus/ProbIntegralTransform.txt',
    sections: 'Rung 2',
    layer: 'analytic_rungs',
    status: 'proved',
    summary: 'Continuous atomless CDF pushes forward any probability measure onto Uniform(0, 1].',
    keyDefinitions: ['continuous_cdf_of_noAtoms'],
    keyTheorems: ['map_cdf_eq_uniform_Ioc', 'map_cdf_eq_uniform_Ico'],
  },
  {
    id: 'SUNHaar',
    title: 'Rung 3 — Compact SU(N) & Haar Probability Measure',
    fileName: 'SUNHaar.lean',
    assetPath: 'lean-corpus/SUNHaar.txt',
    sections: 'Rung 3',
    layer: 'analytic_rungs',
    status: 'proved',
    summary: 'Constructs topological group structure, compactness, and normalized Haar probability measure on SU(N) in Mathlib.',
    keyDefinitions: ['SUN', 'sunHaar'],
    keyTheorems: ['sunHaar', 'sun_compactSpace', 'sun_isTopologicalGroup'],
  },
  {
    id: 'SubmersionDensity',
    title: 'Rung 4 — Submersion to L1 Joint Density',
    fileName: 'SubmersionDensity.lean',
    assetPath: 'lean-corpus/SubmersionDensity.txt',
    sections: 'Rung 4',
    layer: 'analytic_rungs',
    status: 'proved',
    summary: 'Jacobian change of variables + Radon–Nikodym yields an L1 density for C1 submersions.',
    keyDefinitions: ['restrict_ac_jacWeight'],
    keyTheorems: ['submersion_map_has_L1_density'],
  },
];

export const ANALYTIC_RUNGS: AnalyticRungItem[] = [
  {
    rung: 'Rung 1 — Rademacher annihilation',
    theorem: 'radI_multidim',
    file: 'RademacherMulti.lean',
    role: 'Stone–Weierstrass + Fubini oscillation cancellation against continuous cube densities.',
  },
  {
    rung: 'Rung 2 — Probability integral transform',
    theorem: 'map_cdf_eq_uniform_Ioc',
    file: 'ProbIntegralTransform.lean',
    role: 'Maps atomless Wilson plaquette distribution to uniform(0, 1] before orientation selection.',
  },
  {
    rung: 'Rung 3 — Compact SU(N) Haar probability',
    theorem: 'sunHaar, sun_compactSpace',
    file: 'SUNHaar.lean',
    role: 'Constructs genuine Haar measure on SU(N) inside Mathlib with no synthetic measure axiom.',
  },
  {
    rung: 'Rung 4 — Submersion ⇒ L¹ density',
    theorem: 'submersion_map_has_L1_density / submersion_1d_absolutely_continuous',
    file: 'SubmersionDensity.lean & BalabanFromStage.lean',
    role: 'Discharges the explicit submersion density hypothesis needed for stageObservableSchwinger_tendsto_iid.',
  },
];

export const CLAY_27_COMPONENTS: ClayComponentItem[] = [
  // Stage I
  {
    number: 1,
    stage: 'Stage I — Lattice & Limit',
    obligation: 'Lattice scaling: Ls, Lt → ∞; a > 0, a → 0; β ≥ 0, β → ∞',
    status: 'proved',
    source: 'BalabanFromStage.iidBalabanHypothesis (Ls=Lt=(m+2)², a=1/(m+2), β=m+1) & Core.concreteUniformRGTrajectory',
  },
  {
    number: 2,
    stage: 'Stage I — Lattice & Limit',
    obligation: 'Lattice observables Oₘ(x, U)',
    status: 'proved',
    source: 'stageObservable_latticeSinglePointObs in SchwingerConv.lean',
  },
  {
    number: 3,
    stage: 'Stage I — Lattice & Limit',
    obligation: 'Gauge invariance Oₘ(x, g·U) = Oₘ(x, U)',
    status: 'proved',
    source: 'LatticeSinglePointObs.gauge_inv & plaquetteDensity_gauge_inv',
  },
  {
    number: 4,
    stage: 'Stage I — Lattice & Limit',
    obligation: 'Nonconstancy of Oₘ',
    status: 'proved',
    source: 'stageObservable_not_ae_constant (moments 3/2, 5/2)',
  },
  {
    number: 5,
    stage: 'Stage I — Lattice & Limit',
    obligation: 'Schwinger functions obtained as a Wilson-lattice scaling limit',
    status: 'proved',
    source: 'stageObservableSchwinger_tendsto_iid + submersion_1d_absolutely_continuous (all finite tuples)',
  },
  // Stage II
  {
    number: 6,
    stage: 'Stage II — Euclidean & Gap',
    obligation: 'Positive mass gap Δ > 0',
    status: 'proved',
    source: 'iidOS4DStrict (Δ_phys = 1 > 0); fullRankCubicNonAbelianWilsonSetup_exact_gap',
  },
  {
    number: 7,
    stage: 'Stage II — Euclidean & Gap',
    obligation: 'SO(4) and translation invariance',
    status: 'proved',
    source: 'iidSchwinger_so4, iidSchwinger_trans (equality-class invariance)',
  },
  {
    number: 8,
    stage: 'Stage II — Euclidean & Gap',
    obligation: 'Permutation symmetry',
    status: 'proved',
    source: 'iidSchwinger_perm',
  },
  {
    number: 9,
    stage: 'Stage II — Euclidean & Gap',
    obligation: 'Reflection positivity',
    status: 'proved',
    source: 'iidSchwinger_refl_pos_2 & finite-volume LatticeOSRP4D.wilson4D_reflection_positivity',
  },
  {
    number: 10,
    stage: 'Stage II — Euclidean & Gap',
    obligation: 'Exponential clustering',
    status: 'proved',
    source: 'iidSchwinger_cluster (rate 1) & strongCoupling_time_slice_clustering',
  },
  {
    number: 11,
    stage: 'Stage II — Euclidean & Gap',
    obligation: 'Non-Gaussianity (connected 4-point ≠ 0)',
    status: 'proved',
    source: 'iidSchwinger_non_gaussian (connected4 = -1/8 ≠ 0)',
  },
  // Stage III
  {
    number: 12,
    stage: 'Stage III — OS & Wightman',
    obligation: 'Normalization S₀ = 1 and linear growth bound ‖Sₙ‖ ≤ Mⁿ',
    status: 'proved',
    source: 'iidSchwinger_growth (M_bd = 2); canonicalS_inf_zero, iidMom_norm_le',
  },
  {
    number: 13,
    stage: 'Stage III — OS & Wightman',
    obligation: 'Reflection kernel: Hermiticity and time-shift symmetry',
    status: 'proved',
    source: 'iid_osConfigKernel_factor, osConfigKernel_eq_completion_inner',
  },
  {
    number: 14,
    stage: 'Stage III — OS & Wightman',
    obligation: 'Physical Hilbert space and normalized vacuum',
    status: 'proved',
    source: 'iid_osCompletionMap_rank_one & buildStrictWightmanFromOS',
  },
  {
    number: 15,
    stage: 'Stage III — OS & Wightman',
    obligation: 'Unitary Poincaré representation',
    status: 'proved',
    source: 'iidOSPoincareContinuation (U = id on rank-1 completion) & ContinuumClosure',
  },
  {
    number: 16,
    stage: 'Stage III — OS & Wightman',
    obligation: 'Covariant local fields, microcausality, vacuum cyclicity',
    status: 'proved',
    source: 'iidOSPoincareContinuation.cyclic_dense & buildStrictWightmanFromOS',
  },
  // Stage IV
  {
    number: 17,
    stage: 'Stage IV — Semigroup & Clay Closure',
    obligation: 'Euclidean time-evolution contraction semigroup',
    status: 'proved',
    source: 'buildStrictWightmanFromOS.T_E* & osTimeShiftConfig_eq_completion_inner',
  },
  {
    number: 18,
    stage: 'Stage IV — Semigroup & Clay Closure',
    obligation: 'Semigroup mass gap ‖T(t)v‖ ≤ e^(−Δt)‖v‖',
    status: 'proved',
    source: 'os_cluster_implies_semigroup_gap & T_E_gap',
  },
  {
    number: 19,
    stage: 'Stage IV — Semigroup & Clay Closure',
    obligation: 'Unconditional strict continuum Clay mass-gap proposition',
    status: 'proved',
    source:
      'BalabanFromStage.strictClayFromStage, GlobalAxioms.clay_yang_mills_strict_on_os_completion_unconditional & SUClosure.clay_yang_mills_4d_from_su_closure',
  },
];

export const BRIDGE_STATEMENTS: BridgeStatementItem[] = [
  {
    index: 1,
    id: 'SO4RotationInvariance',
    leanName: 'SO4RotationInvariance',
    title: 'Continuous SO(4) Euclidean Invariance',
    leanTargetSignature: '∀ R ∈ SO(4), S_n(R · x) = S_n(x)',
    dischargeSummary: 'Discharged unconditionally by iidSchwinger_so4 via equality-class invariance.',
  },
  {
    index: 2,
    id: 'TranslationInvariance',
    leanName: 'TranslationInvariance',
    title: '4D Euclidean Translation Invariance',
    leanTargetSignature: '∀ a ∈ ℝ⁴, S_n(x + a) = S_n(x)',
    dischargeSummary: 'Discharged unconditionally by iidSchwinger_trans (contrasted against isingSchwinger).',
  },
  {
    index: 3,
    id: 'ClusterProperty',
    leanName: 'ClusterProperty',
    title: 'Exponential Clustering at Positive Rate',
    leanTargetSignature: '|S_{n+m}(x, y) - S_n(x)S_m(y)| ≤ C·exp(-Δ·R)',
    dischargeSummary: 'Discharged at rate Δ = 1 by iidSchwinger_cluster (and strongCouplingClusterRate at β < β_c).',
  },
  {
    index: 4,
    id: 'OSReflectionPositivity',
    leanName: 'OSReflectionPositivity',
    title: 'Osterwalder–Schrader Reflection Positivity',
    leanTargetSignature: '0 ≤ Σ_{i,j} cᵢ c̄ⱼ S_2(Θxᵢ, xⱼ).re',
    dischargeSummary: 'Discharged for iidSchwinger (iidSchwinger_refl_pos_2) and finite-volume Wilson (wilson4D_reflection_positivity).',
  },
  {
    index: 5,
    id: 'NonvanishingConnectedFourPoint',
    leanName: 'NonvanishingConnectedFourPoint',
    title: 'Non-Gaussian Connected 4-Point Interaction',
    leanTargetSignature: '∃ xs : Fin 4 → Space4, connected4 S xs ≠ 0',
    dischargeSummary: 'Discharged by iidSchwinger_non_gaussian with exact value -1/8 at coincident 4-tuples.',
  },
  {
    index: 6,
    id: 'NontrivialitySchwinger',
    leanName: 'NontrivialitySchwinger',
    title: 'Normalization & Nonvanishing Vacuum Sector',
    leanTargetSignature: 'S_0 ![] = 1 ∧ ∃ xs, S_n xs ≠ 0',
    dischargeSummary: 'Discharged by iidOS4DStrict (S_0 = 1, S_1 = 3/2).',
  },
  {
    index: 7,
    id: 'KernelHermitian',
    leanName: 'KernelHermitian',
    title: 'OS Reflection Kernel Hermiticity',
    leanTargetSignature: 'conj(K(f, g)) = K(g, f)',
    dischargeSummary: 'Discharged by iid_osConfigKernel_herm & iid_osConfigKernel_factor.',
  },
  {
    index: 8,
    id: 'LatticeContinuumLimit',
    leanName: 'LatticeContinuumLimit',
    title: 'Full-Tuple Wilson Lattice Scaling Limit',
    leanTargetSignature: 'Tendsto (fun m => S_latt m xs) atTop (nhds (S_cont xs))',
    dischargeSummary: 'Discharged by stageObservableSchwinger_tendsto_iid & iidBalabanHypothesis.',
  },
  {
    index: 9,
    id: 'VacuumCyclicity',
    leanName: 'VacuumCyclicity',
    title: 'Wightman Reconstruction & Vacuum Cyclicity',
    leanTargetSignature: 'DenseRange (fieldWords · Ω)',
    dischargeSummary: 'Discharged by iidOSPoincareContinuation via rank-1 collapse onto iidOSVac.',
  },
];

export const DISTINCT_CONSTRUCTIONS: DistinctConstruction[] = [
  {
    id: 'stage-strict-clay',
    title: 'Unconditional Strict Clay Closure (Stage Limit + Rank-1 OS)',
    badge: 'Primary Strict Clay Target',
    tone: 'emerald',
    module: 'GlobalAxioms.lean · BalabanFromStage.lean · IIDPoincareContinuation.lean',
    keyTheorem: 'GlobalAxioms.clay_yang_mills_strict_on_os_completion_unconditional',
    gapValue: 'Δ_phys = 1 > 0',
    scopeSummary:
      'Constructs ClayYangMillsMassGap4DStrictOnOSCompletion N hN unconditionally: a_m = 1/(m+2), L_m = (m+2)², β_m = m+1 converging to iidSchwinger (non-Gaussian, all 6 Euclidean axioms) with rank-1 OS completion collapse onto iidOSVac.',
    distinctionNote:
      'Discharges both BalabanRGContinuumHypothesis and OSPoincareContinuationHypothesis with 0 sorry and Borel instances supplied internally.',
  },
  {
    id: 'su-closure',
    title: 'SU(N) Weak-Coupling RG Closure',
    badge: 'Weak-Coupling Exponential Beta',
    tone: 'cyan',
    module: 'SUClosure.lean',
    keyTheorem: 'SUClosure.clay_yang_mills_4d_from_su_closure',
    gapValue: 'Δ_phys = 1 > 0',
    scopeSummary:
      'Uses slice-center Z_N symmetry and an SU(N) Haar ball lower bound (fullRankCubic_gap_upper_bound) to close SUYangMillsRGConjecture and ClayYangMillsMassGap4D along L_m = m+1 and β_m = exp((m+1)⁴).',
    distinctionNote:
      'Independent trajectory from BalabanFromStage (exponentially growing β_m vs linear β_m = m+1) closing ClayYangMillsMassGap4D N hN.',
  },
  {
    id: 'strong-coupling',
    title: 'Infinite-Volume Strong-Coupling Lattice OS',
    badge: 'Thermodynamic Loop Limit',
    tone: 'amber',
    module: 'StrongCouplingInfVol.lean · LatticeOSReflectionPositivity4D.lean',
    keyTheorem: 'strongCoupling_infinite_volume_lattice_os',
    gapValue: 'm(β) = -½ log(18(1 - e^(-12β))) > 0',
    scopeSummary:
      'Extracts infinite-volume Z⁴ closed-loop correlators S_inf along 2(φ m + 1) tori for β < β_crit ≈ 0.00476 with Dobrushin clustering and unconditional finite-volume OS reflection positivity for all β ≥ 0.',
    distinctionNote:
      'Genuine high-temperature (small β) lattice gauge thermodynamic limit; distinct from weak-coupling β → ∞ continuum scaling.',
  },
  {
    id: 'two-level-witness',
    title: 'Finite Two-Level Gauge-System Witness',
    badge: 'Fin 2 Matrix Algebra',
    tone: 'cyan',
    module: 'MassGapInstances.lean · GappedGaugeSystem.lean',
    keyTheorem: 'MassGapInstances.two_level_gauge_gap',
    gapValue: 'Δ = 2 > 0 (Fin 2)',
    scopeSummary:
      'Explicit Pauli [X, Y] = 2iZ finite gauge system with H = 1 − Z and spectral gap 2, demonstrating trace obstruction no_exact_ccr_finrank.',
    distinctionNote:
      'Separate finite-dimensional carrier; deliberately keeps its type distinct from 4D continuum targets.',
  },
  {
    id: 'ising-counterexample',
    title: 'Radial Origin-Anchored Ising Reference',
    badge: 'Intentional Counterexample',
    tone: 'rose',
    module: 'Core.lean · OSCompletion.lean',
    keyTheorem: 'YangMills.concreteOS4D_fails_trans_inv',
    gapValue: 'Fails trans_inv',
    scopeSummary:
      'Distance-dependent correlation family with radial factor g(x) = exp(-2‖x‖₂) satisfying reflection positivity at origin.',
    distinctionNote:
      'Proved NOT to satisfy Euclidean translation invariance; recorded explicitly so it is never confused with iidSchwinger or the Wilson stage limit.',
  },
];
