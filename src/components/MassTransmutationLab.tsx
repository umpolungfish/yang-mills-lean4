import { useEffect, useMemo, useRef, useState } from 'react';
import {
  B_F_BOUND,
  B_L_BOUND,
  DIRICHLET_GAP,
  KAPPA,
  Q_4D,
  Q_LOCAL,
  T_LOCAL_EIG,
  transmutation,
} from '../utils/trilatticeMath';

export function MassTransmutationLab() {
  const [alpha, setAlpha] = useState<number>(1);
  const [lambdaYM, setLambdaYM] = useState<number>(1.2);
  const [steps, setSteps] = useState<number>(12);

  const m = useMemo(() => transmutation(alpha, lambdaYM), [alpha, lambdaYM]);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    const w = Math.max(320, Math.floor(rect.width));
    const h = 220;
    canvas.width = Math.floor(w * dpr);
    canvas.height = Math.floor(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = '#070b14';
    ctx.fillRect(0, 0, w, h);

    const padL = 42;
    const padR = 14;
    const padT = 16;
    const padB = 28;
    const plotW = w - padL - padR;
    const plotH = h - padT - padB;

    ctx.strokeStyle = 'rgba(148,163,184,0.15)';
    ctx.lineWidth = 1;
    for (let g = 0; g <= 4; g++) {
      const y = padT + (plotH * g) / 4;
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(w - padR, y);
      ctx.stroke();
    }

    const maxK = Math.max(1, steps);
    const xOf = (k: number) => padL + (plotW * k) / maxK;
    const yOf = (v: number) => padT + plotH * (1 - v);

    ctx.strokeStyle = '#34d399';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    m.decay.slice(0, maxK + 1).forEach((p, i) => {
      const x = xOf(p.k);
      const y = yOf(p.value);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();

    ctx.fillStyle = '#94a3b8';
    ctx.font = '10px Fira Code, monospace';
    ctx.fillText('1', 8, padT + 8);
    ctx.fillText('0', 8, padT + plotH + 3);
    ctx.fillText('q₄ᴅ', 8, yOf(Q_4D) + 3);
    ctx.fillText('k →', padL + plotW - 24, h - 8);
  }, [m, steps]);

  const sectors = [
    { label: 'q_local · Φ_D traceless', value: Q_LOCAL, color: '#38bdf8' },
    { label: 'T_local · u-channel', value: T_LOCAL_EIG, color: '#818cf8' },
    { label: 'Dirichlet gap 6/7', value: DIRICHLET_GAP, color: '#34d399' },
    { label: 'b_F bound', value: B_F_BOUND, color: '#fbbf24' },
    { label: 'b_L bound', value: B_L_BOUND, color: '#f472b6' },
    { label: 'q₄ᴅ = 729/2704', value: Q_4D, color: '#10b981' },
  ];

  return (
    <div className="space-y-5">
      <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4 sm:p-5">
        <div className="text-xs font-mono uppercase tracking-wider text-emerald-400">
          Laboratory A3 · Dimensional Transmutation
        </div>
        <p className="mt-1 text-sm text-slate-400">
          The identity <code className="text-emerald-300">exp(−κ·ℓ) = q₄ᴅ</code> with{' '}
          <code className="text-emerald-300">ℓ = α/Λ_YM</code> turns the exact four-dimensional contraction
          into the physical mass <code className="text-emerald-300">m = κΛ_YM/α</code>.
        </p>
        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <label className="block">
            <span className="text-[11px] font-mono text-slate-400">α · blocking ratio = {alpha.toFixed(2)}</span>
            <input
              type="range"
              min={0.25}
              max={4}
              step={0.05}
              value={alpha}
              onChange={(e) => setAlpha(Number(e.target.value))}
              className="mt-1 w-full accent-emerald-400"
            />
          </label>
          <label className="block">
            <span className="text-[11px] font-mono text-slate-400">Λ_YM = {lambdaYM.toFixed(2)}</span>
            <input
              type="range"
              min={0.1}
              max={4}
              step={0.05}
              value={lambdaYM}
              onChange={(e) => setLambdaYM(Number(e.target.value))}
              className="mt-1 w-full accent-cyan-400"
            />
          </label>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-xl border border-emerald-500/25 bg-[#0c1220] p-4">
          <div className="text-xs font-semibold text-slate-300">Mass formula readout</div>
          <div className="mt-3 grid grid-cols-2 gap-2 font-mono text-xs">
            <div className="rounded-lg border border-slate-800 bg-slate-950 p-2.5">
              <div className="text-slate-500">κ = 2 log(52/27)</div>
              <div className="text-emerald-300">{KAPPA.toFixed(8)}</div>
            </div>
            <div className="rounded-lg border border-slate-800 bg-slate-950 p-2.5">
              <div className="text-slate-500">ℓ = α/Λ</div>
              <div className="text-cyan-300">{m.ell.toFixed(6)}</div>
            </div>
            <div className="rounded-lg border border-emerald-500/30 bg-emerald-500/5 p-2.5">
              <div className="text-emerald-400">m_gap = κ/ℓ</div>
              <div className="text-white">{m.massGap.toFixed(8)}</div>
            </div>
            <div className="rounded-lg border border-emerald-500/30 bg-emerald-500/5 p-2.5">
              <div className="text-emerald-400">= (κ/α)·Λ</div>
              <div className="text-white">{((KAPPA / alpha) * lambdaYM).toFixed(8)}</div>
            </div>
            <div className="col-span-2 rounded-lg border border-violet-500/25 bg-violet-500/5 p-2.5">
              <div className="text-violet-300">exp(−m·ℓ) = {m.expCheck.toFixed(10)}</div>
              <div className="mt-1 text-[10px] text-slate-400">
                q₄ᴅ = {Q_4D.toFixed(10)} · |residual| = {m.identityResidual.toExponential(2)}
              </div>
            </div>
          </div>
          <div className="mt-3 text-[11px] text-slate-500">
            Positive gap certified by <code className="text-emerald-300">ym_mass_gap_exists</code> and{' '}
            <code className="text-emerald-300">yang_mills_mass_gap_universal</code>.
          </div>
        </div>

        <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4">
          <div className="flex items-center justify-between">
            <div className="text-xs font-semibold text-slate-300">Blocked transfer decay q⁴ᴅᵏ</div>
            <label className="flex items-center gap-2 font-mono text-[11px] text-slate-400">
              k ≤ {steps}
              <input
                type="range"
                min={2}
                max={24}
                value={steps}
                onChange={(e) => setSteps(Number(e.target.value))}
                className="w-28 accent-teal-400"
              />
            </label>
          </div>
          <canvas ref={canvasRef} className="mt-3 h-[220px] w-full rounded-lg border border-slate-800" />
          <div className="mt-2 text-[10px] text-slate-500">
            <code className="text-emerald-300">blocked_transfer_exponential_decay</code>: qᵏ ≤ q for k &gt; 0
          </div>
        </div>
      </div>

      <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4">
        <div className="text-xs font-semibold text-slate-300">Sector dominance · exact bounds</div>
        <div className="mt-3 space-y-2">
          {sectors.map((s) => (
            <div key={s.label} className="flex items-center gap-3">
              <div className="w-44 shrink-0 font-mono text-[10px] text-slate-400">{s.label}</div>
              <div className="h-2 flex-1 overflow-hidden rounded-full bg-slate-900">
                <div
                  className="h-full rounded-full"
                  style={{ width: `${Math.max(1, s.value * 100 * 0.9)}%`, backgroundColor: s.color }}
                />
              </div>
              <div className="w-20 shrink-0 text-right font-mono text-[10px] text-slate-300">
                {s.value.toFixed(6)}
              </div>
            </div>
          ))}
        </div>
        <div className="mt-3 text-[11px] text-slate-500">
          <code className="text-emerald-300">assigned_sector_dominance</code>: q₄ᴅ dominates b_F ≤ 1/4 and
          b_L ≤ 625/38416, so max = q₄ᴅ.
        </div>
      </div>
    </div>
  );
}
