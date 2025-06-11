from ftplib import FTP
from typing import Iterable
import requests

from models import Server
from security import decrypt_value


def create_user_on_servers(username: str, password: str, server_list: Iterable[Server]):
    for srv in server_list:
        ftp = FTP(srv.host)
        admin_pass = decrypt_value(srv.admin_pass)
        ftp.login(srv.admin_user, admin_pass)
        try:
            ftp.mkd(username)
        except Exception:
            pass
        ftp.quit()


def create_user_via_link(username: str, password: str, server: Server):
    """Notify the datalink agent on a server to create a user."""
    try:
        requests.post(
            f"http://{server.host}:9000/create_user",
            json={"username": username, "password": password},
            timeout=5,
        )
    except Exception:
        pass
