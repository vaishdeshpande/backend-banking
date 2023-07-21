#app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, APIRouter,Depends
from .config.database import engine
from .routers import accounts,transactions
from .models import schemas
from fastapi.responses import HTMLResponse
import os

# Create the logs directory if it does not exist
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Create the log file if it does not exist
log_file = os.path.join(log_dir, "app.log")
if not os.path.exists(log_file):
    with open(log_file, "w"):
        pass


schemas.Base.metadata.create_all(bind=engine)
app = FastAPI()

router = APIRouter()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(accounts.router)
app.include_router(transactions.router)


@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}

@app.get("/logs", response_class=HTMLResponse)
def view_logs():
    with open("logs/app.log", "r") as file:
        logs = file.read()
    return f"<pre>{logs}</pre>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)