// Skriver ut en fristående studiesida (HTML) till PDF med webbläsarens utskriftsstil.
// Sidans egna @media print-regler döljer lampor och knappar, och alla utfällbara svar öppnas.
//
// Kör från repots rot:
//   node _verktyg/sida-till-pdf/render.js sarah/statsskick/studiematerial/index.html sarah/statsskick/studiematerial/fran-rost-till-lag.pdf
//
// Kräver Node med Playwright (Chromium). Front matter (--- ... ---) i HTML-filen tas bort före utskrift.
const fs = require('fs');
const os = require('os');
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const [src, out] = process.argv.slice(2);
  if (!src || !out) { console.error('Användning: node render.js <sida.html> <ut.pdf>'); process.exit(1); }
  const raw = fs.readFileSync(src, 'utf8').replace(/^---\n[\s\S]*?\n---\n/, '');
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'sida-till-pdf-'));
  const tmp = path.join(tmpDir, 'sida.html');
  fs.writeFileSync(tmp, raw);

  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + tmp, { waitUntil: 'networkidle' }).catch(() => {});
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await page.evaluate(() => document.querySelectorAll('details').forEach(d => { d.open = true; }));
  await page.emulateMedia({ media: 'print' });
  await page.pdf({
    path: out,
    format: 'A4',
    printBackground: true,
    margin: { top: '14mm', bottom: '16mm', left: '14mm', right: '14mm' },
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;color:#777"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
  });
  await browser.close();
  fs.rmSync(tmpDir, { recursive: true, force: true });
  console.log('Skrev', out);
})();
