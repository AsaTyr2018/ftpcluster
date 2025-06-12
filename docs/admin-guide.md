# FTPCluster Administration Guide

Welcome to FTPCluster. This document explains how to install the master server, register slaves and manage users.

---

## 1. Installing the Master

### Recommended: setup script
Run the provided script as **root** to deploy FTPCluster and create a systemd service:

```bash
curl -s https://raw.githubusercontent.com/AsaTyr2018/ftpcluster/main/scripts/setup_master.sh | sudo bash
```

The script clones the repository to `/opt/ftpcluster`, creates a Python virtual environment and prints the generated admin password. After completion the service listens on port `8080`.

### Manual installation
If you prefer a manual setup, install the requirements and define the environment variables `SECRET_KEY`, `FERNET_KEY` and `MASTER_URL`:

```bash
pip install -r requirements.txt
export SECRET_KEY=$(openssl rand -hex 16)
export FERNET_KEY=$(python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')
export MASTER_URL=http://<this_host>:8080
uvicorn main:app --host 0.0.0.0 --port 8080
```

---

## 2. Upgrading an Installation

To update a running instance use `scripts/update_master.sh`. The script pulls the latest code, migrates the database and restarts the service.

```bash
sudo scripts/update_master.sh
```

---

## 3. Registering Servers

1. Log in as **admin** and open **Servers**.
2. Enter the alias and host name to create a new entry.
3. Save the generated shell script on the target server and run it as `root`.
4. The script installs Python, `vsftpd` and both agents. Telemetry appears once the agents start.

Alternatively you can create a zero-touch bundle using `generate_slave_bundle.py` and run `ftpcluster-setup.sh` on the slave as described in `docs/slave-workflow.md`.

---

## 4. Managing Users

Use the **Users** page to create accounts. When assigning a server you must also provide the FTP password that will be deployed via the datalink agent.

---

## 5. Monitoring

The **Servers** page lists RAM, CPU, user count and disk usage reported by each slave. If a server stops reporting you can reinstall the agents from the same page.

Enjoy your streamlined FTP management!
