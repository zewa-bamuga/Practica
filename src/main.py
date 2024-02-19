from fastapi import FastAPI
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..')))  # решение проблемs, при которой после распределения файлов по папкам не работыли импорты

from src.auth.router import router as router_protect
from src.questionnaire.router import router as router_survey
from src.walk.router import router as router_walk
from src.calendar.router import router as router_calendar
from src.profile.router import router as router_profile

app = FastAPI(
    title="Путеводитель по необычным местам"
)

app.include_router(router_protect)
app.include_router(router_survey)
app.include_router(router_profile)
app.include_router(router_walk)
app.include_router(router_calendar)
