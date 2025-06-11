# FTPCluster

**One portal. Many FTP servers.**  
FTPCluster bundles user accounts, permissions and proxy access into a single dark-themed web UI.

---

## Highlights

| Feature            | Description                                                           |
|--------------------|-----------------------------------------------------------------------|
| Unified Proxy      | Reach all managed servers through one IP address.                     |
| Central Accounts   | Manage users and their permissions in one place.                      |
| Automatic Agents   | Servers receive a telemetry agent via SSH on registration.            |
| Memory Dashboard   | Agents post RAM usage to the `/telemetry` endpoint.                   |
| Modern Interface   | Comfortable dark theme for daily use.                                 |

---

## Quick Start

1. Install dependencies (now includes `python-multipart`)
```bash
pip install -r requirements.txt
```
2. Set environment variables
```bash
export SECRET_KEY=<secret>
export FERNET_KEY=$(python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')
export MASTER_URL=http://<hostname>:8080  # URL of this instance
```
3. Launch the app
```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```
4. Verify the login page
```bash
curl http://localhost:8080/
```

---

## Using the System

1. Log in as admin and add your first server. The agent is uploaded automatically and begins reporting memory usage.
2. Create users and assign them to servers.
3. Users log in and see their permitted servers as folders.

Example layout for `user1`:
```
/home/user1/
├── serverA/
└── serverB/
```
Any access like `/ftp/user1/serverA/path/to/file.txt` is routed to the correct server.

---

## Repository Layout
```text
ftpcluster/
├── main.py          # FastAPI application
├── db.py            # SQLite initialization
├── models.py        # Database models
├── ftp_sync.py      # User management on remote servers
├── proxy.py         # Proxy endpoint implementation
├── server_agent.py  # Installs and starts slave agents
├── slave_agent.py   # Reports telemetry to MASTER_URL
├── templates/       # Jinja2 HTML templates
├── static/          # CSS and JavaScript
└── README.md
```

---

## License

MIT
