import { useState } from 'react';
import { ContinuumStageLab } from './ContinuumStageLab';
import { DobrushinVisualLab } from './DobrushinVisualLab';
import { FeynmanKacIsingLab } from './FeynmanKacIsingLab';
import { OSCompletionRankOneLab } from './OSCompletionRankOneLab';
import { TesseractAndFlowLab } from './TesseractAndFlowLab';
import { WilsonLoopWitnessLab } from './WilsonLoopWitnessLab';

type LabTabId = 'stage' | 'os_rank1' | 'dobrushin' | 'wilson' | 'feynman' | 'tesseract';

const LAB_TABS: Array<{ id: LabTabId; label: string; subtitle: string }> = [
  { id: 'stage', label: 'Continuum Stage & CDF', subtitle: 'Torus injectivity m* · SUClosure err' },
  { id: 'os_rank1', label: 'OS Rank-1 Completion', subtitle: '4×4 Gram kernel · Poincaré collapse' },
  { id: 'dobrushin', label: '4D Dobrushin Wave', subtitle: '6 plaquettes · 18 neighbors · α<1' },
  { id: 'wilson', label: 'SU(N) Loop & Witness', subtitle: 'CanonicalWitness · Action exp(−βS)' },
  { id: 'feynman', label: 'Time Slices & Ising', subtitle: 'Feynman–Kac Θ mirror · §34 separation' },
  { id: 'tesseract', label: '4D Tesseract & Closure DAG', subtitle: 'S₁₆ bits + Unconditional DAG' },
];

export function InteractiveLabsView() {
  const [activeLab, setActiveLab] = useState<LabTabId>('stage');

  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4 sm:p-5">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <div className="font-mono text-xs uppercase tracking-wider text-cyan-400">
              Interactive Proof Instrumentation (6 Laboratories)
            </div>
            <h1 className="mt-1 text-xl font-bold text-white">
              Continuum Stage Scaling, OS Rank-1 Hilbert Collapse, Lattice &amp; Gauge Explorers
            </h1>
          </div>
        </div>

        <div
          className="mt-4 grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-3"
          role="tablist"
          aria-label="Interactive proof laboratories"
        >
          {LAB_TABS.map((t) => {
            const active = activeLab === t.id;
            return (
              <button
                key={t.id}
                type="button"
                role="tab"
                aria-selected={active}
                onClick={() => setActiveLab(t.id)}
                className={`rounded-lg border px-3.5 py-2.5 text-left transition-colors ${
                  active
                    ? 'border-emerald-500/60 bg-emerald-500/10 text-white'
                    : 'border-slate-800 bg-[#070b14] text-slate-400 hover:border-slate-700 hover:text-slate-200'
                }`}
              >
                <div className={`text-xs font-semibold ${active ? 'text-emerald-300' : 'text-slate-200'}`}>
                  {t.label}
                </div>
                <div className="mt-0.5 font-mono text-[10px] text-slate-400">{t.subtitle}</div>
              </button>
            );
          })}
        </div>
      </div>

      {activeLab === 'stage' && <ContinuumStageLab />}
      {activeLab === 'os_rank1' && <OSCompletionRankOneLab />}
      {activeLab === 'dobrushin' && <DobrushinVisualLab />}
      {activeLab === 'wilson' && <WilsonLoopWitnessLab />}
      {activeLab === 'feynman' && <FeynmanKacIsingLab />}
      {activeLab === 'tesseract' && <TesseractAndFlowLab />}
    </div>
  );
}
