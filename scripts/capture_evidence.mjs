// Capture public source pages without altering their contents.
// Supply KLTN_PLAYWRIGHT_MODULE when Playwright is installed outside this repo.
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';

const { chromium } = await import(process.env.KLTN_PLAYWRIGHT_MODULE || 'playwright');
const root = path.resolve('evidence/2026-10-08');
const pages = [
  ['apple-airpods5-vn', 'https://www.apple.com/vn/airpods-5/specs/', true],
  ['apple-airpods4-md', 'https://www.apple.com/md/airpods-4/specs/', true],
  ['apple-pro3-vn', 'https://www.apple.com/vn/airpods-pro/specs/', true],
  ['apple-max2-vn', 'https://www.apple.com/vn/airpods-max/specs/', true],
  ['apple-airpods2-vn', 'https://support.apple.com/vi-vn/111856', true],
  ['ref07-fever', 'https://aclanthology.org/N18-1074/', false],
  ['ref08-averitec', 'https://arxiv.org/abs/2305.13117', false],
  ['ref09-vifactcheck', 'https://arxiv.org/abs/2412.15308', false],
  ['ref10-viwikifc', 'https://arxiv.org/abs/2405.07615v2', false],
  ['ref11-vinumfcr', 'https://aclanthology.org/2025.inlg-main.9/', false],
];
const browser = await chromium.launch({headless: true});
const context = await browser.newContext({viewport: {width: 1440, height: 1000}, locale: 'vi-VN', timezoneId: 'Asia/Ho_Chi_Minh', deviceScaleFactor: 1});
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const results = [];
const supplement = process.argv.includes('--supplement');
await fs.mkdir(root, {recursive: true});
try {
  for (const [id, url, takeScreenshots] of pages) {
    const dir = path.join(root, id);
    try {
      const previous = JSON.parse(await fs.readFile(path.join(dir, 'metadata.json'), 'utf8'));
      if (previous.status === 200 && previous.files?.['page.txt']) {
        if (supplement && takeScreenshots) {
          const detail = await context.newPage();
          try {
            const response = await detail.goto(url, {waitUntil: 'networkidle', timeout: 45000});
            if (response.status() !== 200) throw new Error(`HTTP ${response.status()}`);
            await detail.evaluate(() => document.fonts.ready);
            const screenshots = {};
            for (const [name, selector] of [
              ['dimensions-section.png', '.section-dimensions'],
              ['battery-section.png', '.section-battery'],
              ['connectivity-section.png', '.section-wireless'],
              ['footnotes-section.png', '.ac-gf-sosumi'],
            ]) {
              const region = detail.locator(selector).first();
              if (!await region.count()) continue;
              await region.scrollIntoViewIfNeeded();
              await detail.waitForFunction(selector => [...document.querySelectorAll(`${selector} img`)].every(img => img.complete && img.naturalWidth > 0), selector, {timeout: 15000});
              // Lazy pictures change the section's height after loading.
              await detail.waitForTimeout(800);
              const bytes = await region.screenshot({animations: 'disabled'});
              await fs.writeFile(path.join(dir, name), bytes);
              previous.files[name] = {sha256: hash(bytes), bytes: bytes.length};
              screenshots[name] = selector;
            }
            previous.supplement = {captured_at_utc: new Date().toISOString(), final_url: detail.url(), status: response.status(), screenshots};
            await fs.writeFile(path.join(dir, 'metadata.json'), JSON.stringify(previous, null, 2) + '\n');
          } finally { await detail.close(); }
        }
        results.push(previous);
        console.log(`Already captured: ${id}`);
        continue;
      }
    } catch {}
    const page = await context.newPage();
    const metadata = {id, requested_url: url, captured_at_utc: new Date().toISOString(), capture_method: 'Chromium via Playwright, live URL; no content replacement', viewport: {width: 1440, height: 1000}, files: {}};
    await fs.mkdir(dir, {recursive: true});
    const save = async (name, bytes) => {
      await fs.writeFile(path.join(dir, name), bytes);
      metadata.files[name] = {sha256: hash(bytes), bytes: Buffer.byteLength(bytes)};
    };
    try {
      const response = await page.goto(url, {waitUntil: 'domcontentloaded', timeout: 45000});
      metadata.final_url = page.url();
      metadata.status = response?.status();
      metadata.title = await page.title();
      if (metadata.status !== 200) throw new Error(`HTTP ${metadata.status}`);
      await save('response.html', await response.body());
      // Scroll to load the page's own lazy images, then return to its top.
      await page.evaluate(async () => {
        for (let y = 0; y < document.body.scrollHeight; y += 850) {
          window.scrollTo(0, y);
          await new Promise(resolve => setTimeout(resolve, 70));
        }
        window.scrollTo(0, 0);
        await document.fonts.ready;
      });
      await save('page.html', await page.content());
      await save('page.txt', await page.locator('body').innerText());
      if (takeScreenshots) {
        await save('full-page.png', await page.screenshot({fullPage: true, animations: 'disabled', timeout: 30000}));
        const patterns = [
          ['dimensions', /Kích Thước|Kích thước|Size and Weight|Size.*Weight/i],
          ['battery', /^Pin$|^Battery$/i],
          ['connectivity', /Kết Nối|Kết nối|Connectivity/i],
        ];
        for (const [name, pattern] of patterns) {
          const heading = page.getByRole('heading').filter({hasText: pattern}).first();
          if (await heading.count()) {
            await heading.scrollIntoViewIfNeeded();
            await page.evaluate(() => window.scrollBy(0, -90));
            await save(`${name}.png`, await page.screenshot({animations: 'disabled'}));
          }
        }
      }
      console.log(`Captured: ${id}, HTTP ${metadata.status}, ${metadata.final_url}`);
    } catch (error) {
      metadata.error = String(error);
      console.log(`FAILED: ${id}: ${metadata.error}`);
    } finally {
      await fs.writeFile(path.join(dir, 'metadata.json'), JSON.stringify(metadata, null, 2) + '\n');
      results.push(metadata);
      await page.close();
    }
  }
} finally {
  await browser.close();
}
await fs.writeFile(path.join(root, 'capture-index.json'), JSON.stringify(results, null, 2) + '\n');
if (results.some(result => result.error)) process.exitCode = 1;
