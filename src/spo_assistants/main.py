from fastapi import FastAPI

from spo_assistants.assistants.router import router as site_assistant_router
from spo_assistants.health import router as health_router

app = FastAPI(title="Site Assistant API")
app.include_router(health_router)
app.include_router(site_assistant_router)
