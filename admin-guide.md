# FTPCluster Administration

Welcome, administrator! This guide covers server installation, agent handling and common tasks.

---

## 1. Installation

### Requirements
- Python 3.11+
- Access to one or more FTP/SFTP servers

### Steps
```bash
pip install -r requirements.txt
export SECRET_KEY=<random>
export FERNET_KEY=$(python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')
export MASTER_URL=http://<this_host>:8080
uvicorn main:app --host 0.0.0.0 --port 8080
```
The `MASTER_URL` must point to the running instance so slave agents can post telemetry.

---

## Vorbereitung

Beim Anlegen eines neuen Servers liefert der Master ein Shell-Skript, das auf
dem Zielsystem als `root` ausgeführt wird. Dieses Skript

1. legt den angegebenen Admin-Benutzer an und sperrt dessen Passwort,
2. trägt ihn mit `NOPASSWD` in `/etc/sudoers.d/` ein,
3. erzeugt ein SSH-Schlüsselpaar und sendet den privaten Schlüssel an den Master.

Der Master speichert den Schlüssel für die zukünftige Kommunikation und
installiert danach automatisch die benötigten Pakete sowie die Agents.

Beispielablauf:

```bash
curl -F alias=meinserver -F host=10.0.0.5 http://MASTER/servers > setup.sh
sudo bash setup.sh
```

Nach Ausführung des Skripts erscheint der Server in der Liste.

---

## 2. Registering a Server

1. Log in as admin and open **Servers**.
2. Choose **Add** and gib Host sowie Alias an.
3. Speichere das ausgegebene Skript auf dem Zielserver und führe es als `root` aus.
4. Danach installiert der Master automatisch die benötigten Pakete und startet die Agents (datalink-Port 9000).
5. Der neue Server erscheint anschließend in der Liste und zeigt seine letzte Speicherauslastung.

---

## 3. Managing Users

- Use the **Users** page to create accounts and assign servers.
- Users only see the servers you select.

---

## 4. Monitoring

The **Servers** page displays telemetry from agents. If a server stops reporting, check connectivity or reinstall the agent from the same page.

Enjoy your streamlined FTP management!
