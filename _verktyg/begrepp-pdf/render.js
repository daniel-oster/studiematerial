// Skriver ut en HTML-fil till A4-PDF med Chromium. Användning: node render.js in.html ut.pdf
const path = require('path');
const { chromium } = require('playwright');
(async () => {
  const [inp, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.resolve(inp), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const foot = `<div style="width:100%;font:8px 'Source Sans 3',sans-serif;color:#7a7a72;padding:0 14mm;display:flex;justify-content:space-between">
    <span>Ekologins 44 begrepp · Ekologi och hållbar utveckling</span>
    <span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`;
  await p.pdf({ path: out, format: 'A4', printBackground: true, displayHeaderFooter: true,
    headerTemplate: '<span></span>', footerTemplate: foot,
    margin: { top: '14mm', bottom: '16mm', left: '14mm', right: '14mm' } });
  await b.close();
})();
