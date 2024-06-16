from fastapi import FastAPI, HTTPException
from typing import List
import uvicorn
import endpoints

HOST = "127.0.0.1"
PORT = 5000

app = FastAPI(title="DIC_EXC3")

@app.get("/")
def get_health_check():
    return {"health_check": "ok"}

app.include_router(endpoints.router, prefix="/exc3", tags=["EXC3"])

if __name__ == "__main__":
    uvicorn.run("main:app", host = HOST, port= PORT, reload=True)