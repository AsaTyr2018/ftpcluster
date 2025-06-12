import os
import io
import paramiko
from models import Server
from security import decrypt_value

AGENT_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'slave_agent.py')
LINK_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'datalink_agent.py')
MASTER_URL = os.environ.get('MASTER_URL', 'http://localhost:8080')


def generate_setup_script(server: Server) -> str:
    """Return a shell script for preparing the server."""
    return f"""#!/bin/bash
set -e
ADMIN_USER={server.admin_user}
MASTER_URL={MASTER_URL}
ALIAS={server.alias}

if [ \"$EUID\" -ne 0 ]; then
  echo 'Run as root'
  exit 1
fi

id $ADMIN_USER >/dev/null 2>&1 || useradd -m -s /bin/bash $ADMIN_USER
passwd -l $ADMIN_USER

SUDO_FILE=/etc/sudoers.d/ftpcluster-$ADMIN_USER
echo "$ADMIN_USER ALL=(ALL) NOPASSWD:ALL" > $SUDO_FILE
chmod 440 $SUDO_FILE

su - $ADMIN_USER -c 'ssh-keygen -t rsa -b 2048 -N "" -f ~/.ssh/id_rsa'
cat /home/$ADMIN_USER/.ssh/id_rsa.pub >> /home/$ADMIN_USER/.ssh/authorized_keys
chown $ADMIN_USER:$ADMIN_USER /home/$ADMIN_USER/.ssh/authorized_keys
chmod 600 /home/$ADMIN_USER/.ssh/authorized_keys

curl -F alias=$ALIAS -F key=@/home/$ADMIN_USER/.ssh/id_rsa $MASTER_URL/register_key
"""


def install_agent(server: Server, key: str | None = None):
    """Install and start the slave agent on the given server via SSH."""
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.RejectPolicy())

    if key is None and server.ssh_key:
        key = decrypt_value(server.ssh_key)

    if key:
        pkey = paramiko.RSAKey.from_private_key(io.StringIO(key))
        ssh.connect(server.host, username=server.admin_user, pkey=pkey)
    else:
        ssh.connect(server.host, username=server.admin_user, password=decrypt_value(server.admin_pass))
    sftp = ssh.open_sftp()
    remote_agent = '/tmp/slave_agent.py'
    remote_link = '/tmp/datalink_agent.py'

    with open(AGENT_SCRIPT_PATH, 'r') as f:
        sftp.file(remote_agent, 'w').write(f.read())

    with open(LINK_SCRIPT_PATH, 'r') as f:
        sftp.file(remote_link, 'w').write(f.read())

    sftp.close()

    install_cmds = [
        'sudo apt-get update -y',
        'sudo apt-get install -y python3 python3-pip vsftpd',
        'pip3 install fastapi uvicorn requests psutil',
    ]
    for c in install_cmds:
        ssh.exec_command(c)

    cmd_agent = f"MASTER_URL={MASTER_URL} SERVER_ALIAS={server.alias} nohup python3 {remote_agent} >/dev/null 2>&1 &"
    cmd_link = f"nohup python3 {remote_link} >/dev/null 2>&1 &"
    ssh.exec_command(cmd_agent)
    ssh.exec_command(cmd_link)
    ssh.close()
