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
    <div className="min-h-screen bg-slate-50 text-slate-900">
      {/* 3-Zone Top Bar */}
      <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/95 backdrop-blur-sm">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-8 px-4 py-2.5 sm:px-6">
          {/* Zone 1: Brand */}
          <div className="flex shrink-0 items-center gap-2.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-md bg-slate-900 text-white">
              <Layers className="h-4 w-4" aria-hidden="true" />
            </div>
            <div className="leading-tight">
              <div className="whitespace-nowrap text-sm font-semibold tracking-tight text-slate-900">
                Yang–Mills 4D Visuals
              </div>
              <div className="whitespace-nowrap font-mono text-[11px] text-slate-500">
                Interactive Gauge &amp; Mass-Gap Lab
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
                  className={`whitespace-nowrap shrink-0 rounded-md px-3 py-1.5 text-xs font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-blue-600/30 ${
                    active
                      ? 'bg-slate-900 text-white'
                      : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
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
            className={`hidden shrink-0 items-center gap-1.5 whitespace-nowrap rounded-md border px-3 py-1.5 text-xs font-medium focus:outline-none focus:ring-2 focus:ring-blue-600/40 sm:inline-flex ${
              activeLab === 'source'
                ? 'border-slate-900 bg-slate-900 text-white'
                : 'border-blue-600 bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            <Code2 className="h-3.5 w-3.5" aria-hidden="true" />
            {activeLab === 'source' ? 'Back to Visuals' : 'Raw .lean Archive'}
          </button>
        </div>
      </header>

      {/* Main Visual Stage */}
      <main className="mx-auto max-w-7xl px-4 py-5 sm:px-6">
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
