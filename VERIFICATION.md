# Prüfprotokoll V2

Prüfdatum: 13. September 2026

## Erfolgreich geprüft

- JSON-Schema und alle Pflichtbestandteile für genau drei Pakete
- je drei Hooks, drei Plattformtitel und drei Plattform-Captions
- zwei bis fünf Hashtags und mindestens eine HTTPS-Quelle je Paket
- Schutz vor typischen absoluten Überversprechen
- Python-Syntax beider Skripte
- drei vollständige technische Testrenderings mit Testton
- Video: H.264, 1080 × 1920, 30 fps, yuv420p
- Audio im Container: AAC
- Testdauern: 25,93 s; 27,04 s; 25,93 s
- visuelle Prüfung der Portal-Identität und der CTA-Safe-Zone
- Sommer-/Winterzeit-Gate für 18:30 Uhr Europe/Berlin
- Stopp bei veralteter Wochenedition

## Noch nicht erfolgreich prüfbar

- Reale `edge-tts`-Stimme: Die lokale isolierte Umgebung brach beim externen
  TLS-Zertifikat ab. Zertifikatsprüfung wurde nicht deaktiviert. Der echte Nachweis
  muss durch einen grünen GitHub-Actions-Lauf erfolgen.
- GitHub-Upload: Der bisherige Connector antwortet bei Datei, Blob und Issue mit
  HTTP 403. Es wurde nichts am Repository verändert.
- Automatische Übernahme des sonntäglichen Recherchepakets in GitHub: erst nach
  nachgewiesenem Schreibzugriff aktivierbar.
- Veröffentlichung über Metricool: nicht Bestandteil dieses Render-Workflows und
  noch nicht Ende-zu-Ende getestet.
