from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Internship API is running successfully!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}