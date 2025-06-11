from ftplib import FTP
from typing import Iterable

from models import Server


def create_user_on_servers(username: str, password: str, server_list: Iterable[Server]):
    for srv in server_list:
        ftp = FTP(srv.host)
        ftp.login(srv.admin_user, srv.admin_pass)
        try:
            ftp.mkd(username)
        except Exception:
            pass
        ftp.quit()
