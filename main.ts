// news-image-20261123 — entrypoint.
// Copies the pre-drawn infographic (entry.png, in this repository) to the
// output directory the harness provides, then verifies the output is a
// whole, in-limits PNG. The image sums up the world news of Monday
// 23 November 2026. Deterministic: the same bytes every run.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const outPath = join(outDir, "entry.png");
copyFileSync(join(here, "entry.png"), outPath);

// Real output check: the file must exist, be a whole PNG within the
// competition limits (<= 1 MiB, <= 1024x1024), and read back cleanly.
const bytes = readFileSync(outPath);
const stat = statSync(outPath);
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error("output is not a PNG");
}
if (stat.size > 1048576) {
  throw new Error(`output too large: ${stat.size} bytes`);
}
// PNG IHDR: width at offset 16, height at offset 20 (big-endian uint32).
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`output too big: ${width}x${height}`);
}
console.log(`wrote ${outPath}: PNG ${width}x${height}, ${stat.size} bytes`);
