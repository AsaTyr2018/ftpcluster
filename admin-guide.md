# Admin Guide

Dieses Dokument beschreibt, wie die FTPCluster-Instanz installiert wird und wie Administratoren neue FTP-Server einbinden.

## Installation des Servers

1. **Voraussetzungen**
   - Python 3.11 oder neuer
   - Zugriff auf mindestens einen FTP- oder SFTP-Server

2. **Abhängigkeiten installieren**
   ```bash
   pip install -r requirements.txt
   ```

3. **Umgebungsvariablen setzen**
   ```bash
   export SECRET_KEY=<zufaelliger_wert>
   export FERNET_KEY=$(python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')
   ```

4. **Datenbank erstellen und Anwendung starten**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8080
   ```
   Beim ersten Start wird die SQLite-Datenbank `ftpcluster.db` automatisch angelegt.

## Hinzufügen neuer Server

1. Melden Sie sich mit einem Admin-Account im Webinterface an.
2. Öffnen Sie die Seite **Serververwaltung** (`/servers`).
3. Tragen Sie dort Alias, Hostname sowie die Admin-Zugangsdaten des Zielservers ein.
4. Nach dem Speichern erscheint der Server in der Liste und kann Benutzern zugewiesen werden.

Alternativ können Server auch per API angelegt werden:
```bash
curl -X POST -F alias=<alias> -F host=<host> -F admin_user=<user> -F admin_pass=<pass> http://<server>:8080/servers
```
