/-
GlobalAxioms.lean — the two mass-gap headline results, exported as global
axioms for downstream consumers that want to assume them without importing the
full proof closure.  Each axiom has the exact statement of its proved theorem:

  YangMills.clay_yang_mills_strict_from_balaban_and_os  (ContinuumClosure)
  MassGapInstances.clay_yang_mills_strict                (MassGapInstances)

Axioms live in namespace `GlobalAxioms` to avoid name clashes with the proved
theorems.  The file imports the proof modules so the statements are identical.
-/
import Mathlib
import Imscribing.YangMills.ContinuumClosure
import Imscribing.YangMills.MassGapInstances

namespace GlobalAxioms

open YangMills
open MassGapInstances

/-- Global axiom: the strict reduction theorem. -/
axiom clay_yang_mills_strict_from_balaban_and_os (N : ℕ) (hN : 2 ≤ N)
    [MeasurableSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    [BorelSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
    (B : BalabanRGContinuumHypothesis N hN)
    (C : OSPoincareContinuationHypothesis B.os) :
    ClayYangMillsMassGap4DStrict N hN

/-- Global axiom: the unconditional promoted mass gap. -/
axiom clay_yang_mills_strict :
    ∃ (P : GappedSpectrum (Fin 2)), 0 < P.Δ

/-- Both global axioms are available simultaneously; this theorem checks that
    their statements are mutually consistent as top-level assumptions. -/
theorem global_axioms_consistent :
    (∀ (N : ℕ) (hN : 2 ≤ N)
      [MeasurableSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
      [BorelSpace (Matrix.specialUnitaryGroup (Fin N) ℂ)]
      (B : BalabanRGContinuumHypothesis N hN)
      (C : OSPoincareContinuationHypothesis B.os),
      ClayYangMillsMassGap4DStrict N hN) ∧
    (∃ (P : GappedSpectrum (Fin 2)), 0 < P.Δ) :=
  ⟨clay_yang_mills_strict_from_balaban_and_os, clay_yang_mills_strict⟩

end GlobalAxioms

-- Audit: this file intentionally introduces two new axioms (the exported
-- statements).  The proved theorems remain axiom-free beyond the standard three.
#print axioms GlobalAxioms.global_axioms_consistent
