#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path("Imscribing/YangMills")


def write_file(rel: str, content: str) -> None:
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"[WROTE] {p}")


def write_if_missing(rel: str, content: str) -> None:
    p = ROOT / rel
    if p.exists():
        print(f"[SKIP exists] {p}")
        return
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"[CREATED] {p}")


def patch_file(rel: str, transforms: list[tuple[str, str, str]]) -> None:
    p = ROOT / rel
    if not p.exists():
        print(f"[MISSING] {p}")
        return
    text = p.read_text(encoding="utf-8")
    orig = text
    for desc, old, new in transforms:
        if old in text:
            text = text.replace(old, new)
            print(f"[PATCHED] {p}: {desc}")
        else:
            print(f"[NOTE] {p}: pattern not found for ({desc})")
    text2 = re.sub(r"\n#print axioms\s*$", "\n", text)
    if text2 != text:
        text = text2
        print(f"[PATCHED] {p}: removed bare #print axioms")
    if text != orig:
        p.write_text(text, encoding="utf-8")


SEMIGROUP_CFC = '''import Mathlib.Analysis.CStarAlgebra.ContinuousLinearMap
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Basic
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Instances
import Mathlib.Analysis.CStarAlgebra.Spectrum
import Mathlib.Analysis.InnerProductSpace.Projection
import Mathlib.Analysis.NormedSpace.Extend
import Mathlib.Topology.ContinuousMap.StoneWeierstrass
import Imscribing.YangMills.SpatialISO3UnitariesOnOS

/-!
# Direct Minkowski Time-Translation Unitary Group from Any OS Contraction Semigroup

Constructs `U₀ : ℝ → H →ₗᵢ[ℂ] H` (`exp(-i s H)`) directly from any strongly
continuous symmetric contraction semigroup `T : ℝ → H →L[ℂ] H` using the
C⋆-algebra `continuousFunctionalCalculus` on `A = T 1` (`0 sorry`).
-/

namespace Imscribing.YangMills.SemigroupCFC

open scoped InnerProductSpace Topology
open Imscribing.YangMills.ClaySpec
open Imscribing.YangMills.OSBorchers
open Imscribing.YangMills.BorchersReconstruction
open Imscribing.YangMills.UnitaryExtension
open Imscribing.YangMills.SpatialISO3Unitaries

section CFCTimeGroup

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

private lemma clm_isSelfAdjoint_of_symm (M : H →L[ℂ] H)
    (h_symm : ∀ x y : H, ⟪x, M y⟫_ℂ = ⟪M x, y⟫_ℂ) :
    IsSelfAdjoint M := by
  rw [IsSelfAdjoint, ContinuousLinearMap.star_eq_adjoint]
  apply ContinuousLinearMap.ext
  intro y
  apply ext_inner_left ℂ
  intro x
  rw [ContinuousLinearMap.adjoint_inner_right, h_symm x y]
'''

