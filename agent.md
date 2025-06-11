# Projekt: FTPCluster - Zentrale FTP-Benutzerverwaltung mit Proxy-Mapping

## Überblick

FTPCluster ist eine zentrale Verwaltungsinstanz zur Benutzer- und Serververwaltung in einem verteilten FTP-Cluster. Ziel ist es, Benutzern über eine einzige IP-Adresse Zugriff auf mehrere FTP-Server zu geben, entsprechend individuell zugewiesener Rechte.

## Hauptfunktionen

* Webinterface zur Verwaltung von Benutzern und Servern
* Zentrale Authentifizierung und Benutzer-Synchronisation auf Zielservern
* Konfigurierbares Mapping von Benutzern zu Servern
* Reverse-Proxy-Zugriff auf entfernte Server über zentrale IP
* Virtuelle Ordnerstruktur für Benutzerzugriff

## Architektur

### Komponenten

1. **FastAPI Backend**

   * REST API & HTML-Endpoints (Jinja2)
   * Benutzerverwaltung (Anmeldung, Rechte, Sessions)

2. **SQLite Datenbank**

   * Tabellen: `User`, `Server`, `Permission`

3. **FTP-/SFTP-Module**

   * Verbindung zu Remote-Servern über `ftplib` oder `paramiko`

4. **Proxy-Interface**

   * Routen: `/ftp/{username}/{server_alias}/{path}`
   * Dynamische Zugriffskontrolle pro Benutzer

5. **Frontend**

   * Bootstrap-basiertes UI
   * Seiten: Login, Dashboard, Benutzerverwaltung, Serververwaltung

## Ablauf

1. Admin erstellt Benutzer und ordnet ihnen Server zu
2. Benutzer meldet sich an zentraler Weboberfläche an
3. Virtuelle Ordnerstruktur zeigt freigegebene Server als Subordner
4. Zugriffe auf Dateien werden zentral verarbeitet und über Proxy weitergeleitet

## Datenmodell

### Tabelle: `User`

* id (int)
* username (str)
* password\_hash (str)

### Tabelle: `Server`

* id (int)
* alias (str)
* host (str)
* admin\_user (str)
* admin\_pass (str)

### Tabelle: `Permission`

* id (int)
* user\_id (FK -> User.id)
* server\_id (FK -> Server.id)
* user\_pass (str)

## Beispiel

**User1** hat Zugriff auf Server2 und Server3. Beim Login sieht er:

```
/home/user1/
├── server2/
└── server3/
```

Zugriff auf `/ftp/user1/server2/files/data.csv` wird intern über Proxy zu Server2 weitergeleitet.

## Sicherheit

* Passwort-Hashes mit bcrypt
* JWT-Token oder session-based Auth
* HTTPS empfohlen (uvicorn + TLS)

## Erweiterungen

* Zwei-Faktor-Authentifizierung
* Audit-Logging
* API für externe Anbindung

## Deployment

* Systemvoraussetzungen: Python 3.11+, uvicorn, SQLite, FTP/SFTP Server
* Start: `uvicorn main:app --host 0.0.0.0 --port 8080`
* Optionale TLS-Konfiguration für produktive Umgebung

## Lizenz

MIT-Lizenz

---

# Technische Dokumentation

## Projektstruktur

```
ftpcluster/
├── main.py               # Einstiegspunkt, FastAPI-App mit Routing
├── db.py                 # DB-Initialisierung & Verbindungen
├── models.py             # SQLAlchemy-Modelle (User, Server, Permission)
├── ftp_sync.py           # FTP-Operationen: Benutzer anlegen/löschen
├── proxy.py              # Zugriff auf Remote-Server über zentrale Instanz
├── templates/            # Jinja2 Templates für HTML-UI
├── static/               # CSS/JS
└── README.md             # Anleitung
```

## API-Endpunkte

### Benutzer

* `POST /login` - Authentifizierung
* `GET /logout` - Logout
* `GET /users` - Benutzerliste (Admin)
* `POST /users` - Benutzer erstellen

### Server

* `GET /servers` - Serverliste (Admin)
* `POST /servers` - Neuen Server registrieren

### Berechtigungen

* `POST /permissions` - Benutzer/Server-Zuordnung erstellen

### Proxy-Zugriff

* `GET /ftp/{username}/{server_alias}/{path:path}` - Zugriff über zentrale IP

## FTP-Logik (`ftp_sync.py`)

```python
from ftplib import FTP

def create_user_on_servers(username, password, server_list):
    for srv in server_list:
        ftp = FTP(srv.host)
        ftp.login(srv.admin_user, srv.admin_pass)
        try:
            ftp.mkd(username)
        except:
            pass
        ftp.quit()
```

## Reverse Proxy (`proxy.py`)

```python
@app.get('/ftp/{user}/{srv_alias}/{path:path}')
async def proxy_ftp(user, srv_alias, path):
    perm = db.get_permission(user, srv_alias)
    if not perm:
        raise HTTPException(403, 'Kein Zugriff')
    srv = db.get_server(srv_alias)
    ftp = FTP(srv.host)
    ftp.login(user, perm.user_pass)
    bio = io.BytesIO()
    ftp.retrbinary(f'RETR {path}', bio.write)
    return Response(bio.getvalue(), media_type='application/octet-stream')
```

## Datenbank-Setup (`db.py`)

```python
from sqlalchemy import create_engine
engine = create_engine('sqlite:///ftpcluster.db')
Base.metadata.create_all(engine)
```

## UI-Komponenten (Jinja2)

* `login.html` - Formular für Login
* `dashboard.html` - Übersicht für Benutzer
* `users.html` - Benutzerverwaltung
* `servers.html` - Serververwaltung
