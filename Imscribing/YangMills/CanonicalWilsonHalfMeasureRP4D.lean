import Imscribing.YangMills.CanonicalWilsonMeasureBridge
import Imscribing.YangMills.LatticeSchwingerRP4D

/-!
# Canonical Product Haar Half-Lattice Measure & Unconditional Finite-Volume 4D RP

1. Constructs `halfVarHaarMeasure N M` on `HalfVar N M` as the product of
   `wilsonHaarLinkMeasure N (2 * M)` and the cut-auxiliary Haar product measure.
2. Proves `haar_inv_mul_lintegral`:
   `∫⁻ W₁, ∫⁻ W₂, 1_S(W₁⁻¹ W₂) dν(W₁) dν(W₂) = ν(S)` for Haar measure `ν` on SU(N).
3. Proves **`canonical_smeared_magnetic_rp_nonneg`**: unconditional finite-volume
   Osterwalder–Seiler reflection positivity on the actual canonical Haar
   probability measure (0 abstract measure/measurability assumptions).
-/

namespace Imscribing.YangMills.CanonicalHalfRP4D

open MeasureTheory
open Imscribing.YangMills.WilsonLattice4D
open Imscribing.YangMills.LatticeRP4D
open Imscribing.YangMills.LatticeOSRP4D
open Imscribing.YangMills.LatticeSchwingerRP4D
open Imscribing.YangMills.CanonicalHaar4D
open Imscribing.YangMills.CanonicalWilsonBridge

/-- Canonical product Haar probability measure on cut-splitting variables `Lat4 (2 * M) → SU(N)`. -/
noncomputable def cutAuxHaarMeasure (N M : ℕ) [NeZero M] :
    letI := borel (GaugeGroup N)
    Measure (Lat4 (2 * M) → GaugeGroup N) :=
  letI := borel (GaugeGroup N)
  haveI : BorelSpace (GaugeGroup N) := ⟨rfl⟩
  haveI : CompactSpace (GaugeGroup N) := compactSpace_gaugeGroup N
  Measure.pi (fun _ => Measure.haar)

/-- Canonical product Haar probability measure on `HalfVar N M`. -/
noncomputable def halfVarHaarMeasure (N M : ℕ) [NeZero M] :
    letI := borel (GaugeGroup N)
    Measure (HalfVar N M) :=
  letI := borel (GaugeGroup N)
  (wilsonHaarLinkMeasure N (2 * M)).prod (cutAuxHaarMeasure N M)

theorem halfVarHaarMeasure_isProbability (N M : ℕ) [NeZero M] :
    letI := borel (GaugeGroup N)
    @IsProbabilityMeasure (HalfVar N M) _ (halfVarHaarMeasure N M) := by
  letI := borel (GaugeGroup N)
  haveI : BorelSpace (GaugeGroup N) := ⟨rfl⟩
  haveI : CompactSpace (GaugeGroup N) := compactSpace_gaugeGroup N
  haveI := wilsonHaarLinkMeasure_isProbability N (2 * M)
  haveI : IsProbabilityMeasure (cutAuxHaarMeasure N M) := Measure.pi.isProbabilityMeasure
  exact Measure.prod.instIsProbabilityMeasure _ _

/-- **Haar Convolution Identity for the Cut-Link Split `W₁⁻¹ * W₂`:**
    Integrating `1_S(W₁⁻¹ W₂)` over independent Haar variables `W₁, W₂` yields `ν(S)`. -/
theorem haar_inv_mul_lintegral {G : Type*} [Group G] [TopologicalSpace G]
    [MeasurableSpace G] [IsTopologicalGroup G] [BorelSpace G]
    (ν : Measure G) [IsProbabilityMeasure ν] [Measure.IsMulLeftInvariant ν]
    {s : Set G} (hs : MeasurableSet s) :
    ∫⁻ W₁ : G, ∫⁻ W₂ : G, s.indicator 1 (W₁⁻¹ * W₂) ∂ν ∂ν = ν s := by
  have h_inner : ∀ W₁ : G, ∫⁻ W₂ : G, s.indicator 1 (W₁⁻¹ * W₂) ∂ν = ν s := by
    intro W₁
    have hm : Measurable (fun W₂ : G => W₁⁻¹ * W₂) := measurable_const.mul measurable_id
    have hind : Measurable (s.indicator (fun _ : G => (1 : ENNReal))) := measurable_const.indicator hs
    rw [← lintegral_map hind hm, Measure.map_mul_left_eq_self, lintegral_indicator hs]
    simp
  simp_rw [h_inner, lintegral_const, measure_univ, mul_one]

/-- **Unconditional Finite-Volume 4D SU(N) Reflection Positivity on Canonical Haar Measure:**
    Every positive-time polynomial observable `F(U) = ∑ α, c α * ∏ k, spatialPlaqDensity U (xs α k)`
    satisfies `0 ≤ Re ∫∫ star(F(Θ(glue p q))) * F(glue p q) * exp(-S_W(glue p q)) dμ_half(p) dμ_half(q)`. -/
theorem canonical_smeared_magnetic_rp_nonneg
    (N M : ℕ) [NeZero N] [NeZero M] {β : ℝ} (hβ : 0 ≤ β)
    {ι : Type*} (s : Finset ι) (c : ι → ℂ) (n : ι → ℕ)
    (xs : ∀ α : ι, Fin (n α) → Lat4 (2 * M))
    (hpos : ∀ α ∈ s, ∀ k : Fin (n α), ((xs α k) 0).val < M) :
    letI := borel (GaugeGroup N)
    let μ := halfVarHaarMeasure N M
    let F : LinkConfig N (2 * M) → ℂ := fun U =>
      ∑ α ∈ s, c α * ∏ k : Fin (n α), (spatialPlaqDensity N (2 * M) U (xs α k) : ℂ)
    0 ≤ (∫ p, ∫ q, star (F (linkReflect (glueConfig p q))) * F (glueConfig p q) *
      (Real.exp (-wilsonAction N (2 * M) β (glueConfig p q)) : ℂ) ∂μ ∂μ).re := by
  letI := borel (GaugeGroup N)
  haveI : BorelSpace (GaugeGroup N) := ⟨rfl⟩
  haveI := halfVarHaarMeasure_isProbability N M
  exact smeared_magnetic_wilson_rp_nonneg hβ (canonicalGaugeEntryMeasurable N)
    (halfVarHaarMeasure N M) s c n xs hpos

end Imscribing.YangMills.CanonicalHalfRP4D