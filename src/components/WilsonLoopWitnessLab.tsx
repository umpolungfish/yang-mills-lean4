import { useEffect, useMemo, useRef, useState } from 'react';
import { Pause, Play } from 'lucide-react';
import { evaluateCanonicalWitness } from '../utils/ymProofMath';
import { computeKogutSusskindPathGap } from '../utils/visualSimMath';

export function WilsonLoopWitnessLab() {
  const [suN, setSuN] = useState<number>(3);
  const [fieldMode, setFieldMode] = useState<'one' | 'flip'>('flip');
  const [playing, setPlaying] = useState<boolean>(true);
  const [loopPhase, setLoopPhase] = useState<number>(0);
  const [actionBeta, setActionBeta] = useState<number>(2.5);

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

  const traveler = useMemo(() => {
    const seg = Math.floor(loopPhase * 4);
    const local = loopPhase * 4 - seg;
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
      afterFlip: fieldMode === 'flip' && seg >= 1,
    };
  }, [loopPhase, fieldMode]);

  const eigenvalues = useMemo(() => {
    return witness.diagonalEntries.map((val, idx) => {
      const isFlipped = fieldMode === 'flip' && val === -1;
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
      <div className="flex flex-wrap items-center justify-between gap-4 rounded-xl border border-slate-800 bg-[#0c1220] px-5 py-3.5">
        <div>
          <div className="font-mono text-[11px] uppercase tracking-wider text-slate-400">
            §46W CanonicalWitness · §28 Kogut–Susskind Non-Commutation
          </div>
          <h2 className="text-lg font-semibold text-slate-100">
            SU({suN}) Plaquette Holonomy, Eigenvalue Spectrum &amp; Electric–Link Bracket
          </h2>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2">
            <label htmlFor="witness-n" className="font-mono text-xs text-slate-300">
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
              className="w-28 accent-emerald-500"
            />
          </div>

          <div className="flex rounded border border-slate-800 bg-slate-900 p-0.5 font-mono text-xs">
            <button
              type="button"
              onClick={() => setFieldMode('one')}
              className={`rounded px-2.5 py-1 ${
                fieldMode === 'one' ? 'bg-slate-800 text-white' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              U = 1
            </button>
            <button
              type="button"
              onClick={() => setFieldMode('flip')}
              className={`rounded px-2.5 py-1 ${
                fieldMode === 'flip' ? 'bg-rose-600 text-white' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              U = suFlip2
            </button>
          </div>

          <button
            type="button"
            onClick={() => setPlaying((p) => !p)}
            aria-label={playing ? 'Pause Wilson loop animation' : 'Play Wilson loop animation'}
            className="inline-flex items-center gap-1 rounded border border-slate-800 bg-slate-900 px-2.5 py-1 font-mono text-xs text-slate-300 hover:bg-slate-800"
          >
            {playing ? <Pause className="h-3.5 w-3.5" /> : <Play className="h-3.5 w-3.5" />}
            {playing ? 'Pause' : 'Play'}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-12">
        <div className="rounded-xl border border-slate-800 bg-[#070b14] p-4 text-slate-100 lg:col-span-5">
          <div className="flex items-center justify-between font-mono text-xs">
            <span className="text-slate-300">Animated Wilson Loop Holonomy</span>
            <span className={fieldMode === 'flip' ? 'text-rose-400' : 'text-emerald-400'}>
              W_P = {activeTrace.toFixed(4)}
            </span>
          </div>

          <svg viewBox="0 0 320 235" className="mt-2 w-full" role="img" aria-label="Animated plaquette loop holonomy">
            <line
              x1="65"
              y1="185"
              x2="245"
              y2="185"
              stroke={fieldMode === 'flip' ? '#f43f5e' : '#38bdf8'}
              strokeWidth={fieldMode === 'flip' ? 5 : 3}
            />
            <line x1="245" y1="185" x2="245" y2="55" stroke="#38bdf8" strokeWidth="2.5" />
            <line x1="245" y1="55" x2="65" y2="55" stroke="#38bdf8" strokeWidth="2.5" strokeDasharray="5 4" />
            <line x1="65" y1="55" x2="65" y2="185" stroke="#38bdf8" strokeWidth="2.5" strokeDasharray="5 4" />

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

        <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4 lg:col-span-3">
          <div className="font-mono text-xs font-semibold text-slate-200">
            SU({suN}) Eigenvalues on S¹ ⊂ ℂ
          </div>
          <div className="font-mono text-[11px] text-slate-400">
            {fieldMode === 'flip' ? '2 at −1, (N−2) at +1' : 'All N at +1'}
          </div>

          <svg viewBox="0 0 220 220" className="mx-auto mt-1 h-48 w-48" role="img" aria-label="SU(N) eigenvalue unit circle">
            <line x1="20" y1="110" x2="200" y2="110" stroke="#334155" />
            <line x1="110" y1="20" x2="110" y2="200" stroke="#334155" />
            <circle cx="110" cy="110" r="72" fill="none" stroke="#64748b" strokeWidth="1.5" />

            {eigenvalues.map((ev) => (
              <g key={ev.idx}>
                <line
                  x1="110"
                  y1="110"
                  x2={ev.cx}
                  y2={ev.cy}
                  stroke={ev.val === -1 ? '#f43f5e' : '#34d399'}
                  strokeWidth="1.5"
                  opacity="0.5"
                />
                <circle
                  cx={ev.cx}
                  cy={ev.cy}
                  r="5.5"
                  fill={ev.val === -1 ? '#e11d48' : '#10b981'}
                />
              </g>
            ))}

            <text x="206" y="102" textAnchor="end" className="fill-emerald-300 font-mono text-[10px] font-semibold">
              +1
            </text>
            <text x="14" y="102" textAnchor="start" className="fill-rose-300 font-mono text-[10px] font-semibold">
              −1
            </text>
          </svg>

          <div className="mt-1 space-y-1">
            <div className="flex justify-between font-mono text-[11px] text-slate-400 tabular-nums">
              <span>Re Tr(hol)/N:</span>
              <span className="font-semibold text-slate-100">
                {activeTrace.toFixed(4)} ({fieldMode === 'one' ? `${suN}/${suN}` : `${suN - 4}/${suN}`})
              </span>
            </div>
            <div className="relative h-2.5 w-full overflow-hidden rounded bg-slate-800">
              <div
                className={`h-full transition-all duration-300 ${
                  fieldMode === 'flip' ? 'bg-rose-600' : 'bg-emerald-600'
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

        <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4 lg:col-span-4">
          <div className="flex items-center justify-between gap-2">
            <div className="font-mono text-xs font-semibold text-slate-200">
              [T_electric(suFlip2), Tr(U_e)] ≠ 0 (§28)
            </div>
            <span className="font-mono text-xs font-semibold text-emerald-400 tabular-nums">
              gap = 4/{suN} = {ksGap.commutatorMag.toFixed(3)}
            </span>
          </div>

          <svg viewBox="0 0 340 198" className="mt-2 w-full" role="img" aria-label="Kogut-Susskind commutator square animation">
            <path d="M 32 142 L 32 40 L 252 40" fill="none" stroke="#34d399" strokeWidth="2.5" />
            <path
              d="M 32 142 L 252 142 L 252 62"
              fill="none"
              stroke="#e11d48"
              strokeWidth="2.5"
              strokeDasharray="5 3"
            />

            <circle
              cx={loopPhase < 0.35 ? 32 : 32 + ((loopPhase - 0.35) / 0.65) * 220}
              cy={loopPhase < 0.35 ? 142 - (loopPhase / 0.35) * 102 : 40}
              r="5"
              fill="#10b981"
            />
            <circle
              cx={loopPhase < 0.65 ? 32 + (loopPhase / 0.65) * 220 : 252}
              cy={loopPhase < 0.65 ? 142 : 142 - ((loopPhase - 0.65) / 0.35) * 80}
              r="5"
              fill="#e11d48"
            />

            <circle cx="32" cy="142" r="5" fill="#cbd5e1" />
            <text x="32" y="164" textAnchor="middle" className="fill-slate-300 font-mono text-[10px] font-semibold">
              |1⟩ vac
            </text>

            <text x="150" y="27" textAnchor="middle" className="fill-emerald-300 font-mono text-[10px]">
              T_shift · Tr(U_e) ⇒ 1.000
            </text>
            <text x="166" y="164" textAnchor="middle" className="fill-rose-300 font-mono text-[10px]">
              Tr(U_e) · T_shift ⇒ {ksGap.shiftThenTrace.toFixed(3)}
            </text>

            <rect x="266" y="34" width="60" height="22" rx="4" fill="#0c1a36" stroke="#34d399" />
            <text x="296" y="49" textAnchor="middle" className="fill-sky-300 font-mono text-[10px] font-semibold">
              1.00
            </text>

            <rect x="266" y="130" width="60" height="22" rx="4" fill="#4c0519" stroke="#fb7185" />
            <text x="296" y="145" textAnchor="middle" className="fill-rose-300 font-mono text-[10px] font-semibold">
              {ksGap.shiftThenTrace.toFixed(2)}
            </text>
          </svg>

          <div className="mt-1 flex items-center justify-between border-t border-slate-800 pt-2 font-mono text-[11px] text-slate-400">
            <span>witnessFieldOne vs witnessFieldFlip</span>
            <span className="font-semibold text-slate-100 tabular-nums">
              {witness.oneNormalized.toFixed(2)} ≠ {witness.flipNormalized.toFixed(2)}
            </span>
          </div>
        </div>
      </div>

      {/* SU(N) Matrix & Wilson Action Weight Strip */}
      <div className="grid grid-cols-1 gap-5 rounded-xl border border-slate-800 bg-[#0c1220] p-4 lg:grid-cols-12">
        <div className="lg:col-span-6">
          <div className="flex items-center justify-between font-mono text-xs">
            <span className="font-semibold text-white">
              Active Base Link Matrix U ∈ SU({suN})
            </span>
            <span className="text-emerald-400 tabular-nums">det U = {witness.detProduct}</span>
          </div>
          <div className="mt-2.5 flex flex-wrap gap-1.5">
            {witness.diagonalEntries.map((val, idx) => {
              const eff = fieldMode === 'one' ? 1 : val;
              return (
                <div
                  key={idx}
                  className={`flex h-9 w-12 flex-col items-center justify-center rounded border font-mono text-xs tabular-nums ${
                    eff === -1
                      ? 'border-rose-500/50 bg-rose-950/30 text-rose-300'
                      : 'border-emerald-500/40 bg-emerald-950/20 text-emerald-300'
                  }`}
                >
                  <span className="text-[9px] text-slate-400">[{idx},{idx}]</span>
                  <span className="font-bold">{eff > 0 ? '+1' : '−1'}</span>
                </div>
              );
            })}
          </div>
        </div>

        <div className="space-y-2.5 lg:col-span-6">
          <div className="flex items-center justify-between font-mono text-xs">
            <label htmlFor="wilson-beta-action" className="text-slate-300">
              Plaquette Action S_P = 1 − Re Tr(U_P)/N &amp; Weight exp(−β S_P)
            </label>
            <span className="font-semibold text-cyan-300 tabular-nums">β = {actionBeta.toFixed(2)}</span>
          </div>
          <input
            id="wilson-beta-action"
            type="range"
            min={0}
            max={6}
            step={0.1}
            value={actionBeta}
            onChange={(e) => setActionBeta(Number(e.target.value))}
            className="w-full accent-cyan-500"
          />
          <div className="grid grid-cols-3 gap-2 font-mono text-xs tabular-nums">
            <div className="rounded border border-slate-800 bg-[#070b14] p-2">
              <div className="text-[10px] text-slate-400">S_P(U)</div>
              <div className="font-bold text-white">{(1 - activeTrace).toFixed(4)}</div>
            </div>
            <div className="rounded border border-slate-800 bg-[#070b14] p-2">
              <div className="text-[10px] text-slate-400">exp(−β S_P)</div>
              <div className="font-bold text-emerald-400">
                {Math.exp(-actionBeta * (1 - activeTrace)).toFixed(4)}
              </div>
            </div>
            <div className="rounded border border-slate-800 bg-[#070b14] p-2">
              <div className="text-[10px] text-slate-400">Gap ΔS_P</div>
              <div className="font-bold text-cyan-300">{(4 / suN).toFixed(4)}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
