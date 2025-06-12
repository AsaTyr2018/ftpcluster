# Zero-Touch Slave Setup

This document describes the workflow for adding a new slave server. A dedicated script
packages all required files and generates credentials on the master.

1. **Generate a bundle** on the master:

```bash
python3 scripts/generate_slave_bundle.py myserver 10.0.0.42 --ssh-user ubuntu
```

The script creates a `myserver_bundle.tar.gz` file containing:
- `ftpcluster-setup.sh`
- `config.json` with `slave_id` and `api_key`
- `pubkey_master.pub` (SSH key)

It also stores the server in the database with pending status.

2. **Copy the bundle** to the target machine and extract it.

3. **Run the setup script** as root on the slave:

```bash
sudo ./ftpcluster-setup.sh
```

The script creates the `ftpcluster-admin` user, installs the master key and
registers the machine with the master via `/api/register`.

Once the registration succeeds the server status becomes `ready` and the master
can connect using SSH keys.
