import os

import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Секретный ключ для проверки JWT
SECRET_KEY = "12345678"

ALGORITHM = "HS256"

security = HTTPBearer()


@app.get("/")
async def home(
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        # Проверяем подпись и декодируем JWT
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Получаем имя пользователя
        user = payload.get("user")

        if not isinstance(user, str) or not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid user in token"
            )

    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "user": user
        }
    )


@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={
            "request": request,
            "title": "О нас"
        }
    )
