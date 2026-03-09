from fastapi import FastAPI
from app.api import router
from app.core.db import init_db
import uvicorn

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app=app)