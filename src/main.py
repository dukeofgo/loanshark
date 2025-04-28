from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.client import router as client_router
from src.loan import router as loan_router


app = FastAPI(
    prefix="/api"
)

app.include_router(loan_router.router)
app.include_router(client_router.router)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


