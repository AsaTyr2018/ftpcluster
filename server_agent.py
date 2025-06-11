import os
import paramiko
from models import Server
from security import decrypt_value

AGENT_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'slave_agent.py')
LINK_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'datalink_agent.py')
MASTER_URL = os.environ.get('MASTER_URL', 'http://localhost:8080')


def install_agent(server: Server):
    """Install and start the slave agent on the given server via SSH."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
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
