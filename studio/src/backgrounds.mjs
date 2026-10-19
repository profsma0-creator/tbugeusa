// Atmospheric backgrounds, authored once as SVG and emitted both as vector
// markup (for the preview/PDF) and as high-resolution JPEGs (for PowerPoint).
import fs from 'node:fs';
import path from 'node:path';
import { Resvg } from '@resvg/resvg-js';
import sharp from 'sharp';

const W = 1280, H = 720;

const svgDoc = (inner) => `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">${inner}</svg>`;

function arcs(cx, cy, radii, color, opacity, width = 0.6) {
  return radii.map((r, i) => `<circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${color}" stroke-opacity="${opacity - i * 0.012}" stroke-width="${width}"/>`).join('');
}

export function bgMarkup(kind = 'paper') {
  if (kind === 'cover') {
    return `
<defs>
  <radialGradient id="bgwarm" cx="0.80" cy="0.06" r="0.78">
    <stop offset="0" stop-color="#C79A57" stop-opacity="0.30"/>
    <stop offset="0.42" stop-color="#8A6234" stop-opacity="0.13"/>
    <stop offset="1" stop-color="#0B0D0C" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="bgcool" cx="0.06" cy="1.02" r="0.75">
    <stop offset="0" stop-color="#2E4A3E" stop-opacity="0.55"/>
    <stop offset="1" stop-color="#0B0D0C" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="bgbase" x1="0" y1="0" x2="0.85" y2="1">
    <stop offset="0" stop-color="#0A0C0B"/>
    <stop offset="0.55" stop-color="#0E100E"/>
    <stop offset="1" stop-color="#171208"/>
  </linearGradient>
  <radialGradient id="bgvig" cx="0.5" cy="0.45" r="0.78">
    <stop offset="0.45" stop-color="#000000" stop-opacity="0"/>
    <stop offset="1" stop-color="#000000" stop-opacity="0.55"/>
  </radialGradient>
</defs>
<rect width="${W}" height="${H}" fill="url(#bgbase)"/>
<rect width="${W}" height="${H}" fill="url(#bgcool)"/>
<rect width="${W}" height="${H}" fill="url(#bgwarm)"/>
${arcs(1205, -125, [300, 372, 448, 530, 620], '#C2A05F', 0.13, 0.7)}
${arcs(1205, -125, [470, 700], '#C2A05F', 0.06, 1.4)}
<rect width="${W}" height="${H}" fill="url(#bgvig)"/>`;
  }

  if (kind === 'section') {
    return `
<defs>
  <linearGradient id="sbase" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0A0C0B"/>
    <stop offset="0.62" stop-color="#111310"/>
    <stop offset="1" stop-color="#1B1409"/>
  </linearGradient>
  <radialGradient id="sglow" cx="0.16" cy="0.30" r="0.72">
    <stop offset="0" stop-color="#B98B4C" stop-opacity="0.22"/>
    <stop offset="0.55" stop-color="#6E5330" stop-opacity="0.10"/>
    <stop offset="1" stop-color="#0B0D0C" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="svig" cx="0.55" cy="0.5" r="0.75">
    <stop offset="0.4" stop-color="#000" stop-opacity="0"/>
    <stop offset="1" stop-color="#000" stop-opacity="0.5"/>
  </radialGradient>
</defs>
<rect width="${W}" height="${H}" fill="url(#sbase)"/>
<rect width="${W}" height="${H}" fill="url(#sglow)"/>
${arcs(-110, 640, [260, 330, 410, 500, 600, 720], '#C2A05F', 0.10, 0.65)}
<rect width="${W}" height="${H}" fill="url(#svig)"/>`;
  }

  if (kind === 'closing') {
    return `
<defs>
  <linearGradient id="cbase" x1="0" y1="0" x2="0.2" y2="1">
    <stop offset="0" stop-color="#0B0D0C"/>
    <stop offset="1" stop-color="#161006"/>
  </linearGradient>
  <radialGradient id="cglow" cx="0.52" cy="0.38" r="0.55">
    <stop offset="0" stop-color="#D0A363" stop-opacity="0.22"/>
    <stop offset="0.6" stop-color="#7A5628" stop-opacity="0.08"/>
    <stop offset="1" stop-color="#0B0D0C" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="cvig" cx="0.5" cy="0.5" r="0.8">
    <stop offset="0.35" stop-color="#000" stop-opacity="0"/>
    <stop offset="1" stop-color="#000" stop-opacity="0.62"/>
  </radialGradient>
</defs>
<rect width="${W}" height="${H}" fill="url(#cbase)"/>
<rect width="${W}" height="${H}" fill="url(#cglow)"/>
${arcs(640, 760, [330, 396, 470, 560, 670], '#C2A05F', 0.11, 0.6)}
<rect width="${W}" height="${H}" fill="url(#cvig)"/>`;
  }

  // paper
  return `
<defs>
  <linearGradient id="pbase" x1="0" y1="0" x2="0.35" y2="1">
    <stop offset="0" stop-color="#FBF7EE"/>
    <stop offset="0.55" stop-color="#F8F3E9"/>
    <stop offset="1" stop-color="#F2EBDD"/>
  </linearGradient>
  <radialGradient id="pglow" cx="0.12" cy="0.02" r="0.85">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.55"/>
    <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="pvig" cx="0.5" cy="0.45" r="0.8">
    <stop offset="0.55" stop-color="#C9B99B" stop-opacity="0"/>
    <stop offset="1" stop-color="#C9B99B" stop-opacity="0.13"/>
  </radialGradient>
</defs>
<rect width="${W}" height="${H}" fill="url(#pbase)"/>
<rect width="${W}" height="${H}" fill="url(#pglow)"/>
<rect width="${W}" height="${H}" fill="url(#pvig)"/>`;
}

export async function writeBackgrounds(dir) {
  fs.mkdirSync(dir, { recursive: true });
  const out = {};
  for (const kind of ['cover', 'section', 'closing', 'paper']) {
    const svg = svgDoc(bgMarkup(kind));
    const resvg = new Resvg(svg, { fitTo: { mode: 'width', value: 2560 } });
    const png = resvg.render().asPng();
    const file = path.join(dir, `bg-${kind}.jpg`);
    await sharp(png).jpeg({ quality: 90, chromaSubsampling: '4:4:4' }).toFile(file);
    out[kind] = file;
  }
  return out;
}
