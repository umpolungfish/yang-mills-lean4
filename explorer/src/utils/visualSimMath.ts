import { dobrushinMetrics } from './yangMillsMath';

export interface Vec3 {
  x: number;
  y: number;
  z: number;
}

export interface Vec4 {
  x: number;
  y: number;
  z: number;
  w: number;
}

export interface ProjectedPoint {
  x: number;
  y: number;
  depth: number;
  scale: number;
}

/** Rotate a 3D point by yaw (around Y) and pitch (around X), then perspective-project. */
export function project3D(
  p: Vec3,
  yaw: number,
  pitch: number,
  fov = 420,
  cameraDist = 4.6,
  cx = 0,
  cy = 0,
): ProjectedPoint {
  const cosY = Math.cos(yaw);
  const sinY = Math.sin(yaw);
  const cosP = Math.cos(pitch);
  const sinP = Math.sin(pitch);

  // Yaw around Y
  const x1 = p.x * cosY + p.z * sinY;
  const z1 = -p.x * sinY + p.z * cosY;

  // Pitch around X
  const y2 = p.y * cosP - z1 * sinP;
  const z2 = p.y * sinP + z1 * cosP;

  const denom = Math.max(0.5, cameraDist + z2);
  const scale = fov / denom;
  return {
    x: cx + x1 * scale,
    y: cy - y2 * scale,
    depth: z2,
    scale,
  };
}

/** Rotate a 4D point in (x,w) and (y,z) planes, project 4D->3D->2D. */
export function project4D(
  p: Vec4,
  angleXW: number,
  angleYW: number,
  yaw3D: number,
  pitch3D: number,
  wDist = 2.8,
  fov = 380,
  cx = 0,
  cy = 0,
): ProjectedPoint {
  const cXW = Math.cos(angleXW);
  const sXW = Math.sin(angleXW);
  const x1 = p.x * cXW - p.w * sXW;
  const w1 = p.x * sXW + p.w * cXW;

  const cYW = Math.cos(angleYW);
  const sYW = Math.sin(angleYW);
  const y2 = p.y * cYW - w1 * sYW;
  const w2 = p.y * sYW + w1 * cYW;

  const persp4 = wDist / Math.max(0.6, wDist - w2);
  return project3D(
    { x: x1 * persp4, y: y2 * persp4, z: p.z * persp4 },
    yaw3D,
    pitch3D,
    fov,
    4.5,
    cx,
    cy,
  );
}

/** Generate the 16 vertices & 32 edges of the S16 4D tesseract in [-1, 1]^4. */
export function buildTesseractGeometry(): {
  vertices: Array<{ idx: number; bits: [boolean, boolean, boolean, boolean]; pos: Vec4 }>;
  edges: Array<[number, number, number]>; // [u, v, axis]
} {
  const vertices: Array<{ idx: number; bits: [boolean, boolean, boolean, boolean]; pos: Vec4 }> = [];
  for (let idx = 0; idx < 16; idx++) {
    const b0 = Boolean((idx >> 3) & 1);
    const b1 = Boolean((idx >> 2) & 1);
    const b2 = Boolean((idx >> 1) & 1);
    const b3 = Boolean(idx & 1);
    vertices.push({
      idx,
      bits: [b0, b1, b2, b3],
      pos: {
        x: b0 ? 1 : -1,
        y: b1 ? 1 : -1,
        z: b2 ? 1 : -1,
        w: b3 ? 1 : -1,
      },
    });
  }

  const edges: Array<[number, number, number]> = [];
  for (let u = 0; u < 16; u++) {
    for (let bit = 0; bit < 4; bit++) {
      const v = u ^ (1 << (3 - bit));
      if (u < v) {
        edges.push([u, v, bit]);
      }
    }
  }

  return { vertices, edges };
}

/** Amplitude of the Dobrushin influence wave at radial hop distance r and animation phase t. */
export function waveRingAmplitude(beta: number, hopR: number, phase: number): number {
  const m = dobrushinMetrics(beta);
  if (m.regime === 'zero_coupling') return hopR === 0 ? 1 : 0;

  const pulse = 0.5 + 0.5 * Math.cos(phase * 3.2 - hopR * 1.15);
  if (m.regime === 'contractive') {
    const damped = Math.pow(m.rho, hopR);
    return Math.min(1, damped * (0.45 + 0.55 * pulse));
  }
  // Supercritical alpha >= 1 diverges / saturates visually
  const growth = Math.min(2.2, Math.pow(m.rho, Math.min(hopR, 4)));
  return Math.min(1, 0.5 * growth * (0.5 + 0.5 * pulse));
}

/** Compute the 6 orthogonal plaquettes around a central target link in 3D+t isometric view. */
export interface VisualPlaquette3D {
  id: string;
  planeIndex: 0 | 1 | 2; // 3 orthogonal normal planes around the central link
  polarity: 1 | -1;
  corners: [Vec3, Vec3, Vec3, Vec3];
}

export function buildCentralLinkPlaquettes3D(): VisualPlaquette3D[] {
  // Target link runs along X from (-0.5, 0, 0) to (+0.5, 0, 0)
  // 3 orthogonal directions in 4D mapped visually to Y, Z, and diagonal W-tilt
  const axisDirs: Array<{ vec: Vec3; planeIndex: 0 | 1 | 2; label: string }> = [
    { vec: { x: 0, y: 1.0, z: 0 }, planeIndex: 0, label: 'x–y' },
    { vec: { x: 0, y: 0, z: 1.0 }, planeIndex: 1, label: 'x–z' },
    { vec: { x: 0, y: 0.68, z: 0.68 }, planeIndex: 2, label: 'x–t (4th axis)' },
  ];

  const plaquettes: VisualPlaquette3D[] = [];
  for (const ax of axisDirs) {
    for (const pol of [1, -1] as const) {
      const dy = ax.vec.y * pol;
      const dz = ax.vec.z * pol;
      plaquettes.push({
        id: `${ax.label}:${pol > 0 ? '+' : '-'}`,
        planeIndex: ax.planeIndex,
        polarity: pol,
        corners: [
          { x: -0.5, y: 0, z: 0 },
          { x: 0.5, y: 0, z: 0 },
          { x: 0.5, y: dy, z: dz },
          { x: -0.5, y: dy, z: dz },
        ],
      });
    }
  }
  return plaquettes;
}

/** Kogut-Susskind non-commutation visual check on diagonal basis state. */
export function computeKogutSusskindPathGap(N: number): {
  shiftThenTrace: number;
  traceThenShift: number;
  commutatorMag: number;
} {
  // Using canonical suFlip2 shift on diagonal trace observable:
  // Re Tr(1)/N = 1, Re Tr(suFlip2)/N = (N-4)/N
  const shiftThenTrace = (N - 4) / N;
  const traceThenShift = 1;
  return {
    shiftThenTrace,
    traceThenShift,
    commutatorMag: Math.abs(traceThenShift - shiftThenTrace),
  };
}
