
import Imscribing.YangMills.CanonicalLatticeBorchers4D
import Imscribing.YangMills.LatticeChessboardAndTransfer4D

/-!
# Canonical Finite-Volume 4D SU(N) Borchers Sesquilinear Form
-/

namespace Imscribing.YangMills.CanonicalFVBorchers4D

open MeasureTheory
open Imscribing.YangMills.ClaySpec
open Imscribing.YangMills.ContinuumInterfaces
open Imscribing.YangMills.WilsonLattice4D
open Imscribing.YangMills.WilsonBounds4D
open Imscribing.YangMills.LatticeRP4D
open Imscribing.YangMills.LatticeCutSplit4D
open Imscribing.YangMills.LatticeOSRP4D
open Imscribing.YangMills.LatticeSchwingerRP4D
open Imscribing.YangMills.CenteredTranslation4D
open Imscribing.YangMills.CanonicalHaar4D
open Imscribing.YangMills.CanonicalWilsonBridge
open Imscribing.YangMills.CanonicalHalfRP4D
open Imscribing.YangMills.BorchersReconstruction
open Imscribing.YangMills.LatticeChessboardTransfer

private lemma reflectSite_sub_step0_cutMid (M : ℕ) [NeZero M] (x : Lat4 (2 * M))
    (hx : (x 0).val = M - 1) :
    reflectSite (2 * M) x - stepDir (2 * M) 0 = x := by
  have hM : 0 < M := NeZero.pos M
  ext ν
  by_cases hν : ν = 0
  · subst hν
    simp only [reflectSite, stepDir, Pi.sub_apply, ↓reduceIte]
    have h2 : 2 * (x 0 + 1) = 0 := by
      have hsub : 2 * ((x 0).val + 1) = 2 * M := by omega
      have hcast := congrArg (Nat.cast (R := ZMod (2 * M))) hsub
      push_cast at hcast
      rw [ZMod.natCast_zmod_val, ZMod.natCast_self] at hcast
      linear_combination hcast
    linear_combination -h2
  · simp [reflectSite, stepDir, hν]

private lemma reflectSite_sub_step0_cutTop (M : ℕ) [NeZero M] (x : Lat4 (2 * M))
    (hx : (x 0).val = 2 * M - 1) :
    reflectSite (2 * M) x - stepDir (2 * M) 0 = x := by
  have hM : 0 < M := NeZero.pos M
  ext ν
  by_cases hν : ν = 0
  · subst hν
    simp only [reflectSite, stepDir, Pi.sub_apply, ↓reduceIte]
    have h1 : x 0 + 1 = 0 := by
      have hsub : (x 0).val + 1 = 2 * M := by omega
      have hcast := congrArg (Nat.cast (R := ZMod (2 * M))) hsub
      push_cast at hcast
      rw [ZMod.natCast_zmod_val, ZMod.natCast_self] at hcast
      exact hcast
    linear_combination -2 * h1
  · simp [reflectSite, stepDir, hν]

private lemma reflectSite_sub_step0_val {M : ℕ} [NeZero M] (x : Lat4 (2 * M))
    (hx : (x 0).val < 2 * M - 1) :
    ((reflectSite (2 * M) x - stepDir (2 * M) 0) 0).val = 2 * M - 2 - (x 0).val := by
  have hM : 0 < M := NeZero.pos M
  simp only [reflectSite, stepDir, Pi.sub_apply, ↓reduceIte]
  have heq : -(x 0 + 1) - 1 = (((2 * M - 2 - (x 0).val : ℕ) : ZMod (2 * M))) := by
    have hsub : ((x 0).val + (2 * M - 2 - (x 0).val) + 2 : ℕ) = 2 * M := by omega
    have hz := congrArg (Nat.cast (R := ZMod (2 * M))) hsub
    push_cast at hz
    rw [ZMod.natCast_zmod_val, ZMod.natCast_self] at hz
    linear_combination hz
  rw [heq, ZMod.val_natCast_of_lt (by omega)]

private lemma reflectSite_zero_val' {M : ℕ} [NeZero M] (x : Lat4 (2 * M)) :
    ((reflectSite (2 * M) x) 0).val = 2 * M - 1 - (x 0).val := by
  have hM : 0 < M := NeZero.pos M
  have hx_lt : (x 0).val < 2 * M := (x 0).isLt
  simp only [reflectSite, ↓reduceIte]
  have heq : -(x 0 + 1) = (((2 * M - 1 - (x 0).val : ℕ) : ZMod (2 * M))) := by
    have hsub : ((x 0).val + (2 * M - 1 - (x 0).val) + 1 : ℕ) = 2 * M := by omega
    have hz := congrArg (Nat.cast (R := ZMod (2 * M))) hsub
    push_cast at hz
    rw [ZMod.natCast_zmod_val, ZMod.natCast_self] at hz
    linear_combination hz
  rw [heq, ZMod.val_natCast_of_lt (by omega)]

/-- **Exact Swapping-Reflection Symmetry of `glueConfig`:**
    `glueConfig q p = linkReflect (glueConfig p q)` across all 4 link sectors. -/
theorem glueConfig_swap {N M : ℕ} [NeZero M] (p q : HalfVar N M) :
    glueConfig q p = linkReflect (glueConfig p q) := by
  classical
  have hM : 0 < M := NeZero.pos M
  funext x μ
  have hx_lt : (x 0).val < 2 * M := (x 0).isLt
  by_cases hp : IsPosLink M x μ