BOUNDARY_LIMIT = '''import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.Distribution.SchwartzSpace.Deriv
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Topology.MetricSpace.Cauchy

noncomputable section

namespace Imscribing.YangMills.BoundaryLimit

open Filter Topology

/-- Bootstrapped MVT bound: if `g : ℝ → E` satisfies `HasDerivAt g (g' t) t` with
`‖g' t‖ ≤ C * t ^ (-p)` on `(0, δ)` for `0 ≤ p < 1`, then for `0 < a ≤ b < δ`,
`‖g b - g a‖ ≤ (C / (1 - p)) * (b ^ (1 - p) - a ^ (1 - p))`. -/
theorem norm_sub_le_rpow_of_hasDerivAt {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {g g' : ℝ → E} {δ C p : ℝ} (hδ : 0 < δ) (hC : 0 ≤ C) (hp0 : 0 ≤ p) (hp1 : p < 1)
    (h_deriv : ∀ t ∈ Set.Ioo 0 δ, HasDerivAt g (g' t) t)
    (h_bound : ∀ t ∈ Set.Ioo 0 δ, ‖g' t‖ ≤ C * t ^ (-p))
    {a b : ℝ} (ha : 0 < a) (hab : a ≤ b) (hb : b < δ) :
    ‖g b - g a‖ ≤ (C / (1 - p)) * (b ^ (1 - p) - a ^ (1 - p)) := by
  have h1p : 0 < 1 - p := sub_pos.mpr hp1
  have h_cont_g : ContinuousOn g (Set.Icc a b) := by
    intro t ht
    have ht_oo : t ∈ Set.Ioo 0 δ := ⟨lt_of_lt_of_le ha ht.1, lt_of_le_of_lt ht.2 hb⟩
    exact (h_deriv t ht_oo).continuousAt.continuousWithinAt
  have h_rpow_deriv : ∀ t : ℝ, 0 < t →
      HasDerivAt (fun s : ℝ => s ^ (1 - p)) ((1 - p) * t ^ (-p)) t := by
    intro t ht
    have hd := Real.hasDerivAt_rpow_const (p := 1 - p) (Or.inl ht.ne')
    simpa [sub_sub_cancel_left, neg_eq_zero_sub] using hd
  have h_cont_rpow : ContinuousOn (fun t : ℝ => t ^ (1 - p)) (Set.Icc a b) := by
    intro t ht
    exact (h_rpow_deriv t (lt_of_lt_of_le ha ht.1)).continuousAt.continuousWithinAt
  suffices h_eps : ∀ ε > 0,
      ‖g b - g a‖ ≤ (C / (1 - p)) * (b ^ (1 - p) - a ^ (1 - p)) + ε * (b - a) by
    refine le_of_forall_pos_le_add fun ε hε => ?_
    by_cases hba : b - a = 0
    · have : a = b := by linarith
      subst this; simp
    · have hba_pos : 0 < b - a := lt_of_le_of_ne (sub_nonneg.mpr hab) (Ne.symm hba)
      have h1 := h_eps (ε / (b - a)) (div_pos hε hba_pos)
      rwa [div_mul_cancel₀ _ hba_pos.ne'] at h1
  intro ε hε
  let φ : ℝ → ℝ := fun t => (C / (1 - p)) * (t ^ (1 - p) - a ^ (1 - p)) + ε * (t - a)
  let S : Set ℝ := {t ∈ Set.Icc a b | ‖g t - g a‖ ≤ φ t}
  have ha_mem : a ∈ S := ⟨⟨le_rfl, hab⟩, by simp [φ]⟩
  have hS_closed : IsClosed S := by
    refine isClosed_Icc.inter ?_
    exact isClosed_le ((h_cont_g.sub continuousOn_const).norm)
      (ContinuousOn.add
        (continuousOn_const.mul (h_cont_rpow.sub continuousOn_const))
        (continuousOn_const.mul (continuousOn_id.sub continuousOn_const)))
  have hS_bdd : BddAbove S := ⟨b, fun _ ht => ht.1.2⟩
  let c : ℝ := sSup S
  have hc_mem : c ∈ S := hS_closed.csSup_mem ⟨a, ha_mem⟩ hS_bdd
  have hc_le : c ≤ b := hc_mem.1.2
  have hc_ge : a ≤ c := hc_mem.1.1
  by_contra! h_gt
  have hc_lt : c < b := lt_of_le_of_ne hc_le (by
    rintro rfl
    exact not_le_of_gt h_gt hc_mem.2)
  have hc_oo : c ∈ Set.Ioo 0 δ := ⟨lt_of_lt_of_le ha hc_ge, lt_trans hc_lt hb⟩
  have hc_pos : 0 < c := hc_oo.1
  have h_deriv_g := h_deriv c hc_oo
  have h_deriv_φ : HasDerivAt φ (C * c ^ (-p) + ε) c := by
    have hr := (h_rpow_deriv c hc_pos).sub_const (a ^ (1 - p))
    have hmul := hr.const_mul (C / (1 - p))
    have he := (hasDerivAt_id c).sub_const a |>.const_mul ε
    convert hmul.add he using 1
    field_simp [h1p.ne']
    ring
  have hg_close : ∀ᶠ t in 𝓝[>] c, ‖g t - g c‖ ≤ (‖g' c‖ + ε / 4) * (t - c) := by
    have h_diff := h_deriv_g.isLittleO
    have h_ev := h_diff.bound (show 0 < ε / 4 by linarith)
    filter_upwards [nhdsWithin_le_nhds h_ev, self_mem_nhdsWithin] with t ht ht_gt
    have htc : 0 < t - c := sub_pos.mpr ht_gt
    have h1 := norm_sub_norm_le (g t - g c) ((t - c) • g' c)
    have h2 : ‖(t - c) • g' c‖ = (t - c) * ‖g' c‖ := by
      rw [norm_smul, Real.norm_of_nonneg htc.le]
    have h3 : ‖g t - g c - (t - c) • g' c‖ ≤ ε / 4 * ‖t - c‖ := by
      simpa [smul_eq_mul] using ht
    rw [Real.norm_of_nonneg htc.le] at h3
    linarith [h1, h2, h3]
  have hφ_close : ∀ᶠ t in 𝓝[>] c, (C * c ^ (-p) + ε / 2) * (t - c) ≤ φ t - φ c := by
    have h_diff := h_deriv_φ.isLittleO
    have h_ev := h_diff.bound (show 0 < ε / 2 by linarith)
    filter_upwards [nhdsWithin_le_nhds h_ev, self_mem_nhdsWithin] with t ht ht_gt
    have htc : 0 < t - c := sub_pos.mpr ht_gt
    have h1 : ‖φ t - φ c - (t - c) * (C * c ^ (-p) + ε)‖ ≤ ε / 2 * ‖t - c‖ := by
      simpa [smul_eq_mul] using ht
    rw [Real.norm_eq_abs, Real.norm_eq_abs, abs_of_pos htc, abs_le] at h1
    linarith [h1.1]
  have hIoo : Set.Ioo c b ∈ 𝓝[>] c := Ioo_mem_nhdsGT hc_lt
  obtain ⟨t, ht_oo, hgt, hφt⟩ := (hIoo.and (hg_close.and hφ_close)).exists
  have ht_mem : t ∈ S := by
    refine ⟨⟨le_trans hc_ge ht_oo.1.le, ht_oo.2.le⟩, ?_⟩
    have htc : 0 < t - c := sub_pos.mpr ht_oo.1
    have hbnd := h_bound c hc_oo
    have h_tri : ‖g t - g a‖ ≤ ‖g t - g c‖ + ‖g c - g a‖ := by
      simpa using norm_add_le (g t - g c) (g c - g a)
    have h_step : (‖g' c‖ + ε / 4) * (t - c) ≤ (C * c ^ (-p) + ε / 2) * (t - c) := by
      gcongr; linarith
    linarith [h_tri, hgt, hφt, hc_mem.2, h_step]
  exact absurd (le_csSup hS_bdd ht_mem) (not_le_of_gt ht_oo.1)

/-- Existence and norm bound of the `ε → 0⁺` boundary limit from a polynomially singular
derivative bound `‖g' t‖ ≤ C * t ^ (-p)` with `0 ≤ p < 1`. -/
theorem boundary_value_of_deriv_bound {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [CompleteSpace E] {g g' : ℝ → E} {δ C p : ℝ}
    (hδ : 0 < δ) (hC : 0 ≤ C) (hp0 : 0 ≤ p) (hp1 : p < 1)
    (h_deriv : ∀ t ∈ Set.Ioo 0 δ, HasDerivAt g (g' t) t)
    (h_bound : ∀ t ∈ Set.Ioo 0 δ, ‖g' t‖ ≤ C * t ^ (-p)) :
    ∃ L : E, Filter.Tendsto g (𝓝[>] 0) (𝓝 L) ∧
      ∀ t ∈ Set.Ioo 0 δ, ‖L - g t‖ ≤ (C / (1 - p)) * t ^ (1 - p) := by
  have h1p : 0 < 1 - p := sub_pos.mpr hp1
  haveI : (𝓝[>] (0 : ℝ)).NeBot := nhdsWithin_Ioi_self_neBot
  have h_cauchy : Cauchy (Filter.map g (𝓝[>] 0)) := by
    rw [Metric.cauchy_iff]
    refine ⟨inferInstance, fun ε hε => ?_⟩
    have hcoeff : 0 < C / (1 - p) + 1 := by positivity
    let r : ℝ := min (δ / 2) ((ε / (2 * (C / (1 - p) + 1))) ^ (1 / (1 - p)))
    have hr_pos : 0 < r := lt_min (half_pos hδ) (Real.rpow_pos_of_pos (by positivity) _)
    refine ⟨g '' Set.Ioo 0 r, Filter.mem_map.mpr (Filter.mem_of_superset (Ioo_mem_nhdsGT hr_pos)
      (fun t ht => ⟨t, ht, rfl⟩)), ?_⟩
    rintro _ ⟨t₁, ht₁, rfl⟩ _ ⟨t₂, ht₂, rfl⟩
    wlog h12 : t₁ ≤ t₂
    · rw [dist_comm]; exact this hδ hC hp0 hp1 h_deriv h_bound ε hε r hr_pos t₂ ht₂ t₁ ht₁ (le_of_not_ge h12)
    have ht₂_lt : t₂ < δ := lt_of_lt_of_le ht₂.2 (le_trans (min_le_left _ _) (half_lt_self hδ).le)
    have hMVT := norm_sub_le_rpow_of_hasDerivAt hδ hC hp0 hp1 h_deriv h_bound ht₁.1 h12 ht₂_lt
    have hr_le : t₂ ^ (1 - p) ≤ r ^ (1 - p) :=
      Real.rpow_le_rpow ht₂.1.le ht₂.2.le h1p.le
    have hr2 : r ^ (1 - p) ≤ ε / (2 * (C / (1 - p) + 1)) := by
      calc r ^ (1 - p)
          ≤ ((ε / (2 * (C / (1 - p) + 1))) ^ (1 / (1 - p))) ^ (1 - p) :=
            Real.rpow_le_rpow hr_pos.le (min_le_right _ _) h1p.le
        _ = ε / (2 * (C / (1 - p) + 1)) := by
            rw [← Real.rpow_mul (by positivity), one_div_mul_cancel h1p.ne', Real.rpow_one]
    have ht₁_nn : 0 ≤ t₁ ^ (1 - p) := Real.rpow_nonneg ht₁.1.le _
    rw [dist_eq_norm, norm_sub_rev]
    calc ‖g t₂ - g t₁‖
        ≤ (C / (1 - p)) * (t₂ ^ (1 - p) - t₁ ^ (1 - p)) := hMVT
      _ ≤ (C / (1 - p)) * t₂ ^ (1 - p) := by gcongr; linarith
      _ ≤ (C / (1 - p)) * (ε / (2 * (C / (1 - p) + 1))) := by gcongr; exact le_trans hr_le hr2
      _ ≤ (C / (1 - p) + 1) * (ε / (2 * (C / (1 - p) + 1))) := by gcongr; linarith
      _ = ε / 2 := by field_simp [hcoeff.ne']
      _ < ε := half_lt_self hε
  obtain ⟨L, hL⟩ := CompleteSpace.complete h_cauchy
  refine ⟨L, hL, fun t ht => ?_⟩
  have h_ev : ∀ᶠ s in 𝓝[>] 0, s ∈ Set.Ioo 0 t := Ioo_mem_nhdsGT ht.1
  have h_le : ∀ᶠ s in 𝓝[>] 0, ‖g t - g s‖ ≤ (C / (1 - p)) * t ^ (1 - p) := by
    filter_upwards [h_ev] with s hs
    have hMVT := norm_sub_le_rpow_of_hasDerivAt hδ hC hp0 hp1 h_deriv h_bound hs.1 hs.2.le ht.2
    have hs_nn : 0 ≤ s ^ (1 - p) := Real.rpow_nonneg hs.1.le _
    calc ‖g t - g s‖ ≤ (C / (1 - p)) * (t ^ (1 - p) - s ^ (1 - p)) := hMVT
      _ ≤ (C / (1 - p)) * t ^ (1 - p) := by gcongr; linarith
  have h_tend : Filter.Tendsto (fun s => ‖g t - g s‖) (𝓝[>] 0) (𝓝 ‖g t - L‖) :=
    (tendsto_const_nhds.sub hL).norm
  simpa [norm_sub_rev] using le_of_tendsto h_tend h_le

/-- Tempered boundary distribution extracted from a family of continuous linear functionals
on a Schwartz space satisfying a uniform seminorm-controlled singular derivative bound. -/
theorem wightman_boundary_tempered {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (W_reg W_deriv : ℝ → SchwartzMap E ℂ →L[ℂ] ℂ)
    {δ : ℝ} (hδ : 0 < δ) {p : ℝ} (hp0 : 0 ≤ p) (hp1 : p < 1)
    {C : ℝ} (hC : 0 ≤ C) {k m : ℕ}
    (h_deriv : ∀ f : SchwartzMap E ℂ, ∀ t ∈ Set.Ioo 0 δ,
      HasDerivAt (fun s => W_reg s f) (W_deriv t f) t)
    (h_bound : ∀ f : SchwartzMap E ℂ, ∀ t ∈ Set.Ioo 0 δ,
      ‖W_deriv t f‖ ≤ C * (SchwartzMap.seminorm ℂ k m f) * t ^ (-p))
    {C₀ : ℝ} (hC₀ : 0 ≤ C₀) {k₀ m₀ : ℕ} {t₀ : ℝ} (ht₀ : t₀ ∈ Set.Ioo 0 δ)
    (h_init : ∀ f : SchwartzMap E ℂ, ‖W_reg t₀ f‖ ≤ C₀ * SchwartzMap.seminorm ℂ k₀ m₀ f) :
    ∃ W₀ : SchwartzMap E ℂ →ₗ[ℂ] ℂ,
      (∀ f, Filter.Tendsto (fun t => W_reg t f) (𝓝[>] 0) (𝓝 (W₀ f))) ∧
      (∀ f, ‖W₀ f‖ ≤
        (C / (1 - p)) * t₀ ^ (1 - p) * SchwartzMap.seminorm ℂ k m f +
        C₀ * SchwartzMap.seminorm ℂ k₀ m₀ f) := by
  have h_lim : ∀ f : SchwartzMap E ℂ,
      ∃ L : ℂ, Filter.Tendsto (fun t => W_reg t f) (𝓝[>] 0) (𝓝 L) ∧
        ‖L - W_reg t₀ f‖ ≤ (C * SchwartzMap.seminorm ℂ k m f / (1 - p)) * t₀ ^ (1 - p) := by
    intro f
    have hCf : 0 ≤ C * SchwartzMap.seminorm ℂ k m f :=
      mul_nonneg hC (apply_nonneg (SchwartzMap.seminorm ℂ k m) f)
    obtain ⟨L, hL, hLbd⟩ := boundary_value_of_deriv_bound hδ hCf hp0 hp1
      (h_deriv f) (h_bound f)
    exact ⟨L, hL, hLbd t₀ ht₀⟩
  let W₀Fun : SchwartzMap E ℂ → ℂ := fun f => Classical.choose (h_lim f)
  have hW₀_tend : ∀ f, Filter.Tendsto (fun t => W_reg t f) (𝓝[>] 0) (𝓝 (W₀Fun f)) :=
    fun f => (Classical.choose_spec (h_lim f)).1
  refine ⟨{
    toFun := W₀Fun
    map_add' := fun f g => by
      have h1 := (hW₀_tend f).add (hW₀_tend g)
      have h2 : Filter.Tendsto (fun t => W_reg t (f + g)) (𝓝[>] 0) (𝓝 (W₀Fun f + W₀Fun g)) := by
        simpa [map_add] using h1
      exact tendsto_nhds_unique (hW₀_tend (f + g)) h2
    map_smul' := fun c f => by
      have h1 := tendsto_const_nhds.mul (hW₀_tend f)
      have h2 : Filter.Tendsto (fun t => W_reg t (c • f)) (𝓝[>] 0) (𝓝 (c * W₀Fun f)) := by
        simpa [map_smul, smul_eq_mul] using h1
      exact tendsto_nhds_unique (hW₀_tend (c • f)) h2
  }, hW₀_tend, fun f => ?_⟩
  have h_diff := (Classical.choose_spec (h_lim f)).2
  have h_tri : ‖W₀Fun f‖ ≤ ‖W₀Fun f - W_reg t₀ f‖ + ‖W_reg t₀ f‖ := by
    simpa using norm_add_le (W₀Fun f - W_reg t₀ f) (W_reg t₀ f)
  have h_alg : (C * SchwartzMap.seminorm ℂ k m f / (1 - p)) * t₀ ^ (1 - p) =
      (C / (1 - p)) * t₀ ^ (1 - p) * SchwartzMap.seminorm ℂ k m f := by ring
  linarith [h_tri, h_diff, h_init f, h_alg]

end Imscribing.YangMills.BoundaryLimit
'''

