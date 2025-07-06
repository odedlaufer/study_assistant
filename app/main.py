from fastapi import FastAPI

from .routes import router

app = FastAPI(title="Study Assistant")
app.include_router(router)
