#!/usr/bin/env python3
"""
Idempotent patch script for:
  - Imscribing/YangMills/SpatialISO3UnitariesOnOS.lean
  - Imscribing/YangMills/SchwingerToClayMaster.lean
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


TARGET_SPATIAL = Path("Imscribing/YangMills/SpatialISO3UnitariesOnOS.lean")
TARGET_MASTER = Path("Imscribing/YangMills/SchwingerToClayMaster.lean")


def load_original_lines(path: Path) -> list[str]:
    bak = path.with_suffix(path.suffix + ".prepatch.bak")
    if bak.exists():
        text = bak.read_text(encoding="utf-8")
    else:
        text = path.read_text(encoding="utf-8")
        shutil.copy2(path, bak)
    return text.splitlines(keepends=True)


def write_patched(path: Path, new_text: str, dry_run: bool) -> None:
    cur_text = path.read_text(encoding="utf-8")
    if cur_text == new_text:
        print(f"[unchanged] {path}")
        return
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
        print(f"[written]   {path}")


def detect_spacetime4_kind(root: Path) -> str:
    ym_dir = root / "Imscribing" / "YangMills"
    re_st4 = re.compile(r"^\s*(?:abbrev|def)\s+Spacetime4\b[\s\S]{0,200}?(?=\n\S|\Z)", re.M)
    for f in sorted(ym_dir.rglob("*.lean")):
        m = re_st4.search(f.read_text(encoding="utf-8", errors="ignore"))
        if m:
            block = m.group(0)
            if "Fin 4" in block and "→" in block and "PiLp" not in block and "EuclideanSpace" not in block:
                return "pi"
            return "pilp"
    return "pilp"


def find_near(lines: list[str], zero_idx: int, pattern: str, radius: int = 5) -> int | None:
    lo = max(0, zero_idx - radius)
    hi = min(len(lines), zero_idx + radius + 1)
    rx = re.compile(pattern)
    for i in [zero_idx, *range(lo, hi)]:
        if 0 <= i < len(lines) and rx.search(lines[i]):
            return i
    return None


def find_decl_top(lines: list[str], decl_idx: int) -> int:
    i = decl_idx
    while i > 0:
        prev = lines[i - 1].strip()
        if prev == "" or prev.startswith("--") or prev.startswith("@[") or prev in {"private", "protected", "noncomputable"}:
            i -= 1
            continue
        if "-/" in prev:
            i -= 1
            while i > 0 and "/-" not in lines[i]:
                i -= 1
            continue
        break
    return i


def patch_spatial_iso3(lines: list[str], st4_kind: str) -> tuple[str, list[str]]:
    lines = list(lines)
    notes: list[str] = []

    # 1. L32: spaceShiftVec n 0 = 0
    idx32 = find_near(lines, 31, r"PiLp\.ext")
    if idx32 is not None and "funext" not in lines[idx32]:
        ext_fn = "funext" if st4_kind == "pi" else "PiLp.ext"
        lines[idx32] = re.sub(r"\bPiLp\.ext\b", f"funext fun _ => {ext_fn}", lines[idx32], count=1)
        notes.append(f"L{idx32 + 1}: wrapped `PiLp.ext`.")

    # 2. L54: rewrite `iteratedFDeriv ℝ m fun y ↦ f (y - v)` via `funext ih` before `h_fd`
    idx54 = find_near(lines, 53, r"\bh_fd\b")
    if idx54 is not None and "funext ih" not in lines[idx54]:
        h_eq_fix = (
            "(show (iteratedFDeriv ℝ m fun y ↦ f (y - v)) = "
            "fun y ↦ iteratedFDeriv ℝ m f (y - v) from funext ih), h_fd"
        )
        lines[idx54] = re.sub(r"\bh_fd\b", h_eq_fix, lines[idx54], count=1)
        notes.append(f"L{idx54 + 1}: added `funext ih` rewrite.")

    # 3. L61: term-mode `ContDiff.differentiable_iteratedFDeriv`
    idx61 = find_near(lines, 60, r"(?:ContDiff\.)?differentiable|iteratedFDeriv_right|f\.smooth'")
    if idx61 is not None:
        indent = re.match(r"^(\s*)", lines[idx61]).group(1)
        lines[idx61] = (
            f"{indent}(f.smooth (j + 1 : ℕ)).differentiable_iteratedFDeriv "
            f"(by exact_mod_cast Nat.lt_succ_self j)\n"
        )
        notes.append(f"L{idx61 + 1}: fixed `differentiable_iteratedFDeriv`.")

    # 4. L137: add `DFinsupp.mapRange_apply, Subtype.coe_mk`
    idx137 = find_near(lines, 136, r"DFinsupp\.mapRange\.linearMap_apply")
    if idx137 is not None and "DFinsupp.mapRange_apply" not in lines[idx137]:
        lines[idx137] = lines[idx137].replace(
            "DFinsupp.mapRange.linearMap_apply,",
            "DFinsupp.mapRange.linearMap_apply, DFinsupp.mapRange_apply, Subtype.coe_mk,",
            1,
        )
        notes.append(f"L{idx137 + 1}: added `DFinsupp.mapRange_apply, Subtype.coe_mk`.")

    # 5. L140: replace `abel` / `abel?` with `abel_nf`
    idx140 = find_near(lines, 139, r"\babel(\?|(?![_1!\w]))")
    if idx140 is not None:
        lines[idx140] = re.sub(r"\babel(\?|(?![_1!\w]))", "abel_nf", lines[idx140])
        notes.append(f"L{idx140 + 1}: replaced `abel` with `abel_nf`.")

    # 6. L154-158: place `set_option maxSynthPendingDepth 1 in` ABOVE doc comment of `spatialTranslationUnitaryGroup`
    idx_stug = find_near(lines, 157, r"noncomputable\s+def\s+spatialTranslationUnitaryGroup\b")
    if idx_stug is not None:
        stug_top = find_decl_top(lines, idx_stug)
        lines[stug_top] = "set_option maxSynthPendingDepth 1 in\n" + lines[stug_top]
        notes.append(f"L{stug_top + 1}: added `set_option maxSynthPendingDepth 1 in` above `spatialTranslationUnitaryGroup` doc comment.")

    # 7. L176-252: build `U₀` before `letI`, keep exact `InnerProductSpace.ofCore core.toCore`, drop `set H₀`/`set H`
    idx176 = find_near(lines, 175, r"letI\s*:\s*NormedAddCommGroup\s*\(BorchersPos\s*⧸\s*nullSubmodule pre\)")
    idx194 = find_near(lines, 193, r"fun\s+_\s+_\s*=>\s*rfl")
    idx252 = find_near(lines, 251, r"rw\s*\[hU_coe v _,\s*hU₀_mk\]")
    if idx176 is not None and idx194 is not None and idx252 is not None:
        u0_block = [
            l.replace("H₀ →ₗ[ℂ] H₀", "(BorchersPos ⧸ nullSubmodule pre) →ₗ[ℂ] (BorchersPos ⧸ nullSubmodule pre)")
            for l in lines[idx176 + 4 : idx194 + 1]
        ]
        inst_and_u0prime = [
            "  letI : NormedAddCommGroup (BorchersPos ⧸ nullSubmodule pre) := core.toNormedAddCommGroup\n",
            "  letI : InnerProductSpace ℂ (BorchersPos ⧸ nullSubmodule pre) := InnerProductSpace.ofCore core.toCore\n",
            "  let U₀' : (Fin 3 → ℝ) → (BorchersPos ⧸ nullSubmodule pre) →ₗ[ℂ] (BorchersPos ⧸ nullSubmodule pre) := fun v =>\n",
            "    { toFun := fun x => U₀ v x\n",
            "      map_add' := fun x y => by\n",
            "        induction x using Submodule.Quotient.induction_on with\n",
            "        | _ F =>\n",
            "          induction y using Submodule.Quotient.induction_on with\n",
            "          | _ G =>\n",
            "            change U₀ v (Submodule.Quotient.mk (F + G)) =\n",
            "              U₀ v (Submodule.Quotient.mk F) + U₀ v (Submodule.Quotient.mk G)\n",
            "            simp only [hU₀_mk, map_add]; rfl\n",
            "      map_smul' := fun c x => by\n",
            "        induction x using Submodule.Quotient.induction_on with\n",
            "        | _ F =>\n",
            "          change U₀ v (Submodule.Quotient.mk (c • F)) = c • U₀ v (Submodule.Quotient.mk F)\n",
            "          simp only [hU₀_mk, map_smul]; rfl }\n",
            "  have hU₀'_mk : ∀ v (F : BorchersPos),\n",
            "      U₀' v (Submodule.Quotient.mk F) = Submodule.Quotient.mk (borchersSpaceShift v F) :=\n",
            "    fun v F => hU₀_mk v F\n",
        ]
        tail_block: list[str] = []
        skip_next = False
        for l in lines[idx194 + 1 : idx252 + 1]:
            if skip_next:
                skip_next = False
                continue
            if "rw [hU_coe (u + v) _, hU_coe v _, hU₀_mk, hU_coe u _, hU₀_mk, hU₀_mk," in l:
                tail_block.append(
                    "          rw [hU_coe (u + v) (Submodule.Quotient.mk F), hU₀'_mk (u + v) F,\n"
                    "              hU_coe v (Submodule.Quotient.mk F), hU₀'_mk v F,\n"
                    "              hU_coe u (Submodule.Quotient.mk (borchersSpaceShift v F)),\n"
                    "              hU₀'_mk u (borchersSpaceShift v F), borchersSpaceShift_add]\n"
                )
                skip_next = True
                continue
            l2 = re.sub(r"\bH₀\b", "(BorchersPos ⧸ nullSubmodule pre)", l)
            l2 = re.sub(r"\bH\b", "(UniformSpace.Completion (BorchersPos ⧸ nullSubmodule pre))", l2)
            l2 = l2.replace("hU₀_mk", "hU₀'_mk")
            l2 = l2.replace("(U₀ v)", "(U₀' v)")
            l2 = l2.replace("U₀ v", "U₀' v")
            l2 = l2.replace("hU_coe 0 _", "hU_coe 0 (Submodule.Quotient.mk F)")
            l2 = l2.replace("hU_coe v _", "hU_coe v (Submodule.Quotient.mk _)")
            tail_block.append(l2)
        lines[idx176 : idx252 + 1] = u0_block + inst_and_u0prime + tail_block
        notes.append("L176..252: built `U₀` before `letI`, kept `ofCore core.toCore`, added `U₀'`/`hU₀'_mk`, fixed `rw` order.")

    # 8. L256-290: single `local instance` pair in `section`, remove duplicate `letI`s, fix `intro`
    decl_idx = None
    for k in range(len(lines) - 1, -1, -1):
        if re.match(r"^\s*theorem\s+spatialTranslation_commutes_with_os_semigroup\b", lines[k]):
            decl_idx = k
            break
    if decl_idx is not None:
        top_idx = find_decl_top(lines, decl_idx)
        k = decl_idx
        while k < len(lines):
            s = lines[k].strip()
            if (
                s == "let core := quotInnerCore pre"
                or s == "intro core"
                or s.startswith("letI : NormedAddCommGroup (BorchersPos ⧸ nullSubmodule pre)")
                or s.startswith("letI : InnerProductSpace ℂ (BorchersPos ⧸ nullSubmodule pre)")
                or s.startswith("set U_space :=")
            ):
                lines.pop(k)
                continue
            if s == "intro v t ht x":
                lines[k] = "  intro U_space v t ht x\n"
            elif s.startswith("rw [hT_coe t ht F"):
                lines[k] = (
                    "        rw [hT_coe t ht F]\n"
                    "        dsimp only [U_space]\n"
                    "        rw [hU_mk v (pre.θ t F), hU_mk v F, hT_coe t ht (borchersSpaceShift v F), h_comm_θ v t ht F]\n"
                )
                if k + 1 < len(lines) and "hT_coe t ht (borchersSpaceShift" in lines[k + 1]:
                    lines.pop(k + 1)
                break
            k += 1

        inst_block = (
            "section\n"
            "set_option maxSynthPendingDepth 1\n"
            "private noncomputable local instance (pre : EuclideanPreData BorchersPos) :\n"
            "    NormedAddCommGroup (BorchersPos ⧸ OSBorchers.nullSubmodule pre) :=\n"
            "  (quotInnerCore pre).toNormedAddCommGroup\n\n"
            "private noncomputable local instance (pre : EuclideanPreData BorchersPos) :\n"
            "    InnerProductSpace ℂ (BorchersPos ⧸ OSBorchers.nullSubmodule pre) :=\n"
            "  @InnerProductSpace.ofCore ℂ (BorchersPos ⧸ OSBorchers.nullSubmodule pre) _\n"
            "    (Submodule.Quotient.addCommGroup _) (Submodule.Quotient.module _) (quotInnerCore pre).toCore\n\n"
        )
        lines[top_idx] = inst_block + lines[top_idx]

        end_idx = None
        for k in range(len(lines) - 1, top_idx, -1):
            if re.match(r"^\s*end\s+\S+", lines[k]):
                end_idx = k
                break
        if end_idx is not None:
            lines[end_idx] = "end\n\n" + lines[end_idx]
        else:
            lines.append("\nend\n")
        notes.append("Wrapped `spatialTranslation_commutes_with_os_semigroup` with single `local instance` pair & `maxSynthPendingDepth 1`.")

    return "".join(lines), notes


def patch_schwinger_master(lines: list[str]) -> tuple[str, list[str]]:
    lines = list(lines)
    notes: list[str] = []
    idx103 = find_near(lines, 102, r"have\s+_h_W₀\s*:=\s*wightman_boundary_tempered")
    if idx103 is not None:
        end_call = idx103
        if end_call + 1 < len(lines) and "h_at1" in lines[end_call + 1]:
            end_call += 1
        proof_block = """  have _h_W₀ :
      ∃ W₀ : TestFn4 →ₗ[ℂ] ℂ,
        (∀ f, Filter.Tendsto (fun t => W_reg t f) (nhdsWithin 0 (Set.Ioi 0)) (nhds (W₀ f))) ∧
        (∀ f, ‖W₀ f‖ ≤ (C₁ + C₂) * p f) := by
    have h_mvt : ∀ (f : TestFn4) {a b : ℝ},
        a ∈ Set.Ioc (0 : ℝ) 1 → b ∈ Set.Ioc (0 : ℝ) 1 →
        ‖W_reg a f - W_reg b f‖ ≤ C₂ * p f * |a - b| := by
      intro f a b ha hb
      simpa only [Real.norm_eq_abs] using
        (convex_Ioc (0 : ℝ) 1).norm_image_sub_le_of_norm_hasDerivWithin_le
          (fun t ht => (h_deriv f t ht).hasDerivWithinAt)
          (fun t ht => h_dbound f t ht) hb ha
    have h_lim : ∀ f : TestFn4,
        ∃ L : ℂ, Filter.Tendsto (fun t => W_reg t f) (nhdsWithin 0 (Set.Ioi 0)) (nhds L) := by
      intro f
      have hM : 0 ≤ C₂ * p f := mul_nonneg hC₂ (hp_nn f)
      let u : ℕ → ℂ := fun n => W_reg (1 / ((n : ℝ) + 1)) f
      have hu_cauchy : CauchySeq u := by
        rw [Metric.cauchySeq_iff]
        intro ε hε
        obtain ⟨N, hN⟩ := exists_nat_gt ((C₂ * p f + 1) / ε)
        refine ⟨N, fun m hm n hn => ?_⟩
        have hm1 : (1 / ((m : ℝ) + 1)) ∈ Set.Ioc (0 : ℝ) 1 :=
          ⟨by positivity, div_le_one_of_le₀ (by linarith) (by positivity)⟩
        have hn1 : (1 / ((n : ℝ) + 1)) ∈ Set.Ioc (0 : ℝ) 1 :=
          ⟨by positivity, div_le_one_of_le₀ (by linarith) (by positivity)⟩
        have hmN : (1 / ((m : ℝ) + 1)) ≤ 1 / ((N : ℝ) + 1) :=
          one_div_le_one_div_of_le (by positivity) (by exact_mod_cast Nat.add_le_add_right hm 1)
        have hnN : (1 / ((n : ℝ) + 1)) ≤ 1 / ((N : ℝ) + 1) :=
          one_div_le_one_div_of_le (by positivity) (by exact_mod_cast Nat.add_le_add_right hn 1)
        have h_abs : |1 / ((m : ℝ) + 1) - 1 / ((n : ℝ) + 1)| ≤ 1 / ((N : ℝ) + 1) := by
          rw [abs_le]
          constructor <;> linarith [hm1.1, hn1.1]
        have hN_lt : 1 / ((N : ℝ) + 1) < ε / (C₂ * p f + 1) := by
          have hN' : (C₂ * p f + 1) / ε < (N : ℝ) + 1 := lt_trans hN (lt_add_one _)
          rw [div_lt_div_iff₀ (by positivity) (by positivity)]
          rw [div_lt_iff₀ hε] at hN'
          linarith
        have h_est := h_mvt f hm1 hn1
        rw [dist_eq_norm]
        calc
          ‖u m - u n‖ ≤ C₂ * p f * |1 / ((m : ℝ) + 1) - 1 / ((n : ℝ) + 1)| := h_est
          _ ≤ C₂ * p f * (1 / ((N : ℝ) + 1)) := mul_le_mul_of_nonneg_left h_abs hM
          _ ≤ C₂ * p f * (ε / (C₂ * p f + 1)) := mul_le_mul_of_nonneg_left hN_lt.le hM
          _ < ε := by
            rw [← mul_div_assoc, div_lt_iff₀ (by positivity)]
            nlinarith
      obtain ⟨L, hL⟩ := cauchySeq_tendsto_of_complete hu_cauchy
      refine ⟨L, Metric.tendsto_nhdsWithin_nhds.mpr fun ε hε => ?_⟩
      let δ : ℝ := min 1 (ε / (2 * (C₂ * p f + 1)))
      have hδ_pos : 0 < δ := lt_min one_pos (div_pos hε (by positivity))
      obtain ⟨N₁, hN₁⟩ := exists_nat_one_div_lt hδ_pos
      obtain ⟨N₂, hN₂⟩ := Metric.tendsto_atTop.mp hL (ε / 2) (half_pos hε)
      let k : ℕ := max N₁ N₂
      have hk_lt : (1 / ((k : ℝ) + 1)) < δ := by
        refine lt_of_le_of_lt ?_ hN₁
        exact one_div_le_one_div_of_le (by positivity) (by exact_mod_cast Nat.add_le_add_right (le_max_left N₁ N₂) 1)
      have hk_dist : dist (u k) L < ε / 2 := hN₂ k (le_max_right N₁ N₂)
      refine ⟨δ, hδ_pos, fun {t} ht_pos ht_dist => ?_⟩
      have ht_lt : t < δ := by
        have ht0 : 0 < t := ht_pos
        simpa [Real.dist_eq, abs_of_pos ht0] using ht_dist
      have ht1 : t ∈ Set.Ioc (0 : ℝ) 1 := ⟨ht_pos, ht_lt.le.trans (min_le_left _ _)⟩
      have hk1 : (1 / ((k : ℝ) + 1)) ∈ Set.Ioc (0 : ℝ) 1 :=
        ⟨by positivity, hk_lt.le.trans (min_le_left _ _)⟩
      have h_abs : |t - 1 / ((k : ℝ) + 1)| < δ := by
        rw [abs_sub_lt_iff]
        constructor <;> linarith [ht1.1, hk1.1]
      have h_mvt_tk : dist (W_reg t f) (u k) ≤ ε / 2 := by
        rw [dist_eq_norm]
        calc
          ‖W_reg t f - u k‖ ≤ C₂ * p f * |t - 1 / ((k : ℝ) + 1)| := h_mvt f ht1 hk1
          _ ≤ C₂ * p f * δ := mul_le_mul_of_nonneg_left h_abs.le hM
          _ ≤ C₂ * p f * (ε / (2 * (C₂ * p f + 1))) :=
            mul_le_mul_of_nonneg_left (min_le_right _ _) hM
          _ ≤ ε / 2 := by
            rw [← mul_div_assoc, div_le_iff₀ (by positivity)]
            nlinarith
      exact lt_of_le_of_lt (dist_triangle (W_reg t f) (u k) L) (by linarith)
    choose W₀_fun hW₀_tend using h_lim
    refine ⟨{ toFun := W₀_fun
              map_add' := fun f g => by
                have hadd : Filter.Tendsto (fun t => W_reg t (f + g)) (nhdsWithin 0 (Set.Ioi 0))
                    (nhds (W₀_fun f + W₀_fun g)) := by
                  simpa only [map_add] using (hW₀_tend f).add (hW₀_tend g)
                exact tendsto_nhds_unique (hW₀_tend (f + g)) hadd
              map_smul' := fun c f => by
                have hsmul : Filter.Tendsto (fun t => W_reg t (c • f)) (nhdsWithin 0 (Set.Ioi 0))
                    (nhds (c • W₀_fun f)) := by
                  simpa only [map_smul] using (hW₀_tend f).const_smul c
                exact tendsto_nhds_unique (hW₀_tend (c • f)) hsmul },
      hW₀_tend, fun f => ?_⟩
    refine le_of_tendsto (hW₀_tend f).norm ?_
    refine Filter.eventually_of_mem (Ioc_mem_nhdsGT (zero_lt_one : (0 : ℝ) < 1)) fun t ht => ?_
    have h1 : (1 : ℝ) ∈ Set.Ioc (0 : ℝ) 1 := ⟨zero_lt_one, le_rfl⟩
    have h_abs1 : |t - 1| ≤ 1 := abs_le.mpr ⟨by linarith [ht.1], by linarith [ht.2]⟩
    calc
      ‖W_reg t f‖ = ‖(W_reg t f - W_reg 1 f) + W_reg 1 f‖ := by simp
      _ ≤ ‖W_reg t f - W_reg 1 f‖ + ‖W_reg 1 f‖ := norm_add_le _ _
      _ ≤ C₂ * p f * |t - 1| + C₁ * p f := add_le_add (h_mvt f ht h1) (h_at1 f)
      _ ≤ C₂ * p f * 1 + C₁ * p f :=
        add_le_add (mul_le_mul_of_nonneg_left h_abs1 (mul_nonneg hC₂ (hp_nn f))) le_rfl
      _ = (C₁ + C₂) * p f := by ring
