#!/usr/bin/env python3
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

REQUIRED = {"id", "topic_reason", "hooks", "narration", "cta", "scenes", "platforms", "hashtags", "thumbnail", "pinned_comment", "publish_recommendation", "sources"}
PLATFORMS = {"tiktok", "instagram", "youtube"}
BANNED_CLAIMS = ("garantiert", "100%", "in 30 sekunden verstehen", "fehlerfrei")


def fail(number, message):
    raise ValueError(f"Video {number}: {message}")


def validate(path: Path, require_current_week: bool = False) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    videos = data.get("videos")
    if not isinstance(videos, list) or len(videos) != 3:
        raise ValueError("'videos' muss genau drei Einträge enthalten")
    if not re.fullmatch(r"\d{4}-W\d{2}", data.get("edition", "")):
        raise ValueError("edition muss dem Format YYYY-Www entsprechen")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", data.get("checked_on", "")):
        raise ValueError("checked_on muss dem Format YYYY-MM-DD entsprechen")
    current = date.today().isocalendar()
    expected_edition = f"{current.year}-W{current.week:02d}"
    if require_current_week and data["edition"] != expected_edition:
        raise ValueError(
            f"Veraltete Edition {data['edition']}; erwartet wird {expected_edition}. "
            "Automatische Veröffentlichung wird bewusst gestoppt."
        )
    ids = set()
    for number, video in enumerate(videos, 1):
        missing = REQUIRED - set(video)
        if missing:
            fail(number, f"Felder fehlen: {sorted(missing)}")
        if video["id"] in ids:
            fail(number, f"doppelte ID {video['id']}")
        ids.add(video["id"])
        if not isinstance(video["hooks"], list) or len(video["hooks"]) != 3:
            fail(number, "hooks muss genau drei Varianten enthalten")
        if not isinstance(video["scenes"], list) or len(video["scenes"]) < 3:
            fail(number, "scenes muss mindestens drei Szenen enthalten")
        if set(video["platforms"]) != PLATFORMS:
            fail(number, "platforms muss tiktok, instagram und youtube enthalten")
        for platform, metadata in video["platforms"].items():
            if not metadata.get("title") or not metadata.get("caption"):
                fail(number, f"Titel oder Caption für {platform} fehlt")
        if not isinstance(video["hashtags"], list) or not 2 <= len(video["hashtags"]) <= 5:
            fail(number, "hashtags muss zwei bis fünf Einträge enthalten")
        if any(not tag.startswith("#") for tag in video["hashtags"]):
            fail(number, "jedes Hashtag muss mit # beginnen")
        if not isinstance(video["sources"], list) or not video["sources"]:
            fail(number, "mindestens eine Quelle fehlt")
        for source in video["sources"]:
            parsed = urlparse(source)
            if parsed.scheme != "https" or not parsed.netloc:
                fail(number, f"ungültige HTTPS-Quelle: {source}")
        combined = " ".join(str(value) for value in video.values()).lower()
        for phrase in BANNED_CLAIMS:
            if phrase in combined:
                fail(number, f"unzulässiges Überversprechen: {phrase}")
        estimated_seconds = len(video["narration"].split()) / 2.55
        if not 20 <= estimated_seconds <= 35:
            fail(number, f"Sprechtext liegt geschätzt bei {estimated_seconds:.1f} Sekunden")
    return data


if __name__ == "__main__":
    try:
        arguments = [arg for arg in sys.argv[1:] if arg != "--require-current-week"]
        result = validate(
            Path(arguments[0] if arguments else "content/queue.json"),
            require_current_week="--require-current-week" in sys.argv,
        )
        print(f"OK: {len(result['videos'])} vollständige, quellenbelegte Pakete geprüft")
    except Exception as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        raise SystemExit(1)
