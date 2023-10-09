# app/main.py

from fastapi import FastAPI
from app.api import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to your FastAPI application"}

# Including the API router
app.include_router(router)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend application's URL for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)