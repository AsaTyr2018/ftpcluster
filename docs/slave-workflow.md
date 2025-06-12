# Zero-Touch Slave Setup

This workflow installs all required agents on a new server without manual configuration.

1. **Generate the bundle** on the master:
   ```bash
   python3 scripts/generate_slave_bundle.py myserver 10.0.0.42 --ssh-user ubuntu
   ```
   The command stores the server in the database and creates `myserver_bundle.tar.gz`.

2. **Copy and extract** the bundle on the target machine.

3. **Run `ftpcluster-setup.sh`** as root:
   ```bash
   sudo ./ftpcluster-setup.sh
   ```
   The script creates the `ftpcluster-admin` user, installs Python and `vsftpd`, launches the `slave_agent.py` and `datalink_agent.py` services and registers the machine at the master via `/api/register`.

When the registration succeeds the server status changes to `ready` and telemetry starts flowing to the dashboard.
