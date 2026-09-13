# Einmaliger MacBook-Abschluss

Nicht erneut unter **Plugins → GitHub** suchen. Die dortige Verbindung besitzt in
diesem Projekt keinen nutzbaren Schreibzugriff.

1. Den vorbereiteten Ordner `ki-spart-zeit-automation-ready` entpacken.
2. ChatGPT Desktop öffnen und links **Codex** auswählen.
3. Den entpackten Ordner als lokales Projekt öffnen.
4. In der Git-Ansicht den vorhandenen Commit prüfen und **Push** wählen.
5. Nur falls GitHub fragt: Konto `kispartzeit` im geschützten Browserfenster anmelden
   und den Push bestätigen.

Der Ordner ist bereits ein Git-Klon des richtigen Repositorys. Keine neue
Initialisierung, kein neues Repository und kein Token im Chat sind erforderlich.

Nach dem Push wird GitHub Actions automatisch durch die neue Workflow-Datei
gestartet. Erst der grüne Lauf bestätigt die reale Spracherzeugung.

Offizielle Anleitung zu lokalen Codex-Umgebungen und eingebauten Git-Funktionen:
https://learn.chatgpt.com/docs/environments/local-environment
