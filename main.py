from fastapi import FastAPI
from app.routers.users import router as users_router

app = FastAPI()

app.include_router(users_router)


@app.get("/")
def home():
    return {"message": "Internship API is running successfully!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}