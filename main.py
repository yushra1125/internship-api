from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.routers.user import router as users_router
from app.routers.tasks import router as tasks_router
from app.routers.auth import router as auth_router
app = FastAPI()

app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(auth_router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation failed",
            "errors": jsonable_encoder(exc.errors())
        }
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": "Resource not found"
        }
    )


@app.get("/")
def home():
    return {"message": "Internship API is running successfully!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}