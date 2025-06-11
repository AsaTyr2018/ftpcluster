# Project: FTPCluster - Central FTP User Management with Proxy Mapping

## Overview

FTPCluster acts as a central management instance for users and servers in a distributed FTP cluster. The aim is to provide users access to multiple FTP servers through a single IP address while respecting individually assigned permissions.

## Main Features

* Web interface for managing users and servers
* Central authentication and user synchronization on target servers
* Configurable mapping of users to servers
* Reverse proxy access to remote servers via a central IP
* Virtual folder structure for user access

## Architecture

### Components

1. **FastAPI backend**
   * REST API and HTML endpoints (Jinja2)
   * User management (login, permissions, sessions)
2. **SQLite database**
   * Tables: `User`, `Server`, `Permission`
3. **FTP/SFTP modules**
   * Connection to remote servers via `ftplib` or `paramiko`
4. **Proxy interface**
   * Routes: `/ftp/{username}/{server_alias}/{path}`
   * Dynamic access control per user
5. **Frontend**
   * Bootstrap-based UI
   * Pages: login, dashboard, user management, server management

## Workflow

1. Admin creates users and assigns them to servers
2. Users log in through the central web interface
3. The virtual folder structure shows assigned servers as subfolders
4. File access is handled centrally and forwarded through the proxy

## Data Model

### Table: `User`
* id (int)
* username (str)
* password_hash (str)

### Table: `Server`
* id (int)
* alias (str)
* host (str)
* admin_user (str)
* admin_pass (str)

### Table: `Permission`
* id (int)
* user_id (FK -> User.id)
* server_id (FK -> Server.id)
* user_pass (str)

## Example

**User1** has access to Server2 and Server3. On login they see:

```
/home/user1/
├── server2/
└── server3/
```

Accessing `/ftp/user1/server2/files/data.csv` is internally forwarded to Server2.

## Security

* Password hashes with bcrypt
* JWT tokens or session-based authentication
* HTTPS recommended (uvicorn + TLS)

## Extensions

* Two-factor authentication
* Audit logging
* API for external integration

## Deployment

* Requirements: Python 3.11+, uvicorn, SQLite, FTP/SFTP server
* Start: `uvicorn main:app --host 0.0.0.0 --port 8080`
* Optional TLS configuration for production

## License

MIT License

---

# Technical Documentation

## Project Structure

```
ftpcluster/
├── main.py               # entry point, FastAPI app with routing
├── db.py                 # DB initialization & connections
├── models.py             # SQLAlchemy models (User, Server, Permission)
├── ftp_sync.py           # FTP operations: create/delete users
├── proxy.py              # access remote servers through central instance
├── templates/            # Jinja2 templates for HTML UI
├── static/               # CSS/JS
└── README.md             # instructions
```

## API Endpoints

### Users
* `POST /login` - authentication
* `GET /logout` - log out
* `GET /users` - list users (admin)
* `POST /users` - create user

### Servers
* `GET /servers` - list servers (admin)
* `POST /servers` - register new server

### Permissions
* `POST /permissions` - create user/server association

### Proxy Access
* `GET /ftp/{username}/{server_alias}/{path:path}` - access via central IP

## FTP Logic (`ftp_sync.py`)
```python
from ftplib import FTP


def create_user_on_servers(username, password, server_list):
    for srv in server_list:
        ftp = FTP(srv.host)
        ftp.login(srv.admin_user, srv.admin_pass)
        try:
            ftp.mkd(username)
        except Exception:
            pass
        ftp.quit()
```

## Reverse Proxy (`proxy.py`)
```python
@app.get('/ftp/{user}/{srv_alias}/{path:path}')
async def proxy_ftp(user, srv_alias, path):
    perm = db.get_permission(user, srv_alias)
    if not perm:
        raise HTTPException(403, 'No access')
    srv = db.get_server(srv_alias)
    ftp = FTP(srv.host)
    ftp.login(user, perm.user_pass)
    bio = io.BytesIO()
    ftp.retrbinary(f'RETR {path}', bio.write)
    return Response(bio.getvalue(), media_type='application/octet-stream')
```

## Database Setup (`db.py`)
```python
from sqlalchemy import create_engine
engine = create_engine('sqlite:///ftpcluster.db')
Base.metadata.create_all(engine)
```

## UI Components (Jinja2)
* `login.html` - login form
* `dashboard.html` - user overview
* `users.html` - user management
* `servers.html` - server management
