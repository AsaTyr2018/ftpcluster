# Admin Guide

This document describes how to install the FTPCluster instance and how administrators can add new FTP servers.

## Installing the server

1. **Prerequisites**
   - Python 3.11 or newer
   - Access to at least one FTP or SFTP server

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   ```bash
   export SECRET_KEY=<zufaelliger_wert>
   export FERNET_KEY=$(python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')
   ```

4. **Create the database and start the application**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8080
   ```
   On first start the SQLite database `ftpcluster.db` is created automatically.

## Adding new servers

1. Log in with an admin account in the web interface.
2. Open the **Server management** page (`/servers`).
3. Enter alias, host name and the admin credentials of the target server.
4. After saving, the server appears in the list and can be assigned to users.

Servers can also be created via the API:
```bash
curl -X POST -F alias=<alias> -F host=<host> -F admin_user=<user> -F admin_pass=<pass> http://<server>:8080/servers
```
