# Verbindlicher Projektstatus

Stand: 13. September 2026

## Nachgewiesen

- Ziel-Repository: `kispartzeit/-ki-spart-zeit-automation` (öffentlich, Branch `main`).
- Lesen über den bisherigen GitHub-Connector funktioniert.
- Schreiben von Datei, Blob und Issue scheitert jeweils mit HTTP 403: `Resource not accessible by integration`.
- Das Repository selbst ist nicht die Ursache. Der verwendete Connector besitzt keinen nutzbaren Schreibzugriff.
- Für Dateiänderungen braucht die GitHub-Integration `Contents: write`; Änderungen unter `.github/workflows` brauchen zusätzlich `Workflows: write`.

## Gewählter MacBook-Pfad

Das Repository wurde öffentlich und unverändert geklont. V2 wird in diesem echten
lokalen Git-Klon vorbereitet, geprüft und committed. Der verbleibende externe
Schritt ist ausschließlich die GitHub-Anmeldung beim ersten Push aus Codex Desktop.

Die nicht anklickbare Zeile unter „Plugins → GitHub“ wird nicht weiter verwendet.
Sie ist für den lokalen Git-Push nicht erforderlich.

## Bewusste Grenzen

- Der Workflow erzeugt fertige MP4-Dateien und Posting-Metadaten.
- Neue aktuelle Themen kommen erst dann automatisch ins Repository, wenn eine Automation nachweislich Schreibzugriff besitzt.
- Automatisches öffentliches Posten wird erst als aktiv bezeichnet, wenn jede Plattform den konkreten Veröffentlichungsweg erfolgreich bestätigt hat.
- `edge-tts` ist kostenlos, aber eine inoffizielle Web-Abhängigkeit und daher nicht garantiert ausfallsicher.
