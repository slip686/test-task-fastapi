from fastapi import FastAPI
import uvicorn

from routers.vehicle import vehicle_router


app = FastAPI(title="TEST-TASK")
app.include_router(vehicle_router, tags=["vehicles"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

