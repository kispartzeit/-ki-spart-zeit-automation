# Prüfprotokoll V2 – echter GitHub-Actions-Nachweis

Prüfdatum: 13. September 2026, Europe/Berlin. Produktionsartefakt technisch geprüft um 21:18:45 UTC.

## Geprüfter Produktionsstand

- Finaler Produktionscommit: `39fc170217ebff7924247c11b2a7a25b5e537d43` auf `main`.
- Repository: `https://github.com/kispartzeit/-ki-spart-zeit-automation.git`.
- Workflow: **KI spart Zeit – Video produzieren**, `.github/workflows/render.yml`.
- Run-ID: `34782854550`, erster Versuch, Trigger `push`, Ergebnis **success**.
- [Echter Workflow-Lauf](https://github.com/kispartzeit/-ki-spart-zeit-automation/actions/runs/34782854550).
- Job `produzieren`: 21:07:25–21:08:57 UTC; Validierung, Rendering und Upload erfolgreich ausgeführt.
- Reparaturdurchläufe: **0**. Keine Änderung an Workflow, Renderer oder Inhaltswarteschlange.

Diese Abschlussdokumentation wird anschließend separat committed und gepusht.
Ihr Commit unterscheidet sich vom geprüften Produktionscommit. Reine
Dokumentationsänderungen lösen wegen `push.paths` keinen neuen Renderlauf aus.
Den Dokumentationscommit bezeichnet der Git-Verlauf dieser Datei; sein eigener
SHA kann nicht vorab in ihm stehen.

## Tatsächlich heruntergeladenes Artefakt

- Name: `ki-spart-zeit-videos`; Artefakt-ID: `10325681320`.
- [Artefakt beim geprüften Lauf](https://github.com/kispartzeit/-ki-spart-zeit-automation/actions/runs/34782854550/artifacts/10325681320).
- ZIP-Größe laut GitHub: `5749473` Bytes.
- ZIP-SHA-256 laut GitHub-API und Upload-Log: `c2f474997beb817f65870adbee641d378c6de1fabbdfcd324da5b760adea4309`.
- Ablaufzeit laut GitHub: `2026-10-13T21:08:52Z`; Aufbewahrung 30 Tage.
- Download mit `gh run download` erfolgreich; entpackte Dateien anschließend lokal geprüft.

Exakt sieben Dateien:

```text
2026-w38-01-pdf-zum-lernquiz-posting.txt
2026-w38-01-pdf-zum-lernquiz.mp4
2026-w38-02-gemini-gems-posting.txt
2026-w38-02-gemini-gems.mp4
2026-w38-03-adobe-express-untertitel-posting.txt
2026-w38-03-adobe-express-untertitel.mp4
posting-plan.csv
```

Alle drei Postingtexte wurden gegen die Queue geprüft: Hooks, Sprechtexte,
Szenenpläne, Plattformtitel und Captions, Hashtags, Thumbnail-Texte, Kommentare,
Veröffentlichungsempfehlungen und Quellen sind enthalten. Die CSV enthält drei
Datenzeilen mit passenden IDs und Dateinamen. Ihr Feld `Sekunden` enthält die
gerundete Eingangsaudiodauer; das Abschluss-Gate nutzt die tatsächliche MP4-Dauer.

## Prüfung der drei echten MP4-Dateien

Alle Dateien: **1080 × 1920**, Hochformat, **H.264 / AAC**, **30 fps** in nominaler
und durchschnittlicher Bildrate, **yuv420p**. Je eine Video- und Audiospur;
Audio: 24 kHz, mono. Alle Containerdauern liegen zwischen 20 und 35 Sekunden.

| Produktionsdatei | MP4-Dauer | Mittlerer Audiopegel | Spitzenpegel |
| --- | ---: | ---: | ---: |
| 2026-w38-01-pdf-zum-lernquiz.mp4 | 31.056 s | -20.8 dB | -3.0 dB |
| 2026-w38-02-gemini-gems.mp4 | 32.376 s | -20.6 dB | -2.8 dB |
| 2026-w38-03-adobe-express-untertitel.mp4 | 33.384 s | -20.9 dB | -2.8 dB |

SHA-256 der tatsächlich heruntergeladenen MP4-Dateien:

```text
ea10cc8dd5bfac9a7887b2fd2d6fd5dd43a2c389617edad3397480ce57c68a2f  2026-w38-01-pdf-zum-lernquiz.mp4
d18fda612e2bbc3c08d69954aba88861661f7e9f83cbe6fcf61e9793c11667d3  2026-w38-02-gemini-gems.mp4
f2bc790745319cf37237fcfc8bf54e7f190ddf6221956f675a9d3d1d69f1afb2  2026-w38-03-adobe-express-untertitel.mp4
```

Der echte Lauf führte `python scripts/render.py --index "all"` ohne
`--test-tone` aus. Die geprüfte Queue verwendet `de-DE-ConradNeural`; dieser
Codepfad erzeugt Audio über `edge-tts`. Alle vollständigen Audiospuren wurden
dekodiert und mit `volumedetect` geprüft: keine ist vollständig stumm.
Eine vollständige Hörprüfung von Aussprache, Verständlichkeit und gesprochenem
Inhalt erfolgte nicht; dafür wird keine Qualitätszusage gemacht.

Eingebrannte Untertitel wurden anhand von neun aus den echten MP4-Dateien
extrahierten Einzelbildern visuell bestätigt: pro Video bei 1 Sekunde, in der
Mitte und 1 Sekunde vor dem Ende. Keine vollständige Wiedergabeprüfung und
keine Prüfung wortgenauer Untertitelsynchronität.

Prüfbefehle pro Produktionsdatei:

```sh
ffprobe -v error -show_streams -show_format -of json VIDEO.mp4
ffmpeg -hide_banner -nostats -i VIDEO.mp4 -vn -af volumedetect -f null -
```

Lokale Prüfwerkzeuge: FFmpeg/FFprobe 9.0.1 für macOS arm64 im temporären
Prüfverzeichnis, von [Martin Riedls Buildserver](https://ffmpeg.martin-riedl.de/),
Build `1787073674_9.0.1`; Drittanbieter-Binaries, keine offiziellen FFmpeg-Binaries.
Beide ZIP-Prüfsummen stimmten mit den Anbieterdateien überein. Beide
Codesignaturen bestanden außerhalb der Sandbox `codesign --verify --strict`:
Developer ID `Martin Riedl (KU3N25YGLU)`. Keine systemweite Installation oder
Umgehung einer Signatur- oder Zertifikatsprüfung.

## Frische lokale Prüfungen

- `python3 scripts/validate_content.py content/queue.json`: erfolgreich, drei Pakete.
- `python3 -m py_compile scripts/render.py scripts/validate_content.py`: erfolgreich.
- `python3 scripts/render.py --index all --test-tone --output PRUEFVERZEICHNIS`:
  drei vollständige technische Testrenderings erfolgreich, getrennt vom Produktionsartefakt.
- `ffprobe` auf allen drei lokalen Testrenderings: H.264/AAC, 1080 × 1920,
  30 fps, yuv420p; tatsächliche MP4-Dauern 27,766667 s, 28,833333 s und 27,766667 s.
- Musterbasierte Zugangsdatenprüfung der aktuellen getrackten und nicht
  ignorierten Repositorydateien, `.git/config` und der GitHub-CLI-Hostkonfiguration:
  keine Treffer. Keine Git-Historienprüfung und kein absoluter Geheimnisfreiheitsnachweis.
  Es wurden keine geheimen Werte ausgegeben.

## Grenzen des Nachweises

- Geprüfte Edition: `2026-W38`, Quellenprüfdatum laut Queue: `2026-09-13`.
  Der Validator prüft Pflichtfelder, Paketanzahl, HTTPS-Quellenstruktur,
  geschätzte Sprechdauer und definierte Überversprechen. Er prüft nicht den
  fachlichen Inhalt der Quellen; deren Aktualität wurde hier nicht vollständig erneut geprüft.
- Der Wochenzeitplan ist konfiguriert, aber durch diesen Push-Lauf nicht
  Ende-zu-Ende nachgewiesen. Das Gate verlangt die tatsächliche Startminute
  exakt 18:30 Uhr Europe/Berlin; verspätete Schedule-Läufe können sämtliche
  produktiven Schritte überspringen und dennoch grün enden.
- Nur Schedule-Läufe verlangen die aktuelle ISO-Wochenedition. Push und manuelle
  Läufe akzeptieren die bereitgestellte Edition. Schedule rendert das jeweilige
  Tagesvideo; dieser Push-Lauf erzeugte alle drei Videos.
- Der Push-Filter umfasst Queue, Skripte und Workflow. Reine Änderungen an
  `requirements.txt` oder Dokumentation starten keinen Renderlauf.
- Die Videos zeigen den gezeichneten Hintergrund, Hook, CTA und Untertitel.
  Der gelieferte Szenenplan wird nicht als echte App-Bildschirmaufnahme umgesetzt.
  Untertitelzeiten werden proportional zur Wortzahl verteilt.
- `edge-tts` bleibt eine kostenlose, inoffizielle Web-Abhängigkeit. Ein grüner
  Lauf beweist keine dauerhafte Verfügbarkeit oder zukünftige erfolgreiche Läufe.
- Der lokale CLI-Schreibpfad ist bewiesen. Eine automatische aktuelle
  ChatGPT-Themenrecherche mit Übergabe ins Repository ist damit noch nicht bewiesen.
- Nichts wurde auf TikTok, Instagram oder YouTube veröffentlicht.
  Veröffentlichung/Metricool und etwaige Plattformbestätigungen bleiben separate,
  noch nicht Ende-zu-Ende geprüfte Schritte. Keine kostenpflichtige Funktion wurde genutzt.

Frühere lokale TLS- und Connector-403-Beobachtungen betrafen den damaligen
Test- beziehungsweise Connectorpfad. Der hier belegte CLI-Push und echte
Actions-Lauf sind erfolgreich; der frühere Connector wurde nicht erneut qualifiziert.