write_file("SemigroupToUnitaryGroupCFC.lean", SEMIGROUP_CFC)
write_if_missing("BoundaryDistributionLimit.lean", BOUNDARY_LIMIT)

patch_file("LorentzBoostAndMinkowskiFields.lean", [
    ("deprecated SchwartzSpace import",
     "import Mathlib.Analysis.Distribution.SchwartzSpace",
     "import Mathlib.Analysis.Distribution.SchwartzSpace.Deriv"),
])

patch_file("OSPoincareMasterDischarge.lean", [])

patch_file("CanonicalLatticeBorchers4D.lean", [
    ("prove canonicalMagneticSchwinger_perm_symm",
     '''theorem canonicalMagneticSchwinger_perm_symm (N L n : ℕ) [NeZero N] [NeZero L]
    (a β Z_ren : ℝ) (π : Equiv.Perm (Fin n)) (f f_π : EuclideanSchwartz n)
    (hf : ∀ y : Fin n → Spacetime4, f_π y = f (fun k => y (π k))) :
    canonicalMagneticSchwinger N L n a β Z_ren f_π =
      canonicalMagneticSchwinger N L n a β Z_ren f := by
  sorry''',
     '''theorem canonicalMagneticSchwinger_perm_symm (N L n : ℕ) [NeZero N] [NeZero L]
    (a β Z_ren : ℝ) (π : Equiv.Perm (Fin n)) (f f_π : EuclideanSchwartz n)
    (hf : ∀ y : Fin n → Spacetime4, f_π y = f (fun k => y (π k))) :
    canonicalMagneticSchwinger N L n a β Z_ren f_π =
      canonicalMagneticSchwinger N L n a β Z_ren f := by
  dsimp [canonicalMagneticSchwinger]
  congr 1
  let e : (Fin n → Lat4 L) ≃ (Fin n → Lat4 L) :=
    { toFun := fun xs k => xs (π.symm k)
      invFun := fun xs k => xs (π k)
      left_inv := fun xs => by funext k; simp
      right_inv := fun xs => by funext k; simp }
  refine Fintype.sum_equiv e _ _ fun xs => ?_
  have hf_eq : f_π (fun k => centeredLatSite L a (xs k)) =
      f (fun k => centeredLatSite L a (e xs k)) := by
    rw [hf]
    congr 1
    funext k
    simp [e]
  have hprod_eq : (fun U : LinkConfig N L => (∏ k : Fin n, spatialPlaqDensity N L U (xs k) : ℂ)) =
      (fun U : LinkConfig N L => (∏ k : Fin n, spatialPlaqDensity N L U (e xs k) : ℂ)) := by
    funext U
    exact (Fintype.prod_equiv π.symm _ _ fun k => by simp [e]).symm
  rw [hf_eq, hprod_eq]'''),
])

