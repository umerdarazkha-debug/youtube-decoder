# youtube-decoder

A free Claude skill that reads any YouTube video and tells you why it works.

Paste a link. Claude pulls the captions with timestamps, then gives you:

1. **The hook**: the line that earns the next 30 seconds, and why it works.
2. **The structure**: the 3 to 7 beats the video follows, each with its timestamp.
3. **Moments worth jumping to**: 3 to 5 timestamps a viewer would want.
4. **Your version**: the same structure rebuilt as an outline for your niche.

No YouTube API key and no extra account. The video itself is never downloaded, only its caption track.

## Install

You need [Claude Code](https://claude.com/claude-code), Python 3.9 or newer, and either [yt-dlp](https://github.com/yt-dlp/yt-dlp) or [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/umerdarazkha-debug/youtube-decoder ~/.claude/skills/youtube-decoder
```

Then install yt-dlp if you don't have it:

```bash
pip install yt-dlp
```

If you have uv instead, skip that step. The script runs `uvx yt-dlp` on its own.

## Use it

Open Claude Code, paste a YouTube link and say what you want:

```
decode this video: https://www.youtube.com/watch?v=VIDEO_ID
```

"Why does this video work?", "give me the timestamps" and "turn this into a script for my niche" work too.

## What you get

The reply follows this shape (placeholders shown in braces):

```
The hook
[0:00] "{the opening line}"
Why it works: {curiosity, stakes, contrast or promise}

The structure (pattern: {list, three stories, before and after...})
[0:00] {beat name}: {one line}
[0:45] {beat name}: {one line}
[2:10] {beat name}: {one line}
...

Moments worth jumping to
[4:30] {why a viewer would want this moment}

Your version
The same beats in the same order, rewritten for your topic, with a hook under 12 words.
```

Every point comes with a timestamp from the transcript.

## How it works

| File | Job |
| --- | --- |
| `scripts/fetch_transcript.py` | Uses yt-dlp to fetch the caption track and prints a clean, timestamped transcript. |
| `SKILL.md` | Tells Claude how to read the transcript, what to report and how to rebuild the structure for you. |

You can run the script on its own:

```bash
python3 ~/.claude/skills/youtube-decoder/scripts/fetch_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" --out transcript.md
```

| Option | Default | What it does |
| --- | --- | --- |
| `--lang xx` | `en` | Caption language, for example `es` or `de` |
| `--out file.md` | prints to the terminal | Also saves the transcript to a file |

It prefers human-made captions and falls back to YouTube's auto-captions, with the repeated lines removed.

## Limits

- It reads what is said, not what is shown. If the answer depends on the visuals, Claude will tell you.
- No captions, no transcript. Some creators turn captions off.
- The script contacts YouTube to fetch the captions, and Claude reads the transcript in your normal session. Nothing goes to any other service.
- Use it to learn how a video is built. Borrow the shape, never the creator's words. Check YouTube's terms before using transcripts for anything beyond your own study.

## License

MIT. Use it, change it, share it.

Built by [Umer Daraz Khan](https://github.com/umerdarazkha-debug) with Claude Code. More at [@umer.does.ai](https://www.instagram.com/umer.does.ai/) and [YouTube](https://www.youtube.com/@umerdoesai).
