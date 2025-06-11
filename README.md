# FTPCluster

**One portal. Many FTP servers.**  
FTPCluster bundles user accounts, permissions and proxy access into a single dark-themed web UI.

## Latest Updates
- Remote setup script automatically installs slave and datalink agents via SSH.
- Added datalink agent for remote user creation.
- Documentation translated to English.

---

## Highlights

| Feature            | Description                                                           |
|--------------------|-----------------------------------------------------------------------|
| Unified Proxy      | Reach all managed servers through one IP address.                     |
| Central Accounts   | Manage users and their permissions in one place.                      |
| Automatic Agents   | Servers receive telemetry and datalink agents via SSH on registration. |
| Zero-Touch Setup   | Python environment and FTP server are installed automatically. |
| Memory Dashboard   | Agents post RAM usage to the `/telemetry` endpoint.                   |
| Modern Interface   | Comfortable dark theme for daily use.                                 |

---

## Quick Start
(See `admin-guide.md` for detailed instructions.)

1. Install dependencies
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

1. Log in as admin and open **Servers**. Generate the setup script and run it on the target machine.
2. The script installs slave and datalink agents which start reporting memory usage.
3. Create users and assign them to servers.
4. Users log in and see their permitted servers as folders.

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
├── server_agent.py  # Installs and starts slave and datalink agents
├── slave_agent.py   # Reports telemetry to MASTER_URL
├── datalink_agent.py # Accepts user creation requests
├── admin-guide.md   # Detailed administrator manual
├── user-guide.md    # Short manual for end users
├── templates/       # Jinja2 HTML templates
├── static/          # CSS and JavaScript
└── README.md
```

---

## License

MIT
