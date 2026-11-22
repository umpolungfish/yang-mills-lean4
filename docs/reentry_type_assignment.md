# Re-entered Type assignment — the Schwinger subject

Subject: one Schwinger function with non-Gaussian correlations, continuous
SO(4) invariance, Euclidean translation invariance, reflection positivity, and
exponential clustering, obtained as the β → ∞, a → 0 limit of 4D SU(N) Wilson
loops.

Evidence: the constructed 15-glyph ℤ/15ℤ word
`⊢≻⋈⊙∈≺≻⊤⊥⊞⋈⊤∋⊣⊡`, its phase-bearing ROTAT readout (A at cuts 0–8, Ttf at 9,
T at 10–11, N at 12–14), the annular braid reading (writhe 1, ρ = 2.2304,
ancestry ∈₄ → ∋₁₂), and the artifact's Lean-verified `IGProtocol` scaffold with
Frobenius closure `μ∘δ = id`.

## Prior assignment

`⟨𐑦𐑸𐑽𐑗𐑐𐑧𐑲𐑵⊙𐑓𐑙𐑟⟩`

field map: dim=𐑦(if'), top=𐑸(are), rel=𐑽(ear), pol=𐑗(church), fid=𐑐(peep),
kin=𐑧(egg), gran=𐑲(ice), gram=𐑵(ooze), crit=⊙(monad), chir=𐑓(fee),
stoi=𐑙(hung), prot=𐑟(zoo).

## Correction derived from the framework's own predicates

`Primitives/Imscription.lean` defines two checked predicates:

- `ImscriptiveClosure i : Prop` — `i.dim = if' → i.top = are → i.prot ≥ ah → i.pol = or'`
- `WindingNeedsChirality i : Prop` — `i.prot ≥ ah → i.chir ≥ sure`

The subject carries dim=if', top=are, prot=zoo (zoo ≥ ah). Therefore:

1. pol must be or' = 𐑹, not church = 𐑗;
2. chir must be ≥ sure = 𐑖, not fee = 𐑓.

The prior assignment fails both predicates. The measured execution resolves the
conflict in the B state: the word's `μ∘δ` closes over transformed reconnections
(Frobenius), and the braid protection is non-Abelian, so the two corrected
coordinates are forced.

## Returned assignment

`⟨𐑦𐑸𐑽𐑹𐑐𐑧𐑲𐑵⊙𐑖𐑙𐑟⟩`

Changed coordinates: pol 𐑗 → 𐑹 (church → or'), chir 𐑓 → 𐑖 (fee → sure).
All other coordinates unchanged.

## Grounding reasoning (contradictions preserved)

- dim 𐑦 / top 𐑸: the boundary losslessly encodes the bulk (ΔS ≈ 0 across the
  continuum limit).
- rel 𐑽: adjoint bulk–boundary coupling; forward and pullback arms are both live.
- pol 𐑹: `μ∘δ = id` — the critical split into bulk and boundary arms rejoins by
  union, with transformed reconnection closing. The four-valued phase-bearing
  readout is kept: A at cuts 0–8, Ttf at 9, T at 10–11, N at 12–14.
- fid 𐑐: reflection positivity affirms exact discrimination; the falsity arm
  refutes Gaussian factorization. Both are held, not collapsed.
- kin 𐑧: fixed at 15, settled in two rounds.
- gran 𐑲: scale-free propagation as ξ → ∞.
- gram 𐑵: cooperative assembly of SU(N) gauge links around the Wilson loop.
- crit ⊙: β → ∞, a → 0 threshold; correlation length diverges.
- chir 𐑖: persistent continuous symmetry (SO(4) with reflection); no preferred
  direction survives.
- stoi 𐑙: equal symmetric conjugate color pairing; braid has 4 strands,
  3 components, writhe 1.
- prot 𐑟: non-Abelian braid protection — the B state holds trivial and
  non-trivial topological classes simultaneously, unresolved.

## Audit boundary

The `IGProtocol` scaffold verifies the protocol term and `μ∘δ = id` on the
imscription. It does not, by itself, prove the analytic properties of the
continuum Schwinger function in `ContinuumClosure.lean`. The p4ramill build-state
guard reports drift in `lakefile.toml` and `toolchain/lib/libleanshared.so`; no
Lake build was started there.
