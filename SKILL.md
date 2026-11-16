---
name: youtube-decoder
description: Decode any YouTube video that has captions - pull its full timestamped transcript (no API key, no account), then break down the hook, the structure and the moments worth jumping to, and rebuild that structure as an outline for the user's own niche. Use whenever the user pastes a YouTube link and asks what's in it, wants a summary, wants to know why a video works, wants timestamps, or wants to "steal the structure" / turn a video into their own script, even if they don't say "decode".
---

# YouTube Decoder

Claude can't play videos, and pasting a YouTube link alone gives it almost nothing to work with. This skill reads
the video's captions instead: every spoken word, with timestamps. It cannot see the visuals, so say so when the
answer depends on what is shown rather than said.

## 1. Get the transcript

Run the bundled script with the link the user gave (captions only, the video itself is never downloaded):

```bash
python3 scripts/fetch_transcript.py "<youtube url>" --out transcript.md
```

- It prefers human-made captions and falls back to YouTube's auto-captions (de-duplicated).
- It needs `yt-dlp` (`pip install yt-dlp`) or `uv` (it then runs `uvx yt-dlp`). If neither exists, install yt-dlp with the user's permission.
- Other languages: `--lang es`, `--lang de`, ...
- If it reports no captions, tell the user plainly: the creator turned captions off, so there is nothing to read.

Read `transcript.md` in full before answering. Long podcasts are fine; read them in chunks.

## 2. The breakdown

Reply in this order, short and scannable. Every claim must point at a timestamp from the transcript, never at a guess.

1. **The hook**: the line that earns the next 30 seconds, with its timestamp, and why it works (curiosity, stakes, contrast, promise).
2. **The structure**: the 3-7 beats the video actually follows, each as `[m:ss] beat name: one line`. Name the pattern if it has one (e.g. "three stories", problem -> agitation -> solution, list, before/after).
3. **Moments worth jumping to**: 3-5 timestamps a viewer would actually want, one line each.
4. **What carries it**: in two lines, the technique that makes it work (a repeated phrase, a turn, a specific story, a callback in the ending).

Quote at most a short phrase at a time from the transcript; describe the rest in your own words.

## 3. Rebuild it for the user

Ask for their niche or topic if you don't know it, then turn the structure (not the words) into an outline for their next video or post:

- same beats in the same order, each rewritten with their topic
- a hook written in their voice, in under 12 words
- a suggested length per beat based on the original's timestamps

Borrow the shape, never the creator's lines. The point is to learn why something works, not to copy it.