patch_file("CanonicalFiniteVolumeBorchers4D.lean", [
    ("prove latticeBorchersForm_cauchy_schwarz",
     '''theorem latticeBorchersForm_cauchy_schwarz (N M : ℕ) [NeZero N] [NeZero M]
    (a : ℝ) {β : ℝ} (hβ : 0 ≤ β) (Z_ren : ℝ) (F G : BorchersPos) :
    ‖latticeBorchersForm N M a β Z_ren F G‖ ^ 2 ≤
      (latticeBorchersForm N M a β Z_ren F F).re *
      (latticeBorchersForm N M a β Z_ren G G).re := by
  sorry''',
     '''theorem latticeBorchersForm_cauchy_schwarz (N M : ℕ) [NeZero N] [NeZero M]
    (a : ℝ) {β : ℝ} (hβ : 0 ≤ β) (Z_ren : ℝ) (F G : BorchersPos) :
    ‖latticeBorchersForm N M a β Z_ren F G‖ ^ 2 ≤
      (latticeBorchersForm N M a β Z_ren F F).re *
      (latticeBorchersForm N M a β Z_ren G G).re := by
  let B := latticeBorchersForm N M a β Z_ren
  obtain ⟨h_add1, h_smul1, h_add2, h_smul2⟩ := latticeBorchersForm_sesquilinear N M a hβ Z_ren
  have h_quad : ∀ u v : ℂ,
      0 ≤ (star u * u * B F F + star u * v * B F G +
           star v * u * star (B F G) + star v * v * B G G).re := by
    intro u v
    have h_nn := latticeBorchersForm_nonneg N M a hβ Z_ren (u • F + v • G)
    change 0 ≤ (B (u • F + v • G) (u • F + v • G)).re at h_nn
    rw [h_add1, h_add2, h_add2, h_smul1, h_smul1, h_smul2, h_smul2, h_smul2, h_smul2,
      latticeBorchersForm_herm N M a hβ Z_ren F G] at h_nn
    convert h_nn using 2
    ring
  have hFF_nn : 0 ≤ (B F F).re := latticeBorchersForm_nonneg N M a hβ Z_ren F
  have hGG_nn : 0 ≤ (B G G).re := latticeBorchersForm_nonneg N M a hβ Z_ren G
  have h_re_real : ∀ (r : ℝ) (z : ℂ), (((r : ℂ) * z)).re = r * z.re := by
    intro r z; simp
  have h_nsq_self : ∀ z : ℂ, star z * z = ((‖z‖ ^ 2 : ℝ) : ℂ) := by
    intro z
    rw [mul_comm, RCLike.star_def, Complex.mul_conj]
    norm_cast
    exact Complex.normSq_eq_norm_sq z
  by_cases hFF0 : (B F F).re = 0
  · by_cases hFG0 : ‖B F G‖ = 0
    · rw [hFG0]; simp; positivity
    · exfalso
      let r : ℝ := -((B G G).re + 1) / (2 * ‖B F G‖ ^ 2)
      have hq := h_quad ((r : ℂ) * B F G) 1
      have h1 : star ((r : ℂ) * B F G) * ((r : ℂ) * B F G) =
          (((r * ‖B F G‖) ^ 2 : ℝ) : ℂ) := by
        rw [star_mul, Complex.star_def, Complex.conj_ofReal]
        calc ((r : ℂ) * star (B F G)) * ((r : ℂ) * B F G)
            = ((r : ℂ) * (r : ℂ)) * (star (B F G) * B F G) := by ring
          _ = ((r ^ 2 : ℝ) : ℂ) * ((‖B F G‖ ^ 2 : ℝ) : ℂ) := by
              rw [h_nsq_self]; push_cast; ring
          _ = (((r * ‖B F G‖) ^ 2 : ℝ) : ℂ) := by push_cast; ring
      have h2 : star ((r : ℂ) * B F G) * 1 * B F G = ((r * ‖B F G‖ ^ 2 : ℝ) : ℂ) := by
        rw [star_mul, Complex.star_def, Complex.conj_ofReal, mul_one, mul_assoc, h_nsq_self]
        push_cast; rfl
      have h3 : star (1 : ℂ) * ((r : ℂ) * B F G) * star (B F G) =
          ((r * ‖B F G‖ ^ 2 : ℝ) : ℂ) := by
        rw [star_one, one_mul, mul_assoc, mul_comm (B F G), h_nsq_self]
        push_cast; rfl
      rw [h1, h2, h3] at hq
      simp only [star_one, one_mul, Complex.add_re, h_re_real, hFF0, mul_zero, zero_add,
        Complex.ofReal_re] at hq
      have hFG2 : 0 < 2 * ‖B F G‖ ^ 2 := by positivity
      have hr : 2 * (r * ‖B F G‖ ^ 2) = -((B G G).re + 1) := by
        dsimp [r]; field_simp [hFG2.ne']; ring
      linarith
  · have hFF_pos : 0 < (B F F).re := lt_of_le_of_ne hFF_nn (Ne.symm hFF0)
    have hq := h_quad (B F G) (-((B F F).re : ℂ))
    have h1 : star (B F G) * B F G = ((‖B F G‖ ^ 2 : ℝ) : ℂ) := h_nsq_self _
    have h2 : star (B F G) * (-((B F F).re : ℂ)) * B F G =
        ((-(B F F).re * ‖B F G‖ ^ 2 : ℝ) : ℂ) := by
      calc star (B F G) * (-((B F F).re : ℂ)) * B F G
          = (-((B F F).re : ℂ)) * (star (B F G) * B F G) := by ring
        _ = ((-(B F F).re * ‖B F G‖ ^ 2 : ℝ) : ℂ) := by rw [h1]; push_cast; ring
    have h3 : star (-((B F F).re : ℂ)) * B F G * star (B F G) =
        ((-(B F F).re * ‖B F G‖ ^ 2 : ℝ) : ℂ) := by
      rw [star_neg, Complex.star_def, Complex.conj_ofReal]
      calc (-((B F F).re : ℂ)) * B F G * star (B F G)
          = (-((B F F).re : ℂ)) * (star (B F G) * B F G) := by ring
        _ = ((-(B F F).re * ‖B F G‖ ^ 2 : ℝ) : ℂ) := by rw [h1]; push_cast; ring
    have h4 : star (-((B F F).re : ℂ)) * (-((B F F).re : ℂ)) =
        (((B F F).re ^ 2 : ℝ) : ℂ) := by
      rw [star_neg, Complex.star_def, Complex.conj_ofReal]
      push_cast; ring
    rw [h1, h2, h3, h4] at hq
    simp only [Complex.add_re, h_re_real, Complex.ofReal_re] at hq
    have h_factor : 0 ≤ (B F F).re * ((B F F).re * (B G G).re - ‖B F G‖ ^ 2) := by
      linarith
    nlinarith'''),
])

