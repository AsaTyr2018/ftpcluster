#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
  echo "Run as root" >&2
  exit 1
fi

CONFIG_DIR=/etc/ftpcluster
USER=ftpcluster-admin

mkdir -p "$CONFIG_DIR"
cp "$(dirname "$0")/config.json" "$CONFIG_DIR/credentials.json"

id $USER >/dev/null 2>&1 || useradd -m -s /bin/bash $USER
install -m 700 -o $USER -g $USER -d /home/$USER/.ssh
cat "$(dirname "$0")/pubkey_master.pub" >> /home/$USER/.ssh/authorized_keys
chown $USER:$USER /home/$USER/.ssh/authorized_keys
chmod 600 /home/$USER/.ssh/authorized_keys

echo "$USER ALL=(ALL) NOPASSWD:ALL" >/etc/sudoers.d/ftpcluster-$USER
chmod 440 /etc/sudoers.d/ftpcluster-$USER

python3 - <<'PY'
import json, socket, requests, os
cfg=json.load(open('/etc/ftpcluster/credentials.json'))
hostname=socket.gethostname()
try:
    ip=socket.gethostbyname(hostname)
except Exception:
    ip='0.0.0.0'
key=open('/home/ftpcluster-admin/.ssh/authorized_keys').read().strip()
requests.post(
    cfg['master_url']+'/api/register',
    json={'slave_id': cfg['slave_id'], 'pubkey': key, 'hostname': hostname, 'ip': ip},
    headers={'Authorization': 'Bearer '+cfg['api_key']},
    timeout=5,
)
PY
