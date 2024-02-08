from fastapi import FastAPI

# Импортируем настройки проекта из config.py.
from app.core.config import settings

app = FastAPI(title=settings.app_title)
