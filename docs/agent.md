# FTPCluster Architecture and Agents

FTPCluster provides a central point of management for multiple FTP servers. Users authenticate once and are transparently proxied to their assigned servers.

---

## Components

### FastAPI master
The master server exposes both a web interface and a JSON API. Data is stored in an SQLite database using SQLAlchemy models `User`, `Server` and `Permission`.

### Remote agents
FTPCluster ships three small Python agents that run on each managed server:

1. **slave_agent.py** – posts telemetry (RAM, CPU, connected users and disk usage) to `/telemetry` every minute.
2. **datalink_agent.py** – listens on port `9000` and creates system users on request via `/create_user`.
3. **server_agent.py** – executed from the master over SSH to install Python, `vsftpd` and the two agents above.

The agents are installed automatically when you register a server through the web interface. Communication with the master is secured via generated API tokens and SSH keys.

### Proxy endpoint
The master hosts `/ftp/{username}/{server_alias}/{path}`. Access is granted only if the `Permission` table links the user and server. The proxy opens an FTP connection to the remote host and streams the requested file to the client.

---

## API Overview

* `POST /login` – authenticate a user
* `GET  /servers` – list registered servers (admin only)
* `POST /servers` – create a new server entry and return the setup script
* `POST /permissions` – assign a user to a server
* `POST /telemetry` – receive monitoring data from slaves
* `POST /api/register` – used by the slave setup script to send the generated SSH key and finalize registration

---

## Deployment Helpers

* `setup_master.sh` – install the master service and print the admin password
* `update_master.sh` – upgrade an existing deployment
* `generate_slave_bundle.py` – build a tarball for zero‑touch slave setup (see `docs/slave-workflow.md`)

---

## Directory Layout

```
ftpcluster/
├── main.py          # FastAPI application
├── db.py            # SQLite helpers
├── models.py        # ORM models
├── security.py      # Cookie signing and encryption
├── ftp_sync.py      # Interacts with remote servers
├── proxy.py         # FTP proxy implementation
├── agents/          # Remote agent scripts
├── scripts/         # Setup and maintenance helpers
└── templates/ and static/  # Web UI
```

This high level overview should help you navigate the code base and understand how the different agents interact with the master.
