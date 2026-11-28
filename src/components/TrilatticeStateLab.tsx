import { useMemo, useState } from 'react';
import { RotateCcw } from 'lucide-react';
import {
  auditState,
  CANONICAL,
  canonicalWalk,
  eqState,
  leF,
  leI,
  leT,
  s16,
  SIXTEEN_STATES,
  stateLabel,
  walkPath,
  type Sixteen3,
} from '../utils/trilatticeMath';

type OrderMode = 'le_i' | 'le_t' | 'le_f';

const ORDER_LABEL: Record<OrderMode, string> = {
  le_i: 'le_i · information',
  le_t: 'le_t · truth',
  le_f: 'le_f · falsity',
};

const ORDER_FN: Record<OrderMode, (a: Sixteen3, b: Sixteen3) => boolean> = {
  le_i: leI,
  le_t: leT,
  le_f: leF,
};

export function TrilatticeStateLab() {
  const [selected, setSelected] = useState<number>(12);
  const [reference, setReference] = useState<number>(15);
  const [orderMode, setOrderMode] = useState<OrderMode>('le_i');

  const state = SIXTEEN_STATES[selected];
  const ref = SIXTEEN_STATES[reference];
  const audit = useMemo(() => auditState(state), [state]);
  const path = useMemo(() => walkPath(state), [state]);
  const orderFn = ORDER_FN[orderMode];

  const stats = useMemo(() => {
    let glut = 0;
    let incFixed = 0;
    let walkFixed = 0;
    for (const s of SIXTEEN_STATES) {
      const a = auditState(s);
      if (a.glut) glut++;
      if (a.incFixed) incFixed++;
      if (a.walkFixed) walkFixed++;
    }
    return { glut, incFixed, walkFixed };
  }, []);

  const renderBits = (s: Sixteen3) => (
    <div className="flex gap-0.5">
      {s.map((b, i) => (
        <span
          key={i}
          className={`h-1.5 w-1.5 rounded-sm ${b ? 'bg-emerald-400' : 'bg-slate-700'}`}
        />
      ))}
    </div>
  );

  return (
    <div className="space-y-5">
      <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4 sm:p-5">
        <div className="text-xs font-mono uppercase tracking-wider text-violet-400">
          Laboratory A1 · Sixteen3 State Dynamics
        </div>
        <p className="mt-1 text-sm text-slate-400">
          The 16 states of Shramko–Wansing's SIXTEEN₃ trilattice{' '}
          (<code className="text-emerald-300">Sixteen3 = Belnap4 → Bool</code>). Select a state and a
          reference, then apply the Lean operations <code className="text-emerald-300">Inc</code>,{' '}
          <code className="text-emerald-300">W</code>, <code className="text-emerald-300">R</code>, and{' '}
          <code className="text-emerald-300">μ</code> directly.
        </p>

        <div className="mt-4 grid gap-3 sm:grid-cols-3">
          <label className="block">
            <span className="text-[11px] font-mono text-slate-400">Selected state</span>
            <select
              value={selected}
              onChange={(e) => setSelected(Number(e.target.value))}
              className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-2 py-1.5 font-mono text-xs text-slate-200"
            >
              {SIXTEEN_STATES.map((s, i) => (
                <option key={i} value={i}>
                  {s16(s)} · {stateLabel(s)}
                </option>
              ))}
            </select>
          </label>
          <label className="block">
            <span className="text-[11px] font-mono text-slate-400">Reference state</span>
            <select
              value={reference}
              onChange={(e) => setReference(Number(e.target.value))}
              className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-2 py-1.5 font-mono text-xs text-slate-200"
            >
              {SIXTEEN_STATES.map((s, i) => (
                <option key={i} value={i}>
                  {s16(s)} · {stateLabel(s)}
                </option>
              ))}
            </select>
          </label>
          <label className="block">
            <span className="text-[11px] font-mono text-slate-400">Order instrument</span>
            <select
              value={orderMode}
              onChange={(e) => setOrderMode(e.target.value as OrderMode)}
              className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-2 py-1.5 font-mono text-xs text-slate-200"
            >
              {(Object.keys(ORDER_LABEL) as OrderMode[]).map((k) => (
                <option key={k} value={k}>
                  {ORDER_LABEL[k]}
                </option>
              ))}
            </select>
          </label>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4">
          <div className="text-xs font-semibold text-slate-300">State lattice · 4 × 4</div>
          <p className="mt-1 text-[11px] text-slate-500">
            Highlighted: selected (emerald), reference (cyan). Cells are ordered by their bit tuple.
          </p>
          <div className="mt-3 grid grid-cols-4 gap-1.5">
            {SIXTEEN_STATES.map((s, i) => {
              const isSel = i === selected;
              const isRef = i === reference;
              const ordered = orderFn(state, s);
              return (
                <button
                  key={i}
                  type="button"
                  onClick={() => setSelected(i)}
                  className={`min-w-0 rounded-lg border p-2 text-left transition ${
                    isSel
                      ? 'border-emerald-400/70 bg-emerald-500/15'
                      : isRef
                        ? 'border-cyan-400/60 bg-cyan-500/10'
                        : ordered
                          ? 'border-violet-500/30 bg-violet-500/10 hover:border-violet-400/60'
                          : 'border-slate-800 bg-slate-950 hover:border-slate-700'
                  }`}
                >
                  <div className="font-mono text-[10px] text-slate-200">{s16(s)}</div>
                  <div className="mt-1">{renderBits(s)}</div>
                </button>
              );
            })}
          </div>
          <div className="mt-3 flex flex-wrap items-center gap-3 text-[11px] text-slate-400">
            <span><span className="text-emerald-300">■</span> selected</span>
            <span><span className="text-cyan-300">■</span> reference</span>
            <span><span className="text-violet-300">■</span> {orderMode}(selected, cell)</span>
          </div>
        </div>

        <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4">
          <div className="text-xs font-semibold text-slate-300">Operation readout</div>
          <div className="mt-3 space-y-2 font-mono text-xs">
            <div className="rounded-lg border border-slate-800 bg-slate-950 p-2.5">
              <div className="text-slate-500">state</div>
              <div className="text-white">{s16(state)} · {stateLabel(state)}</div>
              <div className="mt-1 text-[10px] text-slate-400">
                {orderMode}(selected, reference) = {orderFn(state, ref) ? 'YES' : 'NO'}
              </div>
            </div>
            <div className="rounded-lg border border-emerald-500/25 bg-emerald-500/5 p-2.5">
              <div className="text-emerald-400">Inc x = joinI x sBoth</div>
              <div className="text-white">{s16(audit.inc)} · {stateLabel(audit.inc)}</div>
              <div className="mt-1 text-[10px] text-slate-400">
                re-entry idempotent: {audit.incFixed ? 'YES' : 'NO'} · R(R x) = R x
              </div>
            </div>
            <div className="rounded-lg border border-cyan-500/25 bg-cyan-500/5 p-2.5">
              <div className="text-cyan-400">W x · monotone walk</div>
              <div className="text-white">{s16(audit.walk)} · {stateLabel(audit.walk)}</div>
              <div className="mt-1 text-[10px] text-slate-400">
                le_i x (W x): {leI(state, canonicalWalk(state)) ? 'YES' : 'NO'} · fixed at top:{' '}
                {audit.walkFixed ? 'YES' : 'NO'}
              </div>
            </div>
            <div className="rounded-lg border border-violet-500/25 bg-violet-500/5 p-2.5">
              <div className="text-violet-400">μ x · fold to the four value-set</div>
              <div className="text-white">{audit.fold}</div>
              <div className="mt-1 text-[10px] text-slate-400">
                core law μ(δ {audit.fold}) = {audit.fold}: {audit.coreLawHolds ? 'YES' : 'NO'}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4">
          <div className="text-xs font-semibold text-slate-300">Walk trajectory to totality</div>
          <div className="mt-3 flex flex-wrap items-center gap-2 font-mono text-[11px]">
            {path.map((s, i) => (
              <span key={i} className="flex items-center gap-2">
                <span
                  className={`rounded-md border px-2 py-1 ${
                    eqState(s, CANONICAL.sTopI)
                      ? 'border-amber-400/50 bg-amber-500/10 text-amber-200'
                      : 'border-slate-700 bg-slate-950 text-slate-200'
                  }`}
                >
                  {s16(s)}
                </span>
                {i < path.length - 1 && <span className="text-slate-600">→</span>}
              </span>
            ))}
          </div>
          <div className="mt-3 text-[11px] text-slate-500">
            <code className="text-emerald-300">walk_iter_le</code> and{' '}
            <code className="text-emerald-300">walk_fixed_at_top</code>: the walk increases information and
            stabilizes at <code className="text-amber-300">[B]</code>.
          </div>
        </div>

        <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4">
          <div className="text-xs font-semibold text-slate-300">Global axioms over all 16 states</div>
          <div className="mt-3 grid grid-cols-3 gap-2 text-center">
            <div className="rounded-lg border border-rose-500/25 bg-rose-500/5 p-3">
              <div className="text-xl font-bold text-rose-300">{stats.glut}</div>
              <div className="text-[10px] text-slate-400">glut states</div>
            </div>
            <div className="rounded-lg border border-emerald-500/25 bg-emerald-500/5 p-3">
              <div className="text-xl font-bold text-emerald-300">{stats.incFixed}</div>
              <div className="text-[10px] text-slate-400">Inc-fixed</div>
            </div>
            <div className="rounded-lg border border-amber-500/25 bg-amber-500/5 p-3">
              <div className="text-xl font-bold text-amber-300">{stats.walkFixed}</div>
              <div className="text-[10px] text-slate-400">W-fixed</div>
            </div>
          </div>
          <div className="mt-3 flex items-center gap-2 text-[11px] text-slate-400">
            <button
              type="button"
              onClick={() => {
                setSelected(12);
                setReference(15);
              }}
              className="inline-flex items-center gap-1 rounded-lg border border-slate-700 bg-slate-900 px-2 py-1 hover:border-emerald-500/50"
            >
              <RotateCcw className="h-3 w-3" /> Reset
            </button>
            <span>
              glut = both T and F marked · <code className="text-emerald-300">totality_not_injective</code>
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
