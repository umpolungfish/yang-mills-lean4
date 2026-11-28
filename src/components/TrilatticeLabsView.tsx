import { useState } from 'react';
import { MassTransmutationLab } from './MassTransmutationLab';
import { SICDualFrameLab } from './SICDualFrameLab';
import { TrilatticeStateLab } from './TrilatticeStateLab';

type LabId = 'states' | 'sic' | 'transmutation';

const LABS: Array<{ id: LabId; label: string; subtitle: string }> = [
  { id: 'states', label: 'Sixteen3 State Dynamics', subtitle: '16 Belnap states · Inc / W / R / μ · core law' },
  { id: 'sic', label: 'SIC Dual Frame', subtitle: 'ζ(−1) · Gram/dual · joint mass kernel' },
  { id: 'transmutation', label: 'Mass Transmutation', subtitle: 'q₄ᴅ = 729/2704 · κ = 2log(52/27) · sector dominance' },
];

export function TrilatticeLabsView() {
  const [active, setActive] = useState<LabId>('states');

  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4 sm:p-5">
        <div className="text-xs font-mono uppercase tracking-wider text-violet-400">
          Route A · Trilattice Interactive Instrumentation (3 Laboratories)
        </div>
        <h1 className="mt-1 text-xl font-bold text-white">
          Re-entrant State Dynamics, SIC Dual Reconstruction, and Dimensional Transmutation
        </h1>
        <p className="mt-1 text-sm text-slate-400">
          Every instrument below shadows a kernel-checked Lean declaration in{' '}
          <code className="text-emerald-300">Imscribing.TrilatticeYM</code>.
        </p>
        <div
          className="mt-4 grid grid-cols-1 gap-2 sm:grid-cols-3"
          role="tablist"
          aria-label="Trilattice proof laboratories"
        >
          {LABS.map((lab) => {
            const on = active === lab.id;
            return (
              <button
                key={lab.id}
                type="button"
                role="tab"
                aria-selected={on}
                onClick={() => setActive(lab.id)}
                className={`rounded-lg border px-3.5 py-2.5 text-left transition-colors ${
                  on
                    ? 'border-violet-500/60 bg-violet-500/10 text-white'
                    : 'border-slate-800 bg-[#070b14] text-slate-400 hover:border-slate-700 hover:text-slate-200'
                }`}
              >
                <div className={`text-xs font-semibold ${on ? 'text-violet-300' : 'text-slate-200'}`}>
                  {lab.label}
                </div>
                <div className="mt-0.5 font-mono text-[10px] text-slate-400">{lab.subtitle}</div>
              </button>
            );
          })}
        </div>
      </div>

      {active === 'states' && <TrilatticeStateLab />}
      {active === 'sic' && <SICDualFrameLab />}
      {active === 'transmutation' && <MassTransmutationLab />}
    </div>
  );
}
