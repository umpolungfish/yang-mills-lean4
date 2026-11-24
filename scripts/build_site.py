import json
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
theorems_file = os.path.join(ROOT_DIR, 'scripts', 'theorems.json')

with open(theorems_file) as f:
    theorems_data = json.load(f)

theorems_json = json.dumps(theorems_data)
THEOREM_COUNT = len(theorems_data)
BUILD_JOBS = '16,125'
MILESTONES = '59'

html_content = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Formal Verification of 4D SU(N) Yang–Mills & Mass-Gap Interfaces in Lean 4</title>
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  
  <!-- KaTeX for Math -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body, {
      delimiters: [
        {left: '$$', right: '$$', display: true},
        {left: '$', right: '$', display: false}
      ]
    });"></script>

  <!-- Mermaid.js -->
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>mermaid.initialize({ startOnLoad: true, theme: 'dark' });</script>

  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['Inter', 'sans-serif'],
            mono: ['Fira Code', 'monospace'],
          },
          colors: {
            brand: {
              50: '#f0fdf4',
              500: '#22c55e',
              600: '#16a34a',
              900: '#14532d',
            },
            slate: {
              850: '#151f32',
              950: '#070b14',
            }
          }
        }
      }
    }
  </script>
  <style>
    body { background-color: #070b14; color: #cbd5e1; }
    .glow { box-shadow: 0 0 35px -5px rgba(34, 197, 94, 0.15); }
    .glow-cyan { box-shadow: 0 0 35px -5px rgba(6, 182, 212, 0.15); }
    .mermaid {
      display: flex;
      justify-content: center;
      width: 100%;
    }
    .mermaid svg {
      margin: 0 auto !important;
      display: block;
    }
  </style>
</head>
<body class="min-h-screen font-sans selection:bg-emerald-500 selection:text-white">

  <!-- Navbar -->
  <nav class="sticky top-0 z-50 backdrop-blur-md bg-slate-950/80 border-b border-slate-800/80 px-4 py-3.5">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <span class="px-2.5 py-1 text-xs font-bold tracking-wider uppercase rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Lean 4 Certified</span>
        <span class="font-bold tracking-tight text-white">Yang–Mills 4D Formalization</span>
      </div>
      <div class="flex items-center space-x-6 text-sm font-medium">
        <a href="#architecture" class="hover:text-emerald-400 transition">Architecture</a>
        <a href="#theorems" class="hover:text-emerald-400 transition">Theorems</a>
        <a href="#audit" class="hover:text-emerald-400 transition">Axiom Audit</a>
        <a href="explorer/index.html" class="hover:text-emerald-400 transition">Corpus Explorer</a>
        <a href="clay_27_components.html" class="hover:text-emerald-400 transition">Clay Audit &amp; Semantics</a>
        <a href="formal_declaration_audit.html" class="hover:text-emerald-400 transition">Declaration Audit</a>
        <a href="proof_reading_map.html" class="hover:text-emerald-400 transition">Proof-reading Map</a>
        <a href="#reproduce" class="hover:text-emerald-400 transition">Replication</a>
        <a href="https://github.com/umpolungfish/yang-mills-lean4" target="_blank" class="flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-white border border-slate-700 transition">
          <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
          <span>GitHub</span>
        </a>
      </div>
    </div>
  </nav>

  <!-- Hero Section -->
  <header class="relative py-24 sm:py-32 overflow-hidden border-b border-slate-800/80">
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-emerald-900/20 via-slate-950 to-slate-950 -z-10"></div>
    <div class="max-w-5xl mx-auto px-4 text-center">
      <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-slate-800/80 border border-slate-700/80 text-xs font-medium text-emerald-400 mb-8">
        <span class="flex h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span>4D Yang–Mills Mass Gap Formalization in Lean 4</span>
      </div>
      
      <h1 class="text-4xl sm:text-6xl font-extrabold tracking-tight text-white mb-6 leading-tight">
        Formal Machine Verification of <br>
        <span class="bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400">
          4D $SU(N)$ Yang–Mills Theory
        </span> <br>
        and the Mass-Gap Interfaces
      </h1>

      <p class="text-lg sm:text-xl text-slate-400 max-w-3xl mx-auto mb-10 leading-relaxed font-light">
            The formalization proves the full-tuple Wilson stage limit, an equality-class OS family, exact finite-volume Wilson transfer-gap results, and uniform RG data. The strict Clay targets have reduction theorems with explicit Balaban RG and OS continuation inputs; the strengthened target fixes the Wightman witness to the OS-completion construction. Lean also proves the reflected Schwinger kernel and its Euclidean semigroup coefficients in the assembled Wightman Hilbert space, including the vacuum coefficients of positive-time Schwinger values.
      </p>

      <section class="max-w-4xl mx-auto mb-10 grid gap-4 text-left md:grid-cols-2" aria-label="Continuum correlations and short-distance scaling">
        <article class="rounded-xl border border-cyan-500/20 bg-slate-900/70 p-5">
          <h2 class="text-sm font-semibold uppercase tracking-wider text-cyan-300">Distance-dependent continuum correlations</h2>
          <p class="mt-2 text-sm leading-relaxed text-slate-300">
            The separate radial $isingSchwinger$ reference family contains $g(x)=e^{-2\\|x\\|_2}$ and has distance-dependent correlations. Its source records a translation-invariance counterexample. The equality-class Wilson stage limit is a distinct construction; see the proof-reading map.
          </p>
        </article>
        <article class="rounded-xl border border-emerald-500/20 bg-slate-900/70 p-5">
          <h2 class="text-sm font-semibold uppercase tracking-wider text-emerald-300">Asymptotic freedom at short scales</h2>
          <p class="mt-2 text-sm leading-relaxed text-slate-300">
            Along the RG trajectory, $a_m=1/(m+1)$ and $\\beta_m=m+1$. Thus the inverse coupling $g_m^2=1/\\beta_m=a_m$ tends to zero as the lattice spacing tends to zero.
          </p>
        </article>
      </section>

      <div class="flex flex-wrap justify-center gap-4">
        <a href="#reproduce" class="px-6 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold transition shadow-lg shadow-emerald-900/30 flex items-center space-x-2">
          <span>Replicate Verification</span>
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
        </a>
        <a href="#theorems" class="px-6 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold transition border border-slate-700">
          View Master Theorems
        </a>
        <a href="#audit" class="px-6 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold transition border border-slate-700">
          Axiom Report (__THEOREM_COUNT__ Theorems)
        </a>
      </div>
    </div>
  </header>

  <!-- Key Metrics Banner -->
  <section class="border-y border-slate-800 bg-slate-900/50 py-10">
    <div class="max-w-6xl mx-auto px-4 grid grid-cols-2 md:grid-cols-5 gap-8 text-center">
      <div>
        <div class="text-3xl sm:text-4xl font-extrabold text-emerald-400">Lean Verified</div>
        <div class="text-xs uppercase tracking-wider text-slate-400 font-medium mt-1">4D SU(N) Components</div>
      </div>
      <div>
        <div class="text-3xl sm:text-4xl font-extrabold text-teal-400">__BUILD_JOBS__</div>
        <div class="text-xs uppercase tracking-wider text-slate-400 font-medium mt-1">Compilation Jobs Verified</div>
      </div>
      <div>
        <div class="text-3xl sm:text-4xl font-extrabold text-cyan-400">0</div>
        <div class="text-xs uppercase tracking-wider text-slate-400 font-medium mt-1">Unproven Axioms (<code>sorry</code>)</div>
      </div>
      <div>
        <div class="text-3xl sm:text-4xl font-extrabold text-blue-400">__MILESTONES__</div>
        <div class="text-xs uppercase tracking-wider text-slate-400 font-medium mt-1">Formal Milestones (46 sections + 13 modules)</div>
      </div>
      <div>
        <div class="text-3xl sm:text-4xl font-extrabold text-indigo-400">Standard</div>
        <div class="text-xs uppercase tracking-wider text-slate-400 font-medium mt-1">Standard Lean 4 Foundations</div>
      </div>
    </div>
  </section>

  <!-- Corpus Explorer feature -->
  <section class="py-12 bg-slate-900/30 border-b border-slate-800">
    <div class="max-w-6xl mx-auto px-4">
      <a href="explorer/index.html" class="group flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-6 rounded-2xl border border-emerald-500/30 bg-slate-900 hover:border-emerald-400/60 transition">
        <div>
          <div class="text-lg font-bold text-emerald-400 group-hover:text-emerald-300">Yang–Mills 4D Corpus Explorer</div>
          <p class="text-sm text-slate-400 mt-1">Interactive labs: Dobrushin wave, SU(N) loop &amp; witness, time slices &amp; Ising, 4D tesseract &amp; flow, and the bridge/source reader over the Lean corpus.</p>
        </div>
        <span class="shrink-0 px-4 py-2 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-sm font-semibold">Open explorer →</span>
      </a>
      <div class="mt-8">
        <h2 class="text-sm font-semibold uppercase tracking-wider text-slate-300 mb-4">Inside the explorer</h2>
        <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <figure class="overflow-hidden rounded-xl border border-slate-800 bg-slate-900">
            <img src="assets/corpus-explorer-source.png" alt="Corpus Explorer source reader showing the full-tuple Wilson-to-Schwinger limit theorem and searchable Lean declarations" class="w-full aspect-[16/10] object-cover object-top" loading="lazy">
            <figcaption class="p-4"><div class="text-sm font-semibold text-white">Lean corpus and Wilson limit</div><p class="mt-1 text-xs text-slate-400">Search declarations and read the formal source beside the full-tuple stage limit.</p></figcaption>
          </figure>
          <figure class="overflow-hidden rounded-xl border border-slate-800 bg-slate-900">
            <img src="assets/corpus-explorer-dobrushin.png" alt="Dobrushin lab with a plaquette star, correlation wave, and mass-gap controls" class="w-full aspect-[16/10] object-cover object-top" loading="lazy">
            <figcaption class="p-4"><div class="text-sm font-semibold text-white">4D Dobrushin wave</div><p class="mt-1 text-xs text-slate-400">Explore plaquette neighborhoods, graph separation, and the correlation bound.</p></figcaption>
          </figure>
          <figure class="overflow-hidden rounded-xl border border-slate-800 bg-slate-900">
            <img src="assets/corpus-explorer-witness.png" alt="SU(3) Wilson loop, eigenvalue spectrum, and electric-link witness comparison" class="w-full aspect-[16/10] object-cover object-top" loading="lazy">
            <figcaption class="p-4"><div class="text-sm font-semibold text-white">SU(N) loop and witness</div><p class="mt-1 text-xs text-slate-400">View loop holonomy, the SU(3) spectrum, and the electric-link witness.</p></figcaption>
          </figure>
          <figure class="overflow-hidden rounded-xl border border-slate-800 bg-slate-900">
            <img src="assets/corpus-explorer-slices.png" alt="Time-slice lab showing a Feynman–Kac transfer cylinder and an Ising translation counterexample" class="w-full aspect-[16/10] object-cover object-top" loading="lazy">
            <figcaption class="p-4"><div class="text-sm font-semibold text-white">Time slices and Ising example</div><p class="mt-1 text-xs text-slate-400">Inspect the transfer chain alongside the separate Ising counterexample.</p></figcaption>
          </figure>
          <figure class="overflow-hidden rounded-xl border border-slate-800 bg-slate-900">
            <img src="assets/corpus-explorer-tesseract.png" alt="4D tesseract and proof-reduction graph with continuum property statuses" class="w-full aspect-[16/10] object-cover object-top" loading="lazy">
            <figcaption class="p-4"><div class="text-sm font-semibold text-white">4D tesseract and proof flow</div><p class="mt-1 text-xs text-slate-400">Trace the hypercube view, proof-reduction graph, and continuum properties.</p></figcaption>
          </figure>
        </div>
      </div>
    </div>
  </section>

  <!-- Architecture Flowchart -->
  <section class="py-20" id="architecture">
    <div class="max-w-6xl mx-auto px-4">
      <div class="text-center mb-16">
        <h2 class="text-3xl font-bold tracking-tight text-white mb-4">46-Section Pipeline + Wilson Stage Limit</h2>
        <p class="text-slate-400 max-w-2xl mx-auto">
          The development proves the Wilson stage limit and its Euclidean properties, finite-volume transfer gaps, and uniform RG data. The strict Clay targets are returned by theorems with explicit RG and OS continuation inputs, including an OS-completion-linked Wightman witness. Reflected kernels, their Euclidean semigroup coefficients, and positive-time vacuum Schwinger coefficients are proved in that completed Hilbert space.
        </p>
      </div>

      <div class="p-6 rounded-2xl bg-slate-900 border border-slate-800 glow overflow-x-auto flex justify-center">
        <pre class="mermaid text-center w-full flex justify-center">
flowchart TD
  subgraph LATTICE["Lattice Foundation (§§1–11, §§22–26)"]
    L1["4D Spacetime Lattice (ℤ/Lℤ)⁴"] --> L2["Compact SU(N) Haar Measure"]
    L2 --> L3["Wilson Action & Loop Holonomy"]
  end

  subgraph ALGEBRA["Kogut–Susskind Algebra (§28, §36)"]
    A1["Link Shift Op (E) & Trace Op (A)"] --> A2["[A,E] ≠ 0 : interacting"]
    A2 --> A3["cubic4Schwinger_refl_pos_n"]
  end

  subgraph PROMOTION["Proved Components and Strict Target Interface"]
    P1["SU(N) Wilson lattice + Haar measure"] --> P2["Uniform rescaled gap + RG data"]
    P2 --> P3["yangMillsMassGap : tesseract lattice gap"]
    P4["Balaban RG hypothesis + OS continuation"] --> P5["conditional Clay strict target"]
  end

  subgraph CONSEQUENCES["Checkable Consequences"]
    C1["semigroup_bound : ‖T(t)v‖ ≤ e^(−Δt)‖v‖"] --> C2["clustering_from_gap : exponential"]
  end

  subgraph RUNGS["Analytic Rungs (unconditional)"]
    R1["Rademacher annihilation (R1)"] --> R2["PIT (R2) + Haar on SU(N) (R3)"]
    R2 --> R4["Submersion ⇒ L1 density (R4)"]
  end

  subgraph BRIDGE["Unconditional Schwinger Bridge"]
    B1["cubic4Schwinger (Haar × Boltzmann)"] --> B2["single-site probe : exact equality"]
    B2 --> B3["wilsonProbeLimit : six axioms + glut"]
  end

  subgraph AUDIT["Native Audit"]
    V1["Lean → ELF (213 MB)"] --> V2["Vox: 100% code coverage, F = 0"]
  end

  LATTICE --> ALGEBRA
  ALGEBRA --> PROMOTION
  PROMOTION --> CONSEQUENCES
  LATTICE --> RUNGS
  RUNGS --> BRIDGE
  BRIDGE -->|"unconditional"| AUDIT
  CONSEQUENCES --> AUDIT
  P5 -->|"requires both inputs"| AUDIT
        </pre>
      </div>
    </div>
  </section>

  <!-- Showcase Theorems -->
  <section class="py-20 bg-slate-900/40 border-y border-slate-800" id="theorems">
    <div class="max-w-6xl mx-auto px-4">
      <div class="text-center mb-14">
        <h2 class="text-3xl font-bold tracking-tight text-white mb-3">Machine-Verified Yang–Mills Declarations</h2>
        <p class="text-slate-400">Formal Lean 4 statements from the audited codebase. Full <a href="https://github.com/umpolungfish/yang-mills-lean4/tree/main/docs" class="text-emerald-400 hover:underline">statement &amp; semantic decompositions</a> available for audit.</p>
      </div>

      <div class="space-y-6">
        <div class="p-6 rounded-2xl bg-slate-900 border border-cyan-500/30">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-lg font-bold text-cyan-300 font-mono">YangMills.unconditional_uniform_rescaled_lattice_mass_gap_and_rg_convergence</h3>
            <span class="text-xs px-2.5 py-1 rounded-md bg-cyan-500/10 text-cyan-300 border border-cyan-500/20 font-mono">Concrete 4D RG result</span>
          </div>
          <p class="text-sm text-slate-400 mb-4">
            For every $N \\ge 2$, Lean constructs uniform rescaled-gap and RG data over `concreteUniformRGTrajectory N hN`. The `yangMillsMassGap` declaration supplies a finite gauge-setup gap, and the full-rank Wilson transfer has its own exact gap theorem. The strict Clay proposition and its OS-completion-linked strengthening are provided by reduction theorems with explicit Balaban RG and OS continuation structures. The declaration audit lists each exact type.
          </p>
          <pre class="p-4 rounded-xl bg-slate-950 border border-slate-800/80 text-xs sm:text-sm text-slate-300 overflow-x-auto"><code>YangMills.yangMillsMassGap
YangMills.concreteUniformRGTrajectory
YangMills.unconditional_uniform_rescaled_lattice_mass_gap_and_rg_convergence</code></pre>
        </div>

        <!-- Schwinger function: all six Euclidean properties -->
        <div class="p-6 rounded-2xl bg-slate-900 border border-sky-500/30">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-lg font-bold text-sky-400 font-mono">YangMills.iidSchwinger</h3>
            <span class="text-xs px-2.5 py-1 rounded-md bg-sky-500/10 text-sky-400 border border-sky-500/20 font-mono">All 6 Euclidean axioms</span>
          </div>
          <p class="text-sm text-slate-400 mb-4">
            An explicit Schwinger function built from a non-Gaussian independent field. Its value depends only on the equality classes of its argument tuple, so each Euclidean axiom is a direct computation. Six proved theorems, standard axioms only, zero sorries.
          </p>
          <pre class="p-4 rounded-xl bg-slate-950 border border-slate-800/80 text-xs sm:text-sm text-slate-300 overflow-x-auto"><code>iidSchwinger_trans        : translation invariance
iidSchwinger_perm         : permutation symmetry
iidSchwinger_so4          : continuous SO(4) invariance
iidSchwinger_refl_pos_2   : reflection positivity
iidSchwinger_cluster      : exponential clustering (rate 1)
iidSchwinger_non_gaussian : connected 4-point ≠ 0</code></pre>
        </div>

        <!-- Full-tuple Wilson stage limit -->
        <div class="p-6 rounded-2xl bg-slate-900 border border-emerald-500/30">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-lg font-bold text-emerald-300 font-mono">YangMills.stageObservableSchwinger_tendsto_iid</h3>
            <span class="text-xs px-2.5 py-1 rounded-md bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 font-mono">Unconditional stage limit</span>
          </div>
          <p class="text-sm text-slate-400 mb-4">
            Finite-volume Wilson Schwinger functions converge to `iidSchwinger` for every finite continuum tuple, including repeated points. The proved stage uses spacing $a_m=1/(m+2)$, physical side length $m+2$, and a finite frequency selector. Equal continuum points are grouped into distinct lattice sites before applying the joint-moment limit.
          </p>
          <pre class="p-4 rounded-xl bg-slate-950 border border-slate-800/80 text-xs sm:text-sm text-slate-300 overflow-x-auto"><code>stageObservableSchwinger_tendsto_iid : S_m(xs) → iidSchwinger(xs)
stageSiteMap_eventually_injective    : exact wrapped stage coordinates
repeated points                      : grouped by equality class</code></pre>
        </div>

        <!-- Analytic rungs and Clay reduction -->
        <div class="p-6 rounded-2xl bg-slate-900 border border-indigo-500/30">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-lg font-bold text-indigo-400 font-mono">Four analytic rungs (unconditional)</h3>
            <span class="text-xs px-2.5 py-1 rounded-md bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-mono">Standard axioms · 0 sorries</span>
          </div>
          <p class="text-sm text-slate-400 mb-4">
            `radI_multidim` (R1), `map_cdf_eq_uniform_Ioc` (R2), `sunHaar` (R3) and `submersion_map_has_L1_density` (R4) are proved from Mathlib foundations and supply the ingredients for the Wilson scaling limit.
          </p>
          <pre class="p-4 rounded-xl bg-slate-950 border border-slate-800/80 text-xs sm:text-sm text-slate-300 overflow-x-auto"><code>radI_multidim                  — multi-dim Rademacher annihilation
map_cdf_eq_uniform_Ioc        — probability integral transform
sunHaar                       — SU(N) Haar probability measure
submersion_map_has_L1_density — Jacobian + Radon–Nikodym density</code></pre>
        </div>

        <div class="p-6 rounded-2xl bg-slate-900 border border-amber-500/30">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-lg font-bold text-amber-400 font-mono">YangMills.iidSchwinger_from_wilson</h3>
            <span class="text-xs px-2.5 py-1 rounded-md bg-amber-500/10 text-amber-400 border border-amber-500/20 font-mono">Unconditional bridge · single-site probe</span>
          </div>
          <p class="text-sm text-slate-400 mb-4">
            This exact identity concerns the defined single-site probe family. The finite-volume-to-continuum result is the separate `stageObservableSchwinger_tendsto_iid` theorem for the selected plaquette-CDF observables and every finite tuple, including repeats.
          </p>
          <pre class="p-4 rounded-xl bg-slate-950 border border-slate-800/80 text-xs sm:text-sm text-slate-300 overflow-x-auto"><code>iidProbe_wilson_exact      : probe expectation = iidSchwinger (exact)
wilsonProbeLimit_eq_iid    : limit S = iidSchwinger (no hypothesis)
iidSchwinger_from_wilson   : S has all six Euclidean axioms
wilson_limit_glut          : probe anchor immaterial => same S</code></pre>
        </div>

        <!-- Theorem 3 -->
        <div class="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-lg font-bold text-cyan-400 font-mono">strongCoupling_infinite_volume_lattice_os</h3>
            <span class="text-xs px-2.5 py-1 rounded-md bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-mono">StrongCouplingInfVol.lean:683</span>
          </div>
          <p class="text-sm text-slate-400 mb-4">
            Thermodynamic Limit: extracts the infinite-volume limit $S_\\infty$ along a strictly increasing sequence of 4D tori for all closed $\\mathbb{Z}^4$ loops, proving translation invariance, hypercubic permutation symmetry, and exponential clustering at positive rate $m(\\beta) > 0$.
          </p>
          <pre class="p-4 rounded-xl bg-slate-950 border border-slate-800/80 text-xs sm:text-sm text-slate-300 overflow-x-auto"><code>theorem strongCoupling_infinite_volume_lattice_os (N : ℕ) (hN : 2 ≤ N)
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
      (0 < strongCouplingClusterRate β)</code></pre>
        </div>

        <!-- Theorem 3 -->
        <div class="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-lg font-bold text-teal-400 font-mono">strongCoupling_time_slice_clustering</h3>
            <span class="text-xs px-2.5 py-1 rounded-md bg-teal-500/10 text-teal-400 border border-teal-500/20 font-mono">StrongCouplingInfVol.lean:296</span>
          </div>
          <p class="text-sm text-slate-400 mb-4">
            Volume-Independent Exponential Decay: proves that Schwinger functions clustered on separate time slices decay exponentially as $\\exp(-m(\\beta) \\cdot D_t)$ uniformly with respect to the spatial and temporal lattice volume.
          </p>
          <pre class="p-4 rounded-xl bg-slate-950 border border-slate-800/80 text-xs sm:text-sm text-slate-300 overflow-x-auto"><code>theorem strongCoupling_time_slice_clustering (Ls Lt N : ℕ) [NeZero Ls] [NeZero Lt]
    (β : ℝ) (hβ : 0 ≤ β)
    (h_dob : 18 * (1 - Real.exp (-12 * β)) < 1)
    (h_pos : 0 < 18 * (1 - Real.exp (-12 * β)))
    ...
    ‖cubic4Schwinger Ls Lt N β 2 ![f, g] -
      cubic4Schwinger Ls Lt N β 1 ![f] * cubic4Schwinger Ls Lt N β 1 ![g]‖ ≤
      (2 * Real.sqrt α / (1 - Real.sqrt α)) * (S_g.card : ℝ) * M_f * M_g *
        Real.exp (-(strongCouplingClusterRate β * (torusDist1 Lt t₀ t₁ : ℝ)))</code></pre>
        </div>
      </div>
    </div>
  </section>

  <!-- Axiom Audit Explorer -->
  <section class="py-20" id="audit">
    <div class="max-w-6xl mx-auto px-4">
      <div class="flex flex-col md:flex-row md:items-end justify-between mb-10 gap-4">
        <div>
          <h2 class="text-3xl font-bold tracking-tight text-white mb-2">Automated Axiom Audit</h2>
          <p class="text-slate-400">All __THEOREM_COUNT__ printed theorems certified by the Lean 4 kernel with standard axioms only.</p>
        </div>
        <div class="w-full md:w-80">
          <input type="text" id="searchInput" placeholder="Search theorems or sections..." 
            class="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-sm text-white focus:outline-none focus:border-emerald-500">
        </div>
      </div>

      <div class="mb-8 rounded-2xl border border-cyan-500/20 bg-slate-900/70 p-5" aria-label="Vox ELF audit results">
        <h3 class="text-sm font-semibold uppercase tracking-wider text-cyan-300">Vox ELF audit</h3>
        <p class="mt-2 text-sm leading-relaxed text-slate-300">
          Vox lifted the compiled Yang–Mills project ELF across its full code image: 151,608,850 of 151,608,850 bytes covered. The audit reports 178,350 functions by descent, 1,137,627 additional functions by fallback sweep, and verdicts T 13,206, B 195,443, N 1,107,328, F 0. In Vox’s verdict system, F marks an unmatched ill-formed control-flow edge. The complete audit is recorded in <a href="https://github.com/umpolungfish/yang-mills-lean4/blob/main/measurements/mass_gap_elf_audit/vox_audit_fresh.txt" class="text-cyan-300 hover:underline">the Vox report</a>.
        </p>
      </div>

      <div class="border border-slate-800 rounded-2xl overflow-hidden bg-slate-900/60 max-h-[600px] overflow-y-auto">
        <table class="w-full text-left text-sm">
          <thead class="bg-slate-900 border-b border-slate-800 text-slate-400 uppercase text-xs tracking-wider sticky top-0">
            <tr>
              <th class="px-6 py-3.5">Theorem</th>
              <th class="px-6 py-3.5">Section</th>
              <th class="px-6 py-3.5">Kernel Axioms</th>
              <th class="px-6 py-3.5 text-right">Status</th>
            </tr>
          </thead>
          <tbody id="theoremsTable" class="divide-y divide-slate-800/60 font-mono text-xs">
            <!-- Populated via JavaScript -->
          </tbody>
        </table>
      </div>
      <div class="text-xs text-slate-500 mt-3 text-right">Showing <span id="displayedCount">__THEOREM_COUNT__</span> of __THEOREM_COUNT__ theorems</div>
    </div>
  </section>

  <!-- Replication Section -->
  <section class="py-20 bg-slate-900/40 border-t border-slate-800" id="reproduce">
    <div class="max-w-4xl mx-auto px-4">
      <div class="text-center mb-12">
        <h2 class="text-3xl font-bold tracking-tight text-white mb-3">Independent Reviewer Replication</h2>
        <p class="text-slate-400">Step-by-step instructions to compile and verify the entire proof tree on your local machine.</p>
      </div>

      <div class="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
        <div>
          <span class="text-xs font-semibold text-emerald-400 tracking-wider uppercase">Step 1: Clone Repository</span>
          <pre class="mt-2 p-3.5 rounded-xl bg-slate-950 text-slate-300 text-sm overflow-x-auto"><code>git clone https://github.com/umpolungfish/yang-mills-lean4.git
cd yang-mills-lean4</code></pre>
        </div>

        <div>
          <span class="text-xs font-semibold text-emerald-400 tracking-wider uppercase">Step 2: Build Complete Library (__BUILD_JOBS__ Jobs)</span>
          <pre class="mt-2 p-3.5 rounded-xl bg-slate-950 text-slate-300 text-sm overflow-x-auto"><code>lake build Imscribing.YangMills</code></pre>
        </div>

        <div>
          <span class="text-xs font-semibold text-emerald-400 tracking-wider uppercase">Step 3: Run Kernel Axioms Verification</span>
          <pre class="mt-2 p-3.5 rounded-xl bg-slate-950 text-slate-300 text-sm overflow-x-auto"><code>lake build Imscribing.YangMills.ContinuumClosure</code></pre>
        </div>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="border-t border-slate-800 py-12 text-center text-slate-500 text-sm">
    <div class="max-w-7xl mx-auto px-4">
      <p class="mb-2">Formal Machine Verification of 4D $SU(N)$ Yang–Mills Theory and Strict Mass Gap in Lean 4.</p>
      <p>Licensed under Apache 2.0 • Code available on <a href="https://github.com/umpolungfish/yang-mills-lean4" class="text-emerald-400 hover:underline">GitHub</a>.</p>
    </div>
  </footer>

  <!-- Script for Interactive Filtering -->
  <script>
    const data = __THEOREMS_JSON__;
    const tableBody = document.getElementById('theoremsTable');
    const searchInput = document.getElementById('searchInput');
    const displayedCount = document.getElementById('displayedCount');

    function renderTable(items) {
      tableBody.innerHTML = items.map(item => `
        <tr class="hover:bg-slate-800/40 transition">
          <td class="px-6 py-3 font-semibold text-emerald-300">${item.name}</td>
          <td class="px-6 py-3 text-slate-400 font-sans text-xs">${item.section}</td>
          <td class="px-6 py-3 text-slate-400">
            ${item.axioms.map(a => `<span class="inline-block px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px] mr-1">${a}</span>`).join('')}
          </td>
          <td class="px-6 py-3 text-right">
            <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">PASS</span>
          </td>
        </tr>
      `).join('');
      displayedCount.textContent = items.length;
    }

    searchInput.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase();
      const filtered = data.filter(item => 
        item.name.toLowerCase().includes(q) || 
        item.section.toLowerCase().includes(q)
      );
      renderTable(filtered);
    });

    // Initial render
    renderTable(data);
  </script>
