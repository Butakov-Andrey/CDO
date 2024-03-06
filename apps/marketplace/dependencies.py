from fastapi import Request
from loguru import logger
from postgres import SessionLocal


# database dependency
async def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def logging(request: Request):
    logger.debug("\n" + "~" * 40)
    logger.debug("REQUEST:")
    logger.debug(f"{request.method} {request.url}")
    logger.debug("Params:")
    for name, value in request.path_params.items():
        logger.debug(f"\t{name}: {value}")
    logger.debug("Headers:")
    for name, value in request.headers.items():
        logger.debug(f"\t{name}: {value}")
