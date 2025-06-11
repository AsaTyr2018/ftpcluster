import os
import paramiko
from models import Server
from security import decrypt_value

AGENT_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'slave_agent.py')
MASTER_URL = os.environ.get('MASTER_URL', 'http://localhost:8080')


def install_agent(server: Server):
    """Install and start the slave agent on the given server via SSH."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server.host, username=server.admin_user, password=decrypt_value(server.admin_pass))
    sftp = ssh.open_sftp()
    remote_path = '/tmp/slave_agent.py'
    with open(AGENT_SCRIPT_PATH, 'r') as f:
        script_data = f.read()
    with sftp.file(remote_path, 'w') as remote_file:
        remote_file.write(script_data)
    sftp.close()
    cmd = f"MASTER_URL={MASTER_URL} SERVER_ALIAS={server.alias} nohup python3 {remote_path} >/dev/null 2>&1 &"
    ssh.exec_command(cmd)
    ssh.close()
