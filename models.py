from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    permissions = relationship("Permission", back_populates="user")

class Server(Base):
    __tablename__ = "servers"
    id = Column(Integer, primary_key=True, index=True)
    alias = Column(String, unique=True, index=True, nullable=False)
    host = Column(String, nullable=False)
    admin_user = Column(String, nullable=False)
    admin_pass = Column(String, nullable=False)
    ssh_key = Column(String, nullable=True)
    slave_id = Column(String, unique=True, nullable=True)
    api_key = Column(String, nullable=True)
    public_key = Column(String, nullable=True)
    status = Column(String, nullable=True)
    memory_usage = Column(Integer, default=0)
    cpu_usage = Column(Integer, default=0)
    connected_users = Column(Integer, default=0)
    root_usage = Column(Integer, default=0)

    permissions = relationship("Permission", back_populates="server")

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    server_id = Column(Integer, ForeignKey("servers.id"))
    user_pass = Column(String, nullable=False)

    user = relationship("User", back_populates="permissions")
    server = relationship("Server", back_populates="permissions")
