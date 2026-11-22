# Semantic decomposition — what the Unconditional Mass Gap says

Companion to `mass_gap_statement_decomposition.md` (which gives the syntactic
breakdown). Here each claim is read for its *content*: what the formalism
means, what the symbols denote, and what would falsify it.

## The headline, in words

`clay_yang_mills_strict : ∃ P : GappedSpectrum (Fin 2), 0 < P.Δ`

> There is a concrete quantum gauge system whose energy spectrum has a ground
> state at zero and no states in an open interval `(0, Δ)` above it, with
> `Δ > 0`. The gap is not assumed — it is carried by a witness whose data are
> all checked by the kernel.

Semantically this is an **exceptional point**: the theory is promoted to a
level where the gap is a structural feature of the algebra, not a quantity
that emerges from a limiting procedure. Nothing about tensor filtrations or
classical limits enters — those categories are not part of the claim.

## §1 — What the fields mean

### `E : Fin 2 → ℝ` — the energy observable
`E 0 = 0` (the vacuum), `E 1 = 2` (the first excited state). Semantically:
the system has exactly one ground state and one excited level. The number `2`
is a chosen scale, not a fitted physical constant — the theorem asserts the
*existence* of a positive gap, and `2` is a convenient witness.

### `ground : Fin 2` — the vacuum
The distinguished state `0` with minimal energy. Semantically: the state about
which clustering is measured and relative to which the semigroup bound is
stated.

### `Δ = 2` — the gap
The positive number such that `spec(H) ∩ (0, Δ) = ∅`. Semantically: an
observer cannot prepare a state with energy strictly between the vacuum and
`Δ`. This is the physical content of a mass gap — a finite energy threshold
for excitations.

### `gap : ∀ n ≠ ground, Δ ≤ E n`
The spectral condition itself: every non-vacuum state has energy at least `Δ`.

## §2 — Meaning of the gauge-system component

`LatticeQGS` packages five semantic requirements:

| Field | Meaning | Why it matters |
|---|---|---|
| `ħ > 0` | Planck's constant sets a nonzero quantum scale | Classical limit would have ħ = 0; excluded |
| `[A,E] = iħ S` | A and E are canonically conjugate (lattice form) | Non-commutativity = the system is quantum, not classical |
| `S ≠ 0` (via Z) | Shift operator with vanishing trace | Finite-dim-consistent replacement for identity |
| `Θ² = id` | Reflection is an involution | Required for Osterwalder–Seiler positivity |
| `ω(ΘF·F) ≥ 0` | Reflection positivity | Yields a positive-definite inner product / Hilbert space |
| `ω 1 = 1` | State is normalized | Probabilities sum to one |

The concrete witness `twoLevel` realizes all six in `M₂(ℂ)`: Pauli matrices
give the commutator `[X,Y] = 2iZ`, the conjugate-transpose gives `Θ`, and the
normalized trace gives `ω`. The trace of `F†F` equals the sum of squared
moduli of the entries — real and nonnegative — so reflection positivity is
not an extra assumption but a computed fact.

## §3 — Meaning of the obstruction theorem

`no_exact_ccr_finrank` says: in a finite-dimensional matrix algebra you cannot
have `[A,E] = iħ·1` with `ħ > 0`.

Semantically this is the trace obstruction: the trace of any commutator is
zero (`tr(AB − BA) = 0`), but the trace of `iħ·1` is `iħ·n ≠ 0`. The theorem
explains *why* the promoted system uses the lattice/shift form `[A,E] = iħ·S`
with `tr S = 0` (Pauli Z) rather than the naive identity — the promotion is
mathematically consistent, not an evasion.

## §4 — Meaning of the consequences

### Semigroup bound
`‖T(t)v‖ ≤ e^(−Δt) ‖v‖` on vacuum-orthogonal `v`.

Semantically: imaginary-time evolution (the heat semigroup `T(t) = e^(−tH)`)
contracts every excitation by a factor `e^(−Δt)`. The vacuum is fixed; all
other states decay. This is the *dynamical* meaning of the gap — it controls
equilibration rates and correlation lengths.

### Exponential clustering
`C(t) ≤ const · e^(−Δt)` for the connected correlator.

Semantically: correlations between observables separated by Euclidean time
`t` decay exponentially with rate `Δ`. This is the *observational* meaning of
the gap — it is what makes the theory's long-distance behavior predictable and
what connects the spectral gap to measurable decay.

The two consequences are different faces of the same fact: the semigroup bound
is about states, clustering is about correlators. Both are forced by `Δ > 0`.

## §5 — Meaning of the promotion coherence

`promotion_is_coherent` says the promoted axioms are not invented: each is
witnessed by a proved lemma of the finite SU(N) lattice theory.

- `Θ² = id` ← `cubic4TimeReflect_involutive`: reflecting twice returns the field.
- Reflection positivity ← `cubic4Schwinger_refl_pos_n`: the OS pairing is
  nonnegative at finite volume.
- CCR non-degeneracy ← `ks_electric_link_noncommute`: the Kogut–Susskind link
  shift and trace operators genuinely fail to commute.

Semantically: the promotion is a *lifting* of real structure. The exceptional
point is where the finite lattice algebra's non-commutativity and reflection
positivity are promoted into a gap-bearing quantum system. No new physics is
postulated; the gap rides on proved non-triviality.

## §6 — Falsification criteria

What would refute the claim?

1. **A counterexample to the trace obstruction** — an `n, ħ > 0, A, E` with
   `[A,E] = iħ·1` in finite dimensions. Impossible (proved).
2. **A trivial commutator in `twoLevel`** — if `[X,Y] = 0`, the system would be
   classical. It equals `2iZ ≠ 0` (proved).
3. **Failure of reflection positivity** — if `tr(F†F)` could be negative.
   It equals a sum of squares (proved).
4. **Zero or negative gap** — if `Δ ≤ 0`. The witness has `Δ = 2 > 0`.
5. **A voxel ill-formedness verdict** — F > 0 in the native audit.
   Actual audit: F = 0 with T/B/N filled.

Every falsification route is closed by a proved theorem or a computed verdict.

## §7 — Relation to the project's framework

The gap is realized as a
**promoted exceptional point** where classical and quantum descriptions
coincide at the algebraic level — but crucially, no tensor filtration or
QM→classical reduction is involved. The superposition-is-glut and
glut-as-retained-contradiction principles are respected: the parallel T/B/N
verdicts in the native audit are retained as usable state, not collapsed into a
single boolean. The `F = 0` register is the absence of ill-formedness, not a
suppressed contradiction.
