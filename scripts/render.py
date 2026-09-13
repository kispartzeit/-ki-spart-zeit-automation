#!/usr/bin/env python3
import argparse
import asyncio
import csv
import random
import subprocess
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from validate_content import validate

WIDTH, HEIGHT = 1080, 1920
FPS = 30


def command(args):
    subprocess.run(args, check=True)


def font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def wrapped(draw, text, box, face, fill, spacing=12, anchor="mm"):
    x0, y0, x1, y1 = box
    max_width = x1 - x0
    words, lines, current = text.split(), [], ""
    for word in words:
        test = f"{current} {word}".strip()
        if draw.textbbox((0, 0), test, font=face)[2] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    line_height = face.size + spacing
    start_y = (y0 + y1 - len(lines) * line_height) / 2
    for i, line in enumerate(lines):
        draw.text(((x0 + x1) / 2, start_y + i * line_height), line, font=face, fill=fill, anchor=anchor)


def background(video, target):
    seed = sum(ord(c) for c in video["id"])
    rng = random.Random(seed)
    im = Image.new("RGB", (WIDTH, HEIGHT))
    px = im.load()
    top, bottom = (7, 10, 30), (26, 0, 58)
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        color = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        for x in range(WIDTH):
            px[x, y] = color
    draw = ImageDraw.Draw(im, "RGBA")

    # Futuristische Skyline statt Roboter-Motiv.
    horizon = 1180
    for x in range(-20, WIDTH + 20, 70):
        w = rng.randint(65, 145)
        h = rng.randint(220, 760)
        y = horizon - h
        draw.rounded_rectangle((x, y, x + w, HEIGHT), radius=10, fill=(8, 13, 35, 245), outline=(0, 235, 255, 110), width=3)
        for wy in range(y + 35, horizon - 20, 48):
            for wx in range(x + 18, x + w - 10, 28):
                if rng.random() > .35:
                    draw.rectangle((wx, wy, wx + 11, wy + 22), fill=rng.choice([(0, 240, 255, 180), (255, 40, 200, 180), (130, 85, 255, 170)]))
    draw.polygon([(0, 1510), (WIDTH, 1280), (WIDTH, HEIGHT), (0, HEIGHT)], fill=(4, 5, 20, 245))
    for offset in range(-700, 900, 120):
        draw.line((WIDTH // 2, 1320, WIDTH // 2 + offset, HEIGHT), fill=(0, 230, 255, 90), width=3)
    for y in range(1380, HEIGHT, 100):
        draw.line((0, y, WIDTH, y), fill=(255, 30, 210, 80), width=3)

    draw.ellipse((420, 95, 660, 335), fill=(8, 15, 45, 245), outline=(0, 245, 255, 255), width=10)
    draw.ellipse((442, 117, 638, 313), outline=(255, 35, 220, 210), width=7)
    draw.text((540, 215), "KI", font=font(92, True), fill=(245, 250, 255), anchor="mm")
    draw.text((540, 370), "KI SPART ZEIT", font=font(42, True), fill=(110, 245, 255), anchor="mm")

    draw.rounded_rectangle((70, 470, 1010, 850), radius=42, fill=(5, 10, 35, 210), outline=(80, 235, 255, 170), width=4)
    wrapped(draw, video["hooks"][0], (120, 510, 960, 810), font(70, True), (255, 255, 255, 255), spacing=18)
    # CTA oberhalb der typischen Plattform-Bedienelemente halten.
    wrapped(draw, video["cta"], (100, 1430, 980, 1590), font(42, True), (245, 250, 255, 255), spacing=10)
    im.save(target)


async def make_voice(text, voice, target):
    import edge_tts
    await edge_tts.Communicate(text=text, voice=voice, rate="+5%", volume="+0%").save(str(target))


def duration(path):
    value = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path)
    ], text=True)
    return float(value.strip())


