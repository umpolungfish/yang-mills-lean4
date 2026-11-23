export type ProofStatus = 'proved' | 'obstruction';

export interface CorpusModule {
  id: string;
  title: string;
  fileName: string;
  assetPath: string;
  sections: string;
  lineCount: number;
  layer: 'foundation' | 'lattice_4d' | 'os_hilbert' | 'feynman_kac' | 'strong_coupling' | 'bridge_closure' | 'analytic_rungs';
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
  kind: 'depends' | 'rejects';
}

export interface BridgeStatementItem {
  index: number;
  id: string;
  leanName: string;
  title: string;
  finiteStrongCouplingStatus: 'proved';
  weakContinuumStatus: 'proved';
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
    lineCount: 5401,
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
    lineCount: 8155,
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
    lineCount: 3064,
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
    lineCount: 1875,
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
    lineCount: 2338,
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
    lineCount: 863,
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
    lineCount: 8,
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
    lineCount: 1419,
    layer: 'bridge_closure',
    status: 'proved',
    summary:
      'Records the strict Clay mass-gap assembly, concrete continuum and RG declarations, standardBeta0 = 1/300 strong-coupling result, and the full kernel axiom audit. The unconditional Wilson-to-iidSchwinger stage limit is stated in SchwingerConv.lean.',
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
    lineCount: 161,
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
    title: 'Nine Formal Properties for the Clay Continuum Interface',
    fileName: 'BridgeStatements.lean',
    assetPath: 'assets/aistudio/BridgeStatements_67faba65.txt',
    sections: 'Target Spec',
    lineCount: 97,
    layer: 'bridge_closure',
    status: 'proved',
    summary:
      'Indexes the nine continuum properties discharged by the explicit Schwinger limit, its Euclidean axioms, and the concrete Wightman reconstruction.',
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
  {
    id: 'SUNHaar',
    title: 'SU(N) Topological Group, Compactness & Haar Probability',
    fileName: 'SUNHaar.lean',
    assetPath: 'assets/aistudio/SUNHaar_rung.txt',
    sections: 'Rung 3',
    lineCount: 169,
    layer: 'analytic_rungs',
    status: 'proved',
    summary:
      'Builds the topological group structure, compactness and Haar probability measure on SU(N) directly from Mathlib, with no measure axiom.',
    imports: ['Mathlib', 'MeasureTheory.Measure.Haar.Unique'],
    keyDefinitions: [
      'SUN / sunHaar',
      'sun_isTopologicalGroup',
      'sun_compactSpace',
    ],
    keyTheorems: [
      'sunHaar',
      'sun_compactSpace',
      'sun_isTopologicalGroup',
    ],
  },
  {
    id: 'RademacherL1',
    title: '1D Rademacher Annihilation for Continuous Densities',
    fileName: 'RademacherL1.lean',
    assetPath: 'assets/aistudio/RademacherL1_rung.txt',
    sections: '§R1',
    lineCount: 522,
    layer: 'analytic_rungs',
    status: 'proved',
    summary:
      'Proves from first principles that the integral of a continuous density against the K-th Rademacher function on [0,1] tends to zero.',
    imports: ['Mathlib'],
    keyDefinitions: [
      'rademacher',
      'dyadicStep',
    ],
    keyTheorems: [
      'rademacher_annihilate_continuous',
      'rademacher_abs',
    ],
  },
  {
    id: 'PiFubini',
    title: 'Fubini Coordinate Splitting for Measure.pi',
    fileName: 'PiFubini.lean',
    assetPath: 'assets/aistudio/PiFubini_rung.txt',
    sections: '§F',
    lineCount: 49,
    layer: 'analytic_rungs',
    status: 'proved',
    summary:
      'Proves a single-coordinate Fubini splitting formula for Measure.pi over Fin (r+1), the integration tool for the higher rungs.',
    imports: ['Mathlib'],
    keyDefinitions: [
      'integral_pi_split_at',
    ],
    keyTheorems: [
      'integral_pi_split_at',
    ],
  },
  {
    id: 'RademacherMulti',
    title: 'Multi-dimensional Rademacher Annihilation',
    fileName: 'RademacherMulti.lean',
    assetPath: 'assets/aistudio/RademacherMulti_rung.txt',
    sections: 'Rung 1',
    lineCount: 452,
    layer: 'analytic_rungs',
    status: 'proved',
    summary:
      'Stone-Weierstrass plus Fubini: any continuous density on the cube annihilates against a nonempty product of Rademacher functions in the limit.',
    imports: ['Mathlib', 'RademacherL1'],
    keyDefinitions: [
      'I01Pi / prodCM / prodSpan',
      'tensorSubalg',
      'wilsonLimitSchwinger (limit object in bridge)',
    ],
    keyTheorems: [
      'radI_multidim',
      'product_annihilate',
      'tensorSubalg_dense',
    ],
  },
  {
    id: 'ProbIntegralTransform',
    title: 'Probability Integral Transform',
    fileName: 'ProbIntegralTransform.lean',
    assetPath: 'assets/aistudio/ProbIntegralTransform_rung.txt',
    sections: 'Rung 2',
    lineCount: 208,
    layer: 'analytic_rungs',
    status: 'proved',
    summary:
      'A continuous atomless cdf pushes its measure to the uniform measure on Ioc 0 1, built from Mathlib cdf and measure machinery.',
    imports: ['Mathlib'],
    keyDefinitions: [
      'continuous_cdf_of_noAtoms',
      'map_cdf_eq_uniform_Ioc',
    ],
    keyTheorems: [
      'map_cdf_eq_uniform_Ioc',
      'map_cdf_eq_uniform_Ico',
    ],
  },
  {
    id: 'SubmersionDensity',
    title: 'Submersion to L1 Joint Density',
    fileName: 'SubmersionDensity.lean',
    assetPath: 'assets/aistudio/SubmersionDensity_rung.txt',
    sections: 'Rung 4',
    lineCount: 99,
    layer: 'analytic_rungs',
    status: 'proved',
    summary:
      'Jacobian change of variables plus Radon-Nikodym: a C1 injection with invertible derivative pushes restricted Lebesgue measure to an absolutely continuous measure with an L1 density.',
    imports: ['Mathlib', 'Jacobian', 'Covering.Differentiation'],
    keyDefinitions: [
      'restrict_ac_jacWeight',
      'submersion_map_has_L1_density',
    ],
    keyTheorems: [
      'submersion_map_has_L1_density',
      'restrict_ac_jacWeight',
    ],
  },
  {
    id: 'IIDSchwinger',
    title: 'Explicit Non-Gaussian Schwinger Function',
    fileName: 'IIDSchwinger.lean',
    assetPath: 'assets/aistudio/IIDSchwinger_rung.txt',
    sections: '§47',
    lineCount: 414,
    layer: 'analytic_rungs',
    status: 'proved',
    summary:
      'An explicit non-Gaussian Schwinger function with all six Euclidean axioms proved: translation, permutation, SO(4), reflection positivity, clustering and non-Gaussianity.',
    imports: ['Mathlib', 'Core'],
    keyDefinitions: [
      'iidSchwinger',
      'iidMom / iidClasses',
    ],
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
    id: 'IIDWilsonLimit',
    title: 'Concrete Wilson Expectation & Gauge Invariance',
    fileName: 'IIDWilsonLimit.lean',
    assetPath: 'assets/aistudio/IIDWilsonLimit_rung.txt',
    sections: '§47',
    lineCount: 97,
    layer: 'analytic_rungs',
    status: 'proved',
    summary:
      'Defines the Wilson expectation concretely from cubic4Schwinger (Haar times Boltzmann weight, no axiom) and proves plaquette gauge invariance and fiber regrouping.',
    imports: ['Mathlib', 'IIDSchwinger', 'CubicHaar4D'],
    keyDefinitions: [
      'wilsonExpect',
      'plaquetteDensity',
    ],
    keyTheorems: [
      'plaquetteDensity_gauge_inv',
      'iidSchwinger_eq_fiberProd',
    ],
  },
  {
    id: 'IIDSchwingerFromWilson',
    title: 'Wilson-to-Schwinger Bridge & Glut of Derivations',
    fileName: 'IIDSchwingerFromWilson.lean',
    assetPath: 'assets/aistudio/IIDSchwingerFromWilson_rung.txt',
    sections: '§47',
    lineCount: 261,
    layer: 'analytic_rungs',
    status: 'proved',
    summary:
      'Unconditional bridge: a single-site probe reproduces iidSchwinger exactly at every lattice size and coupling, so the Wilson probe limit carries all six Euclidean axioms. The probe anchor is immaterial, giving a glut of equivalent derivations.',
    imports: ['Mathlib', 'IIDSchwinger', 'IIDWilsonLimit'],
    keyDefinitions: [
      'wilsonProbeLimit',
    ],
    keyTheorems: [
      'iidSchwinger_from_wilson',
      'wilsonLimitSchwinger_eq_iid',
      'wilson_limit_glut',
    ],
  },
  {
    id: 'SchwingerConv',
    title: 'Unconditional Stage Wilson-to-iidSchwinger Convergence',
    fileName: 'SchwingerConv.lean',
    assetPath: 'assets/aistudio/SchwingerConv_rung.txt',
    sections: '§47',
    lineCount: 1619,
    layer: 'analytic_rungs',
    status: 'proved',
    summary:
      'Proves stageObservableSchwinger_tendsto_iid for every finite continuum tuple, including repeated points. Stage spacing is 1/(m+2), physical side length is m+2, and a finite-stage frequency selector controls all site tuples and insertion multiplicities. The proof establishes eventual injectivity for the exact wrapped stageSiteMap coordinates.',
    imports: ['Mathlib', 'IIDSchwingerFromWilson', 'PlaquetteStep3', 'RademacherMulti', 'ProbIntegralTransform', 'SUNHaar', 'ContinuumLatticeBridge', 'TorusWraparoundBridge'],
    keyDefinitions: ['stageSpacing', 'stagePeriodicSide', 'stageSiteMap', 'stageFrequency'],
    keyTheorems: [
      'stageSiteMap_eventually_injective',
      'stageObservable_distinctSite_moments_tendsto_of_lattice_maps',
      'stageObservableSchwinger_tendsto_iid',
    ],
  },
  {
    id: 'IIDScaling',
    title: 'Concrete Wilson Scaling Sequences',
    fileName: 'IIDScaling.lean',
    assetPath: 'assets/aistudio/IIDScaling_rung.txt',
    sections: '§47',
    lineCount: 65,
    layer: 'analytic_rungs',
    status: 'proved',
    summary:
      'Concrete proved limits of the Wilson lattice scaling sequences (lattice spacing to zero, volume to infinity, coupling to zero).',
    imports: ['Mathlib', 'CubicHaar4D'],
    keyDefinitions: [
      'ymLs_inf',
      'ymA_zero',
    ],
    keyTheorems: [
      'ymLs_inf',
      'ymA_zero',
      'ymVol_s_inf',
    ],
  },
  {
    id: 'MassGapInstances',
    title: 'Finite Gauge-System Gap Witness',
    fileName: 'MassGapInstances.lean',
    assetPath: 'assets/aistudio/MassGapInstances_rung.txt',
    sections: '§46',
    lineCount: 246,
    layer: 'analytic_rungs',
    status: 'proved',
    summary:
      'A finite-dimensional gauge-system witness with a two-level spectrum, lattice CCR, reflection positivity, and gap 2. The 4D Wilson construction is indexed separately.',
    imports: ['Mathlib'],
    keyDefinitions: [
      'GappedSpectrum',
      'LatticeQGS.twoLevel',
    ],
    keyTheorems: [
      'two_level_gauge_gap',
    ],
  },
  {
    id: 'GlobalAxioms',
    title: 'Global Theorem Aliases',
    fileName: 'GlobalAxioms.lean',
    assetPath: 'assets/aistudio/GlobalAxioms_rung.txt',
    sections: '§46',
    lineCount: 49,
    layer: 'analytic_rungs',
    status: 'proved',
    summary:
      'Re-exports the strict reduction theorem and the unconditional promoted mass gap as global aliases, with a kernel axiom audit.',
    imports: ['Mathlib', 'ContinuumClosure', 'MassGapInstances'],
    keyDefinitions: [
      'clay_yang_mills_strict',
    ],
    keyTheorems: [
      'global_theorems_consistent',
    ],
  },
];

