// main.ts — GTA VI Delivery Tracking meme entry (gta6-meme-x-01, v2).
// Node 22, standard library only. Copies the meme image and POST.json
// byte-identical into the output directory so the grader can serve them.
// No network, no randomness, no timestamps.
//
// Output directory: the grader sets MAKEFUN_OUTPUT_DIR. When it is unset
// (local runs), files go to "output/" next to this script instead.
const fs = require("node:fs");
const path = require("node:path");

const root = __dirname;
// Fall back to a local "output/" directory when MAKEFUN_OUTPUT_DIR is unset.
const outDir = process.env.MAKEFUN_OUTPUT_DIR || path.join(root, "output");

fs.mkdirSync(outDir, { recursive: true });

// Copy each deliverable byte-identical; copyFileSync never rewrites content.
for (const name of ["assets/meme.png", "POST.json"]) {
  const src = path.join(root, name);
  const dest = path.join(outDir, path.basename(name));
  fs.copyFileSync(src, dest);
}
