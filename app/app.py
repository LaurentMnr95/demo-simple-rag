from fastapi import FastAPI

from app.rest import router


app = FastAPI()
app.include_router(router)
