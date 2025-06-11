#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
  echo "Run this script as root" >&2
  exit 1
fi

DEST_DIR=/opt/ftpcluster
REPO_URL="https://github.com/AsaTyr2018/ftpcluster.git"
BACKUP_DB=/tmp/ftpcluster_backup.db

echo "Updating FTPCluster in $DEST_DIR"

# Stop running service if present
if systemctl is-active --quiet ftpcluster.service; then
  systemctl stop ftpcluster.service
fi

if [ -d "$DEST_DIR/.git" ]; then
  echo "Pulling latest changes"
  cd "$DEST_DIR"
  git fetch --all
  git reset --hard origin/main
else
  echo "Cloning repository"
  rm -rf "$DEST_DIR"
  git clone "$REPO_URL" "$DEST_DIR"
  cd "$DEST_DIR"
fi

# Prepare Python environment
if [ ! -d venv ]; then
  python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip >/dev/null
pip install -r requirements.txt >/dev/null

# Backup and migrate database if it exists and is not empty
DB_FILE="$DEST_DIR/ftpcluster.db"
if [ -s "$DB_FILE" ]; then
  echo "Backing up database to $BACKUP_DB"
  cp "$DB_FILE" "$BACKUP_DB"
  rm "$DB_FILE"

  python3 - <<PY
from db import Base, engine
Base.metadata.create_all(bind=engine)
PY

  python3 - <<'PY'
import sqlite3, os
backup = os.environ['BACKUP_DB']
newdb = os.path.join(os.environ['DEST_DIR'], 'ftpcluster.db')
if not os.path.exists(backup):
    raise SystemExit('Backup database missing')
src = sqlite3.connect(backup)
src.row_factory = sqlite3.Row
dst = sqlite3.connect(newdb)
try:
    dst.execute('BEGIN')
    tables = [r[0] for r in dst.execute("SELECT name FROM sqlite_master WHERE type='table'") if not r[0].startswith('sqlite_')]
    for name in tables:
        rows = src.execute(f'SELECT * FROM {name}').fetchall()
        if not rows:
            continue
        cols = rows[0].keys()
        placeholders = ','.join('?' for _ in cols)
        colnames = ','.join(cols)
        dst.executemany(
            f'INSERT INTO {name} ({colnames}) VALUES ({placeholders})',
            [tuple(row[c] for c in cols) for row in rows]
        )
    dst.commit()
finally:
    src.close()
    dst.close()
os.remove(backup)
PY
else
  python3 - <<'PY'
from db import Base, engine
Base.metadata.create_all(bind=engine)
PY
fi

systemctl daemon-reload
systemctl start ftpcluster.service

echo "Update complete"

