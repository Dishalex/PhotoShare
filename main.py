from fastapi import Depends, FastAPI, HTTPException

from sqlalchemy import text
from sqlalchemy.ext.asyncio  import AsyncSession
from fastapi.middleware.cors import CORSMiddleware


from src.database.db import get_db
from src.routes import photo_routes
from src.utils import messages
from src.routes import comment_routes, auth_routes, photo_routes

app = FastAPI()

origins = [
    "http://localhost:3000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(auth_routes.router, prefix='/api')
app.include_router(comment_routes.router, prefix='/api')
app.include_router(photo_routes.router, prefix='/api')

@app.get("/")
def index():
    return {"message": "PhotoShare Application"}


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        # Make request
        result = await db.execute(text(messages.SELECT_1))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail=messages.DATABASE_IS_NOT_CONFIGURED_CORRECTLY)
        return {messages.MESSAGE: messages.WELCOME_TO_FASTAPI}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=messages.ERROR_CONNECTING_TO_DB)
