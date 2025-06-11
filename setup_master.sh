#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
  echo "Run this script as root" >&2
  exit 1
fi

DEST_DIR=/opt/ftpcluster
SRC_DIR=$(cd "$(dirname "$0")" && pwd)

echo "Installing FTPCluster to $DEST_DIR"

mkdir -p "$DEST_DIR"
rsync -a --exclude='.git' "$SRC_DIR/" "$DEST_DIR/"

cd "$DEST_DIR"

# Create virtual environment and install dependencies
if [ ! -d venv ]; then
  python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip >/dev/null
pip install -r requirements.txt >/dev/null

# Generate environment variables
SECRET_KEY=$(openssl rand -hex 16)
FERNET_KEY=$(python3 - <<'PY'
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
PY
)
HOST_IP=$(hostname -I | awk '{print $1}')
MASTER_URL="http://${HOST_IP}:8080"

cat > .env <<ENV
SECRET_KEY=${SECRET_KEY}
FERNET_KEY=${FERNET_KEY}
MASTER_URL=${MASTER_URL}
ENV
chmod 600 .env

# Initialize database and create admin account
ADMIN_PASS=$(python3 - <<'PY'
import secrets
from sqlalchemy.orm import Session
from db import Base, engine, SessionLocal
from models import User
from passlib.hash import bcrypt

Base.metadata.create_all(bind=engine)
session = SessionLocal()
admin = session.query(User).filter_by(username="admin").first()
if admin:
    print("EXISTS")
else:
    pwd = secrets.token_urlsafe(8)
    user = User(username="admin", password_hash=bcrypt.hash(pwd))
    session.add(user)
    session.commit()
    print(pwd)
PY
)

if [[ $ADMIN_PASS == "EXISTS" ]]; then
  echo "Admin user already exists"
  ADMIN_PASS="(unchanged)"
fi

# Create systemd service
cat >/etc/systemd/system/ftpcluster.service <<SERVICE
[Unit]
Description=FTPCluster Master Server
After=network.target

[Service]
Type=simple
WorkingDirectory=${DEST_DIR}
EnvironmentFile=${DEST_DIR}/.env
ExecStart=${DEST_DIR}/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8080
Restart=on-failure

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable ftpcluster.service >/dev/null
systemctl restart ftpcluster.service

chmod -R 755 "$DEST_DIR"

cat <<MSG
#################################
Master initialized successfully!
UI: http://${HOST_IP}:8080
Admin Login: admin / ${ADMIN_PASS}
Enjoy your Freedom dear Admin!
#################################
MSG