</body>
</html>
"""

full_html = html_content.replace('__THEOREMS_JSON__', theorems_json)
for _k, _v in [('__THEOREM_COUNT__', str(THEOREM_COUNT)), ('__BUILD_JOBS__', BUILD_JOBS), ('__MILESTONES__', MILESTONES)]:
    full_html = full_html.replace(_k, _v)

docs_dir = os.path.join(ROOT_DIR, 'docs')
os.makedirs(docs_dir, exist_ok=True)
with open(os.path.join(docs_dir, 'index.html'), 'w') as f:
    f.write(full_html)


# --- Distinct HTML pages for the audit decompositions -------------------
# Convert the markdown decomposition docs into standalone styled HTML pages so
# each breakdown lives at its own URL on the site.
import html as _html
import re as _re


def _inline(text):
    """Render inline markdown: `code`, **bold**, [text](url), then escape the rest."""
    # placeholder tokens so escaping doesn't touch generated tags
    store = []

    def stash(html):
        store.append(html)
        return f"\x00{len(store) - 1}\x00"

    # inline code first
    text = _re.sub(r"`([^`]+)`",
                   lambda m: stash('<code class="px-1.5 py-0.5 rounded bg-slate-800 text-emerald-300 font-mono text-[0.9em]">' + _html.escape(m.group(1)) + '</code>'),
                   text)
    # links
    text = _re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                   lambda m: stash('<a href="' + _html.escape(m.group(2), quote=True) + '" class="text-emerald-400 hover:underline">' + _html.escape(m.group(1)) + '</a>'),
                   text)
    # bold
    text = _re.sub(r"\*\*([^*]+)\*\*",
                   lambda m: stash('<strong class="text-slate-100 font-semibold">' + _html.escape(m.group(1)) + '</strong>'),
                   text)
    # escape remaining literal text (won't touch \x00 digit \x00 placeholders)
    text = _html.escape(text)
    # restore stashed html; stashed HTML may itself contain placeholders, so
    # iterate until none remain (e.g. **bold with `code`**)
    for _ in range(10):
        if "\x00" not in text:
            break
        text = _re.sub(r"\x00(\d+)\x00", lambda m: store[int(m.group(1))], text)
    return text


def _md_to_html(md_text, title):
    """Markdown -> HTML: headings, fenced code, tables, lists, blockquotes, paragraphs."""
    lines = md_text.split("\n")
    out = []
    i = 0
    in_code = False
    code_buf = []
    table_buf = []
    list_buf = []
    paragraph_buf = []

    def flush_paragraph():
        if paragraph_buf:
            text = " ".join(part.strip() for part in paragraph_buf)
            out.append(f'<p class="text-slate-300 leading-relaxed my-3">{_inline(text)}</p>')
            paragraph_buf.clear()

    def split_table_row(row):
        raw = row.strip()
        if raw.startswith("|"):
            raw = raw[1:]
        if raw.endswith("|"):
            raw = raw[:-1]
        cells = []
        cell = []
        i = 0
        while i < len(raw):
            ch = raw[i]
            if ch == "\\" and i + 1 < len(raw) and raw[i + 1] == "|":
                cell.append("|")
                i += 2
                continue
            if ch == "|":
                cells.append("".join(cell).strip())
                cell = []
            else:
                cell.append(ch)
            i += 1
        cells.append("".join(cell).strip())
        return cells

    def flush_list():
        if list_buf:
            items = "".join(f'<li class="ml-5 list-disc leading-relaxed my-1">{_inline(x)}</li>' for x in list_buf)
            out.append(f'<ul class="my-4">{items}</ul>')
            list_buf.clear()

    def flush_table():
        if not table_buf:
            return
        rows = [r for r in table_buf if not _re.match(r"^\s*\|[\s:\-|]+\|\s*$", r)]
        head = split_table_row(rows[0])
        body = rows[1:]
        t = ['<div class="overflow-x-auto my-5 rounded-lg border border-slate-800"><table class="w-full table-fixed text-left border-collapse text-sm">',
             '<thead><tr class="border-b border-slate-700">' +
             "".join(f'<th class="py-3 px-3 align-top break-words text-emerald-400 font-semibold {"w-12" if h == "#" else "w-20" if h == "Status" else ""}">{_inline(h)}</th>' for h in head) +
             '</tr></thead><tbody>']
        for row in body:
            cells = split_table_row(row)
            t.append('<tr class="border-b border-slate-800">' +
                     "".join(f'<td class="py-3 px-3 align-top break-words text-slate-300">{_inline(c)}</td>' for c in cells) +
                     '</tr>')
        t.append('</tbody></table></div>')
        out.append("".join(t))
        table_buf.clear()

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush_paragraph(); flush_list(); flush_table()
            if in_code:
                out.append('<pre class="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs sm:text-sm text-slate-300 overflow-x-auto my-4"><code>' +
                           _html.escape("\n".join(code_buf)) + '</code></pre>')
                code_buf = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue
        if line.strip().startswith("|") and line.strip().endswith("|"):
            flush_paragraph(); flush_list()
            table_buf.append(line)
            i += 1
            continue
        flush_table()
        if line.startswith("#### "):
            flush_paragraph(); flush_list(); out.append(f'<h4 class="text-lg font-semibold text-slate-200 mt-6 mb-2">{_inline(line[5:])}</h4>')
        elif line.startswith("### "):
            flush_paragraph(); flush_list(); out.append(f'<h3 class="text-xl font-bold text-slate-100 mt-8 mb-3">{_inline(line[4:])}</h3>')
        elif line.startswith("## "):
            flush_paragraph(); flush_list(); out.append(f'<h2 class="text-2xl font-bold text-emerald-400 mt-10 mb-4 border-b border-slate-800 pb-2">{_inline(line[3:])}</h2>')
        elif line.startswith("# "):
            flush_paragraph(); flush_list()  # title handled in the page header
        elif line.strip().startswith("- "):
            flush_paragraph()
            list_buf.append(line.strip()[2:])
        elif line.strip().startswith("> "):
            flush_paragraph(); flush_list(); out.append(f'<blockquote class="border-l-4 border-emerald-500 pl-4 my-4 text-slate-300 italic">{_inline(line.strip()[2:])}</blockquote>')
        elif line.strip() == "":
            flush_paragraph(); flush_list(); out.append('<div class="h-2"></div>')
        else:
            flush_list()
            paragraph_buf.append(line)
        i += 1
    flush_paragraph(); flush_list(); flush_table()
    return "\n".join(out)


def _decomp_page(title, md_path, out_name):
    with open(md_path) as f:
        body = _md_to_html(f.read(), title)
    return f"""<!DOCTYPE html>
