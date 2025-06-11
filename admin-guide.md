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

## 2. Registering a Server

1. Log in as admin and open **Servers**.
2. Choose **Add** and provide host, alias and credentials.
3. On save the master installs Python and an FTP server on the target, copies both agents and starts them.
4. The datalink agent listens on port `9000` so new users can be created remotely.
5. The new server appears in the list showing its last reported memory usage.

---

## 3. Managing Users

- Use the **Users** page to create accounts and assign servers.
- Users only see the servers you select.

---

## 4. Monitoring

The **Servers** page displays telemetry from agents. If a server stops reporting, check connectivity or reinstall the agent from the same page.

Enjoy your streamlined FTP management!