patch_file("BalabanRGToClayMaster.lean", [
    ("prove S_zero in h_fv_conv",
     "          S_zero := by sorry",
     """          S_zero := by
            have h_ev := h_lim 0 1
            have h_eq : (fun m => canonicalMagneticSchwinger N (2 * M_vol m) 0
                (ymSpacing m) (ymBetaAF N m) (Z_ren m) 1) = fun _ => (1 : ℂ) := by
              funext m
              exact canonicalMagneticSchwinger_zero N (2 * M_vol m) (ymSpacing m)
                (ymBetaAF_pos N hN m).le (Z_ren m)
            rw [h_eq] at h_ev
            exact tendsto_nhds_unique h_ev tendsto_const_nhds"""),
])

patch_file("ClayStatement.lean", [
    ("deprecated SchwartzSpace import",
     "import Mathlib.Analysis.Distribution.SchwartzSpace",
     "import Mathlib.Analysis.Distribution.SchwartzSpace.Deriv"),
    ("remove @[universe_polymorphic]",
     "@[universe_polymorphic]\n",
     ""),
    ("pin universe in ClayYangMillsConjecture",
     "HasYangMillsUVScaling N Q",
     "HasYangMillsUVScaling.{0, 0} N Q"),
])

patch_file("AsymptoticFreedomAndOSClosure.lean", [
    ("deprecated SchwartzSpace import",
     "import Mathlib.Analysis.Distribution.SchwartzSpace",
     "import Mathlib.Analysis.Distribution.SchwartzSpace.Deriv\nimport Mathlib.Analysis.InnerProductSpace.PiL2"),
    ("fix Filter.tendsto_natCast_atTop_atTop.add",
     "Filter.tendsto_natCast_atTop_atTop.add tendsto_const_nhds",
     "(Filter.tendsto_natCast_atTop_atTop.atTop_add tendsto_const_nhds)"),
    ("fix Real.log_pos in ymBetaAF_pos",
     "Real.log_pos h₃",
     "Real.log_pos (one_lt_one_div (ymSpacing_pos m) hsp)"),
    ("add One (EuclideanSchwartz 0) instance",
     "def EuclideanSchwartz (n : ℕ) := SchwartzMap (Fin n → Spacetime4) ℂ",
     """def EuclideanSchwartz (n : ℕ) := SchwartzMap (Fin n → Spacetime4) ℂ

noncomputable def vacTest0 : EuclideanSchwartz 0 where
  toFun := fun _ => (1 : ℂ)
  smooth' := contDiff_const
  decay' k n := by
    refine ⟨1, fun x => ?_⟩
    have hx : x = 0 := Subsingleton.elim x 0
    subst hx
    by_cases hk : k = 0 <;> by_cases hn : n = 0
    · subst hk; subst hn
      have h0 : ‖iteratedFDeriv ℝ 0 (fun _ : Fin 0 → Spacetime4 => (1 : ℂ)) 0‖ ≤ 1 := by
        refine ContinuousMultilinearMap.opNorm_le_bound _ zero_le_one (fun _ => ?_)
        simp [iteratedFDeriv_zero_apply]
      simpa using h0
    · subst hk; simp [iteratedFDeriv_const_of_ne hn]
    · subst hn; simp [zero_pow hk]
    · simp [zero_pow hk, iteratedFDeriv_const_of_ne hn]

noncomputable instance : One (EuclideanSchwartz 0) := ⟨vacTest0⟩"""),
])

