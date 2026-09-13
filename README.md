# KI spart Zeit – kostenlose Kurzvideo-Produktion

Dieses Repository rendert aus drei geprüften Produktionspaketen fertige
9:16-Videos und vollständige Begleittexte für TikTok, Instagram Reels und
YouTube Shorts.

## Automatisiert

- 1080 × 1920 Pixel, H.264/AAC, 30 fps
- deutsche Stimme über `edge-tts`
- eingebrannte Untertitel
- cyan-violett-magenta Portal-Identität mit futuristischer Stadt, ohne Roboter
- getrennte Titel und Captions für TikTok, Instagram und YouTube
- Szenenplan, drei Hooks, Hashtags, Thumbnail, angepinnter Kommentar und Quellen
- Rendering Montag, Mittwoch und Freitag um 18:30 Uhr Europe/Berlin
- Download als GitHub-Actions-Artefakt für 30 Tage

## Qualitäts-Gates

Der Validator stoppt den Lauf, wenn Pflichtbestandteile oder Quellen fehlen,
Überversprechen vorkommen, die Sprechdauer nicht passt oder eine alte
Wochenedition automatisch erneut verarbeitet würde. Der Renderer kontrolliert
zusätzlich die tatsächliche Audiodauer.

## Einmaliger Funktionstest nach dem Upload

1. In GitHub **Actions** öffnen.
2. **KI spart Zeit – Video produzieren** wählen.
3. **Run workflow** mit Auswahl `all` starten.
4. Das Artefakt **ki-spart-zeit-videos** herunterladen.

Erst ein grüner Actions-Lauf bestätigt, dass die externe kostenlose
Spracherzeugung in GitHub funktioniert.

## Ehrliche Systemgrenzen

- `edge-tts` ist kostenlos, aber eine inoffizielle Web-Abhängigkeit und kann
  sich ändern oder zeitweise ausfallen.
- Die sonntägliche ChatGPT-Recherche und das GitHub-Rendering sind erst nach
  einem erfolgreichen Schreib- und Übergabetest durchgängig verbunden.
- Das Repository veröffentlicht nicht selbst auf sozialen Plattformen.
  Fertige MP4-Dateien werden anschließend in Metricool übernommen; einzelne
  Plattformen können Bestätigungen verlangen.
- Veröffentlichungstermine sind Startwerte, keine Erfolgsgarantie. Nach vier
  Wochen werden sie anhand echter Kontodaten bewertet.

Weitere Details: `PROJECT_STATUS.md`, `VERIFICATION.md` und `SETUP_CODEX.md`.
