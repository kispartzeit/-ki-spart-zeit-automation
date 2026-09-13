# Verbindlicher Projektstatus

Stand: 13. September 2026, Europe/Berlin.

## Nachgewiesen

Das vorhandene lokale Repository wurde über `main` erfolgreich nach
`https://github.com/kispartzeit/-ki-spart-zeit-automation.git` gepusht.
Kein neues Repository, kein Force-Push und keine Umschreibung der Git-Historie.

- Finaler Produktionscommit: `39fc170217ebff7924247c11b2a7a25b5e537d43`.
- GitHub CLI 2.100.0 für macOS arm64 installiert; die vorgegebene ZIP-SHA-256-Summe
  wurde vor der Installation bestätigt.
- Browseranmeldung und API-Login `kispartzeit` bestätigt; HTTPS-Git eingerichtet.
  GitHub CLI meldet sichere Speicherung im macOS-Schlüsselbund (`keyring`).
- Automatisch durch den Push gestarteter Workflow **KI spart Zeit – Video produzieren**:
  Run-ID `34782854550`, erster Versuch, Ergebnis **success**.
- [Erfolgreicher Lauf](https://github.com/kispartzeit/-ki-spart-zeit-automation/actions/runs/34782854550),
  Job abgeschlossen am 13. September 2026 um 21:08:57 UTC.
- Keine Reparatur an Produktionsdateien notwendig; **0 Reparaturdurchläufe**.
- [Artefakt `ki-spart-zeit-videos`](https://github.com/kispartzeit/-ki-spart-zeit-automation/actions/runs/34782854550/artifacts/10325681320)
  heruntergeladen und geprüft: genau drei MP4-Dateien, drei Postingtexte und
  `posting-plan.csv` mit drei Datenzeilen.
- Alle echten MP4: **1080 × 1920, H.264/AAC, 30 fps, yuv420p**;
  Dauern **31,056 / 32,376 / 33,384 Sekunden**.
- Normaler deutscher TTS-Pfad mit `de-DE-ConradNeural`, kein Testton im
  Produktionslauf, vorhandene und nicht vollständig stumme Audiospuren.
- Eingebrannte Untertitel in neun geprüften Einzelbildern sichtbar.
- Lokaler Validator, Python-Syntaxprüfung sowie drei separate technische
  Testrenderings mit Testton und deren ffprobe-Prüfung erfolgreich.

Details, Dateinamen, Hashes und Prüfumfang stehen in [VERIFICATION.md](VERIFICATION.md).
Artefakt-ID: `10325681320`; Ablaufzeit laut GitHub: `2026-10-13T21:08:52Z`.

Die Abschlussdokumentation wird separat committed und gepusht. Dieser spätere
Dokumentationscommit enthält dieselben Produktionsdateien wie der geprüfte
Render-Commit. Reine Dokumentationsänderungen lösen keinen neuen Renderlauf aus.

## Bewusste Grenzen und verbleibende Schritte

- Der Renderer erzeugt fertige Produktionsdateien. Sprachqualität und vollständige
  Untertitelsynchronität wurden nicht durch vollständiges Anhören/Abspielen geprüft.
  Vor Veröffentlichung bleibt eine redaktionelle Prüfung erforderlich.
- Die Videos enthalten Grafik, Hook, CTA und Untertitel; echte App-Demonstrationen
  aus den mitgelieferten Szenenplänen werden nicht automatisch aufgenommen.
- Eine automatische aktuelle Themenrecherche von ChatGPT in dieses Repository
  ist erst nach einem getesteten automatischen Schreib- und Übergabepfad bewiesen.
  Der erfolgreiche lokale CLI-Push ersetzt diesen Nachweis nicht.
- Die Queue enthält Edition `2026-W38`. Der Validator prüft Quellenstruktur,
  keine vollständige fachliche Aktualität der Inhalte.
- Der Wochenzeitplan ist nicht durch einen echten Schedule-Lauf bewiesen.
  Das exakte 18:30-Minuten-Gate kann verspätete Läufe überspringen; ein grüner
  solcher Lauf wäre noch kein Rendernachweis.
- `edge-tts` ist kostenlos, aber eine inoffizielle Web-Abhängigkeit und nicht
  garantiert ausfallsicher. Der erfolgreiche Lauf ist keine Dauerbetriebsgarantie.
- Nichts wurde auf TikTok, Instagram oder YouTube veröffentlicht. Übernahme in
  Metricool und etwaige Plattformbestätigungen bleiben separate Schritte;
  der Veröffentlichungsweg wurde nicht Ende-zu-Ende geprüft.
- Keine Veröffentlichung und keine kostenpflichtige Funktion ohne ausdrücklichen Auftrag.

Der frühere Connector-403 und der frühere lokale TLS-Fehler sind historische
Beobachtungen anderer Zugriffspfade. Sie blockieren den hier nachgewiesenen
CLI-/Actions-Weg nicht; eine erneute Qualifizierung dieser Pfade erfolgte nicht.
