#!/usr/bin/env node
// news-image-20261124 entrypoint: copy entry.png to $MAKEFUN_OUTPUT_DIR
// (default /output). Node 22, stdlib only. Refuses a truncated file.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const buf = readFileSync(src);

// PNG signature: 89 50 4E 47 0D 0A 1A 0A
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (buf.length < 8 || !buf.subarray(0, 8).equals(PNG_SIG)) {
  console.error("entry.png: bad PNG signature");
  process.exit(1);
}
// IHDR must follow the signature and declare 1024x1024 (this entry's size).
// Layout: 8-byte signature, 4-byte length, 4-byte "IHDR", 4-byte width,
// 4-byte height. A file too short to hold IHDR is truncated by definition.
if (buf.length < 33 || buf.toString("ascii", 12, 16) !== "IHDR") {
  console.error("entry.png: missing IHDR chunk (truncated file?)");
  process.exit(1);
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  console.error(`entry.png: expected 1024x1024, got ${width}x${height}`);
  process.exit(1);
}
// IEND chunk: last 12 bytes must be length 0, type IEND, CRC AE426082
const tail = buf.subarray(buf.length - 12);
if (
  tail.readUInt32BE(0) !== 0 ||
  tail.toString("ascii", 4, 8) !== "IEND" ||
  tail.readUInt32BE(8) !== 0xae426082
) {
  console.error("entry.png: missing or corrupt IEND chunk (truncated file?)");
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "entry.png"), buf);
console.log(`wrote ${join(outDir, "entry.png")} (${buf.length} bytes)`);
