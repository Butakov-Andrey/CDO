import sys

from config import settings
from dependencies import logging
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from feedback.router import router as feedback_router
from loguru import logger
from products.router import router as product_router

app = FastAPI(
    title="Marketplace API",
    version="0.0.1",
    contact={
        "name": "Andrey Butakov",
        "email": "6669.butakov@gmail.com",
    },
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url=None,
)


# logger
logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format=settings.LOGURU_FORMAT,
)


# middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(product_router, dependencies=[Depends(logging)])
app.include_router(feedback_router, dependencies=[Depends(logging)])
