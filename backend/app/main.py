from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from contextlib import asynccontextmanager

from app.config import settings
from app.middleware import ExceptionHandlerMiddleware
from app.database import init_db

@asynccontextmanager
async def app_lifespan(application: FastAPI):
    print("Init Application")
    init_db()
    yield
    print("Finish Init")
    

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url="/openapi.json",
    docs_url="/docs"
)

# Sets all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handling
app.add_middleware(ExceptionHandlerMiddleware)

# Guards against HTTP Host Header attacks
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
