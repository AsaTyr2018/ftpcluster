# FTPCluster

**Zentrale FTP-Benutzerverwaltung mit Proxy-Zugriff auf mehrere Server über eine einzige IP-Adresse.**

---

## Features

* Webinterface zur Benutzer- und Serververwaltung
* Benutzer-Zugriffsrechte pro Server konfigurierbar
* Zentrale Authentifizierung mit Passwort-Hashing
* Zugriff über zentrale IP per Proxy-Routing
* Virtuelle Subfolder für Benutzer gemäß Server-Zuweisung

---

## Projektstruktur

```text
ftpcluster/
├── main.py          # FastAPI App & Routing
├── db.py            # SQLite Setup
├── models.py        # SQLAlchemy Modelle
├── ftp_sync.py      # FTP Benutzerverwaltung
├── proxy.py         # Proxyzugriff via zentrale IP
├── templates/       # HTML UI via Jinja2
├── static/          # CSS/JS
└── README.md        # Diese Datei
```

---

## Setup

### Voraussetzungen

* Python 3.11+
* FTP oder SFTP-Server erreichbar

### Installation

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080
```

---

## Beispiel

Benutzer "user1" hat Zugriff auf Server2 und Server3. Nach dem Login:

```
/home/user1/
├── server2/
└── server3/
```

Zugriffe wie:

```
/ftp/user1/server2/path/to/file.txt
```

werden intern zu Server2 geroutet.

---

## API (Auswahl)

### Auth

* `POST /login`
* `GET /logout`

### Benutzerverwaltung

* `GET /users`
* `POST /users`

### Serververwaltung

* `GET /servers`
* `POST /servers`

### Proxy-Zugriff

* `GET /ftp/{username}/{server_alias}/{path:path}`

---

## Sicherheit

* Passwörter gehashed mit bcrypt
* Optional: HTTPS mit TLS-Zertifikat

---

## Lizenz

MIT

---

## Autor

AsaTyr // 2025