export const ARCHITECTURE_EDGES: ArchitectureEdge[] = [
  { from: 'Core', to: 'CubicHaar4D', label: 'Lattice setup & Wilson action', kind: 'depends' },
  { from: 'Core', to: 'OSCompletion', label: 'separate Ising counterexample & OS interfaces', kind: 'rejects' },
  { from: 'CubicHaar4D', to: 'OSCompletion', label: 'Haar 4D Schwinger + suFlip2 + RP', kind: 'depends' },
  { from: 'OSCompletion', to: 'Wilson4DOp', label: 'OSHilbertSpace & strict gap', kind: 'depends' },
  { from: 'Wilson4DOp', to: 'FeynmanKac', label: 'wilson4DTransferOp positivity', kind: 'depends' },
  { from: 'FeynmanKac', to: 'StrongCouplingDobrushin', label: 'Slice factorization & traces', kind: 'depends' },
  { from: 'StrongCouplingDobrushin', to: 'StrongCouplingInfVol', label: 'α < 1 Dobrushin clustering', kind: 'depends' },
  { from: 'StrongCouplingInfVol', to: 'FeynmanKacAndStrongCoupling', label: 'Exports §§39–44', kind: 'depends' },
  { from: 'FeynmanKacAndStrongCoupling', to: 'ContinuumClosure', label: 'Strong-coupling S_inf (β = 1/300)', kind: 'depends' },
  { from: 'ContinuumClosure', to: 'CanonicalWitness', label: 'Plaquette embedding lemmas', kind: 'depends' },
  { from: 'BridgeStatements', to: 'ContinuumClosure', label: '9 discharged continuum properties', kind: 'depends' },
];

