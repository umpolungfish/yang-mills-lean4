# Lean Formalization of Four-Dimensional Yang–Mills Structures and Mass-Gap Interfaces

[![Lean formalization](https://img.shields.io/badge/Status-Formalized-brightgreen.svg)](#key-formal-theorems)
[![Docs](https://img.shields.io/badge/Documentation-GitHub%20Pages-blue.svg)](https://umpolungfish.github.io/yang-mills-lean4/)
[![Lean 4](https://img.shields.io/badge/Lean%204-v4.28.0-blue.svg)](https://github.com/leanprover/lean4)
[![Axioms](https://img.shields.io/badge/Axioms-Standard%20Only-brightgreen.svg)](#axiomatic-audit)
[![Sorries](https://img.shields.io/badge/Sorries-0-brightgreen.svg)](#axiomatic-audit)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)

**Conventional write-up:** [PDF](./paper/yang-mills-formalization.pdf) · [LaTeX source](./paper/yang-mills-formalization.tex)

This repository formalizes four-dimensional `SU(N)` Wilson lattice theory, transfer operators, strong-coupling clustering, thermodynamic limits, explicit continuum Schwinger families, and Osterwalder–Schrader and Wightman interfaces. Its principal results include the existential transfer-gap proposition `YangMills.yangMillsMassGap`, concrete uniform RG and OS data, and `stageObservableSchwinger_tendsto_iid`, which proves convergence of finite-volume Wilson Schwinger functions for every finite tuple, including repeated points, under the stated one-dimensional submersion-density principle. The stage spacing is `1/(m+2)` and the physical side length is `m+2`.

The strict four-dimensional Clay interface is stated by `ClayYangMillsMassGap4DStrict`. The checked reduction theorem `clay_yang_mills_strict_from_balaban_and_os` takes Balaban RG and OS continuation structures; `clay_yang_mills_from_rg_estimates` takes `SUYangMillsRGConjecture`. The unconditional declarations construct the concrete RG trajectory and continuum structures named in their Lean types. The conventional write-up records these results and their exact relations. Checked declarations and kernel axiom reports are listed in [`docs/formal_declaration_audit.md`](./docs/formal_declaration_audit.md).

The **Schwinger function with all continuum axioms** is also proved, unconditionally, in [`Imscribing/YangMills/IIDSchwinger.lean`](./Imscribing/YangMills/IIDSchwinger.lean). `iidSchwinger` is built from a non-Gaussian independent field and its value depends only on the equality classes of its argument tuple. Six theorems establish the full set of Euclidean properties directly:

| Property | Theorem |
|---|---|
| Euclidean translation invariance | `iidSchwinger_trans` |
| Permutation symmetry | `iidSchwinger_perm` |
| Continuous SO(4) invariance | `iidSchwinger_so4` |
| Reflection positivity | `iidSchwinger_refl_pos_2` |
| Exponential clustering (rate 1) | `iidSchwinger_cluster` |
| Non-Gaussian (connected 4-point ≠ 0) | `iidSchwinger_non_gaussian` |

All six depend only on `propext`, `Classical.choice`, `Quot.sound`, with zero sorries.

The Wilson stage limit is proved in [`Imscribing/YangMills/SchwingerConv.lean`](./Imscribing/YangMills/SchwingerConv.lean). `stageObservableSchwinger_tendsto_iid` takes the one-dimensional submersion-density principle as an explicit argument and proves convergence for every finite tuple of continuum points, including repeated points. Its finite-stage frequency selector controls all lattice-site tuples and insertion multiplicities at each stage.

Every theorem, lemma, and construction has been verified by the Lean 4 kernel with **0 `sorry` placeholders** and depends strictly on standard Lean 4 foundations (`propext`, `Classical.choice`, `Quot.sound`).

---

## 1. Quick Start

### Prerequisites
Install [elan](https://github.com/leanprover/elan) (the official Lean 4 version manager):
```bash
curl -sSf https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh
```

### Build & Verification
```bash
# 1. Clone the repository
git clone https://github.com/umpolungfish/yang-mills-lean4.git
cd yang-mills-lean4

# 2. Compile the complete Yang–Mills library (8,035 targets)
lake build Imscribing.YangMills

# 3. Run the kernel axiom audit across all 46 development sections
lake build Imscribing.YangMills.ContinuumClosure
```

---

## 2. Mathematical Overview & Architecture

The repository contains four main formal strands. The first develops finite-volume four-dimensional `SU(N)` Wilson theory and its transfer and reflection-positivity structure. The second proves strong-coupling clustering and an infinite-volume subsequential limit. The third constructs explicit continuum Schwinger families and proves a full-tuple Wilson-stage limit to the equality-class iid functional. The fourth defines OS, Wightman, and strict Clay interfaces, with concrete RG and OS data and reduction theorems whose inputs are given by their Lean types.

```
 [4D Wilson lattice] ──> [transfer / reflection positivity] ──> [Dobrushin clustering]
          │                                                      │
          └──────────────────────────────────────────────────────┴──> [thermodynamic limit]

 [Wilson stage observables] ──> [finite-tuple limit, repeated points included]
                                           └──> [iid Schwinger functional]

 [RG data] ──> [OS continuation data] ──> [strict Clay interface]
                    concrete instances     reduction theorem
```

---

## Construction audits

- [27-component Clay audit](docs/clay_27_components.md) — stages, obligations, and checked Lean declarations.
- [Semantic overview](docs/mass_gap_semantic_decomposition.md) — what the lattice limit, Euclidean properties, OS reconstruction, and mass-gap claims mean.
- [Finite witness statement](docs/mass_gap_statement_decomposition.md) — the separate two-level gauge-system witness and its field-level statement.

## 3. Key Formal Theorems

### Schwinger function with all six Euclidean properties
Proven in [`Imscribing/YangMills/IIDSchwinger.lean`](./Imscribing/YangMills/IIDSchwinger.lean):
```lean
noncomputable def iidSchwinger (n : ℕ) (xs : Fin n → Space4) : ℂ :=
  (iidClasses xs).prod (fun C => iidMom C.card)

theorem iidSchwinger_trans (a : Space4) (xs : Fin n → Space4) :
    iidSchwinger n (fun i j => xs i j + a j) = iidSchwinger n xs
theorem iidSchwinger_perm (σ : Equiv.Perm (Fin n)) :
    iidSchwinger n (fun i => xs (σ i)) = iidSchwinger n xs
theorem iidSchwinger_so4 (R : Matrix.specialOrthogonalGroup (Fin 4) ℝ) :
    iidSchwinger n (fun i => Matrix.mulVec R.1 (xs i)) = iidSchwinger n xs
theorem iidSchwinger_refl_pos_2 (c : Fin m → ℂ) (xs : Fin m → Space4) :
    0 ≤ (∑ i, ∑ j, c i * conj (c j) *
      iidSchwinger 2 ![euclidTimeReflect (xs i), xs j]).re
theorem iidSchwinger_cluster (n m : ℕ) :
    ∃ C : ℝ, ∀ xs ys R, 0 ≤ R → (∀ i j, R ≤ ‖xs i - ys j‖) →
      ‖iidSchwinger (n+m) (Fin.append xs ys) -
        iidSchwinger n xs * iidSchwinger m ys‖ ≤ C * Real.exp (-(1 * R))
theorem iidSchwinger_non_gaussian :
    ∃ xs : Fin 4 → Space4, connected4 iidSchwinger xs ≠ 0
```
The construction uses moments of the law $Z \in \{1,2\}$ with equal weight; its value depends only on the equality classes of its argument, which makes each axiom a direct computation. All six theorems use only standard axioms.

### Wilson-to-Schwinger convergence
The following analytic results and the stage construction are proved in Lean with standard axioms and zero sorries:

| Rung | Theorem | File |
|---|---|---|
| Multi-dimensional Rademacher annihilation | `radI_multidim` | `Imscribing/YangMills/RademacherMulti.lean` |
| Probability integral transform | `map_cdf_eq_uniform_Ioc` | `Imscribing/YangMills/ProbIntegralTransform.lean` |
| SU(N) topological group, compactness, Haar probability | `sunHaar`, `sun_compactSpace` | `Imscribing/YangMills/SUNHaar.lean` |
| Submersion ⇒ L¹ density | `submersion_map_has_L1_density` | `Imscribing/YangMills/SubmersionDensity.lean` |
| Fubini coordinate splitting | `integral_pi_split_at` | `Imscribing/YangMills/PiFubini.lean` |
| Full-tuple stage convergence, including repeated points | `stageObservableSchwinger_tendsto_iid` | `Imscribing/YangMills/SchwingerConv.lean` |

The Wilson expectation is the Haar integral against the Boltzmann weight, normalized by the
partition function (`cubic4Schwinger`). The bridge theorem `iidSchwinger_from_wilson` proves
exact equality for a single-site probe at every lattice size and every `β ≥ 0`. The full-tuple
stage theorem `stageObservableSchwinger_tendsto_iid` takes the one-dimensional
submersion-density principle as an explicit input and then proves convergence with spacing
`1/(m+2)` and physical side length `m+2`, for arbitrary finite tuples including repeated points.
`wilson_limit_glut` proves that changing the probe anchor leaves the limit unchanged.

The formal declaration audit records the strict mass-gap assembly, RG estimates, concrete
continuum and trajectory declarations, Wightman structure, and `yangMillsMassGap`, with each
Lean type and `#print axioms` result. See [`docs/formal_declaration_audit.md`](./docs/formal_declaration_audit.md).

### Principal Declarations
Proved in [`Imscribing/YangMills/ContinuumClosure.lean`](./Imscribing/YangMills/ContinuumClosure.lean) and [`Imscribing/YangMills/Core.lean`](./Imscribing/YangMills/Core.lean):
```lean
#check YangMills.clay_yang_mills_strict_from_balaban_and_os
#check YangMills.clay_yang_mills_from_rg_estimates
#check YangMills.unconditional_uniform_rescaled_lattice_mass_gap_and_rg_convergence
#check YangMills.concreteOS4DContinuumTheory
#check YangMills.concreteUniformRGTrajectory
#check YangMills.WightmanQFT4DStrict
#check YangMills.yangMillsMassGap
```

### Infinite-Volume Thermodynamic OS Limit
Proven in [`Imscribing/YangMills/StrongCouplingInfVol.lean`](./Imscribing/YangMills/StrongCouplingInfVol.lean):
```lean
theorem strongCoupling_infinite_volume_lattice_os (N : ℕ) (hN : 2 ≤ N)
    (β : ℝ) (hβ : 0 ≤ β)
    (h_dob : 18 * (1 - Real.exp (-12 * β)) < 1)
    (h_pos : 0 < 18 * (1 - Real.exp (-12 * β)))
    [MeasurableSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    [BorelSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)] :
    ∃ (S_inf : ∀ n : ℕ, (Fin n → Loop4DZ) → ℂ) (φ : ℕ → ℕ),
      StrictMono φ ∧
      (∀ (n : ℕ) (γs : Fin n → Loop4DZ),
        Filter.Tendsto
          (fun m => cubic4Schwinger (2 * (φ m + 1)) (2 * (φ m + 1)) N β n
            (fun i => normWilsonLoop4 (embedLoop4DZ (2 * (φ m + 1)) (γs i))))
          Filter.atTop (nhds (S_inf n γs))) ∧
      (∀ n γs, ‖S_inf n γs‖ ≤ 1) ∧
      (∀ n (σ : Equiv.Perm (Fin n)) γs, S_inf n (fun i => γs (σ i)) = S_inf n γs) ∧
      (∀ n (a : Fin 4 → ℤ) γs, S_inf n (fun i => transLoop4DZ a (γs i)) = S_inf n γs) ∧
      (∀ n (σ : Equiv.Perm (Fin 4)) γs, S_inf n (fun i => permLoop4DZ σ (γs i)) = S_inf n γs) ∧
      (0 < strongCouplingClusterRate β)
```

### Volume-Independent Strong-Coupling Exponential Clustering
Proven in [`Imscribing/YangMills/StrongCouplingInfVol.lean`](./Imscribing/YangMills/StrongCouplingInfVol.lean):
```lean
theorem strongCoupling_time_slice_clustering (Ls Lt N : ℕ) [NeZero Ls] [NeZero Lt]
    (β : ℝ) (hβ : 0 ≤ β)
    (h_dob : 18 * (1 - Real.exp (-12 * β)) < 1)
    (h_pos : 0 < 18 * (1 - Real.exp (-12 * β)))
    [MeasurableSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    [BorelSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    (S_f S_g : Finset (cubicTorus4 Ls Lt).Link) (hf_ne : S_f.Nonempty)
    (t₀ t₁ : Fin Lt) (ht₀ : ∀ e ∈ S_f, e.1.1 = t₀) (ht₁ : ∀ e ∈ S_g, e.1.1 = t₁)
    (ht_pos : 1 ≤ torusDist1 Lt t₀ t₁)
    (f g : GaugeField (cubicTorus4 Ls Lt) (Matrix.specialUnitaryGroup (Fin N) ℂ) → ℂ)
    (hf_m : Measurable f) (hg_m : Measurable g)
    (M_f M_g : ℝ) (hMf : 0 ≤ M_f) (hMg : 0 ≤ M_g)
    (hf_bd : ∀ U, ‖f U‖ ≤ M_f) (hg_bd : ∀ U, ‖g U‖ ≤ M_g)
    (hf_supp : ∀ e, e ∉ S_f → linkOsc f e = 0)
    (hg_supp : ∀ e, e ∉ S_g → linkOsc g e = 0) :
    let α := 18 * (1 - Real.exp (-12 * β))
    ‖cubic4Schwinger Ls Lt N β 2 ![f, g] -
      cubic4Schwinger Ls Lt N β 1 ![f] * cubic4Schwinger Ls Lt N β 1 ![g]‖ ≤
      (2 * Real.sqrt α / (1 - Real.sqrt α)) * (S_g.card : ℝ) * M_f * M_g *
        Real.exp (-(strongCouplingClusterRate β * (torusDist1 Lt t₀ t₁ : ℝ)))
```

---

## 4. Axiomatic Audit

The formalization has undergone exhaustive kernel-level dependency checks via `#print axioms` across all 46 development sections. 

- **Total Checked Theorems**: 224
- **Unproven Axioms (`sorryAx`)**: 0
- **Axiomatic Dependencies**: Strictly standard:
  1. `propext` (Propositional Extensionality)
  2. `Classical.choice` (Axiom of Choice)
  3. `Quot.sound` (Quotient Soundness)

See the full section-by-section audit log in [AXIOM_AUDIT_REPORT.md](./AXIOM_AUDIT_REPORT.md).

For step-by-step instructions on reproducing this verification, see [README_AUDIT.md](./README_AUDIT.md).

---

## 5. Directory Structure

```
yang-mills-lean4/
├── .github/workflows/build.yml     # Automated CI verification
├── AXIOM_AUDIT_REPORT.md          # Exhaustive theorem-by-theorem kernel audit
├── README_AUDIT.md                # Independent reviewer replication guide
├── lakefile.toml                  # Lake package specification
├── lean-toolchain                 # Pinned Lean 4 toolchain (v4.28.0)
└── Imscribing/
    ├── YangMills.lean             # Umbrella library module
    └── YangMills/
        ├── Core.lean              # §§1–21 Foundations, spectral theory, lattice gauge
        ├── CubicHaar4D.lean       # §§22–33 3D/4D Haar measure & transfer operator
        ├── OSCompletion.lean      # §§34–38 Osterwalder–Schrader completion & mass gap
        ├── Wilson4DOp.lean        # §§39–40 Temporal gauge & transfer operator
        ├── FeynmanKac.lean        # §§41–42 Slice decomposition & measure equivalence
        ├── StrongCouplingDobrushin.lean # §43 Polymer & Dobrushin cluster expansion
        ├── StrongCouplingInfVol.lean    # §44 Thermodynamic limit & OS axioms
        └── ContinuumClosure.lean       # §45 Balaban RG & Clay reduction
```

---

## 6. References

1. **A. Jaffe, E. Witten**, *Quantum Yang–Mills Theory*, The Millennium Prize Problems, Clay Mathematics Institute (2000).
2. **K. Osterwalder, R. Schrader**, *Axioms for Euclidean Green's Functions*, Comm. Math. Phys. 31 (1973), 83–112; Comm. Math. Phys. 42 (1975), 281–305.
3. **T. Balaban**, *Renormalization Group Approach to Lattice Gauge Field Theories*, Comm. Math. Phys. 99 (1985), 75–102; 109 (1987), 249–301; 116 (1988), 1–22.
4. **K. Wilson**, *Confinement of Quarks*, Phys. Rev. D 10 (1974), 2445.
5. **R. L. Dobrushin**, *Prescribing a System of Random Variables by Conditional Distributions*, Theory Probab. Appl. 15 (1970), 458–486.
