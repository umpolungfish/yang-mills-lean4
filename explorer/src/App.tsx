import { useState } from 'react';
import { Code2, Layers } from 'lucide-react';
import { DobrushinVisualLab } from './components/DobrushinVisualLab';
import { WilsonLoopWitnessLab } from './components/WilsonLoopWitnessLab';
import { FeynmanKacIsingLab } from './components/FeynmanKacIsingLab';
import { TesseractAndFlowLab } from './components/TesseractAndFlowLab';
import { BridgeAndSourceView } from './components/BridgeAndSourceView';

type ActiveLab = 'dobrushin' | 'witness' | 'slices' | 'tesseract' | 'source';

export default function App() {
  const [activeLab, setActiveLab] = useState<ActiveLab>('dobrushin');
  const [selectedModuleId, setSelectedModuleId] = useState<string>('StrongCouplingDobrushin');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200">
      {/* 3-Zone Top Bar */}
      <header className="sticky top-0 z-30 border-b border-slate-800 bg-slate-950/90 backdrop-blur-md">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-8 px-4 py-2.5 sm:px-6">
          {/* Zone 1: Brand */}
          <div className="flex shrink-0 items-center gap-2.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-md border border-emerald-500/20 bg-emerald-500/10 text-emerald-400">
              <Layers className="h-4 w-4" aria-hidden="true" />
            </div>
            <div className="leading-tight">
              <div className="whitespace-nowrap text-sm font-semibold tracking-tight text-white">
                Yang–Mills 4D Formalization
              </div>
              <div className="whitespace-nowrap font-mono text-[10px] uppercase tracking-wider text-slate-400">
                Corpus Explorer · Lean 4
              </div>
            </div>
          </div>

          {/* Zone 2: 4 Visual Lab Tabs */}
          <nav aria-label="Visual labs" className="flex items-center gap-1 overflow-x-auto">
            {(
              [
                { id: 'dobrushin', label: '4D Dobrushin Wave' },
                { id: 'witness', label: 'SU(N) Loop & Witness' },
                { id: 'slices', label: 'Time Slices & Ising' },
                { id: 'tesseract', label: '4D Tesseract & Flow' },
              ] as const
            ).map((item) => {
              const active = activeLab === item.id;
              return (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => setActiveLab(item.id)}
                  className={`whitespace-nowrap shrink-0 rounded-md border px-3 py-1.5 text-xs font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-emerald-500/40 ${
                    active
                      ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-300'
                      : 'border-transparent text-slate-400 hover:bg-slate-800 hover:text-slate-100'
                  }`}
                >
                  {item.label}
                </button>
              );
            })}
          </nav>

          {/* Zone 3: Optional Raw Source Peek CTA */}
          <button
            type="button"
            onClick={() => setActiveLab((cur) => (cur === 'source' ? 'dobrushin' : 'source'))}
            className={`hidden shrink-0 items-center gap-1.5 whitespace-nowrap rounded-md border px-3 py-1.5 text-xs font-medium focus:outline-none focus:ring-2 focus:ring-emerald-500/40 sm:inline-flex ${
              activeLab === 'source'
                ? 'border-slate-700 bg-slate-800 text-white'
                : 'border-emerald-500/30 bg-emerald-500/10 text-emerald-300 hover:bg-emerald-500/20'
            }`}
          >
            <Code2 className="h-3.5 w-3.5" aria-hidden="true" />
            {activeLab === 'source' ? 'Back to Visuals' : 'Raw .lean Archive'}
          </button>
        </div>
      </header>

      {/* Main Visual Stage */}
      <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6">
        {activeLab === 'dobrushin' && <DobrushinVisualLab />}
        {activeLab === 'witness' && <WilsonLoopWitnessLab />}
        {activeLab === 'slices' && <FeynmanKacIsingLab />}
        {activeLab === 'tesseract' && <TesseractAndFlowLab />}
        {activeLab === 'source' && (
          <BridgeAndSourceView
            selectedModuleId={selectedModuleId}
            onSelectModule={setSelectedModuleId}
          />
        )}
      </main>
    </div>
  );
}
