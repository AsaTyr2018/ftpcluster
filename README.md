# FTPCluster

**One portal. Many FTP servers.**  
FTPCluster bundles user accounts, permissions and proxy access into a single dark-themed web UI.

> **WARNING:** This repository is a work in progress and not ready for production use!

## Latest Updates
- Remote setup script automatically installs slave and datalink agents via SSH.
- Added datalink agent for remote user creation.
- Documentation translated to English.
- New `update_master.sh` script upgrades existing installations.
- UI now has navigation links, footers and a user list.
- Bcrypt version pinned to maintain passlib compatibility.
- Added `generate_slave_bundle.py` for zero-touch slave registration.

---

## Highlights

| Feature            | Description                                                           |
|--------------------|-----------------------------------------------------------------------|
| Unified Proxy      | Reach all managed servers through one IP address.                     |
| Central Accounts   | Manage users and their permissions in one place.                      |
| Automatic Agents   | Servers receive telemetry and datalink agents via SSH on registration. |
| Zero-Touch Setup   | Python environment and FTP server are installed automatically. |
| Usage Dashboard    | Agents post RAM, CPU, user count and disk usage to the `/telemetry` endpoint. |
| Modern Interface   | Comfortable dark theme for daily use.                                 |

---
## Installation via Script

The easiest way to get started is to run the setup script. It clones this
repository, installs the Python dependencies and configures a systemd service so
FTPCluster starts automatically on boot.

```bash
curl -s https://raw.githubusercontent.com/AsaTyr2018/ftpcluster/main/scripts/setup_master.sh | sudo bash
```

---

## Quick Start

1. Run the installation command above.
2. Wait for the script to print the generated admin password.
3. Open `http://<server>:8080` in your browser and log in as **admin**.

That's it! The service is already running in the background thanks to the
systemd unit created by the script. See `docs/admin-guide.md` if you prefer a
manual setup.

---

## Using the System

1. Log in as admin and open **Servers**. Generate the setup script and run it on the target machine.
2. The script installs slave and datalink agents which start reporting memory, CPU and disk statistics.
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
├── security.py      # Session and crypto helpers
├── ftp_sync.py      # User management on remote servers
├── proxy.py         # Proxy endpoint implementation
├── agents/
│   ├── server_agent.py  # Installs and starts remote agents
│   ├── slave_agent.py   # Reports telemetry to MASTER_URL
│   └── datalink_agent.py # Accepts user creation requests
├── scripts/
│   ├── setup_master.sh  # Initial deployment
│   └── update_master.sh # Upgrade existing installation
├── docs/
│   ├── admin-guide.md   # Detailed administrator manual
│   ├── user-guide.md    # Short manual for end users
│   └── agent.md         # Technical reference
├── templates/       # Jinja2 HTML templates
├── static/          # CSS and JavaScript
└── README.md
```

---

## License

MIT