patch_file("SemigroupGapBridge.lean", [
    ("RCLike.re_le_norm -> Complex.re_le_norm",
     "RCLike.re_le_norm",
     "Complex.re_le_norm"),
    ("replace innerSL with Filter.Tendsto.inner",
     "(innerSL ℂ ψ).continuousAt.tendsto.comp h_gen",
     "(tendsto_const_nhds.inner h_gen)"),
])

patch_file("PoincareLieAlgebraAndNelson.lean", [
    ("star Complex.I -> Complex.conj_I",
     "have hstar : star Complex.I = -Complex.I := by simp\n      rw [hstar]",
     "rw [Complex.conj_I]\n  ring"),
    ("MVT constant_of_hasDerivAt_zero",
     "Convex.norm_image_sub_le_of_norm_deriv_le",
     "convex_univ.norm_image_sub_le_of_norm_deriv_le"),
])

patch_file("TransferMatrixToSemigroup.lean", [
    ("supply x to h_unif",
     "le_of_tendsto h_norm h_unif",
     "le_of_tendsto h_norm (h_unif x)"),
    ("replace innerSL",
     "(innerSL ℂ x).continuousAt.tendsto.comp hy",
     "(tendsto_const_nhds.inner hy)"),
    ("replace continuous_id.inner",
     "(continuous_id.inner continuous_const).continuousAt.tendsto.comp hx",
     "(hx.inner tendsto_const_nhds)"),
    ("fix add_le_add_right operand order",
     "le_trans h_tri (add_le_add_right (hpow_contr m",
     "le_trans h_tri (add_le_add (hpow_contr m"),
])

patch_file("WilsonHaarCompactness4D.lean", [
    ("remove nonexistent Mathlib.Topology.Algebra.Matrix import",
     "import Mathlib.Topology.Algebra.Matrix\n",
     ""),
])

print("\nDone. Run: lake build")
