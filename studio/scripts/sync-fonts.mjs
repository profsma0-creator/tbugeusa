// Copies the metric-compatible measurement fonts out of node_modules so the
// renderer can load them by path. Georgia/Calibri remain the deck's font
// families; Gelasio/Carlito share their metrics, so preview == PowerPoint.
import fs from 'node:fs';
import path from 'node:path';

const HERE = import.meta.dirname;
const DEST = path.resolve(HERE, '../assets/fonts');
const SRC = path.resolve(HERE, '../node_modules');

const MAP = [
  ['@expo-google-fonts/gelasio/400Regular/Gelasio_400Regular.ttf', 'Gelasio_400Regular.ttf'],
  ['@expo-google-fonts/gelasio/400Regular_Italic/Gelasio_400Regular_Italic.ttf', 'Gelasio_400Regular_Italic.ttf'],
  ['@expo-google-fonts/gelasio/500Medium/Gelasio_500Medium.ttf', 'Gelasio_500Medium.ttf'],
  ['@expo-google-fonts/gelasio/600SemiBold/Gelasio_600SemiBold.ttf', 'Gelasio_600SemiBold.ttf'],
  ['@expo-google-fonts/gelasio/700Bold/Gelasio_700Bold.ttf', 'Gelasio_700Bold.ttf'],
  ['@expo-google-fonts/gelasio/LICENSE_FONT', 'OFL-Gelasio.txt'],
  ['@expo-google-fonts/carlito/400Regular/Carlito_400Regular.ttf', 'Carlito_400Regular.ttf'],
  ['@expo-google-fonts/carlito/400Regular_Italic/Carlito_400Regular_Italic.ttf', 'Carlito_400Regular_Italic.ttf'],
  ['@expo-google-fonts/carlito/700Bold/Carlito_700Bold.ttf', 'Carlito_700Bold.ttf'],
  ['@expo-google-fonts/carlito/700Bold_Italic/Carlito_700Bold_Italic.ttf', 'Carlito_700Bold_Italic.ttf'],
  ['@expo-google-fonts/carlito/LICENSE_FONT', 'OFL-Carlito.txt'],
];

let copied = 0;
for (const [from, to] of MAP) {
  const src = path.join(SRC, from);
  const dest = path.join(DEST, to);
  if (fs.existsSync(dest)) continue;
  if (!fs.existsSync(src)) continue;
  fs.mkdirSync(DEST, { recursive: true });
  fs.copyFileSync(src, dest);
  copied++;
}
if (copied) console.log(`fonts: copied ${copied} file(s) into assets/fonts`);
