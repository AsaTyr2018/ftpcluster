# FTPCluster

**Central FTP user management with proxy access to multiple servers through a single IP address.**

---

## Features

* Web interface for managing users and servers
* User access rights configurable per server
* Central authentication with password hashing
* Access via a single IP through proxy routing
* Virtual subfolders for users based on server assignment

---

## Project Structure

```text
ftpcluster/
├── main.py          # FastAPI app and routing
├── db.py            # SQLite setup
├── models.py        # SQLAlchemy models
├── ftp_sync.py      # FTP user management
├── proxy.py         # Proxy access via central IP
├── templates/       # HTML UI with Jinja2
├── static/          # CSS/JS
└── README.md        # This file
```

---

## Setup

### Requirements

* Python 3.11+
* Reachable FTP or SFTP server

### Installation

```bash
pip install -r requirements.txt
export SECRET_KEY=<random>
export FERNET_KEY=$(python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')
uvicorn main:app --host 0.0.0.0 --port 8080
```

---

## Example

User "user1" has access to Server2 and Server3. After logging in:

```
/home/user1/
├── server2/
└── server3/
```

Requests such as:

```
/ftp/user1/server2/path/to/file.txt
```

are internally routed to Server2.

---

## API (selection)

### Auth

* `POST /login`
* `GET /logout`

### User management

* `GET /users`
* `POST /users`

### Server management

* `GET /servers`
* `POST /servers`

### Proxy access

* `GET /ftp/{username}/{server_alias}/{path:path}`

---

## Security

* Passwords hashed with bcrypt
* Admin and user passwords stored encrypted (Fernet)
* Signed login cookies via `SECRET_KEY`
* Optional: HTTPS with TLS certificate

---

## License

MIT

---

## Author

AsaTyr // 2025