"""
        lines[idx103 : end_call + 1] = [proof_block]
        notes.append(f"L{idx103 + 1}: proved `_h_W₀` directly via MVT + `cauchySeq_tendsto_of_complete`.")
    return "".join(lines), notes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo_root", nargs="?", default=".", help="Path to yang-mills-lean4 root")
    ap.add_argument("--dry-run", action="store_true", help="Do not write files")
    ap.add_argument("--build", action="store_true", help="Run lake build per target")
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    spatial_path = root / TARGET_SPATIAL
    master_path = root / TARGET_MASTER

    st4_kind = detect_spacetime4_kind(root)
    orig_spatial = load_original_lines(spatial_path)
    orig_master = load_original_lines(master_path)

    new_spatial, s_notes = patch_spatial_iso3(orig_spatial, st4_kind)
    new_master, m_notes = patch_schwinger_master(orig_master)

    write_patched(spatial_path, new_spatial, args.dry_run)
    write_patched(master_path, new_master, args.dry_run)

    print("\n=== Patch notes ===")
    for n in s_notes + m_notes:
        print(" *", n)

    rc = 0
    if args.build and not args.dry_run:
        for mod in (
            "Imscribing.YangMills.SpatialISO3UnitariesOnOS",
            "Imscribing.YangMills.SchwingerToClayMaster",
        ):
            print(f"\n[running] lake build {mod}")
            r = subprocess.call(["lake", "build", mod], cwd=root)
            if r != 0:
                rc = r
    return rc


if __name__ == "__main__":
    raise SystemExit(main())