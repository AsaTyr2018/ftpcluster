from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from passlib.hash import bcrypt

from security import encrypt_value, decrypt_value, sign_username, verify_username

from db import Base, engine, get_db
from sqlalchemy.orm import Session
from models import User, Server, Permission
from proxy import proxy_ftp

app = FastAPI()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user or not bcrypt.verify(password, user.password_hash):
        return RedirectResponse("/", status_code=302)
    response = RedirectResponse("/dashboard", status_code=302)
    signed = sign_username(username)
    response.set_cookie(key="session", value=signed, httponly=True)
    return response


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    username = verify_username(request.cookies.get("session"))
    if not username:
        return RedirectResponse("/", status_code=302)
    user = db.query(User).filter_by(username=username).first()
    permissions = db.query(Permission).filter_by(user_id=user.id).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "permissions": permissions, "user": user})


@app.get("/ftp/{username}/{srv_alias}/{path:path}")
async def ftp_proxy(request: Request, username: str, srv_alias: str, path: str):
    session_user = verify_username(request.cookies.get("session"))
    if session_user != username:
        return RedirectResponse("/", status_code=302)
    return proxy_ftp(username, srv_alias, path)


@app.post("/users")
async def create_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    hashed = bcrypt.hash(password)
    user = User(username=username, password_hash=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}


@app.post("/servers")
async def create_server(alias: str = Form(...), host: str = Form(...), admin_user: str = Form(...), admin_pass: str = Form(...), db: Session = Depends(get_db)):
    enc_pass = encrypt_value(admin_pass)
    srv = Server(alias=alias, host=host, admin_user=admin_user, admin_pass=enc_pass)
    db.add(srv)
    db.commit()
    db.refresh(srv)
    return {"id": srv.id, "alias": srv.alias}


@app.post("/permissions")
async def create_permission(user_id: int = Form(...), server_id: int = Form(...), user_pass: str = Form(...), db: Session = Depends(get_db)):
    enc_pass = encrypt_value(user_pass)
    perm = Permission(user_id=user_id, server_id=server_id, user_pass=enc_pass)
    db.add(perm)
    db.commit()
    db.refresh(perm)
    return {"id": perm.id}
