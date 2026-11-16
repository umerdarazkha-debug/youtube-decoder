#!/usr/bin/env python3
"""Fetch the captions of a YouTube video and print a clean, timestamped transcript.

No API key, no account: it uses yt-dlp to download the caption track only (never the video).
Prefers human-made captions; falls back to YouTube's auto-captions, which repeat each line as they
roll, so those are de-duplicated.

    python3 fetch_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" [--lang en] [--out transcript.md]

Needs yt-dlp: either `pip install yt-dlp`, or uv installed (it then runs `uvx yt-dlp` automatically).
"""

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile


def ytdlp_cmd() -> list[str]:
    if shutil.which("yt-dlp"):
        return ["yt-dlp"]
    if shutil.which("uvx"):
        return ["uvx", "yt-dlp"]
    sys.exit("yt-dlp not found. Install it with `pip install yt-dlp` (or install uv), then run again.")


def fetch(url: str, lang: str, workdir: str) -> tuple[str, str, bool]:
    """Download captions only. Returns (vtt_path, metadata line, is_human_made)."""
    base = ytdlp_cmd()
    meta = subprocess.run(
        base + ["--skip-download", "--print", "%(title)s | %(uploader)s | %(duration_string)s", url],
        capture_output=True, text=True,
    )
    title = meta.stdout.strip().splitlines()[-1] if meta.stdout.strip() else url
    # Human tracks are named like "en" or "en-<id>"; auto-translated tracks exist only for auto-captions,
    # so the wide pattern is safe for human captions and the exact code is used for auto-captions.
    for auto, flag, langs in ((False, "--write-subs", f"{lang},{lang}-.*"), (True, "--write-auto-subs", lang)):
        subprocess.run(
            base + ["--skip-download", flag, "--sub-langs", langs, "--sub-format", "vtt", "-o", os.path.join(workdir, "%(id)s.%(ext)s"), url],
            capture_output=True, text=True,
        )
        found = sorted(glob.glob(os.path.join(workdir, "*.vtt")))
        if found:
            return found[0], title, not auto
    sys.exit(f"No '{lang}' captions found for this video. It may have captions turned off.")


def parse(vtt: str) -> list[tuple[str, str]]:
    text = open(vtt, encoding="utf-8").read()
    cues = re.findall(r"(\d\d:\d\d:\d\d)\.\d+ --> [^\n]*\n(.*?)(?:\n\n|\Z)", text, re.S)
    lines: list[tuple[str, str]] = []
    seen_tail = ""
    for ts, body in cues:
        body = re.sub(r"<[^>]+>", "", body)
        for raw in body.splitlines():
            line = re.sub(r"\s+", " ", raw).strip()
            if not line or line.startswith("[") and line.endswith("]"):
                continue
            # auto-captions roll: the same line shows up in several cues, keep it once
            if line == seen_tail or (lines and line == lines[-1][1]):
                continue
            seen_tail = line
            h, m, s = ts.split(":")
            stamp = f"{int(h) * 60 + int(m)}:{s}" if h != "00" else f"{int(m)}:{s}"
            lines.append((stamp, line))
    return lines


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("url")
    p.add_argument("--lang", default="en")
    p.add_argument("--out", default=None, help="write the transcript to this file as well")
    a = p.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        vtt, title, human = fetch(a.url, a.lang, tmp)
        lines = parse(vtt)
    words = sum(len(t.split()) for _, t in lines)
    header = f"# {title}\nSource: {a.url}\nCaptions: {'human-made' if human else 'auto-generated'} | {len(lines)} lines | {words} words\n"
    body = "\n".join(f"[{ts}] {t}" for ts, t in lines)
    out = header + "\n" + body + "\n"
    if a.out:
        open(a.out, "w", encoding="utf-8").write(out)
    print(out)


if __name__ == "__main__":
    main()
