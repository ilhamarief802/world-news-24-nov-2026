// Entry program for make.fun's "Sum up 24 November's world news in one image".
// The picture is entry.png beside this file; this program checks it is a whole,
// valid PNG inside the competition's limits and writes it to /output/entry.png.
// No network, no dependencies beyond Node's standard library, and the same bytes
// out on every run.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { crc32 } from 'node:zlib';

const MAX_BYTES = 1048576;
const MAX_SIDE = 1024;
const SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

type Chunk = { type: string; length: number; crc: number };

function readChunks(buf: Buffer): Chunk[] {
  const chunks: Chunk[] = [];
  let at = SIGNATURE.length;
  while (at + 12 <= buf.length) {
    const length = buf.readUInt32BE(at);
    const type = buf.toString('latin1', at + 4, at + 8);
    const body = buf.subarray(at + 8, at + 8 + length);
    if (body.length !== length) throw new Error(`truncated ${type} chunk`);
    const crc = crc32(buf.subarray(at + 4, at + 8 + length)) >>> 0;
    const stored = buf.readUInt32BE(at + 8 + length);
    if (crc !== stored) throw new Error(`bad checksum on ${type} chunk`);
    chunks.push({ type, length, crc });
    at += 12 + length;
    if (type === 'IEND') break;
  }
  return chunks;
}

function check(buf: Buffer): string {
  if (buf.length > MAX_BYTES) throw new Error(`image is ${buf.length} bytes, over ${MAX_BYTES}`);
  if (!buf.subarray(0, 8).equals(SIGNATURE)) throw new Error('not a PNG');
  const chunks = readChunks(buf);
  const head = chunks[0];
  if (!head || head.type !== 'IHDR') throw new Error('PNG starts without IHDR');
  const width = buf.readUInt32BE(16);
  const height = buf.readUInt32BE(20);
  if (width > MAX_SIDE || height > MAX_SIDE) throw new Error(`image is ${width}x${height}`);
  const last = chunks[chunks.length - 1];
  if (!last || last.type !== 'IEND') throw new Error('PNG ends without IEND');
  return `${width}x${height}, ${buf.length} bytes, ${chunks.length} chunks verified`;
}

const image = readFileSync(new URL('./entry.png', import.meta.url));
const summary = check(image);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
console.log(`entry.png written to ${join(outDir, 'entry.png')} (${summary})`);
