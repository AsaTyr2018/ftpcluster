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

## Preparation

When adding a new server, the master provides a shell script that must be run on
the target system as `root`. This script

1. creates the specified admin user and locks its password,
2. adds the user to `/etc/sudoers.d/` with `NOPASSWD`,
3. generates an SSH key pair and sends the private key to the master.

The master stores the key for future communication and then automatically installs
the required packages and agents.

Example workflow:

```bash
curl -F alias=myserver -F host=10.0.0.5 http://MASTER/servers > setup.sh
sudo bash setup.sh
```

After running the script, the server will appear in the list.

---

## 2. Registering a Server

1. Log in as admin and open **Servers**.
2. Choose **Add** and provide host and alias.
3. Save the generated script on the target server and run it as `root`.
4. The master then installs the required packages and starts the agents (datalink port 9000).
5. The new server will appear in the list and show its last reported memory usage.

---

## 3. Managing Users

- Use the **Users** page to create accounts and assign servers.
- Users only see the servers you select.

---

## 4. Monitoring

The **Servers** page displays telemetry from agents. If a server stops reporting, check connectivity or reinstall the agent from the same page.

Enjoy your streamlined FTP management!
