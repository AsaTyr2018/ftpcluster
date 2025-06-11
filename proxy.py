import io
from fastapi import HTTPException
from fastapi.responses import Response
from ftplib import FTP

from db import SessionLocal
from models import Permission, Server


def get_permission(db, username: str, srv_alias: str):
    return (
        db.query(Permission)
        .join(Server)
        .filter(Permission.user.has(username=username))
        .filter(Server.alias == srv_alias)
        .first()
    )


def proxy_ftp(username: str, srv_alias: str, path: str):
    db = SessionLocal()
    perm = get_permission(db, username, srv_alias)
    if not perm:
        db.close()
        raise HTTPException(status_code=403, detail="Kein Zugriff")
    srv = db.query(Server).filter_by(alias=srv_alias).first()
    db.close()

    ftp = FTP(srv.host)
    ftp.login(username, perm.user_pass)
    bio = io.BytesIO()
    ftp.retrbinary(f"RETR {path}", bio.write)
    ftp.quit()
    return Response(bio.getvalue(), media_type="application/octet-stream")