def timestamp(seconds):
    millis = round(seconds * 1000)
    hours, millis = divmod(millis, 3_600_000)
    minutes, millis = divmod(millis, 60_000)
    secs, millis = divmod(millis, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def subtitles(text, seconds, target):
    words = text.split()
    chunks = [words[i:i + 7] for i in range(0, len(words), 7)]
    weights = [max(1, len(chunk)) for chunk in chunks]
    total = sum(weights)
    cursor = 0.0
    blocks, events = [], []
    for number, (chunk, weight) in enumerate(zip(chunks, weights), 1):
        end = seconds if number == len(chunks) else cursor + seconds * weight / total
        caption = " ".join(chunk)
        blocks.append(f"{number}\n{timestamp(cursor)} --> {timestamp(end)}\n{caption}\n")
        events.append((cursor, end, caption))
        cursor = end
    target.write_text("\n".join(blocks), encoding="utf-8")
    return events


def render_one(video, voice, checked_on, out, test_tone=False):
    work = out / f".{video['id']}"
    work.mkdir(parents=True, exist_ok=True)
    bg, audio, srt = work / "background.png", work / "voice.mp3", work / "captions.srt"
    background(video, bg)
    if test_tone:
        estimate = max(8, len(video["narration"].split()) / 2.7)
        command(["ffmpeg", "-y", "-f", "lavfi", "-i", "sine=frequency=220:sample_rate=44100", "-t", str(estimate), str(audio)])
    else:
        asyncio.run(make_voice(video["narration"], voice, audio))
    seconds = duration(audio)
    if not 20 <= seconds <= 35:
        raise ValueError(
            f"{video['id']}: Audiodauer {seconds:.1f}s liegt außerhalb von 20–35s"
        )
    events = subtitles(video["narration"], seconds, srt)
    target = out / f"{video['id']}.mp4"
    filters = [f"scale=1134:2016,crop={WIDTH}:{HEIGHT}:x='27+20*sin(t/3)':y='48+20*cos(t/4)',fps={FPS}"]
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    for number, (start, end, caption) in enumerate(events):
        caption_file = work / f"caption-{number:02}.txt"
        caption_file.write_text(textwrap.fill(caption, width=24), encoding="utf-8")
        filters.append(
            "drawtext="
            f"fontfile={font_path}:textfile={caption_file}:reload=0:"
            "fontcolor=white:fontsize=58:borderw=5:bordercolor=0x120724:"
            f"x=(w-text_w)/2:y=1120:enable='between(t,{start:.3f},{end:.3f})'"
        )
    vf = ",".join(filters)
    command([
        "ffmpeg", "-y", "-loop", "1", "-i", str(bg), "-i", str(audio),
        "-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest",
        "-movflags", "+faststart", str(target)
    ])
    posting = [
        f"THEMA\n{video['topic_reason']}",
        "HOOKS\n" + "\n".join(f"{index}. {hook}" for index, hook in enumerate(video["hooks"], 1)),
        f"SPRECHERTEXT\n{video['narration']}",
        "SZENENPLAN\n" + "\n".join(
            f"{scene['seconds']} | {scene['visual']} | EINBLENDUNG: {scene['overlay']}"
            for scene in video["scenes"]
        ),
    ]
    for platform in ("tiktok", "instagram", "youtube"):
        meta = video["platforms"][platform]
        posting.append(
            f"{platform.upper()}\nTITEL: {meta['title']}\nCAPTION: {meta['caption']}"
        )
    posting.extend([
        f"HASHTAGS\n{' '.join(video['hashtags'])}",
        f"THUMBNAIL\n{video['thumbnail']}",
        f"ANGEHEFTETER KOMMENTAR\n{video['pinned_comment']}",
        f"VERÖFFENTLICHUNG\n{video['publish_recommendation']}",
        "QUELLEN (geprüft am {date})\n{sources}".format(
            date=checked_on,
            sources="\n".join(video["sources"]),
        ),
    ])
    (out / f"{video['id']}-posting.txt").write_text("\n\n".join(posting) + "\n", encoding="utf-8")
    return target, seconds


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="content/queue.json")
    parser.add_argument("--output", default="dist")
    parser.add_argument("--index", default="all", help="all, auto oder nullbasierter Index")
    parser.add_argument("--test-tone", action="store_true")
    args = parser.parse_args()
    data = validate(Path(args.input))
    videos = data["videos"]
    if args.index == "all":
        selected = videos
    elif args.index == "auto":
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        schedule_slot = {0: 0, 2: 1, 4: 2}.get(now.weekday(), now.timetuple().tm_yday)
        selected = [videos[schedule_slot % len(videos)]]
    else:
        selected = [videos[int(args.index) % len(videos)]]
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for video in selected:
        target, seconds = render_one(
            video,
            data.get("voice", "de-DE-ConradNeural"),
            data["checked_on"],
            out,
            args.test_tone,
        )
        rows.append([
            video["id"], target.name, f"{seconds:.1f}",
            video["platforms"]["tiktok"]["title"],
            video["platforms"]["instagram"]["title"],
            video["platforms"]["youtube"]["title"],
            " ".join(video["hashtags"]),
        ])
    with (out / "posting-plan.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle, delimiter=";")
        writer.writerow(["ID", "Datei", "Sekunden", "TikTok-Titel", "Instagram-Titel", "YouTube-Titel", "Hashtags"])
        writer.writerows(rows)
    print(f"Fertig: {len(rows)} Video(s) in {out}")


if __name__ == "__main__":
    main()
