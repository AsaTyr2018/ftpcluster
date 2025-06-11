import os
import subprocess
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class UserData(BaseModel):
    username: str
    password: str

@app.post("/create_user")
async def create_user(data: UserData):
    """Create a system user for the FTP service."""
    try:
        subprocess.run(["useradd", "-m", data.username], check=False)
        subprocess.run(["bash", "-c", f"echo '{data.username}:{data.password}' | chpasswd"], check=False)
    except Exception:
        pass
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("AGENT_PORT", "9000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
