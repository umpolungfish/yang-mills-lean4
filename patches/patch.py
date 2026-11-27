python3 - << 'EOF' && lake env lean -Dtrace.profiler=true -Dtrace.profiler.threshold=500 Imscribing/YangMills/SUClosure.lean
from pathlib import Path

path = Path("Imscribing/YangMills/SUClosure.lean")
text = path.read_text()

patches = [
    # 1. Eliminate slow `simp` in `frobeniusNormSq_su_inv_sub_one` and `frobeniusNormSq_sub_self_su`
    (
        """  have hinv : ((A⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) : Matrix (Fin N) (Fin N) ℂ) *
      (A : Matrix (Fin N) (Fin N) ℂ) = 1 := by
    change ((A⁻¹ * A : Matrix.specialUnitaryGroup (Fin N) ℂ) : Matrix (Fin N) (Fin N) ℂ) = 1
    simp""",
        """  have hinv : ((A⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) : Matrix (Fin N) (Fin N) ℂ) *
      (A : Matrix (Fin N) (Fin N) ℂ) = 1 :=
    congrArg Subtype.val (inv_mul_cancel A)""",
        1,
    ),
    (
        """  have hB : ((B⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) : Matrix (Fin N) (Fin N) ℂ) *
      (B : Matrix (Fin N) (Fin N) ℂ) = 1 := by
    change ((B⁻¹ * B : Matrix.specialUnitaryGroup (Fin N) ℂ) : Matrix (Fin N) (Fin N) ℂ) = 1
    simp""",
        """  have hB : ((B⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) : Matrix (Fin N) (Fin N) ℂ) *
      (B : Matrix (Fin N) (Fin N) ℂ) = 1 :=
    congrArg Subtype.val (inv_mul_cancel B)""",
        1,
    ),
    # 2. Scope `linarith` in `frobeniusNormSq_holonomy4_le`
    (
        """  have h_all := frobeniusNormSq_su_mul_sub_one (A * B) (C⁻¹ * D⁻¹)
  linarith""",
        """  have h_all := frobeniusNormSq_su_mul_sub_one (A * B) (C⁻¹ * D⁻¹)
  linarith only [hAB, hCD, h_all, hA, hB, hC, hD]""",
        1,
    ),
    # 3. Scope `linarith`/`nlinarith` in `suHaar_ball_ge`
    (
        """      refine ⟨?_, ?_⟩
      · have h1 : 2 * ((K - 1 : ℕ) : ℝ) / (K : ℝ) ≤ 2 :=
          (div_le_iff₀ hK_real_pos).mpr (by linarith)
        linarith
      · rw [hm1, mul_div_cancel_right₀ _ hK_real_pos.ne']; linarith
    · have hr_lt : r < 1 := lt_of_le_of_ne hr_hi hr1
      let t : ℝ := (r + 1) * (K : ℝ) / 2
      have hr1_nn : 0 ≤ r + 1 := by linarith
      have ht_nn : 0 ≤ t := by dsimp [t]; positivity
      have ht_lt : t < (K : ℝ) := by
        dsimp [t]
        have : r + 1 < 2 := by linarith
        nlinarith
      let m_nat : ℕ := Nat.floor t
      have hm_lt : m_nat < K := Nat.floor_lt ht_nn |>.mpr (by exact_mod_cast ht_lt)
      refine ⟨⟨m_nat, hm_lt⟩, ?_⟩
      have hm_le : (m_nat : ℝ) ≤ t := Nat.floor_le ht_nn
      have hm_gt : t < (m_nat : ℝ) + 1 := Nat.lt_floor_add_one t
      refine ⟨?_, ?_⟩
      · dsimp [t] at hm_le
        have : 2 * (m_nat : ℝ) / (K : ℝ) ≤ r + 1 := by
          rw [div_le_iff₀ hK_real_pos]; linarith
        linarith
      · dsimp [t] at hm_gt
        have : r + 1 ≤ 2 * ((m_nat : ℝ) + 1) / (K : ℝ) := by
          rw [le_div_iff₀ hK_real_pos]; linarith
        linarith""",
        """      refine ⟨?_, ?_⟩
      · have h1 : 2 * ((K - 1 : ℕ) : ℝ) / (K : ℝ) ≤ 2 :=
          (div_le_iff₀ hK_real_pos).mpr (by linarith only [hm_le])
        linarith only [h1]
      · rw [hm1, mul_div_cancel_right₀ _ hK_real_pos.ne']; linarith only []
    · have hr_lt : r < 1 := lt_of_le_of_ne hr_hi hr1
      let t : ℝ := (r + 1) * (K : ℝ) / 2
      have hr1_nn : 0 ≤ r + 1 := by linarith only [hr_lo]
      have ht_nn : 0 ≤ t := by dsimp [t]; positivity
      have ht_lt : t < (K : ℝ) := by
        dsimp [t]
        have hr2 : r + 1 < 2 := by linarith only [hr_lt]
        nlinarith only [hr2, hK_real_pos]
      let m_nat : ℕ := Nat.floor t
      have hm_lt : m_nat < K := Nat.floor_lt ht_nn |>.mpr (by exact_mod_cast ht_lt)
      refine ⟨⟨m_nat, hm_lt⟩, ?_⟩
      have hm_le : (m_nat : ℝ) ≤ t := Nat.floor_le ht_nn
      have hm_gt : t < (m_nat : ℝ) + 1 := Nat.lt_floor_add_one t
      refine ⟨?_, ?_⟩
      · dsimp [t] at hm_le
        have h2m : 2 * (m_nat : ℝ) / (K : ℝ) ≤ r + 1 := by
          rw [div_le_iff₀ hK_real_pos]; linarith only [hm_le]
        linarith only [h2m]
      · dsimp [t] at hm_gt
        have hr2m : r + 1 ≤ 2 * ((m_nat : ℝ) + 1) / (K : ℝ) := by
          rw [le_div_iff₀ hK_real_pos]; linarith only [hm_gt]
        linarith only [hr2m]""",
        1,
    ),
    (
        """          have hre_diff : |((A : Matrix (Fin N) (Fin N) ℂ) i j).re -
              ((A₀ : Matrix (Fin N) (Fin N) ℂ) i j).re| ≤ 2 / (K : ℝ) := by
            obtain ⟨ha1, ha2⟩ := (hA i j).1
            obtain ⟨hb1, hb2⟩ := (hA₀ i j).1
            rw [abs_le]
            constructor <;> linarith [show 2 * ((b (i, j, 0) : ℝ) + 1) / (K : ℝ) -
                2 * (b (i, j, 0) : ℝ) / (K : ℝ) = 2 / (K : ℝ) by ring]
          have him_diff : |((A : Matrix (Fin N) (Fin N) ℂ) i j).im -
              ((A₀ : Matrix (Fin N) (Fin N) ℂ) i j).im| ≤ 2 / (K : ℝ) := by
            obtain ⟨ha1, ha2⟩ := (hA i j).2
            obtain ⟨hb1, hb2⟩ := (hA₀ i j).2
            rw [abs_le]
            constructor <;> linarith [show 2 * ((b (i, j, 1) : ℝ) + 1) / (K : ℝ) -
                2 * (b (i, j, 1) : ℝ) / (K : ℝ) = 2 / (K : ℝ) by ring]""",
        """          have hre_diff : |((A : Matrix (Fin N) (Fin N) ℂ) i j).re -
              ((A₀ : Matrix (Fin N) (Fin N) ℂ) i j).re| ≤ 2 / (K : ℝ) := by
            obtain ⟨ha1, ha2⟩ := (hA i j).1
            obtain ⟨hb1, hb2⟩ := (hA₀ i j).1
            have hspan : 2 * ((b (i, j, 0) : ℝ) + 1) / (K : ℝ) -
                2 * (b (i, j, 0) : ℝ) / (K : ℝ) = 2 / (K : ℝ) := by ring
            rw [abs_le]
            constructor <;> linarith only [ha1, ha2, hb1, hb2, hspan]
          have him_diff : |((A : Matrix (Fin N) (Fin N) ℂ) i j).im -
              ((A₀ : Matrix (Fin N) (Fin N) ℂ) i j).im| ≤ 2 / (K : ℝ) := by
            obtain ⟨ha1, ha2⟩ := (hA i j).2
            obtain ⟨hb1, hb2⟩ := (hA₀ i j).2
            have hspan : 2 * ((b (i, j, 1) : ℝ) + 1) / (K : ℝ) -
                2 * (b (i, j, 1) : ℝ) / (K : ℝ) = 2 / (K : ℝ) := by ring
            rw [abs_le]
            constructor <;> linarith only [ha1, ha2, hb1, hb2, hspan]""",
        1,
    ),
    (
        """          _ ≤ δ ^ 2 := by linarith [sq_nonneg δ]""",
        """          _ ≤ δ ^ 2 := by linarith only [sq_nonneg δ]""",
        1,
    ),
    (
        """  exact (div_le_iff₀ (pow_pos hK_real_pos _)).mpr (by linarith)""",
        """  exact (div_le_iff₀ (pow_pos hK_real_pos _)).mpr (by linarith only [h_real])""",
        1,
    ),
    (
        """  have hre_eq := congrArg Complex.re heq
  rw [hre, Complex.one_re] at hre_eq
  linarith""",
        """  have hre_eq := congrArg Complex.re heq
  rw [hre, Complex.one_re] at hre_eq
  linarith only [hre_eq, hcos_lt]""",
        1,
    ),
    # 4. Insert `fullRank_dirichlet_eps_bound` & `fullRank_lam0_haar_lb` before `fullRankCubic_gap_upper_bound`
    (
        """/-- **Explicit Spectral-Gap Upper Bound & Convergence to `0` (`0 sorry`):**
    On `fullRankCubicNonAbelianWilsonSetup L N hN β hβ`, as `(L³ log β) / β → 0`
    (with `exp(c L³) / β² → 0`), `S.Δ → 0`. -/
theorem fullRankCubic_gap_upper_bound (L N : ℕ) [NeZero L] (hN : 2 ≤ N)""",
        """private lemma fullRank_dirichlet_eps_bound (L N : ℕ) [NeZero L] [NeZero N] (hN : 2 ≤ N)
    {β : ℝ} (hβ : 1 ≤ β)
    (ω : GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ) → ℝ)
    (hω_cont : Continuous ω) (hω_pos : ∀ U, 0 < ω U) (lam0 : ℝ)
    (h_eig_ω : ∀ U,
      ∫ U', wilsonKernel β (cubicPlaquettes L)
        (wilsonGramKernel L N (cubicLinkKineticKernel L N β)) U U' * ω U'
        ∂(by letI := canonSUMeas N; exact latticeHaarMeasure L N) = lam0 * ω U)
    (hω_sq_int : ∫ U, ω U ^ 2 ∂(by letI := canonSUMeas N; exact latticeHaarMeasure L N) = 1)
    (hω_int1 : ∫ U, ω U ∂(by letI := canonSUMeas N; exact latticeHaarMeasure L N) ≤ 1) :
    letI := canonSUMeas N
    haveI := canonSUBorel N
    let μ := latticeHaarMeasure L N
    let links : ℕ := 3 * L ^ 3
    let ε_sq : ℝ := 4 * (N : ℝ) * ((6 * (N : ℝ) ^ 2 * (links : ℝ) + 2) * Real.log β) / β
    let C_bad : ℝ := 4 * (N : ℝ) * Real.exp (β * (links : ℝ)) *
      β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2))
    let κ := fun U W => cubicWilsonWeight L N β U * cubicLinkKineticKernel L N β U W
    ∫ q : (GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ) ×
        GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)) ×
        GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ),
      κ q.1.1 q.2 * κ q.1.2 q.2 * ω q.1.1 * ω q.1.2 *
        frobeniusNormSq ((q.1.1 ((0, 0, 0), 0) : Matrix (Fin N) (Fin N) ℂ) -
          (q.1.2 ((0, 0, 0), 0) : Matrix (Fin N) (Fin N) ℂ)) ∂((μ.prod μ).prod μ) ≤
      4 * ε_sq * lam0 + C_bad := by
  letI := canonSUMeas N
  haveI := canonSUBorel N
  have hβ_pos : 0 < β := lt_of_lt_of_le zero_lt_one hβ
  have hN_pos : (0 : ℝ) < (N : ℝ) := Nat.cast_pos.mpr (NeZero.pos N)
  let G_L := GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)
  let μ := latticeHaarMeasure L N
  haveI := latticeHaarMeasure_prob L N
  let χ := cubicLinkKineticKernel L N β
  let K_kin := wilsonGramKernel L N χ
  let K_W := wilsonKernel β (cubicPlaquettes L) K_kin
  have hχ_cont := continuous_cubicLinkKineticKernel L N β
  have hχ_nn := linkChi_nn L N hN β hβ_pos.le
  have hχ_bd := fun U W => (cubicLinkKineticKernel_bounds L N (by omega) β hβ_pos.le U W).2
  have hK_cont := continuous_wilsonGramKernel L N χ hχ_cont hχ_nn (linkChiUb L β) (linkChiUb_nonneg L β) hχ_bd
  have hKW_cont : Continuous (Function.uncurry K_W) :=
    continuous_cubicWilsonKernel L N β K_kin hK_cont
  let e₀ : (cubicTorus3 L).Link := ((0, 0, 0), 0)
  let links : ℕ := 3 * L ^ 3
  have h_card_links : Fintype.card (cubicTorus3 L).Link = links := by
    simp [cubicTorus3, links, Fintype.card_prod, Fintype.card_fin]; ring
  have hlinks_pos : 0 < links := by
    have hL_pos : 0 < L := NeZero.pos L
    dsimp [links]; positivity
  let ε_sq : ℝ := 4 * (N : ℝ) * ((6 * (N : ℝ) ^ 2 * (links : ℝ) + 2) * Real.log β) / β
  have hε_nn : 0 ≤ ε_sq := by
    have hlog_nn : 0 ≤ Real.log β := Real.log_nonneg hβ
    dsimp [ε_sq]; positivity
  let κ : G_L → G_L → ℝ := fun U W => cubicWilsonWeight L N β U * χ U W
  have hκ_cont : Continuous (Function.uncurry κ) := by
    have hw : Continuous (cubicWilsonWeight L N β) :=
      Real.continuous_exp.comp (continuous_const.mul (continuous_cubicWilsonAction L N β))
    exact (hw.comp continuous_fst).mul hχ_cont
  have hκ_nn : ∀ U W, 0 ≤ κ U W := fun U W =>
    mul_nonneg (Real.exp_pos _).le (hχ_nn U W)
  have hKW_eq_κ : ∀ U U', K_W U U' = ∫ W, κ U W * κ U' W ∂μ := by
    intro U U'
    have h_exp : Real.exp (-(1 / 2 : ℝ) *
        (wilsonAction β (cubicPlaquettes L) U + wilsonAction β (cubicPlaquettes L) U')) =
        cubicWilsonWeight L N β U * cubicWilsonWeight L N β U' := by
      unfold cubicWilsonWeight
      rw [← Real.exp_add]
      congr 1; ring
    dsimp only [K_W, wilsonKernel, K_kin, wilsonGramKernel]
    rw [h_exp, ← MeasureTheory.integral_const_mul]
    refine MeasureTheory.integral_congr_ae (Filter.Eventually.of_forall fun W => ?_)
    dsimp only [κ]; ring
  have h_mat_diff_cont : ∀ i j : Fin N, Continuous (fun p : G_L × G_L =>
      ((p.1 e₀ : Matrix (Fin N) (Fin N) ℂ) - (p.2 e₀ : Matrix (Fin N) (Fin N) ℂ)) i j) :=
    fun i j => (continuous_apply j).comp ((continuous_apply i).comp
      (((continuous_subtype_val.comp (continuous_apply e₀)).comp continuous_fst).sub
       ((continuous_subtype_val.comp (continuous_apply e₀)).comp continuous_snd)))
  have hω_fst_cont : Continuous (fun p : G_L × G_L => ω p.1) := hω_cont.comp continuous_fst
  have hω_snd_cont : Continuous (fun p : G_L × G_L => ω p.2) := hω_cont.comp continuous_snd
  have hfrob_diff_cont : Continuous (fun p : G_L × G_L =>
      frobeniusNormSq ((p.1 e₀ : Matrix (Fin N) (Fin N) ℂ) -
        (p.2 e₀ : Matrix (Fin N) (Fin N) ℂ))) := by
    unfold frobeniusNormSq
    refine continuous_finset_sum _ fun i _ => continuous_finset_sum _ fun j _ => ?_
    exact (continuous_norm.comp (h_mat_diff_cont i j)).pow 2
  have hκ1_cont : Continuous (fun q : (G_L × G_L) × G_L => κ q.1.1 q.2) :=
    hκ_cont.comp ((continuous_fst.comp continuous_fst).prodMk continuous_snd)
  have hκ2_cont : Continuous (fun q : (G_L × G_L) × G_L => κ q.1.2 q.2) :=
    hκ_cont.comp ((continuous_snd.comp continuous_fst).prodMk continuous_snd)
  have hω1_3_cont : Continuous (fun q : (G_L × G_L) × G_L => ω q.1.1) :=
    hω_fst_cont.comp continuous_fst
  have hω2_3_cont : Continuous (fun q : (G_L × G_L) × G_L => ω q.1.2) :=
    hω_snd_cont.comp continuous_fst
  let F3 : (G_L × G_L) × G_L → ℝ := fun q =>
    κ q.1.1 q.2 * κ q.1.2 q.2 * ω q.1.1 * ω q.1.2 *
      frobeniusNormSq ((q.1.1 e₀ : Matrix (Fin N) (Fin N) ℂ) -
        (q.1.2 e₀ : Matrix (Fin N) (Fin N) ℂ))
  have hF3_cont : Continuous F3 :=
    (((hκ1_cont.mul hκ2_cont).mul hω1_3_cont).mul hω2_3_cont).mul
      (hfrob_diff_cont.comp continuous_fst)
  have hF3_int : MeasureTheory.Integrable F3 ((μ.prod μ).prod μ) :=
    integrable_of_continuous_compact ((μ.prod μ).prod μ) F3 hF3_cont
  let good : G_L → G_L → Prop := fun W U =>
    frobeniusNormSq (((U e₀ * (W e₀)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
      Matrix (Fin N) (Fin N) ℂ) - 1) ≤ ε_sq
  let C_bad : ℝ := 4 * (N : ℝ) * Real.exp (β * (links : ℝ)) *
    β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2))
  have hC_bad_nn : 0 ≤ C_bad := by dsimp [C_bad]; positivity
  let G3 : (G_L × G_L) × G_L → ℝ := fun q =>
    4 * ε_sq * (κ q.1.1 q.2 * κ q.1.2 q.2 * ω q.1.1 * ω q.1.2)
  let H3 : (G_L × G_L) × G_L → ℝ := fun q => C_bad * (ω q.1.1 * ω q.1.2)
  have hG3_cont : Continuous G3 :=
    continuous_const.mul (((hκ1_cont.mul hκ2_cont).mul hω1_3_cont).mul hω2_3_cont)
  have hH3_cont : Continuous H3 := continuous_const.mul (hω1_3_cont.mul hω2_3_cont)
  have hG3_int : MeasureTheory.Integrable G3 ((μ.prod μ).prod μ) :=
    integrable_of_continuous_compact ((μ.prod μ).prod μ) G3 hG3_cont
  have hH3_int : MeasureTheory.Integrable H3 ((μ.prod μ).prod μ) :=
    integrable_of_continuous_compact ((μ.prod μ).prod μ) H3 hH3_cont
  have hG3_nn : ∀ q, 0 ≤ G3 q := fun q => by
    dsimp [G3]
    exact mul_nonneg (mul_nonneg (by norm_num) hε_nn)
      (mul_nonneg (mul_nonneg (mul_nonneg (hκ_nn _ _) (hκ_nn _ _))
        (hω_pos _).le) (hω_pos _).le)
  have hH3_nn : ∀ q, 0 ≤ H3 q := fun q => by
    dsimp [H3]
    exact mul_nonneg hC_bad_nn (mul_nonneg (hω_pos _).le (hω_pos _).le)
  have h_fac_ub : ∀ (U W : G_L) (e : (cubicTorus3 L).Link),
      Real.exp ((β / (2 * (N : ℝ))) *
        (Matrix.trace (((U e * (W e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
          Matrix (Fin N) (Fin N) ℂ))).re) ≤ Real.exp (β / 2) := by
    intro U W e
    have htr := (abs_le.mp (abs_re_trace_su_le (U e * (W e)⁻¹))).2
    have hmul : (β / (2 * (N : ℝ))) *
        (Matrix.trace (((U e * (W e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
          Matrix (Fin N) (Fin N) ℂ))).re ≤ β / 2 := by
      have heq : β / 2 = (β / (2 * (N : ℝ))) * (N : ℝ) := by
        field_simp [hN_pos.ne']
      rw [heq]
      exact mul_le_mul_of_nonneg_left htr (by positivity)
    exact Real.exp_le_exp.mpr hmul
  have h_κ_ub : ∀ U W : G_L, κ U W ≤ Real.exp (β * (links : ℝ) / 2) := fun U W => by
    have hwb := (cubicWilsonWeight_bounds L N β hβ_pos.le U).2
    have hcb := hχ_bd U W
    have h_exp_ub : linkChiUb L β = Real.exp (β * (links : ℝ) / 2) := by
      dsimp [linkChiUb]
      rw [h_card_links, ← Real.exp_nat_mul]
      congr 1; ring
    calc κ U W = cubicWilsonWeight L N β U * χ U W := rfl
      _ ≤ 1 * linkChiUb L β := mul_le_mul hwb hcb (hχ_nn U W) zero_le_one
      _ = Real.exp (β * (links : ℝ) / 2) := by rw [one_mul, h_exp_ub]
  have h_κ_bad : ∀ U W : G_L, ¬ good W U →
      κ U W ≤ Real.exp (β * (links : ℝ) / 2) *
        β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
    intro U W hnot
    have hgt : ε_sq < frobeniusNormSq (((U e₀ * (W e₀)⁻¹ :
        Matrix.specialUnitaryGroup (Fin N) ℂ) : Matrix (Fin N) (Fin N) ℂ) - 1) :=
      lt_of_not_ge hnot
    have hid := wilson_plaquette_eq_frobenius_sq (U e₀ * (W e₀)⁻¹)
    change frobeniusNormSq (((U e₀ * (W e₀)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
        Matrix (Fin N) (Fin N) ℂ) - 1) =
      2 * ((N : ℝ) - (Matrix.trace (((U e₀ * (W e₀)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
        Matrix (Fin N) (Fin N) ℂ))).re) at hid
    have htr_lt : (Matrix.trace (((U e₀ * (W e₀)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
        Matrix (Fin N) (Fin N) ℂ))).re ≤ (N : ℝ) - ε_sq / 2 := by
      linarith only [hid, hgt]
    have hmul : (β / (2 * (N : ℝ))) *
        (Matrix.trace (((U e₀ * (W e₀)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
          Matrix (Fin N) (Fin N) ℂ))).re ≤
        β / 2 - (6 * (N : ℝ) ^ 2 * (links : ℝ) + 2) * Real.log β := by
      have heq : (β / (2 * (N : ℝ))) * ((N : ℝ) - ε_sq / 2) =
          β / 2 - (6 * (N : ℝ) ^ 2 * (links : ℝ) + 2) * Real.log β := by
        dsimp [ε_sq]
        field_simp [hN_pos.ne', hβ_pos.ne']
        ring
      rw [← heq]
      exact mul_le_mul_of_nonneg_left htr_lt (by positivity)
    have hfac0 :
        Real.exp ((β / (2 * (N : ℝ))) *
          (Matrix.trace (((U e₀ * (W e₀)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
            Matrix (Fin N) (Fin N) ℂ))).re) ≤
          Real.exp (β / 2) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
      have hrp : Real.exp (-((6 * (N : ℝ) ^ 2 * (links : ℝ) + 2) * Real.log β)) =
          β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
        rw [Real.rpow_def_of_pos hβ_pos]
        congr 1; ring
      calc Real.exp ((β / (2 * (N : ℝ))) *
              (Matrix.trace (((U e₀ * (W e₀)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
                Matrix (Fin N) (Fin N) ℂ))).re)
          ≤ Real.exp (β / 2 - (6 * (N : ℝ) ^ 2 * (links : ℝ) + 2) * Real.log β) :=
              Real.exp_le_exp.mpr hmul
        _ = Real.exp (β / 2) *
              Real.exp (-((6 * (N : ℝ) ^ 2 * (links : ℝ) + 2) * Real.log β)) := by
              rw [sub_eq_add_neg, Real.exp_add]
        _ = Real.exp (β / 2) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
              rw [hrp]
    let fac : (cubicTorus3 L).Link → ℝ := fun e =>
      Real.exp ((β / (2 * (N : ℝ))) *
        (Matrix.trace (((U e * (W e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
          Matrix (Fin N) (Fin N) ℂ))).re)
    have hχ_split : χ U W = fac e₀ * ∏ e ∈ Finset.univ.erase e₀, fac e := by
      dsimp only [χ, cubicLinkKineticKernel, fac]
      exact (Finset.mul_prod_erase Finset.univ fac (Finset.mem_univ e₀)).symm
    have hrest_le : ∏ e ∈ Finset.univ.erase e₀, fac e ≤ (Real.exp (β / 2)) ^ (links - 1) := by
      calc ∏ e ∈ Finset.univ.erase e₀, fac e
          ≤ ∏ _e ∈ Finset.univ.erase e₀, Real.exp (β / 2) :=
              Finset.prod_le_prod (fun _ _ => (Real.exp_pos _).le) fun e _ => h_fac_ub U W e
        _ = (Real.exp (β / 2)) ^ (Finset.univ.erase e₀).card := Finset.prod_const _
        _ = (Real.exp (β / 2)) ^ (links - 1) := by
              rw [Finset.card_erase_of_mem (Finset.mem_univ e₀), Finset.card_univ, h_card_links]
    have hχ_bad : χ U W ≤ Real.exp (β * (links : ℝ) / 2) *
        β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
      rw [hχ_split]
      calc fac e₀ * ∏ e ∈ Finset.univ.erase e₀, fac e
          ≤ (Real.exp (β / 2) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2))) *
              (Real.exp (β / 2)) ^ (links - 1) :=
              mul_le_mul hfac0 hrest_le (Finset.prod_nonneg fun _ _ => (Real.exp_pos _).le)
                (by positivity)
        _ = (Real.exp (β / 2) * (Real.exp (β / 2)) ^ (links - 1)) *
              β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by ring
        _ = (Real.exp (β / 2)) ^ links * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
              rw [← pow_succ', Nat.sub_add_cancel hlinks_pos]
        _ = Real.exp (β * (links : ℝ) / 2) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
              rw [← Real.exp_nat_mul]; congr 2; ring
    have hwb := (cubicWilsonWeight_bounds L N β hβ_pos.le U).2
    calc κ U W = cubicWilsonWeight L N β U * χ U W := rfl
      _ ≤ 1 * (Real.exp (β * (links : ℝ) / 2) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2))) :=
          mul_le_mul hwb hχ_bad (hχ_nn U W) zero_le_one
      _ = Real.exp (β * (links : ℝ) / 2) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) :=
          one_mul _
  have hF3_pt_le : ∀ q : (G_L × G_L) × G_L, F3 q ≤ G3 q + H3 q := by
    rintro ⟨⟨U, U'⟩, W⟩
    by_cases hgood : good W U ∧ good W U'
    · have hA : frobeniusNormSq (((U e₀ * (W e₀)⁻¹ :
          Matrix.specialUnitaryGroup (Fin N) ℂ) : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ ε_sq :=
        hgood.1
      have hB : frobeniusNormSq (((U' e₀ * (W e₀)⁻¹ :
          Matrix.specialUnitaryGroup (Fin N) ℂ) : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ ε_sq :=
        hgood.2
      have hdiff_le : frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
          (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ≤ 4 * ε_sq := by
        rw [← frobeniusNormSq_sub_self_su (U e₀) (U' e₀)]
        have heq_grp : U e₀ * (U' e₀)⁻¹ = (U e₀ * (W e₀)⁻¹) * (U' e₀ * (W e₀)⁻¹)⁻¹ := by group
        rw [heq_grp]
        have h1 := frobeniusNormSq_su_mul_sub_one (U e₀ * (W e₀)⁻¹) (U' e₀ * (W e₀)⁻¹)⁻¹
        rw [frobeniusNormSq_su_inv_sub_one (U' e₀ * (W e₀)⁻¹)] at h1
        linarith only [h1, hA, hB]
      have h_coeff_nn : 0 ≤ κ U W * κ U' W * ω U * ω U' :=
        mul_nonneg (mul_nonneg (mul_nonneg (hκ_nn U W) (hκ_nn U' W))
          (hω_pos U).le) (hω_pos U').le
      calc F3 ((U, U'), W)
          ≤ (κ U W * κ U' W * ω U * ω U') * (4 * ε_sq) :=
              mul_le_mul_of_nonneg_left hdiff_le h_coeff_nn
        _ = G3 ((U, U'), W) := by dsimp [G3]; ring
        _ ≤ G3 ((U, U'), W) + H3 ((U, U'), W) := le_add_of_nonneg_right (hH3_nn _)
    · have hκ_prod : κ U W * κ U' W ≤
          Real.exp (β * (links : ℝ)) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
        rw [not_and_or] at hgood
        rcases hgood with hbad1 | hbad2
        · calc κ U W * κ U' W
              ≤ (Real.exp (β * (links : ℝ) / 2) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2))) *
                  Real.exp (β * (links : ℝ) / 2) :=
                  mul_le_mul (h_κ_bad U W hbad1) (h_κ_ub U' W) (hκ_nn U' W) (by positivity)
            _ = (Real.exp (β * (links : ℝ) / 2) * Real.exp (β * (links : ℝ) / 2)) *
                  β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by ring
            _ = Real.exp (β * (links : ℝ)) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
                  rw [← Real.exp_add]; congr 2; ring
        · calc κ U W * κ U' W
              ≤ Real.exp (β * (links : ℝ) / 2) *
                  (Real.exp (β * (links : ℝ) / 2) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2))) :=
                  mul_le_mul (h_κ_ub U W) (h_κ_bad U' W hbad2) (hκ_nn U' W) (by positivity)
            _ = (Real.exp (β * (links : ℝ) / 2) * Real.exp (β * (links : ℝ) / 2)) *
                  β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by ring
            _ = Real.exp (β * (links : ℝ)) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by
                  rw [← Real.exp_add]; congr 2; ring
      have hω_nn : 0 ≤ ω U * ω U' := mul_nonneg (hω_pos U).le (hω_pos U').le
      have hfrob_le : frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
          (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) ≤ 4 * (N : ℝ) :=
        frobeniusNormSq_su_sub_su_le (U e₀) (U' e₀)
      calc F3 ((U, U'), W)
          = (κ U W * κ U' W) *
              frobeniusNormSq ((U e₀ : Matrix (Fin N) (Fin N) ℂ) -
                (U' e₀ : Matrix (Fin N) (Fin N) ℂ)) * (ω U * ω U') := by
              dsimp [F3]; ring
        _ ≤ (Real.exp (β * (links : ℝ)) * β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2))) *
              (4 * (N : ℝ)) * (ω U * ω U') :=
            mul_le_mul_of_nonneg_right
              (mul_le_mul hκ_prod hfrob_le (frobeniusNormSq_nonneg _) (by positivity)) hω_nn
        _ = H3 ((U, U'), W) := by dsimp [H3, C_bad]; ring
        _ ≤ G3 ((U, U'), W) + H3 ((U, U'), W) := le_add_of_nonneg_left (hG3_nn _)
  have hG3_val : ∫ q : (G_L × G_L) × G_L, G3 q ∂((μ.prod μ).prod μ) = 4 * ε_sq * lam0 := by
    have h_int_p : MeasureTheory.Integrable
        (fun p : G_L × G_L => K_W p.1 p.2 * ω p.1 * ω p.2) (μ.prod μ) :=
      integrable_of_continuous_compact (μ.prod μ) _
        ((hKW_cont.mul hω_fst_cont).mul hω_snd_cont)
    have h_eq_p : ∀ p : G_L × G_L,
        ∫ W, G3 (p, W) ∂μ = 4 * ε_sq * (K_W p.1 p.2 * ω p.1 * ω p.2) := fun p => by
      dsimp only [G3]
      rw [MeasureTheory.integral_const_mul, hKW_eq_κ p.1 p.2]
      rw [← MeasureTheory.integral_mul_const, ← MeasureTheory.integral_mul_const]
      congr 1
      refine MeasureTheory.integral_congr_ae (Filter.Eventually.of_forall fun W => ?_)
      dsimp only; ring
    calc ∫ q : (G_L × G_L) × G_L, G3 q ∂((μ.prod μ).prod μ)
        = ∫ p : G_L × G_L, ∫ W, G3 (p, W) ∂μ ∂(μ.prod μ) :=
            MeasureTheory.integral_prod G3 hG3_int
      _ = ∫ p : G_L × G_L, 4 * ε_sq * (K_W p.1 p.2 * ω p.1 * ω p.2) ∂(μ.prod μ) :=
            MeasureTheory.integral_congr_ae (Filter.Eventually.of_forall fun p => h_eq_p p)
      _ = 4 * ε_sq * ∫ p : G_L × G_L, K_W p.1 p.2 * ω p.1 * ω p.2 ∂(μ.prod μ) :=
            MeasureTheory.integral_const_mul _ _
      _ = 4 * ε_sq * ∫ U, ∫ U', K_W U U' * ω U * ω U' ∂μ ∂μ := by
            rw [MeasureTheory.integral_prod _ h_int_p]
      _ = 4 * ε_sq * ∫ U, ω U * (∫ U', K_W U U' * ω U' ∂μ) ∂μ := by
            congr 1
            refine MeasureTheory.integral_congr_ae (Filter.Eventually.of_forall fun U => ?_)
            dsimp only
            rw [← MeasureTheory.integral_const_mul]
            refine MeasureTheory.integral_congr_ae (Filter.Eventually.of_forall fun U' => ?_)
            dsimp only; ring
      _ = 4 * ε_sq * ∫ U, ω U * (lam0 * ω U) ∂μ := by
            congr 1
            refine MeasureTheory.integral_congr_ae (Filter.Eventually.of_forall fun U => ?_)
            dsimp only; rw [h_eig_ω U]
      _ = 4 * ε_sq * (lam0 * ∫ U, ω U ^ 2 ∂μ) := by
            congr 1
            rw [← MeasureTheory.integral_const_mul]
            refine MeasureTheory.integral_congr_ae (Filter.Eventually.of_forall fun U => ?_)
            dsimp only; ring
      _ = 4 * ε_sq * lam0 := by rw [hω_sq_int, mul_one]
  have hH3_le : ∫ q : (G_L × G_L) × G_L, H3 q ∂((μ.prod μ).prod μ) ≤ C_bad := by
    have h_int_p : MeasureTheory.Integrable (fun p : G_L × G_L => ω p.1 * ω p.2) (μ.prod μ) :=
      integrable_of_continuous_compact (μ.prod μ) _ (hω_fst_cont.mul hω_snd_cont)
    have hω_nn : 0 ≤ ∫ U, ω U ∂μ := MeasureTheory.integral_nonneg fun U => (hω_pos U).le
    have h_prod_ω : (∫ U, ω U ∂μ) * (∫ U', ω U' ∂μ) ≤ 1 := by
      calc (∫ U, ω U ∂μ) * (∫ U', ω U' ∂μ) ≤ 1 * 1 :=
            mul_le_mul hω_int1 hω_int1 hω_nn zero_le_one
        _ = 1 := one_mul 1
    calc ∫ q : (G_L × G_L) × G_L, H3 q ∂((μ.prod μ).prod μ)
        = ∫ p : G_L × G_L, ∫ _W, C_bad * (ω p.1 * ω p.2) ∂μ ∂(μ.prod μ) :=
            MeasureTheory.integral_prod H3 hH3_int
      _ = ∫ p : G_L × G_L, C_bad * (ω p.1 * ω p.2) ∂(μ.prod μ) := by
            refine MeasureTheory.integral_congr_ae (Filter.Eventually.of_forall fun p => ?_)
            simp [MeasureTheory.integral_const]
      _ = C_bad * ∫ p : G_L × G_L, ω p.1 * ω p.2 ∂(μ.prod μ) :=
            MeasureTheory.integral_const_mul _ _
      _ = C_bad * ∫ U, ∫ U', ω U * ω U' ∂μ ∂μ := by
            rw [MeasureTheory.integral_prod _ h_int_p]
      _ = C_bad * ∫ U, ω U * (∫ U', ω U' ∂μ) ∂μ := by
            congr 1
            refine MeasureTheory.integral_congr_ae (Filter.Eventually.of_forall fun U => ?_)
            dsimp only; rw [MeasureTheory.integral_const_mul]
      _ = C_bad * ((∫ U, ω U ∂μ) * (∫ U', ω U' ∂μ)) := by
            rw [MeasureTheory.integral_mul_const]
      _ ≤ C_bad * 1 := mul_le_mul_of_nonneg_left h_prod_ω hC_bad_nn
      _ = C_bad := mul_one _
  calc ∫ q : (G_L × G_L) × G_L, F3 q ∂((μ.prod μ).prod μ)
      ≤ ∫ q : (G_L × G_L) × G_L, (G3 q + H3 q) ∂((μ.prod μ).prod μ) :=
          MeasureTheory.integral_mono hF3_int (hG3_int.add hH3_int) hF3_pt_le
    _ = (∫ q : (G_L × G_L) × G_L, G3 q ∂((μ.prod μ).prod μ)) +
          (∫ q : (G_L × G_L) × G_L, H3 q ∂((μ.prod μ).prod μ)) :=
          MeasureTheory.integral_add hG3_int hH3_int
    _ ≤ 4 * ε_sq * lam0 + C_bad := add_le_add hG3_val hH3_le

private lemma fullRank_lam0_haar_lb (L N : ℕ) [NeZero L] [NeZero N] (hN : 2 ≤ N)
    {β : ℝ} (hβ : 1 ≤ β)
    (T_raw : HaarGaugeSpace (by letI := canonSUMeas N; exact latticeHaarMeasure L N) →L[ℂ]
      HaarGaugeSpace (by letI := canonSUMeas N; exact latticeHaarMeasure L N))
    (hT_ae : ∀ ψ,
      ⇑(T_raw ψ) =ᵐ[by letI := canonSUMeas N; exact latticeHaarMeasure L N]
        wilsonIntegralFn L N β (wilsonGramKernel L N (cubicLinkKineticKernel L N β)) ψ)
    (h_fn_int : ∀ ψ U, MeasureTheory.Integrable
      (fun U' => ((wilsonKernel β (cubicPlaquettes L)
        (wilsonGramKernel L N (cubicLinkKineticKernel L N β)) U U' : ℝ) : ℂ) * ⇑ψ U')
      (by letI := canonSUMeas N; exact latticeHaarMeasure L N)) :
    let links : ℕ := 3 * L ^ 3
    let K : ℕ := Nat.ceil (4 * (N : ℝ) / (1 / Real.sqrt β)) + 1
    (((K : ℝ) ^ (2 * N * N)) ^ (2 * links))⁻¹ * Real.exp (β * (links : ℝ)) *
        Real.exp (-(30 * (L : ℝ) ^ 3 / (N : ℝ))) ≤ ‖T_raw‖ := by
  letI := canonSUMeas N
  haveI := canonSUBorel N
  have hβ_pos : 0 < β := lt_of_lt_of_le zero_lt_one hβ
  have hN_pos : (0 : ℝ) < (N : ℝ) := Nat.cast_pos.mpr (NeZero.pos N)
  let G_L := GaugeField (cubicTorus3 L) (Matrix.specialUnitaryGroup (Fin N) ℂ)
  let μ := latticeHaarMeasure L N
  haveI := latticeHaarMeasure_prob L N
  let χ := cubicLinkKineticKernel L N β
  let K_kin := wilsonGramKernel L N χ
  let K_W := wilsonKernel β (cubicPlaquettes L) K_kin
  have hχ_cont := continuous_cubicLinkKineticKernel L N β
  have hχ_nn := linkChi_nn L N hN β hβ_pos.le
  let κ : G_L → G_L → ℝ := fun U W => cubicWilsonWeight L N β U * χ U W
  have hκ_cont : Continuous (Function.uncurry κ) := by
    have hw : Continuous (cubicWilsonWeight L N β) :=
      Real.continuous_exp.comp (continuous_const.mul (continuous_cubicWilsonAction L N β))
    exact (hw.comp continuous_fst).mul hχ_cont
  have hκ_nn : ∀ U W, 0 ≤ κ U W := fun U W =>
    mul_nonneg (Real.exp_pos _).le (hχ_nn U W)
  have hKW_eq_κ : ∀ U U', K_W U U' = ∫ W, κ U W * κ U' W ∂μ := by
    intro U U'
    have h_exp : Real.exp (-(1 / 2 : ℝ) *
        (wilsonAction β (cubicPlaquettes L) U + wilsonAction β (cubicPlaquettes L) U')) =
        cubicWilsonWeight L N β U * cubicWilsonWeight L N β U' := by
      unfold cubicWilsonWeight
      rw [← Real.exp_add]
      congr 1; ring
    dsimp only [K_W, wilsonKernel, K_kin, wilsonGramKernel]
    rw [h_exp, ← MeasureTheory.integral_const_mul]
    refine MeasureTheory.integral_congr_ae (Filter.Eventually.of_forall fun W => ?_)
    dsimp only [κ]; ring
  have hcinner : ∀ a b : ℂ, ⟪a, b⟫_ℂ = starRingEnd ℂ a * b := by
    intro a b
    have h1 : ⟪(1 : ℂ), (1 : ℂ)⟫_ℂ = 1 := by rw [inner_self_eq_norm_sq_to_K]; norm_num
    calc ⟪a, b⟫_ℂ = ⟪a • (1 : ℂ), b • (1 : ℂ)⟫_ℂ := by simp
      _ = starRingEnd ℂ a * (b * ⟪(1 : ℂ), (1 : ℂ)⟫_ℂ) := by
            rw [inner_smul_left, inner_smul_right]
      _ = starRingEnd ℂ a * b := by rw [h1, mul_one]
  let links : ℕ := 3 * L ^ 3
  have h_card_links : Fintype.card (cubicTorus3 L).Link = links := by
    simp [cubicTorus3, links, Fintype.card_prod, Fintype.card_fin]; ring
  let K : ℕ := Nat.ceil (4 * (N : ℝ) / (1 / Real.sqrt β)) + 1
  let δ : ℝ := 1 / Real.sqrt β
  have hδ : 0 < δ := div_pos zero_lt_one (Real.sqrt_pos.mpr hβ_pos)
  have hβδ : β * δ ^ 2 = 1 := by
    dsimp [δ]
    rw [one_div, inv_pow, Real.sq_sqrt hβ_pos.le, mul_inv_cancel₀ hβ_pos.ne']
  let B_su : Set (Matrix.specialUnitaryGroup (Fin N) ℂ) :=
    { A | frobeniusNormSq ((A : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ δ ^ 2 }
  have hB_su_meas : MeasurableSet B_su := by
    have hc : Continuous (fun A : Matrix.specialUnitaryGroup (Fin N) ℂ =>
        frobeniusNormSq ((A : Matrix (Fin N) (Fin N) ℂ) - 1)) := by
      unfold frobeniusNormSq
      refine continuous_finset_sum _ fun i _ => continuous_finset_sum _ fun j _ => ?_
      exact (continuous_norm.comp ((continuous_apply j).comp
        ((continuous_apply i).comp (continuous_subtype_val.sub continuous_const)))).pow 2
    exact measurableSet_Iic.preimage hc.measurable
  have hB_su_lb : (1 : ℝ) / ((K : ℝ) ^ (2 * N * N)) ≤ (suHaar N B_su).toReal :=
    suHaar_ball_ge N hδ
  have hK_real_pos : (0 : ℝ) < (K : ℝ) := Nat.cast_pos.mpr (Nat.succ_pos _)
  let B_L : Set G_L := Set.pi Set.univ (fun _ => B_su)
  have hB_L_meas : MeasurableSet B_L := by
    change @MeasurableSet _ MeasurableSpace.pi B_L
    exact MeasurableSet.univ_pi fun _ => hB_su_meas
  have hB_L_vol_eq : μ.real B_L = ((suHaar N B_su).toReal) ^ links := by
    haveI := suHaar_prob N
    change (MeasureTheory.Measure.pi (fun _ : (cubicTorus3 L).Link => suHaar N)
      (Set.pi Set.univ fun _ => B_su)).toReal = _
    rw [MeasureTheory.Measure.pi_pi (fun _ => suHaar N) _, Finset.prod_const,
      Finset.card_univ, h_card_links, ENNReal.toReal_pow]
  have hB_L_lb : (((K : ℝ) ^ (2 * N * N)) ^ links)⁻¹ ≤ μ.real B_L := by
    rw [hB_L_vol_eq, ← one_div, ← one_div_pow]
    exact pow_le_pow_left₀ (by positivity) hB_su_lb links
  have hB_L_pos : 0 < μ.real B_L := lt_of_lt_of_le (by positivity) hB_L_lb
  have hS_B_L : ∀ U ∈ B_L,
      wilsonAction β (cubicPlaquettes L) U ≤ 24 * (L : ℝ) ^ 3 / (N : ℝ) := by
    intro U hU
    have h_plaq : ∀ (x : (cubicTorus3 L).Site) (d₁ d₂ : Fin 3),
        wilsonPlaquetteTerm
          ⟨x, cubicPlaquette x d₁ d₂, cubicPlaquette_isPath x d₁ d₂⟩ U ≤
          8 * δ ^ 2 / (N : ℝ) := by
      intro x d₁ d₂
      let A := pathHolonomy U (cubicPlaquette x d₁ d₂)
      have hA_eq : A = U (x, d₁) * (U (cubicShift L d₁ x, d₂) *
          ((U (cubicShift L d₂ x, d₁))⁻¹ * ((U (x, d₂))⁻¹ * 1))) := rfl
      have hfrob : frobeniusNormSq ((A : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ 16 * δ ^ 2 := by
        rw [hA_eq]
        exact frobeniusNormSq_holonomy4_le _ _ _ _
          (hU (x, d₁) (Set.mem_univ _))
          (hU (cubicShift L d₁ x, d₂) (Set.mem_univ _))
          (hU (cubicShift L d₂ x, d₁) (Set.mem_univ _))
          (hU (x, d₂) (Set.mem_univ _))
      have hid := wilson_plaquette_eq_frobenius_sq A
      change frobeniusNormSq ((A : Matrix (Fin N) (Fin N) ℂ) - 1) =
        2 * ((N : ℝ) - (Matrix.trace (A : Matrix (Fin N) (Fin N) ℂ)).re) at hid
      have htr : (N : ℝ) - (Matrix.trace (A : Matrix (Fin N) (Fin N) ℂ)).re ≤ 8 * δ ^ 2 := by
        linarith only [hid, hfrob]
      have hterm_eq : wilsonPlaquetteTerm
          ⟨x, cubicPlaquette x d₁ d₂, cubicPlaquette_isPath x d₁ d₂⟩ U =
          ((N : ℝ) - (Matrix.trace (A : Matrix (Fin N) (Fin N) ℂ)).re) / (N : ℝ) := by
        unfold wilsonPlaquetteTerm
        dsimp only [A]
        field_simp [hN_pos.ne']
      rw [hterm_eq]
      exact div_le_div_of_nonneg_right htr hN_pos.le
    unfold wilsonAction cubicPlaquettes
    rw [sum_map_flatMap, sum_map_univ_toList]
    have h_site : ∀ x : Fin L × Fin L × Fin L,
        (([⟨x, cubicPlaquette x 0 1, cubicPlaquette_isPath x 0 1⟩,
           ⟨x, cubicPlaquette x 0 2, cubicPlaquette_isPath x 0 2⟩,
           ⟨x, cubicPlaquette x 1 2, cubicPlaquette_isPath x 1 2⟩]).map
          (fun p => wilsonPlaquetteTerm p U)).sum ≤ 24 * δ ^ 2 / (N : ℝ) := by
      intro x
      simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil, add_zero]
      have h1 := h_plaq x 0 1
      have h2 := h_plaq x 0 2
      have h3 := h_plaq x 1 2
      linarith only [h1, h2, h3]
    have h_sum_sites :
        (∑ x : Fin L × Fin L × Fin L,
          (([⟨x, cubicPlaquette x 0 1, cubicPlaquette_isPath x 0 1⟩,
             ⟨x, cubicPlaquette x 0 2, cubicPlaquette_isPath x 0 2⟩,
             ⟨x, cubicPlaquette x 1 2, cubicPlaquette_isPath x 1 2⟩]).map
            (fun p => wilsonPlaquetteTerm p U)).sum) ≤
          (L : ℝ) ^ 3 * (24 * δ ^ 2 / (N : ℝ)) := by
      calc _ ≤ ∑ _x : Fin L × Fin L × Fin L, (24 * δ ^ 2 / (N : ℝ)) :=
            Finset.sum_le_sum fun x _ => h_site x
        _ = (L : ℝ) ^ 3 * (24 * δ ^ 2 / (N : ℝ)) := by
            simp [Finset.sum_const, Fintype.card_prod, Fintype.card_fin]; ring
    calc β * _ ≤ β * ((L : ℝ) ^ 3 * (24 * δ ^ 2 / (N : ℝ))) :=
          mul_le_mul_of_nonneg_left h_sum_sites hβ_pos.le
      _ = 24 * (L : ℝ) ^ 3 * (β * δ ^ 2) / (N : ℝ) := by ring
      _ = 24 * (L : ℝ) ^ 3 / (N : ℝ) := by rw [hβδ, mul_one]
  have hκ_B_L : ∀ U ∈ B_L, ∀ W ∈ B_L,
      Real.exp (β * (links : ℝ) / 2 - 15 * (L : ℝ) ^ 3 / (N : ℝ)) ≤ κ U W := by
    intro U hU W hW
    have hw_lb : Real.exp (-(12 * (L : ℝ) ^ 3 / (N : ℝ))) ≤ cubicWilsonWeight L N β U := by
      unfold cubicWilsonWeight
      apply Real.exp_le_exp.mpr
      linarith only [hS_B_L U hU]
    have hχ_fac : ∀ e : (cubicTorus3 L).Link,
        Real.exp (β / 2 - 1 / (N : ℝ)) ≤
          Real.exp ((β / (2 * (N : ℝ))) *
            (Matrix.trace (((U e * (W e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
              Matrix (Fin N) (Fin N) ℂ))).re) := by
      intro e
      have hf1 : frobeniusNormSq ((U e : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ δ ^ 2 :=
        hU e (Set.mem_univ e)
      have hf2 : frobeniusNormSq ((W e : Matrix (Fin N) (Fin N) ℂ) - 1) ≤ δ ^ 2 :=
        hW e (Set.mem_univ e)
      have hf_diff : frobeniusNormSq (((U e * (W e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
          Matrix (Fin N) (Fin N) ℂ) - 1) ≤ 4 * δ ^ 2 := by
        rw [frobeniusNormSq_sub_self_su (U e) (W e)]
        have h_sub_eq : (U e : Matrix (Fin N) (Fin N) ℂ) - (W e : Matrix (Fin N) (Fin N) ℂ) =
            ((U e : Matrix (Fin N) (Fin N) ℂ) - 1) + -((W e : Matrix (Fin N) (Fin N) ℂ) - 1) := by
          abel
        rw [h_sub_eq]
        have hadd := frobeniusNormSq_add_le
          ((U e : Matrix (Fin N) (Fin N) ℂ) - 1) (-((W e : Matrix (Fin N) (Fin N) ℂ) - 1))
        rw [frobeniusNormSq_neg] at hadd
        linarith only [hadd, hf1, hf2]
      have hid := wilson_plaquette_eq_frobenius_sq (U e * (W e)⁻¹)
      change frobeniusNormSq (((U e * (W e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
          Matrix (Fin N) (Fin N) ℂ) - 1) =
        2 * ((N : ℝ) - (Matrix.trace (((U e * (W e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
          Matrix (Fin N) (Fin N) ℂ))).re) at hid
      have htr : (N : ℝ) - 2 * δ ^ 2 ≤
          (Matrix.trace (((U e * (W e)⁻¹ : Matrix.specialUnitaryGroup (Fin N) ℂ) :
            Matrix (Fin N) (Fin N) ℂ))).re := by
        linarith only [hid, hf_diff]
      apply Real.exp_le_exp.mpr
      have heq : (β / (2 * (N : ℝ))) * ((N : ℝ) - 2 * δ ^ 2) = β / 2 - 1 / (N : ℝ) := by
        calc (β / (2 * (N : ℝ))) * ((N : ℝ) - 2 * δ ^ 2)
            = β / 2 - (β * δ ^ 2) / (N : ℝ) := by field_simp [hN_pos.ne']; ring
          _ = β / 2 - 1 / (N : ℝ) := by rw [hβδ]
      rw [← heq]
      exact mul_le_mul_of_nonneg_left htr (by positivity)
    have hχ_lb : Real.exp (β * (links : ℝ) / 2 - 3 * (L : ℝ) ^ 3 / (N : ℝ)) ≤ χ U W := by
      have hexp_eq : (Real.exp (β / 2 - 1 / (N : ℝ))) ^ links =
          Real.exp (β * (links : ℝ) / 2 - 3 * (L : ℝ) ^ 3 / (N : ℝ)) := by
        rw [← Real.exp_nat_mul]
        congr 1; dsimp only [links]; push_cast; ring
      rw [← hexp_eq]
      calc (Real.exp (β / 2 - 1 / (N : ℝ))) ^ links
          = ∏ _e : (cubicTorus3 L).Link, Real.exp (β / 2 - 1 / (N : ℝ)) := by
              rw [Finset.prod_const, Finset.card_univ, h_card_links]
        _ ≤ χ U W :=
              Finset.prod_le_prod (fun _ _ => (Real.exp_pos _).le) fun e _ => hχ_fac e
    calc Real.exp (β * (links : ℝ) / 2 - 15 * (L : ℝ) ^ 3 / (N : ℝ))
        = Real.exp (-(12 * (L : ℝ) ^ 3 / (N : ℝ))) *
            Real.exp (β * (links : ℝ) / 2 - 3 * (L : ℝ) ^ 3 / (N : ℝ)) := by
            rw [← Real.exp_add]; congr 1; ring
      _ ≤ cubicWilsonWeight L N β U * χ U W :=
            mul_le_mul hw_lb hχ_lb (Real.exp_pos _).le (Real.exp_pos _).le
  let c_KW : ℝ := μ.real B_L * Real.exp (β * (links : ℝ)) *
    Real.exp (-(30 * (L : ℝ) ^ 3 / (N : ℝ)))
  have hKW_B_L : ∀ U ∈ B_L, ∀ U' ∈ B_L, c_KW ≤ K_W U U' := by
    intro U hU U' hU'
    let c_prod : ℝ := Real.exp (β * (links : ℝ)) * Real.exp (-(30 * (L : ℝ) ^ 3 / (N : ℝ)))
    have h_int_κ : MeasureTheory.Integrable (fun W => κ U W * κ U' W) μ := by
      have hp1 : Continuous (fun W : G_L => (U, W)) := continuous_const.prodMk continuous_id
      have hp2 : Continuous (fun W : G_L => (U', W)) := continuous_const.prodMk continuous_id
      exact integrable_of_continuous_compact μ _ ((hκ_cont.comp hp1).mul (hκ_cont.comp hp2))
    have h_ind_int : MeasureTheory.Integrable (B_L.indicator (fun _ => c_prod)) μ :=
      (MeasureTheory.integrable_const c_prod).indicator hB_L_meas
    have h_le : ∀ W, B_L.indicator (fun _ => c_prod) W ≤ κ U W * κ U' W := by
      intro W
      by_cases hW : W ∈ B_L
      · rw [Set.indicator_of_mem hW]
        have h1 := hκ_B_L U hU W hW
        have h2 := hκ_B_L U' hU' W hW
        calc c_prod = Real.exp (β * (links : ℝ) / 2 - 15 * (L : ℝ) ^ 3 / (N : ℝ)) *
                Real.exp (β * (links : ℝ) / 2 - 15 * (L : ℝ) ^ 3 / (N : ℝ)) := by
                dsimp [c_prod]; rw [← Real.exp_add, ← Real.exp_add]; congr 1; ring
          _ ≤ κ U W * κ U' W :=
                mul_le_mul h1 h2 (Real.exp_pos _).le (hκ_nn U W)
      · rw [Set.indicator_of_notMem hW]
        exact mul_nonneg (hκ_nn U W) (hκ_nn U' W)
    have h_ind_val : ∫ W, B_L.indicator (fun _ => c_prod) W ∂μ = c_KW := by
      rw [MeasureTheory.integral_indicator hB_L_meas, MeasureTheory.setIntegral_const]
      dsimp [c_KW, c_prod]
      simp only [smul_eq_mul]
      ring
    rw [hKW_eq_κ U U', ← h_ind_val]
    exact MeasureTheory.integral_mono h_ind_int h_int_κ h_le
  let ψ_B : HaarGaugeSpace μ :=
    MeasureTheory.indicatorConstLp (2 : ENNReal) hB_L_meas (MeasureTheory.measure_ne_top μ B_L) (1 : ℂ)
  have hψB_norm_sq : ‖ψ_B‖ ^ 2 = μ.real B_L := by
    have hre : (⟪ψ_B, ψ_B⟫_ℂ).re = μ.real B_L := by
      dsimp only [ψ_B]
      rw [MeasureTheory.L2.inner_indicatorConstLp_indicatorConstLp
        (hμs := MeasureTheory.measure_ne_top μ B_L)
        (hμt := MeasureTheory.measure_ne_top μ B_L)]
      have h1 : ⟪(1 : ℂ), (1 : ℂ)⟫_ℂ = 1 := by
        rw [inner_self_eq_norm_sq_to_K]; norm_num
      rw [Set.inter_self, h1, Complex.real_smul, mul_one, Complex.ofReal_re]
    rw [inner_self_eq_norm_sq_to_K] at hre
    simpa [pow_two] using hre
  have hT_raw_re_ub : (⟪ψ_B, T_raw ψ_B⟫_ℂ).re ≤ ‖T_raw‖ * μ.real B_L := by
    calc (⟪ψ_B, T_raw ψ_B⟫_ℂ).re
        ≤ ‖⟪ψ_B, T_raw ψ_B⟫_ℂ‖ := Complex.re_le_norm _
      _ ≤ ‖ψ_B‖ * ‖T_raw ψ_B‖ := norm_inner_le_norm _ _
      _ ≤ ‖ψ_B‖ * (‖T_raw‖ * ‖ψ_B‖) :=
          mul_le_mul_of_nonneg_left (T_raw.le_opNorm ψ_B) (norm_nonneg _)
      _ = ‖T_raw‖ * ‖ψ_B‖ ^ 2 := by ring
      _ = ‖T_raw‖ * μ.real B_L := by rw [hψB_norm_sq]
  have hT_raw_re_lb : μ.real B_L * (μ.real B_L * c_KW) ≤ (⟪ψ_B, T_raw ψ_B⟫_ℂ).re := by
    have hl2 : MeasureTheory.Integrable (fun U => ⟪ψ_B U, (T_raw ψ_B) U⟫_ℂ) μ :=
      MeasureTheory.L2.integrable_inner _ _
    have h_in_re : (⟪ψ_B, T_raw ψ_B⟫_ℂ).re =
        ∫ U, (⟪ψ_B U, (T_raw ψ_B) U⟫_ℂ).re ∂μ := by
      rw [MeasureTheory.L2.inner_def]
      change RCLike.re (∫ U, ⟪ψ_B U, (T_raw ψ_B) U⟫_ℂ ∂μ) = _
      rw [← integral_re hl2]
      rfl
    have hψB_ae := MeasureTheory.indicatorConstLp_coeFn (p := (2 : ENNReal))
      (μ := μ) (s := B_L) (hs := hB_L_meas) (hμs := MeasureTheory.measure_ne_top μ B_L)
      (c := (1 : ℂ))
    have hT_ae_B := hT_ae ψ_B
    have h_fn_lb : ∀ U ∈ B_L,
        μ.real B_L * c_KW ≤ RCLike.re (wilsonIntegralFn L N β K_kin ψ_B U) := by
      intro U hU
      dsimp [wilsonIntegralFn]
      have h_int_fn := h_fn_int ψ_B U
      change _ ≤ RCLike.re (∫ U', ((K_W U U' : ℝ) : ℂ) * ⇑ψ_B U' ∂μ)
      rw [← integral_re h_int_fn]
      have h_ae_U' : ∀ᵐ U' ∂μ,
          B_L.indicator (fun _ => c_KW) U' ≤
            RCLike.re (((K_W U U' : ℝ) : ℂ) * ⇑ψ_B U') := by
        filter_upwards [hψB_ae] with U' hU'
        change _ ≤ (((K_W U U' : ℝ) : ℂ) * ⇑ψ_B U').re
        rw [hU']
        by_cases hU'B : U' ∈ B_L
        · rw [Set.indicator_of_mem hU'B, Set.indicator_of_mem hU'B, mul_one, Complex.ofReal_re]
          exact hKW_B_L U hU U' hU'B
        · rw [Set.indicator_of_notMem hU'B, Set.indicator_of_notMem hU'B, mul_zero,
            Complex.zero_re]
          exact le_rfl
      have h_ind_val : ∫ U', B_L.indicator (fun _ => c_KW) U' ∂μ = μ.real B_L * c_KW := by
        rw [MeasureTheory.integral_indicator hB_L_meas, MeasureTheory.setIntegral_const]
        simp [smul_eq_mul]
      rw [← h_ind_val]
      exact MeasureTheory.integral_mono_ae
        ((MeasureTheory.integrable_const c_KW).indicator hB_L_meas) h_int_fn.re h_ae_U'
    have h_ae_U : ∀ᵐ U ∂μ,
        B_L.indicator (fun _ => μ.real B_L * c_KW) U ≤ (⟪ψ_B U, (T_raw ψ_B) U⟫_ℂ).re := by
      filter_upwards [hψB_ae, hT_ae_B] with U hU hTU
      change _ ≤ (⟪⇑ψ_B U, ⇑(T_raw ψ_B) U⟫_ℂ).re
      rw [hU, hTU, hcinner]
      by_cases hUB : U ∈ B_L
      · rw [Set.indicator_of_mem hUB, Set.indicator_of_mem hUB, map_one, one_mul]
        exact h_fn_lb U hUB
      · rw [Set.indicator_of_notMem hUB, Set.indicator_of_notMem hUB, map_zero, zero_mul,
          Complex.zero_re]
        exact le_rfl
    have h_ind_val2 :
        ∫ U, B_L.indicator (fun _ => μ.real B_L * c_KW) U ∂μ = μ.real B_L * (μ.real B_L * c_KW) := by
      rw [MeasureTheory.integral_indicator hB_L_meas, MeasureTheory.setIntegral_const]
      simp [smul_eq_mul]
    rw [h_in_re, ← h_ind_val2]
    exact MeasureTheory.integral_mono_ae
      ((MeasureTheory.integrable_const (μ.real B_L * c_KW)).indicator hB_L_meas)
      hl2.re h_ae_U
  have h_mul_le : μ.real B_L * (μ.real B_L * c_KW) ≤ ‖T_raw‖ * μ.real B_L :=
    hT_raw_re_lb.trans hT_raw_re_ub
  have h_div_le : μ.real B_L * c_KW ≤ ‖T_raw‖ :=
    (mul_le_mul_iff_left₀ hB_L_pos).mp (h_mul_le.trans_eq (mul_comm ‖T_raw‖ _))
  have hB_sq_lb : (((K : ℝ) ^ (2 * N * N)) ^ (2 * links))⁻¹ ≤ (μ.real B_L) ^ 2 := by
    have h1 := pow_le_pow_left₀ (by positivity) hB_L_lb 2
    rwa [inv_pow, ← pow_mul, mul_comm links 2] at h1
  calc (((K : ℝ) ^ (2 * N * N)) ^ (2 * links))⁻¹ * Real.exp (β * (links : ℝ)) *
          Real.exp (-(30 * (L : ℝ) ^ 3 / (N : ℝ)))
      ≤ (μ.real B_L) ^ 2 * Real.exp (β * (links : ℝ)) *
          Real.exp (-(30 * (L : ℝ) ^ 3 / (N : ℝ))) :=
        mul_le_mul_of_nonneg_right
          (mul_le_mul_of_nonneg_right hB_sq_lb (Real.exp_pos _).le) (Real.exp_pos _).le
    _ = μ.real B_L * c_KW := by dsimp [c_KW]; ring
    _ ≤ ‖T_raw‖ := h_div_le

/-- **Explicit Spectral-Gap Upper Bound & Convergence to `0` (`0 sorry`):**
    On `fullRankCubicNonAbelianWilsonSetup L N hN β hβ`, as `(L³ log β) / β → 0`
    (with `exp(c L³) / β² → 0`), `S.Δ → 0`. -/
theorem fullRankCubic_gap_upper_bound (L N : ℕ) [NeZero L] (hN : 2 ≤ N)""",
        1,
    ),
    # 5. Scope `linarith` in `hgap_sum`, `h_part2`, and final conclusion of `fullRankCubic_gap_upper_bound`
    (
        """      have hg := S.gap (ψ i j) (hψ_orth i j)
      have ha1 : S.a = 1 := rfl
      rw [ha1, mul_one] at hg
      linarith""",
        """      have hg := S.gap (ψ i j) (hψ_orth i j)
      have ha1 : S.a = 1 := rfl
      rw [ha1, mul_one] at hg
      linarith only [hg]""",
        1,
    ),
    (
        """        have hnonneg : 0 ≤ (N : ℝ) * Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ)) *
            ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) *
            β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by positivity
        linarith""",
        """        have hnonneg : 0 ≤ (N : ℝ) * Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ)) *
            ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) *
            β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by positivity
        linarith only [hnonneg]""",
        1,
    ),
    (
        """      _ ≤ 2 * ε_sq + 8 * (N : ℝ) * Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ)) *
            ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) *
            β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by linarith [h_part1, h_part2]
      _ = (N : ℝ) * err := h_N_err.symm
  have h1_sub : 1 - err ≤ Real.exp (-S.Δ) := by
    have hle : 1 - Real.exp (-S.Δ) ≤ err :=
      (mul_le_mul_iff_left₀ hN_pos).mp (by linarith)
    linarith
  have hlog : Real.log (1 - err) ≤ -S.Δ := by
    calc Real.log (1 - err) ≤ Real.log (Real.exp (-S.Δ)) :=
          Real.log_le_log (by linarith) h1_sub
      _ = -S.Δ := Real.log_exp _
  linarith""",
        """      _ ≤ 2 * ε_sq + 8 * (N : ℝ) * Real.exp (30 * (L : ℝ) ^ 3 / (N : ℝ)) *
            ((K : ℝ) ^ (2 * N * N)) ^ (2 * links) *
            β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2)) := by linarith only [h_part1, h_part2]
      _ = (N : ℝ) * err := h_N_err.symm
  have h1_sub : 1 - err ≤ Real.exp (-S.Δ) := by
    have hle : 1 - Real.exp (-S.Δ) ≤ err :=
      (mul_le_mul_iff_left₀ hN_pos).mp (by linarith only [h_gap_err])
    linarith only [hle]
  have herr_pos : 0 < 1 - err := by linarith only [herr_lt]
  have hlog : Real.log (1 - err) ≤ -S.Δ := by
    calc Real.log (1 - err) ≤ Real.log (Real.exp (-S.Δ)) :=
          Real.log_le_log herr_pos h1_sub
      _ = -S.Δ := Real.log_exp _
  linarith only [hlog]""",
        1,
    ),
]

