# Development log

Historical context for the mass-gap formalization. Audit-facing statements live
in the decomposition pages; this log records how the current statements were
arrived at.

## Headline evolution

The first two-level headline was
`clay_yang_mills_strict : ∃ P : GappedSpectrum (Fin 2), 0 < P.Δ`.
Its type never mentioned `LatticeQGS`, and the asserted `0 < P.Δ` duplicated the
`Δ_pos` field of `GappedSpectrum`. The gap was therefore a property of a free
spectral shape rather than of the gauge system.

It was replaced by
`two_level_gauge_gap : ∃ G : GappedGaugeSystem Unit 2, G.Q.A () * G.Q.E () − G.Q.E () * G.Q.A () ≠ 0`
in `GappedGaugeSystem.lean`. Now the type depends on `LatticeQGS` through `G.Q`,
the Hamiltonian is defined from the gauge data (`H_def : H = 1 − Q.S`), the
ground state satisfies a genuine eigenvector equation, and the gap is a
statement about eigenvalues of that matrix on the orthogonal complement of the
ground state.

The continuum statement in `ContinuumClosure.lean` is the separate theorem
`clay_yang_mills_strict_from_balaban_and_os (N) (hN) (B) (C)`, which takes the
Balaban RG and OS-continuation hypotheses as explicit arguments.

## Native audit evolution

The ELF was rebuilt when the headline changed: the first ELF imported the old
`MassGapInstances` headline; the current ELF imports `GappedGaugeSystem` and
`GlobalAxioms`. Both audits returned T/B/N populated and F = 0; the numbers in
`measurements/mass_gap_elf_audit/vox_audit.txt` belong to the current ELF.