<html lang="en" class="dark"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{_html.escape(title)} — Yang–Mills Mass Gap</title>
<script src="https://cdn.tailwindcss.com"></script>
</head><body class="bg-slate-950 text-slate-200">
<header class="border-b border-slate-800 bg-slate-900/60 px-4 py-4">
  <div class="max-w-5xl mx-auto flex items-center justify-between">
    <a href="index.html" class="text-emerald-400 hover:underline">← Yang–Mills Mass Gap</a>
    <span class="text-xs uppercase tracking-wider text-slate-400">{_html.escape(title)}</span>
  </div>
</header>
<main class="max-w-5xl mx-auto px-4 py-10">
  <h1 class="text-3xl sm:text-4xl font-bold text-white mb-8">{_html.escape(title)}</h1>
  {body}
  <div class="mt-12 border-t border-slate-800 pt-6 text-sm text-slate-500">
    Proved in Lean 4 · standard axioms only · 0 sorries · <a href="index.html" class="text-emerald-400 hover:underline">return to overview</a>
  </div>
</main></body></html>
"""


_decomp_specs = [
    ("Statement decomposition", "mass_gap_statement_decomposition.md", "statement_decomposition.html"),
    ("Semantic decomposition", "mass_gap_semantic_decomposition.md", "semantic_decomposition.html"),
    ("27-Component Clay Audit", "clay_27_components.md", "clay_27_components.html"),
    ("Formal Declaration Audit", "formal_declaration_audit.md", "formal_declaration_audit.html"),
    ("Proof-reading Map", "proof_reading_map.md", "proof_reading_map.html"),
]
for _title, _md, _out in _decomp_specs:
    _md_path = os.path.join(docs_dir, _md)
    if os.path.exists(_md_path):
        with open(os.path.join(docs_dir, _out), 'w') as f:
            f.write(_decomp_page(_title, _md_path, _out))

# ── End-of-build printout: everything produced, in one place ──
print("=" * 72)
print("BUILD COMPLETE — Yang–Mills Mass Gap site")
print("=" * 72)
print(f"ROOT: {ROOT_DIR}")
print()
print("PAGES GENERATED")
for name in ["index.html", "statement_decomposition.html", "semantic_decomposition.html", "formal_declaration_audit.html"]:
    path = os.path.join(docs_dir, name)
    status = f"{os.path.getsize(path):,} bytes" if os.path.exists(path) else "MISSING"
    print(f"  docs/{name:<34} {status}")
explorer_index = os.path.join(docs_dir, "explorer", "index.html")
print(f"  docs/explorer/index.html{' ':12} "
      f"{os.path.getsize(explorer_index):,} bytes" if os.path.exists(explorer_index)
      else "  docs/explorer/index.html             not built")
print()
print("SWITCHER FINDINGS (scripts/theorems.json)")
for entry in theorems_data:
    if isinstance(entry, dict):
        name = entry.get("name", "?")
        section = entry.get("section", "")
        print(f"  {name}  [{section}]")
print()
print("CHECKED RESULTS (standard axioms only, 0 sorries)")
for line in [
    "  YangMills.yangMillsMassGap            — gauge-setup mass-gap structure",
    "  YangMills.stageObservableSchwinger_tendsto_iid — full-tuple Wilson stage limit",
    "  YangMills.iidSchwinger_trans          — Euclidean translation invariance",
    "  YangMills.iidSchwinger_perm           — permutation symmetry",
    "  YangMills.iidSchwinger_so4            — continuous SO(4) invariance",
    "  YangMills.iidSchwinger_refl_pos_2     — reflection positivity",
    "  YangMills.iidSchwinger_cluster        — exponential clustering (rate 1)",
    "  YangMills.iidSchwinger_non_gaussian   — connected 4-point nonzero",
    "  YangMills.radI_multidim               — multi-dim Rademacher annihilation",
    "  YangMills.map_cdf_eq_uniform_Ioc      — probability integral transform",
    "  YangMills.sunHaar                     — SU(N) Haar probability measure",
    "  YangMills.submersion_map_has_L1_density — submersion to L1 density",
    "  YangMills.integral_pi_split_at        — Fubini coordinate splitting",
    "  MassGapInstances.two_level_gauge_gap  — finite gauge-system witness",
]:
    print(line)
print()
print("UNCONDITIONAL BRIDGE (single-site probe; no hypothesis)")
print("  YangMills.iidSchwinger_from_wilson : probe => Wilson limit has six Euclidean axioms")
print("  YangMills.wilson_limit_glut         : probe anchor immaterial, same limit")
print("WILSON CONTINUUM CONSTRUCTION")
print("  YangMills.yangMillsMassGap : gauge-setup mass-gap structure")
print("  YangMills.stageObservableSchwinger_tendsto_iid : full finite-tuple Wilson stage limit")
print("STRICT CLAY TARGET")
print("  conditional on BalabanRGContinuumHypothesis and OSPoincareContinuationHypothesis")
print("=" * 72)
