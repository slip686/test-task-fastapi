from fastapi import FastAPI
import uvicorn

from database import init_models
from routers.vehicle import vehicle_router

app = FastAPI(title="TEST-TASK")
app.include_router(vehicle_router, tags=["vehicles"])


@app.on_event("startup")
async def on_startup():
    await init_models()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
