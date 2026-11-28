import { useMemo, useState } from 'react';
import {
  isotropicDual,
  isotropicGram,
  jointKernelEntry,
  Q_LOCAL,
  sicDualEntry,
  sicGramEntry,
  ZETA_NEG_ONE,
} from '../utils/trilatticeMath';

const DIMENSIONS = [2, 4, 12, 16] as const;

export function SICDualFrameLab() {
  const [dimension, setDimension] = useState<number>(4);
  const [input, setInput] = useState<string>('1, 0.5, -0.25, 0.75');
  const [jointSites, setJointSites] = useState<number>(3);

  const n = dimension * dimension;
  const gram = useMemo(() => isotropicGram(n, dimension), [n, dimension]);
  const dual = useMemo(() => isotropicDual(n, dimension), [n, dimension]);

  const vector = useMemo(() => {
    const parts = input
      .split(',')
      .map((p) => Number(p.trim()))
      .filter((v) => Number.isFinite(v));
    const out = parts.slice(0, n);
    while (out.length < n) out.push(0);
    return out;
  }, [input, n]);

  const result = useMemo(() => {
    const matrix = gram;
    const analyzed = matrix.map((row) => row.reduce((a, x, j) => a + x * vector[j], 0));
    const restored = dual.map((row) => row.reduce((a, x, j) => a + x * analyzed[j], 0));
    const residual = Math.max(...restored.map((v, i) => Math.abs(v - vector[i])));
    return { analyzed, restored, residual };
  }, [gram, dual, vector]);

  const tetra = useMemo(
    () =>
      Array.from({ length: 4 }, (_, i) =>
        Array.from({ length: 4 }, (_, j) => ({ g: sicGramEntry(i, j), d: sicDualEntry(i, j) })),
      ),
    [],
  );

  const joint = useMemo(() => {
    const a = Array.from({ length: jointSites }, (_, i) => (i % 2 === 0 ? 1 : 0));
    const b = Array.from({ length: jointSites }, (_, i) => (i % 3 === 0 ? 0 : 1));
    return { a, b, value: jointKernelEntry(a, b) };
  }, [jointSites]);

  return (
    <div className="space-y-5">
      <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4 sm:p-5">
        <div className="text-xs font-mono uppercase tracking-wider text-teal-400">
          Laboratory A2 · SIC Dual-Frame Reconstruction
        </div>
        <p className="mt-1 text-sm text-slate-400">
          Analysis by the isotropic SIC Gram followed by the zeta-derived dual returns the exact coordinates:{' '}
          <code className="text-emerald-300">sic_inverse_general d</code>. Choose a dimension and edit the
          coordinate vector.
        </p>
        <div className="mt-4 grid gap-3 sm:grid-cols-3">
          <label className="block">
            <span className="text-[11px] font-mono text-slate-400">Dimension d (orbit d²)</span>
            <select
              value={dimension}
              onChange={(e) => setDimension(Number(e.target.value))}
              className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-2 py-1.5 font-mono text-xs text-slate-200"
            >
              {DIMENSIONS.map((d) => (
                <option key={d} value={d}>
                  d = {d} · orbit {d * d}
                </option>
              ))}
            </select>
          </label>
          <label className="block sm:col-span-2">
            <span className="text-[11px] font-mono text-slate-400">Coordinates (comma separated, first {n} used)</span>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-2 py-1.5 font-mono text-xs text-slate-200"
            />
          </label>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-xl border border-teal-500/25 bg-[#0c1220] p-4">
          <div className="text-xs font-semibold text-slate-300">Gram ↔ dual coefficients</div>
          <div className="mt-3 space-y-2 font-mono text-xs">
            <div className="rounded-lg border border-slate-800 bg-slate-950 p-2.5">
              <div className="text-slate-500">d = {dimension}, orbit n = d² = {n}</div>
              <div className="text-teal-300">Gram: (d/(d+1))·I + (1/(d+1))·J</div>
              <div className="text-emerald-300">Dual: a·I + b·J</div>
              <div className="text-slate-300">a = {isotropicDual(n, dimension)[0][0].toFixed(6)} · b = {isotropicDual(n, dimension)[0][1].toFixed(8)}</div>
            </div>
            <div className="rounded-lg border border-violet-500/25 bg-violet-500/5 p-2.5">
              <div className="text-violet-300">ζ(−1) = {ZETA_NEG_ONE}</div>
              <div className="text-slate-300">d = 4: 5/4 = 1 − 3ζ(−1), −1/16 = (3/4)ζ(−1)</div>
              <div className="text-[10px] text-slate-500">
                verified by <code>ququart_coefficients</code>
              </div>
            </div>
          </div>

          <div className="mt-4 overflow-x-auto">
            <table className="w-full border-collapse text-center font-mono text-[10px]">
              <thead>
                <tr className="text-slate-500">
                  <th className="p-1">g_ij</th>
                  {[0, 1, 2, 3].map((j) => (
                    <th key={j} className="p-1">j={j}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {tetra.map((row, i) => (
                  <tr key={i}>
                    <td className="p-1 text-slate-500">i={i}</td>
                    {row.map((cell, j) => (
                      <td key={j} className="p-1 text-slate-200">
                        {cell.g.toFixed(3)} / {cell.d.toFixed(3)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="mt-2 text-[10px] text-slate-500">entries shown as Gram / dual</div>
        </div>

        <div className="rounded-xl border border-emerald-500/25 bg-[#0c1220] p-4">
          <div className="flex items-center justify-between">
            <div className="text-xs font-semibold text-slate-300">Reconstruction readout</div>
            <span
              className={`rounded-full px-2 py-0.5 font-mono text-[10px] ${
                result.residual < 1e-9
                  ? 'bg-emerald-500/15 text-emerald-300'
                  : 'bg-rose-500/15 text-rose-300'
              }`}
            >
              residual {result.residual.toExponential(2)}
            </span>
          </div>
          <div className="mt-3 max-h-64 space-y-1 overflow-y-auto font-mono text-[10px]">
            {vector.slice(0, 16).map((v, i) => (
              <div key={i} className="grid grid-cols-3 gap-2 rounded border border-slate-800 bg-slate-950 px-2 py-1">
                <span className="text-slate-500">c[{i}] = {v.toFixed(3)}</span>
                <span className="text-teal-300">G·c = {result.analyzed[i].toFixed(3)}</span>
                <span className="text-emerald-300">G⁻¹·G·c = {result.restored[i].toFixed(3)}</span>
              </div>
            ))}
            {vector.length > 16 && (
              <div className="text-slate-500">… {vector.length - 16} more coordinates</div>
            )}
          </div>
          <div className="mt-3 text-[11px] text-slate-500">
            <code className="text-emerald-300">tetra_coordinate_reconstruction</code> /{' '}
            <code className="text-emerald-300">ququart_coordinate_reconstruction</code>
          </div>
        </div>
      </div>

      <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <div className="text-xs font-semibold text-slate-300">Joint correlated-label kernel</div>
            <p className="mt-1 text-[11px] text-slate-500">
              <code className="text-emerald-300">joint_kernel</code>: tensor product of local ququart dual
              entries, with all source-correlated labels retained.
            </p>
          </div>
          <label className="flex items-center gap-2 font-mono text-[11px] text-slate-400">
            sites k = {jointSites}
            <input
              type="range"
              min={1}
              max={8}
              value={jointSites}
              onChange={(e) => setJointSites(Number(e.target.value))}
              className="w-40 accent-emerald-400"
            />
          </label>
        </div>
        <div className="mt-3 grid gap-2 sm:grid-cols-3 font-mono text-xs">
          <div className="rounded-lg border border-slate-800 bg-slate-950 p-2.5">
            <span className="text-slate-500">i = </span>
            <span className="text-teal-300">[{joint.a.join(', ')}]</span>
          </div>
          <div className="rounded-lg border border-slate-800 bg-slate-950 p-2.5">
            <span className="text-slate-500">j = </span>
            <span className="text-violet-300">[{joint.b.join(', ')}]</span>
          </div>
          <div className="rounded-lg border border-emerald-500/25 bg-emerald-500/5 p-2.5">
            <span className="text-slate-400">kernel = </span>
            <span className="text-emerald-300">{joint.value.toExponential(4)}</span>
          </div>
        </div>
        <div className="mt-2 text-[10px] text-slate-500">
          local entry (δᵢⱼ · 5/4) − 1/16 · local eigenvalue <span className="text-emerald-300">{Q_LOCAL}</span>
        </div>
      </div>
    </div>
  );
}
