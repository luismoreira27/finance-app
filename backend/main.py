from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.finance_db import Base_finance, engine_finance
from backend.auth_db import Base_auth, engine_auth
from backend.routers import transactions, auth

Base_auth.metadata.create_all(bind = engine_auth)
Base_finance.metadata.create_all(bind = engine_finance)

app = FastAPI()

origins = ["http://localhost:8501"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Finance API running"}