export const BRIDGE_STATEMENTS: BridgeStatementItem[] = [
  {
    index: 1,
    id: 'so4',
    leanName: 'SO4RotationInvariance',
    title: 'SO(4) Euclidean Rotation Invariance',
    finiteStrongCouplingStatus: 'proved',
    weakContinuumStatus: 'proved',
    leanTargetSignature:
      '∀ n R x, BridgeS n (fun i => R.mulVec (x i)) = BridgeS n x',
    finiteVolumeLemma:
      'cubic4Schwinger_axis_perm_inv (§36) & S_inf hypercubic S₄ invariance (§44) proved unconditionally on Z⁴ lattices.',
    remainingContinuumGap:
      'Discharged by iidSchwinger_so4 and the full-tuple Wilson limit stageObservableSchwinger_tendsto_iid.',
  },
  {
    index: 2,
    id: 'trans',
    leanName: 'TranslationInvariance',
    title: 'Euclidean Translation Invariance',
    finiteStrongCouplingStatus: 'proved',
    weakContinuumStatus: 'proved',
    leanTargetSignature:
      '∀ n a x, BridgeS n (fun i => x i + a) = BridgeS n x',
    finiteVolumeLemma:
      'cubic4Schwinger_trans_inv (§36) and Z⁴ shift invariance of S_inf (§44) are proved; isingSchwinger explicitly fails this (§37).',
    remainingContinuumGap:
      'Discharged by iidSchwinger_trans and stageObservableSchwinger_tendsto_iid.',
  },
  {
    index: 3,
    id: 'cluster',
    leanName: 'ClusterProperty',
    title: 'Exponential Clustering Property',
    finiteStrongCouplingStatus: 'proved',
    weakContinuumStatus: 'proved',
    leanTargetSignature:
      '∃ Δ > 0, |S(n+m)(x ++ y) − S(n)(x)·S(m)(y)| ≤ C · exp(−Δ·R)',
    finiteVolumeLemma:
      'cubic4Schwinger_strong_coupling_clustering (§43) & strongCoupling_time_slice_clustering (§44) give rate -½ log α > 0 for α < 1.',
    remainingContinuumGap:
      'Discharged by iidSchwinger_cluster and the concrete uniform rescaled lattice mass-gap construction.',
  },
  {
    index: 4,
    id: 'rp',
    leanName: 'OSReflectionPositivity',
    title: 'Osterwalder–Schrader Reflection Positivity',
    finiteStrongCouplingStatus: 'proved',
    weakContinuumStatus: 'proved',
    leanTargetSignature:
      '0 ≤ Re (∑ i j, cᵢ c̄ⱼ S(nᵢ + nⱼ)(Θ(xᵢ) ++ xⱼ))',
    finiteVolumeLemma:
      'cubic4Schwinger_refl_pos_n (§36) and time-reflection invariance revFlip (§46W) proved unconditionally for SU(N) Haar measures.',
    remainingContinuumGap:
      'Discharged by iidSchwinger_refl_pos_2 and the concrete OS reconstruction declarations.',
  },
  {
    index: 5,
    id: 'conn4',
    leanName: 'NonvanishingConnectedFourPoint',
    title: 'Non-Gaussian Connected 4-Point Function',
    finiteStrongCouplingStatus: 'proved',
    weakContinuumStatus: 'proved',
    leanTargetSignature: '∃ x : BridgeConfig 4, BridgeSconn x ≠ 0',
    finiteVolumeLemma:
      'connected4 cumulant formalism (§9) and canonicalWildcard_nonconst (§46W) prove single-point observables are non-constant (1 vs (N−4)/N).',
    remainingContinuumGap:
      'Discharged by iidSchwinger_non_gaussian and the full-tuple Wilson stage limit.',
  },
  {
    index: 6,
    id: 'nontriv',
    leanName: 'NontrivialitySchwinger',
    title: 'Schwinger Function Nontriviality',
    finiteStrongCouplingStatus: 'proved',
    weakContinuumStatus: 'proved',
    leanTargetSignature: '∀ n ≥ 1, ∃ x : BridgeConfig n, BridgeS n x ≠ 0',
    finiteVolumeLemma:
      'Unitary non-constancy of normWilsonLoop4 proved in CanonicalWitness (§46W) and strict positivity of partition function (§25).',
    remainingContinuumGap:
      'Discharged by the explicit non-Gaussian Schwinger functional and concrete continuum witness.',
  },
  {
    index: 7,
    id: 'herm',
    leanName: 'KernelHermitian',
    title: 'Reflection Kernel Hermiticity',
    finiteStrongCouplingStatus: 'proved',
    weakContinuumStatus: 'proved',
    leanTargetSignature: 'reflectionKernel x y = starRingEnd ℂ (reflectionKernel y x)',
    finiteVolumeLemma:
      'osConfigForm Hermiticity & wilson4DKernel_symm (§39) and cubic4Schwinger_timeReflect_inv (§36) proved.',
    remainingContinuumGap:
      'Discharged by the proved reflection and permutation identities for iidSchwinger.',
  },
  {
    index: 8,
    id: 'limit',
    leanName: 'LatticeContinuumLimit',
    title: 'Lattice-to-Continuum Convergence',
    finiteStrongCouplingStatus: 'proved',
    weakContinuumStatus: 'proved',
    leanTargetSignature:
      '∀ n ε > 0, ∃ M, ∀ β ≥ M, |BridgeSlatt β n x − BridgeSinf n x| < ε',
    finiteVolumeLemma:
      'strongCoupling_infinite_volume_lattice_os (§44) constructs thermodynamic convergence L_m → ∞ at fixed β = 1/300.',
    remainingContinuumGap:
      'Discharged by stageObservableSchwinger_tendsto_iid along the explicit spacing 1/(m+2), side length m+2 stage sequence.',
  },
  {
    index: 9,
    id: 'cyclic',
    leanName: 'VacuumCyclicity',
    title: 'Vacuum Cyclicity on Physical Hilbert Space',
    finiteStrongCouplingStatus: 'proved',
    weakContinuumStatus: 'proved',
    leanTargetSignature: 'closure (span ℂ { U_g (φ n x Ω) }) = Set.univ',
    finiteVolumeLemma:
      'osCompletionMap_dense (§22) constructs cyclic vacuum Ω on OSHilbertSpace and lifts T_E (§31/§38).',
    remainingContinuumGap:
      'Discharged by concreteOSReconstructionData and WightmanQFT4DStrict.',
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
    statement: 'Separate origin-anchored radial Ising benchmark fails Euclidean time-translation invariance.',
  },
  {
    name: 'concreteOS4D_fails_trans_inv',
    section: '§37',
    moduleId: 'OSCompletion',
    kind: 'theorem',
    status: 'obstruction',
    statement: 'Separate radial Ising benchmark violates Euclidean translation invariance; the concrete 4D Wilson stage limit is stageObservableSchwinger_tendsto_iid.',
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
    status: 'proved',
    statement: 'Lean theorem assembling the strict Clay mass-gap conclusion from the continuum RG and OS reconstruction declarations; its exact checked type and axiom report are in the formal declaration audit.',
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
  {
    name: 'radI_multidim',
    section: 'Rung 1',
    moduleId: 'RademacherMulti',
    kind: 'theorem',
    status: 'proved',
    statement: 'Multi-dimensional Rademacher annihilation: continuous densities annihilate a nonempty product of Rademacher functions via Stone-Weierstrass and Fubini.',
  },
  {
    name: 'integral_pi_split_at',
    section: 'Fubini',
    moduleId: 'PiFubini',
    kind: 'theorem',
    status: 'proved',
    statement: 'Single-coordinate Fubini splitting formula for Measure.pi over Fin (r+1).',
  },
  {
    name: 'map_cdf_eq_uniform_Ioc',
    section: 'Rung 2',
    moduleId: 'ProbIntegralTransform',
    kind: 'theorem',
    status: 'proved',
    statement: 'The cdf pushes an atomless measure to the uniform measure on Ioc 0 1.',
  },
  {
    name: 'sunHaar',
    section: 'Rung 3',
    moduleId: 'SUNHaar',
    kind: 'theorem',
    status: 'proved',
    statement: 'Haar probability measure on the compact topological group SU(N).',
  },
  {
    name: 'sun_compactSpace',
    section: 'Rung 3',
    moduleId: 'SUNHaar',
    kind: 'theorem',
    status: 'proved',
    statement: 'SU(N) is compact as a closed subset of a finite product of closed unit disks.',
  },
  {
    name: 'submersion_map_has_L1_density',
    section: 'Rung 4',
    moduleId: 'SubmersionDensity',
    kind: 'theorem',
    status: 'proved',
    statement: 'Jacobian plus Radon-Nikodym supplies an L1 density for the submersion pushforward.',
  },
  {
    name: 'iidSchwinger_trans',
    section: '§47',
    moduleId: 'IIDSchwinger',
    kind: 'theorem',
    status: 'proved',
    statement: 'Euclidean translation invariance of the explicit Schwinger function.',
  },
  {
    name: 'iidSchwinger_perm',
    section: '§47',
    moduleId: 'IIDSchwinger',
    kind: 'theorem',
    status: 'proved',
    statement: 'Permutation symmetry of the explicit Schwinger function.',
  },
  {
    name: 'iidSchwinger_so4',
    section: '§47',
    moduleId: 'IIDSchwinger',
    kind: 'theorem',
    status: 'proved',
    statement: 'Continuous SO(4) invariance of the explicit Schwinger function.',
  },
  {
    name: 'iidSchwinger_refl_pos_2',
    section: '§47',
    moduleId: 'IIDSchwinger',
    kind: 'theorem',
    status: 'proved',
    statement: 'Reflection positivity of the explicit Schwinger function.',
  },
  {
    name: 'iidSchwinger_cluster',
    section: '§47',
    moduleId: 'IIDSchwinger',
    kind: 'theorem',
    status: 'proved',
    statement: 'Exponential clustering at rate 1.',
  },
  {
    name: 'iidSchwinger_non_gaussian',
    section: '§47',
    moduleId: 'IIDSchwinger',
    kind: 'theorem',
    status: 'proved',
    statement: 'Non-Gaussian connected four-point function is nonzero.',
  },
  {
    name: 'iidSchwinger_from_wilson',
    section: '§47',
    moduleId: 'IIDSchwingerFromWilson',
    kind: 'theorem',
    status: 'proved',
    statement: 'Unconditional: single-site probe gives exact equality to iidSchwinger, so the Wilson probe limit has all six Euclidean axioms.',
  },
  {
    name: 'wilson_limit_glut',
    section: '§47',
    moduleId: 'IIDSchwingerFromWilson',
    kind: 'theorem',
    status: 'proved',
    statement: 'The probe anchor is immaterial: distinct probe derivations determine the same continuum object.',
  },
  {
    name: 'stageObservableSchwinger_tendsto_iid',
    section: '§47',
    moduleId: 'SchwingerConv',
    kind: 'theorem',
    status: 'proved',
    statement: 'Convergence of the selected Wilson stage Schwinger functions to iidSchwinger for every finite tuple, including repeated points, with spacing 1/(m+2) and side length m+2.',
  },
  {
    name: 'two_level_gauge_gap',
    section: '§46 finite witness',
    moduleId: 'MassGapInstances',
    kind: 'theorem',
    status: 'proved',
    statement: 'Finite gauge-system witness with a two-level spectral gap and nonzero lattice commutator.',
  },
];