for idx, (old, new, expected_count) in enumerate(patches, 1):
    count = text.count(old)
    assert count == expected_count, f"Patch {idx}: expected {expected_count} match(es), found {count}"
    text = text.replace(old, new)

start_marker = "  -- 3. `ε/δ` split & `lam0` Haar-ball lower bound\n"
end_marker = "  -- Combine Dirichlet inequality, `hF3_int_le`, and `hlam0_lb`\n"
assert text.count(start_marker) == 1, "start_marker mismatch"
assert text.count(end_marker) == 1, "end_marker mismatch"
i0 = text.index(start_marker)
i1 = text.index(end_marker)
assert i0 < i1

replacement_mid = """  -- 3. `ε/δ` split & `lam0` Haar-ball lower bound via precomputed lemmas
  let C_bad : ℝ := 4 * (N : ℝ) * Real.exp (β * (links : ℝ)) *
    β ^ (-(6 * (N : ℝ) ^ 2 * (links : ℝ) + 2))
  have hC_bad_nn : 0 ≤ C_bad := by dsimp [C_bad]; positivity
  have hF3_int_le :
      ∫ q : (G_L × G_L) × G_L, F3 q ∂((μ.prod μ).prod μ) ≤ 4 * ε_sq * lam0 + C_bad :=
    fullRank_dirichlet_eps_bound L N hN hβ ω hgs.ω_cont hgs.ω_pos lam0 h_eig_ω hω_sq_int hω_int1
  have hlam0_lb :
      (((K : ℝ) ^ (2 * N * N)) ^ (2 * links))⁻¹ * Real.exp (β * (links : ℝ)) *
          Real.exp (-(30 * (L : ℝ) ^ 3 / (N : ℝ))) ≤ lam0 :=
    fullRank_lam0_haar_lb L N hN hβ T_raw
      (fun ψ => wilsonIntegralOp_apply_ae L N β hβ_pos.le K_kin hK_cont hK_nn
        ((linkChiUb L β) ^ 2) (sq_nonneg _) hK_bd ψ)
      (fun ψ U => wilsonKernel_mul_integrable L N β hβ_pos.le K_kin hK_cont hK_nn
        ((linkChiUb L β) ^ 2) hK_bd ψ U)
"""
text = text[:i0] + replacement_mid + text[i1:]

path.write_text(text)
print("Successfully refactored", path)
EOF