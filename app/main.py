"""
app/main.py
This is the entry point of the application, where the FastAPI app is set up.
It includes routes for creating, updating, and deleting accounts, as well as for checking account details.
 """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, APIRouter,Depends
from .config.database import engine
from .routers import accounts,transactions
from .models import schemas
from fastapi.responses import HTMLResponse


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


@app.get("/ping")
def root():
    return {"message": "Hello Ping!"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)