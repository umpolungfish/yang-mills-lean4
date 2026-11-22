import { useEffect, useMemo, useRef, useState } from 'react';
import { Pause, Play } from 'lucide-react';
import { evaluateCanonicalWitness } from '../utils/yangMillsMath';
import { computeKogutSusskindPathGap } from '../utils/visualSimMath';

export function WilsonLoopWitnessLab() {
  const [suN, setSuN] = useState<number>(3);
  const [fieldMode, setFieldMode] = useState<'one' | 'flip'>('flip');
  const [playing, setPlaying] = useState<boolean>(true);
  const [loopPhase, setLoopPhase] = useState<number>(0);

  const rafRef = useRef<number>(0);

  useEffect(() => {
    let last = performance.now();
    const tick = (now: number) => {
      const dt = Math.max(0, Math.min(0.05, (now - last) / 1000));
      last = now;
      if (playing) {
        setLoopPhase((p) => (p + dt * 0.55) % 1);
      }
      rafRef.current = requestAnimationFrame(tick);
    };
    rafRef.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(rafRef.current);
  }, [playing]);

  const witness = useMemo(() => evaluateCanonicalWitness(suN), [suN]);
  const ksGap = useMemo(() => computeKogutSusskindPathGap(suN), [suN]);

  // Traveler position around the square loop: 0..1 -> 4 edges
  const traveler = useMemo(() => {
    const seg = Math.floor(loopPhase * 4);
    const local = loopPhase * 4 - seg;
    // Square vertices: A(65, 185), B(245, 185), C(245, 55), D(65, 55)
    const corners = [
      { x: 65, y: 185 },
      { x: 245, y: 185 },
      { x: 245, y: 55 },
      { x: 65, y: 55 },
    ];
    const p0 = corners[seg % 4];
    const p1 = corners[(seg + 1) % 4];
    return {
      seg,
      x: p0.x + (p1.x - p0.x) * local,
      y: p0.y + (p1.y - p0.y) * local,
      // Accumulated normalized trace phase as pulse exits Link 1
      afterFlip: fieldMode === 'flip' && seg >= 1,
    };
  }, [loopPhase, fieldMode]);

  // Unit circle eigenvalues for active field
  const eigenvalues = useMemo(() => {
    return witness.diagonalEntries.map((val, idx) => {
      const isFlipped = fieldMode === 'flip' && val === -1;
      // Slight radial spread so overlapping +1 or -1 eigenvalues are all visibly distinct
      const angle = isFlipped ? Math.PI + (idx - 0.5) * 0.14 : (idx - (suN - 1) / 2) * 0.11;
      return {
        idx,
        val: isFlipped ? -1 : 1,
        cx: 110 + 72 * Math.cos(angle),
        cy: 110 - 72 * Math.sin(angle),
      };
    });
  }, [witness.diagonalEntries, fieldMode, suN]);

  const activeTrace = fieldMode === 'one' ? witness.oneNormalized : witness.flipNormalized;

  return (
    <div className="space-y-5">
      {/* Header Control Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 rounded-lg border border-slate-200 bg-white px-5 py-3.5">
        <div>
          <div className="font-mono text-[11px] uppercase tracking-wider text-slate-500">
            §46W CanonicalWitness · §28 Kogut–Susskind Non-Commutation
          </div>
          <h1 className="text-lg font-semibold text-slate-900">
            SU({suN}) Plaquette Holonomy, Eigenvalue Spectrum &amp; Electric–Link Bracket
          </h1>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-1.5">
            <label htmlFor="witness-n" className="font-mono text-xs text-slate-600">
              N = {suN}
            </label>
            <input
              id="witness-n"
              type="range"
              min={2}
              max={10}
              step={1}
              value={suN}
              onChange={(e) => setSuN(Number(e.target.value))}
              className="w-28 accent-blue-600"
            />
          </div>

          <div className="flex rounded border border-slate-200 bg-slate-50 p-0.5 font-mono text-xs">
            <button
              type="button"
              onClick={() => setFieldMode('one')}
              className={`rounded px-2.5 py-1 ${
                fieldMode === 'one' ? 'bg-slate-900 text-white' : 'text-slate-700'
              }`}
            >
              U = 1
            </button>
            <button
              type="button"
              onClick={() => setFieldMode('flip')}
              className={`rounded px-2.5 py-1 ${
                fieldMode === 'flip' ? 'bg-rose-600 text-white' : 'text-slate-700'
              }`}
            >
              U = suFlip2
            </button>
          </div>

          <button
            type="button"
            onClick={() => setPlaying((p) => !p)}
            className="inline-flex items-center gap-1 rounded border border-slate-200 bg-white px-2.5 py-1 font-mono text-xs text-slate-700 hover:bg-slate-50"
          >
            {playing ? <Pause className="h-3.5 w-3.5" /> : <Play className="h-3.5 w-3.5" />}
            {playing ? 'Pause' : 'Play'}
          </button>
        </div>
      </div>

      {/* 3 Visual Figures Grid */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-12">
        {/* FIGURE 1: Animated Plaquette Holonomy Circuit */}
        <div className="rounded-lg border border-slate-200 bg-slate-950 p-4 text-slate-100 lg:col-span-5">
          <div className="flex items-center justify-between font-mono text-xs">
            <span className="text-slate-300">Animated Wilson Loop Holonomy</span>
            <span className={fieldMode === 'flip' ? 'text-rose-400' : 'text-emerald-400'}>
              W_P = {activeTrace.toFixed(4)}
            </span>
          </div>

          <svg viewBox="0 0 320 235" className="mt-2 w-full" role="img" aria-label="Animated plaquette loop holonomy">
            {/* Link 1 (Base link: red when suFlip2) */}
            <line
              x1="65"
              y1="185"
              x2="245"
              y2="185"
              stroke={fieldMode === 'flip' ? '#f43f5e' : '#38bdf8'}
              strokeWidth={fieldMode === 'flip' ? 5 : 3}
            />
            {/* Tail Links 2, 3, 4 */}
            <line x1="245" y1="185" x2="245" y2="55" stroke="#38bdf8" strokeWidth="2.5" />
            <line x1="245" y1="55" x2="65" y2="55" stroke="#38bdf8" strokeWidth="2.5" strokeDasharray="5 4" />
            <line x1="65" y1="55" x2="65" y2="185" stroke="#38bdf8" strokeWidth="2.5" strokeDasharray="5 4" />

            {/* Traveling flux wave orb */}
            <circle
              cx={traveler.x}
              cy={traveler.y}
              r="8"
              fill={traveler.afterFlip ? '#fb7185' : '#34d399'}
              opacity="0.3"
            />
            <circle
              cx={traveler.x}
              cy={traveler.y}
              r="4.5"
              fill={traveler.afterFlip ? '#f43f5e' : '#10b981'}
            />

            {/* Corner vertices */}
            {[
              [65, 185, '⌊x⌋'],
              [245, 185, '+e₁'],
              [245, 55, '+e₁+e₂'],
              [65, 55, '+e₂'],
            ].map(([cx, cy, label]) => (
              <g key={String(label)}>
                <circle cx={Number(cx)} cy={Number(cy)} r="4" fill="#e2e8f0" />
                <text
                  x={Number(cx) + (Number(cx) > 150 ? 10 : -10)}
                  y={Number(cy) + (Number(cy) > 120 ? 16 : -10)}
                  textAnchor={Number(cx) > 150 ? 'start' : 'end'}
                  className="fill-slate-400 font-mono text-[10px]"
                >
                  {label}
                </text>
              </g>
            ))}

            <text
              x="155"
              y="214"
              textAnchor="middle"
              className={`font-mono text-[11px] font-semibold ${
                fieldMode === 'flip' ? 'fill-rose-400' : 'fill-sky-400'
              }`}
            >
              Base Link 1: {fieldMode === 'flip' ? 'suFlip2 ∈ SU(N)' : '1 ∈ SU(N)'}
            </text>
            <text x="155" y="34" textAnchor="middle" className="fill-slate-400 font-mono text-[10px]">
              Tail links = 1 (L ≥ 2 disjoint)
            </text>
          </svg>
        </div>

        {/* FIGURE 2: SU(N) Eigenvalue Circle & Non-Constancy Gauge */}
        <div className="rounded-lg border border-slate-200 bg-white p-4 lg:col-span-3">
          <div className="font-mono text-xs font-semibold text-slate-800">
            SU({suN}) Eigenvalues on S¹ ⊂ ℂ
          </div>
          <div className="font-mono text-[11px] text-slate-500">
            {fieldMode === 'flip' ? '2 at −1, (N−2) at +1' : 'All N at +1'}
          </div>

          <svg viewBox="0 0 220 220" className="mx-auto mt-1 h-48 w-48" role="img" aria-label="SU(N) eigenvalue unit circle">
            <line x1="20" y1="110" x2="200" y2="110" stroke="#e2e8f0" />
            <line x1="110" y1="20" x2="110" y2="200" stroke="#e2e8f0" />
            <circle cx="110" cy="110" r="72" fill="none" stroke="#cbd5e1" strokeWidth="1.5" />

            {eigenvalues.map((ev) => (
              <g key={ev.idx}>
                <line
                  x1="110"
                  y1="110"
                  x2={ev.cx}
                  y2={ev.cy}
                  stroke={ev.val === -1 ? '#f43f5e' : '#2563eb'}
                  strokeWidth="1.5"
                  opacity="0.5"
                />
                <circle
                  cx={ev.cx}
                  cy={ev.cy}
                  r="5.5"
                  fill={ev.val === -1 ? '#e11d48' : '#2563eb'}
                />
              </g>
            ))}

            <text x="206" y="102" textAnchor="end" className="fill-blue-700 font-mono text-[10px] font-semibold">
              +1
            </text>
            <text x="14" y="102" textAnchor="start" className="fill-rose-700 font-mono text-[10px] font-semibold">
              −1
            </text>
          </svg>

          {/* Trace Meter */}
          <div className="mt-1 space-y-1">
            <div className="flex justify-between font-mono text-[11px] text-slate-600 tabular-nums">
              <span>Re Tr(hol)/N:</span>
              <span className="font-semibold text-slate-900">
                {activeTrace.toFixed(4)} ({fieldMode === 'one' ? `${suN}/${suN}` : `${suN - 4}/${suN}`})
              </span>
            </div>
            <div className="relative h-2.5 w-full overflow-hidden rounded bg-slate-100">
              <div
                className={`h-full transition-all duration-300 ${
                  fieldMode === 'flip' ? 'bg-rose-600' : 'bg-blue-600'
                }`}
                style={{ width: `${((activeTrace + 1) / 2) * 100}%` }}
              />
            </div>
            <div className="flex justify-between font-mono text-[9px] text-slate-400">
              <span>−1</span>
              <span>0</span>
              <span>+1</span>
            </div>
          </div>
        </div>

        {/* FIGURE 3: Kogut–Susskind Non-Commutation Animator (§28) */}
        <div className="rounded-lg border border-slate-200 bg-white p-4 lg:col-span-4">
          <div className="flex items-center justify-between">
            <div className="font-mono text-xs font-semibold text-slate-800">
              [T_electric(suFlip2), Tr(U_e)] ≠ 0 (§28)
            </div>
            <span className="font-mono text-xs font-semibold text-emerald-700 tabular-nums">
              gap = 4/{suN} = {ksGap.commutatorMag.toFixed(3)}
            </span>
          </div>

          {/* Animated Commutator Square */}
          <svg viewBox="0 0 340 198" className="mt-2 w-full" role="img" aria-label="Kogut-Susskind commutator square animation">
            {/* Path A (Top: Trace then Shift) -> lands on 1 */}
            <path
              d="M 32 142 L 32 40 L 252 40"
              fill="none"
              stroke="#2563eb"
              strokeWidth="2.5"
            />
            {/* Path B (Bottom: Shift then Trace) -> lands on (N-4)/N */}
            <path
              d="M 32 142 L 252 142 L 252 62"
              fill="none"
              stroke="#e11d48"
              strokeWidth="2.5"
              strokeDasharray="5 3"
            />

            {/* Animated pulse dot on Path A */}
            <circle
              cx={loopPhase < 0.35 ? 32 : 32 + ((loopPhase - 0.35) / 0.65) * 220}
              cy={loopPhase < 0.35 ? 142 - (loopPhase / 0.35) * 102 : 40}
              r="5"
              fill="#2563eb"
            />
            {/* Animated pulse dot on Path B */}
            <circle
              cx={loopPhase < 0.65 ? 32 + (loopPhase / 0.65) * 220 : 252}
              cy={loopPhase < 0.65 ? 142 : 142 - ((loopPhase - 0.65) / 0.35) * 80}
              r="5"
              fill="#e11d48"
            />

            <circle cx="32" cy="142" r="5" fill="#0f172a" />
            <text x="32" y="164" textAnchor="middle" className="fill-slate-700 font-mono text-[10px] font-semibold">
              |1⟩ vac
            </text>

            <text x="150" y="27" textAnchor="middle" className="fill-blue-700 font-mono text-[10px]">
              T_shift · Tr(U_e) ⇒ 1.000
            </text>
            <text x="166" y="164" textAnchor="middle" className="fill-rose-700 font-mono text-[10px]">
              Tr(U_e) · T_shift ⇒ {ksGap.shiftThenTrace.toFixed(3)}
            </text>

            {/* Output Split Bar */}
            <rect x="266" y="34" width="60" height="22" rx="4" fill="#eff6ff" stroke="#2563eb" />
            <text x="296" y="49" textAnchor="middle" className="fill-blue-800 font-mono text-[10px] font-semibold">
              1.00
            </text>

            <rect x="266" y="130" width="60" height="22" rx="4" fill="#fff1f2" stroke="#e11d48" />
            <text x="296" y="145" textAnchor="middle" className="fill-rose-800 font-mono text-[10px] font-semibold">
              {ksGap.shiftThenTrace.toFixed(2)}
            </text>
          </svg>

          <div className="mt-1 flex items-center justify-between border-t border-slate-100 pt-2 font-mono text-[11px] text-slate-600">
            <span>witnessFieldOne vs witnessFieldFlip</span>
            <span className="font-semibold text-slate-900 tabular-nums">
              {witness.oneNormalized.toFixed(2)} ≠ {witness.flipNormalized.toFixed(2)}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
