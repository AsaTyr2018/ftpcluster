# User Guide

Dieses Dokument richtet sich an reguläre Benutzer ohne Adminrechte und erklärt die Nutzung von FTPCluster.

## Anmeldung

1. Öffnen Sie die Login-Seite der Anwendung (`/`).
2. Geben Sie Ihren Benutzernamen und Ihr Passwort ein.
3. Nach erfolgreichem Login werden Sie auf das Dashboard weitergeleitet.

## Dashboard und Serverzugriff

- Auf dem Dashboard werden Ihnen alle Server angezeigt, auf die Sie Zugriff haben.
- Navigieren Sie zu einem Serverordner, um Dateien über den integrierten Proxy abzurufen.
- Datei-URLs folgen dem Schema:
  ```
  /ftp/<username>/<server_alias>/<pfad/zur/datei>
  ```
  Beispiel:
  ```
  /ftp/user1/server2/data/report.csv
  ```
- Laden Sie Dateien mit einem normalen Browserdownload oder einem Kommandozeilenwerkzeug wie `curl` herunter.

Bei Zugriffsproblemen wenden Sie sich an einen Administrator, damit die entsprechenden Berechtigungen gesetzt werden können.
