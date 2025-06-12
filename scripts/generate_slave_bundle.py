import argparse
import io
import json
import os
import tarfile
import uuid
import secrets

import paramiko

from db import SessionLocal
from models import Server
from security import encrypt_value

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_SETUP = os.path.join(SCRIPT_DIR, "slave_setup.sh")


def generate_bundle(alias: str, host: str, ssh_user: str, master_url: str) -> str:
    session = SessionLocal()
    slave_id = uuid.uuid4().hex
    api_key = secrets.token_hex(16)

    key = paramiko.RSAKey.generate(2048)
    priv_io = io.StringIO()
    key.write_private_key(priv_io)
    priv_key = priv_io.getvalue()
    pub_key = f"{key.get_name()} {key.get_base64()}"

    srv = Server(
        alias=alias,
        host=host,
        admin_user=ssh_user,
        admin_pass="",
        ssh_key=encrypt_value(priv_key),
        slave_id=slave_id,
        api_key=api_key,
        public_key=pub_key,
        status="pending",
    )
    session.add(srv)
    session.commit()

    config = {"slave_id": slave_id, "api_key": api_key, "master_url": master_url}
    bundle_dir = os.path.join(SCRIPT_DIR, "bundle_tmp")
    os.makedirs(bundle_dir, exist_ok=True)
    config_path = os.path.join(bundle_dir, "config.json")
    with open(config_path, "w") as f:
        json.dump(config, f)

    pub_path = os.path.join(bundle_dir, "pubkey_master.pub")
    with open(pub_path, "w") as f:
        f.write(pub_key)

    setup_dest = os.path.join(bundle_dir, "ftpcluster-setup.sh")
    with open(TEMPLATE_SETUP, "r") as src, open(setup_dest, "w") as dst:
        dst.write(src.read())
    os.chmod(setup_dest, 0o755)

    bundle_path = os.path.join(SCRIPT_DIR, f"{alias}_bundle.tar.gz")
    with tarfile.open(bundle_path, "w:gz") as tar:
        tar.add(config_path, arcname="config.json")
        tar.add(pub_path, arcname="pubkey_master.pub")
        tar.add(setup_dest, arcname="ftpcluster-setup.sh")

    return bundle_path


def main():
    parser = argparse.ArgumentParser(description="Generate slave setup bundle")
    parser.add_argument("alias")
    parser.add_argument("host")
    parser.add_argument("--ssh-user", default="ubuntu")
    parser.add_argument("--master-url", default=os.environ.get("MASTER_URL", "http://localhost:8080"))
    args = parser.parse_args()

    bundle = generate_bundle(args.alias, args.host, args.ssh_user, args.master_url)
    print(f"Bundle written to {bundle}")


if __name__ == "__main__":
    main()
