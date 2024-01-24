from typing import Callable
import re
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter
from fastapi.templating import Jinja2Templates

import redis.asyncio as redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware

from src.database.db import get_db
from src.utils import messages

from src.conf.config import config
from src.routes import comment_routes, auth_routes, photo_routes, user_routes

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_agent_ban_list = [r"bot-Yandex", r"Googlebot", r"Python-urllib"]


@app.middleware("http")
async def user_agent_ban_middleware(request: Request, call_next: Callable):
    try:
        user_agent = request.headers.get("user-agent")
        for ban_pattern in user_agent_ban_list:
            if re.search(ban_pattern, user_agent):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are banned")
        response = await call_next(request)
        return response
    except HTTPException as exc:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    except Exception as exc:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"})

BASE_DIR = Path(__file__).parent
directory = BASE_DIR.joinpath("src").joinpath("static")
app.mount("/static", StaticFiles(directory=directory), name="static")

app.include_router(auth_routes.router, prefix="/api")
app.include_router(user_routes.router, prefix="/api")
app.include_router(comment_routes.router, prefix='/api')
app.include_router(photo_routes.router, prefix='/api')


@app.on_event("startup")
async def startup():
    try:
        r = await redis.Redis(
            host=config.REDIS_DOMAIN,
            port=config.REDIS_PORT,
            db=0,
            password=config.REDIS_PASSWORD
        )
        await FastAPILimiter.init(r)
    except Exception as e:
        print("Error during startup:", e)

templates = Jinja2Templates(directory=BASE_DIR / 'src' / 'templates')


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(name='index.html',
                                      context={"request": request, "message": "PhotoShare Application"})


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        async with db.begin():
            result = await db.execute(text(messages.SELECT_1))
        result = result.fetchone()

        if result is None:
            raise HTTPException(status_code=500, detail=messages.DATABASE_IS_NOT_CONFIGURED_CORRECTLY)
        return {messages.MESSAGE: messages.WELCOME_TO_FASTAPI}
    except Exception as e:
        print("Error in healthchecker:", e)
        raise HTTPException(status_code=500, detail=messages.ERROR_CONNECTING_TO_DB)
