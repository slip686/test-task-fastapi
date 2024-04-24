from fastapi import FastAPI
import uvicorn

from database import init_models
from routers.vehicle import vehicle_router

app = FastAPI(title="TEST-TASK")
app.include_router(vehicle_router, tags=["vehicles"])


@app.on_event("startup")
async def on_startup():
    """This code defines an event handler that runs the on_startup function when the FastAPI application starts up.
    The function on_startup asynchronously creates the database tables by calling the init_models function."""
    await init_models()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
