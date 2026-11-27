export type EleganceTheme =
  | 'Symmetry & Functoriality'
  | 'Hilbert & Operator Theory'
  | 'Measure & Probability'
  | 'Gauge Algebra & Lean Craft';

export interface ElegantProofGem {
  id: string;
  code: string;
  theme: EleganceTheme;
  title: string;
  declaration: string;
  moduleId: string;
  line: number;
  lineSpan: string;
  coreInsight: string;
  contrastWithBruteForce: string;
  payoff: string;
  leanExcerpt: string;
}

export const ELEGANT_PROOFS: ElegantProofGem[] = [
  {
    id: 'e1-injective-partition',
    code: 'E1',
    theme: 'Symmetry & Functoriality',
    title: 'One Injective Functor Lemma Proves Every Euclidean Symmetry',
    declaration: 'YangMills.iidSchwinger_map & iidSchwinger_so4',
    moduleId: 'IIDSchwinger',
    line: 49,
    lineSpan: 'L37–L85, L401',
    coreInsight:
      'Any injective map g : Space4 → Space4 preserves equality classes iidClasses(g ∘ xs) = iidClasses(xs) identically.',
    contrastWithBruteForce:
      'Rather than writing separate measure-jacobian or combinatorial invariance proofs for ℝ⁴ translations, continuous SO(4) rotations, Euclidean time-reflection θ, and coordinate permutations, all four reduce to proving injectivity in 2–4 lines.',
    payoff:
      'Unifies translation, continuous SO(4), time-reflection, and Fin n permutation invariance under a single 15-line lemma.',
    leanExcerpt: `lemma iidClasses_map {n : ℕ} (xs : Fin n → Space4) (g : Space4 → Space4)
    (hg : Function.Injective g) :
    iidClasses (fun i => g (xs i)) = iidClasses xs := by
  unfold iidClasses; congr 1; funext i; ext j
  simp only [Finset.mem_filter, Finset.mem_univ, true_and]
  exact ⟨fun h => hg h, fun h => congrArg g h⟩`,
  },
  {
    id: 'e2-npoint-rp-normsq',
    code: 'E2',
    theme: 'Symmetry & Functoriality',
    title: 'Full n-Point Reflection Positivity Collapsed to ‖∑ Aᵢ‖² ≥ 0',
    declaration: 'YangMills.iidSchwinger_refl_pos_n',
    moduleId: 'IIDOS',
    line: 59,
    lineSpan: 'L59–L110',
    coreInsight:
      'Because x₀ > 0 and y₀ > 0 imply θ(x) ≠ y, the OS matrix kernel S(θ xᵢ ++ xⱼ) factors as S(θ xᵢ) · S(xⱼ).',
    contrastWithBruteForce:
      'Instead of expanding arbitrary-arity partition matrices or invoking Bochner–Minlos spectral representations, time-reflection conjugacy turns the entire double sum ∑ᵢⱼ cᵢ c̄ⱼ S(θ xᵢ ++ xⱼ) directly into Z · Z̄ = normSq(∑ᵢ Aᵢ).',
    payoff:
      'Proves full Osterwalder–Schrader reflection positivity across arbitrary finite multiplicities in one complex-norm identity.',
    leanExcerpt: `simp_rw [iidSchwinger_append _ _ (fun k l => hdisc _ _ k l)]
let A : Fin m → ℂ := fun i =>
  c i * iidSchwinger (n_pts i) (fun k => euclidTimeReflect (xs i k))
-- double sum rewrites to (∑ i, A i) * starRingEnd ℂ (∑ i, A i)
rw [Complex.mul_conj]; exact Complex.normSq_nonneg _`,
  },
  {
    id: 'e3-rank-one-collapse',
    code: 'E3',
    theme: 'Hilbert & Operator Theory',
    title: 'Zero-Minor Kernel Factorization & 10-Line Rank-1 Hilbert Collapse',
    declaration: 'YangMills.iid_osConfigVector_eq & iid_osCompletionMap_rank_one',
    moduleId: 'IIDPoincareContinuation',
    line: 26,
    lineSpan: 'L10–L129',
    coreInsight:
      'Applying ‖ψ - s·Ω‖² = ‖ψ‖² - 2 Re⟨ψ, s·Ω⟩ + ‖s·Ω‖² = s² - 2s² + s² = 0 collapses every configuration vector onto c·Ω.',
    contrastWithBruteForce:
      'Instead of quotienting Finsupp formal sums by null-space determinants row by row, computing ⟪ψ - s·Ω, ψ - s·Ω⟫ = 0 via inner-product bilinearity forces ψ = s·Ω globally via Finsupp.induction_linear.',
    payoff:
      'Discharges OSPoincareContinuationHypothesis unconditionally with canonical unitary U = id and field φ = id.',
    leanExcerpt: `have hnorm : ‖ψ - s • Ω‖ ^ 2 = 0 := by
  rw [norm_sub_sq (𝕜 := ℂ)]
  ...
  rw [hψnorm, hcross', hnormΩ, hs_abs]
  ring
exact sub_eq_zero.mp (norm_eq_zero.mp (by nlinarith))`,
  },
  {
    id: 'e4-slope-squeeze-gap',
    code: 'E4',
    theme: 'Hilbert & Operator Theory',
    title: 'Calculus Slope Squeeze: Semigroup Decay → Unbounded Generator Gap',
    declaration: 'Imscribing.YangMills.SemigroupGapBridge.generator_gap_of_semigroup_decay',
    moduleId: 'SemigroupGapBridge',
    line: 63,
    lineSpan: 'L63–L126',
    coreInsight:
      'Differential quotient ((1 - e^{-Δt})/t)‖ψ‖² ≤ Re⟨ψ, (ψ - T(t)ψ)/t⟩ bridges bounded semigroup contraction to unbounded H as t → 0⁺.',
    contrastWithBruteForce:
      'Avoids spectral resolution of unbounded self-adjoint operators (Stone/Hille–Yosida measure theory) by differentiating e^{-Δt} directly at 0 via Mathlib’s HasDerivAt.tendsto_slope_zero_right and squeezing.',
    payoff:
      'Establishes Δ‖ψ‖² ≤ Re⟨ψ, Hψ⟩ and vacuum uniqueness for every domain vector ψ ⊥ Ω in 63 lines.',
    leanExcerpt: `have h_ineq : ∀ᶠ t : ℝ in 𝓝[>] 0,
    ((1 - Real.exp (-Δ * t)) / t) * ‖ψ‖ ^ 2 ≤
      (⟪ψ, (t⁻¹ : ℂ) • (ψ - T t ψ)⟫_ℂ).re := by ...
have h_deriv : HasDerivAt (fun t : ℝ => Real.exp (-Δ * t)) (-Δ) 0 := ...
exact le_of_tendsto_of_tendsto h_lhs_tend h_rhs_tend h_ineq`,
  },
  {
    id: 'e5-pit-wilson-moments',
    code: 'E5',
    theme: 'Measure & Probability',
    title: 'Probability Integral Transform on Curved SU(N) → Exact Moments (1ᵏ+2ᵏ)/2',
    declaration: 'YangMills.stageObservable_moment & stageObservable_not_ae_constant',
    moduleId: 'SchwingerConv',
    line: 1552,
    lineSpan: 'L1039, L1552–L1743',
    coreInsight:
      'Composing gauge-invariant plaquette traces with their own Wilson CDF pushes any smooth SU(N) density to Lebesgue[0,1].',
    contrastWithBruteForce:
      'Evaluating non-Abelian character expansions in closed form for arbitrary N ≥ 2 is intractable; pushing forward via the probability integral transform makes every moment (1ᵏ + 2ᵏ)/2 exact and universal across all N ≥ 2, immediately showing (3/2)² ≠ 5/2.',
    payoff:
      'Proves non-constancy a.e. (Var = 1/4 > 0), exact gauge invariance, and exact multi-point convergence to S₄ᶜ = -1/8.',
    leanExcerpt: `-- ∫ O_m^k dμ_Wilson = (1^k + 2^k) / 2  (k=1 ↦ 3/2, k=2 ↦ 5/2)
-- If O_m =ᵐ[μ] c then c = E[O_m] = 3/2, so E[O_m²] = c² = 9/4,
-- contradicting E[O_m²] = 5/2 (since 9/4 ≠ 5/2).`,
  },
  {
    id: 'e6-suflip2-tailfree',
    code: 'E6',
    theme: 'Gauge Algebra & Lean Craft',
    title: 'Uniform Determinant-1 Matrix Flip diag(-1, -1, 1, …, 1) ∀ N ≥ 2',
    declaration: 'YangMills.canonicalWildcard_nonconst',
    moduleId: 'CanonicalWitness',
    line: 128,
    lineSpan: 'L49–L157',
    coreInsight:
      'Flipping exactly two diagonal entries gives det = (-1)(-1) = +1 ∈ SU(N) for every rank N ≥ 2 while isolating one link.',
    contrastWithBruteForce:
      'Center elements e^{2πi/N}·I depend on roots of unity and vary phase with N; suFlip2 works uniformly over all N ≥ 2 without complex roots, while tail_links_ne_base isolates the base link so holonomy evaluates strictly to 1 vs (N-4)/N.',
    payoff:
      'Refutes observable constancy on explicit 4D Wilson gauge fields for all N ≥ 2 and L ≥ 2 in one short ring/linarith finish.',
    leanExcerpt: `noncomputable def witnessFieldFlip (N : ℕ) (hN : 2 ≤ N) (L : ℕ) [NeZero L] (x : Space4) :
    GaugeField (cubicTorus4 L L) (SU N) := fun e =>
  if e = ((projSite4 L (fun i => ⌊x i⌋), 1)) then suFlip2 N hN else 1
-- hv1 : normWilsonLoop4 ... witnessFieldOne  = 1
-- hv2 : normWilsonLoop4 ... witnessFieldFlip = (N - 4) / N  ⇒  1 ≠ (N-4)/N`,
  },
  {
    id: 'e7-center-slice-cancel',
    code: 'E7',
    theme: 'Gauge Algebra & Lean Craft',
    title: 'Measure-Preserving Center-Slice Flip Leaving Wilson Action Identical',
    declaration: 'YangMills.SUClosure.wilsonAction_sliceCenterFlip',
    moduleId: 'SUClosure',
    line: 602,
    lineSpan: 'L570–L625',
    coreInsight:
      'Multiplying a single spatial-slice coordinate direction by central z = e^{2πi/N}·I commutes through every plaquette to z·z⁻¹ = 1.',
    contrastWithBruteForce:
      'In curved non-Abelian lattice integrals, symmetry cancellation usually fails under ordering; placing z in Z(SU(N)) lets z slide past adjacent link matrices A, B, C⁻¹ inside every plaquette while Haar translation preserves the product measure.',
    payoff:
      'Generates an exact symmetry of the 4D Wilson kernel enabling spectral isolation along β_m = exp((m+1)⁴).',
    leanExcerpt: `calc (z * A) * (B * (C⁻¹ * z⁻¹ * (D * 1)))
    = z * (A * (((B * C⁻¹) * z⁻¹) * (D * 1))) := by simp only [mul_assoc]
  _ = z * (A * ((z⁻¹ * (B * C⁻¹)) * (D * 1))) := by rw [hc_inv (B * C⁻¹)]
  _ = (z * z⁻¹) * (A * (B * (C⁻¹ * (D * 1)))) := by ...`,
  },
  {
    id: 'e8-borel-transport',
    code: 'E8',
    theme: 'Gauge Algebra & Lean Craft',
    title: 'Zero-Friction Borel Typeclass Unification Across Arbitrary SU(N) Instances',
    declaration: 'GlobalAxioms.unconditional_balaban_hypothesis',
    moduleId: 'GlobalAxioms',
    line: 35,
    lineSpan: 'L17–L72',
    coreInsight:
      'Two BorelSpace instances on the same TopologicalSpace share Borel sets: rw [instB.measurable_eq, (canonSUBorel N).measurable_eq]; subst h_eq.',
    contrastWithBruteForce:
      'Dependent type theory normally traps downstream users when [MeasurableSpace] diamonds differ between modules. Equating instM = canonSUMeas N via BorelSpace.measurable_eq transports the entire 106-module proof across arbitrary instances cleanly.',
    payoff:
      'Lets global theorems quantify over completely unconstrained [MeasurableSpace] [BorelSpace] typeclasses with zero friction.',
    leanExcerpt: `noncomputable def unconditional_balaban_hypothesis (N : ℕ) (hN : 2 ≤ N)
    [instM : MeasurableSpace (SU N)] [instB : BorelSpace (SU N)] :
    BalabanRGContinuumHypothesis N hN := by
  have h_eq : instM = canonSUMeas N := by
    rw [instB.measurable_eq, (canonSUBorel N).measurable_eq]
  subst h_eq
  exact YangMills.iidBalabanHypothesis N hN`,
  },
];
