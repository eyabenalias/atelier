"""Notification microservice - entry point.

Run:  uvicorn app.main:app --reload --port 8084
  or: python -m app.main
"""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
import py_eureka_client.eureka_client as eureka_client

from app.routers import notification

PORT = int(os.getenv("PORT", "8084"))
EUREKA_SERVER = os.getenv("EUREKA_SERVER", "http://localhost:8761/eureka")
INSTANCE_HOST = os.getenv("INSTANCE_HOST", "localhost")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: register with Eureka with health and info URLs
    await eureka_client.init_async(
        eureka_server=EUREKA_SERVER,
        app_name="NOTIFICATION",
        instance_port=PORT,
        instance_host=INSTANCE_HOST,
        health_check_url=f"http://{INSTANCE_HOST}:{PORT}/health",
        status_page_url=f"http://{INSTANCE_HOST}:{PORT}/info",
    )
    yield
    # Shutdown: stop Eureka client
    await eureka_client.stop_async()


app = FastAPI(
    title="Notification Microservice API",
    version="1.0.0",
    description=(
        "Notification microservice (Python / FastAPI, no database). "
        "Only the hello endpoint is implemented; the notification logic is to be developed by students."
    ),
    contact={"name": "Badia Abouhdid"},
    servers=[{"url": f"http://localhost:{PORT}", "description": "Local"}],
    docs_url="/swagger-ui",       # Swagger UI
    openapi_url="/v3/api-docs",   # OpenAPI JSON
    redoc_url="/redoc",           # alternative documentation
    lifespan=lifespan,
)


@app.get("/health", tags=["Actuator"])
def health():
    return {"status": "UP"}


@app.get("/info", tags=["Actuator"])
def info():
    return {
        "app": {
            "name": "notification",
            "version": "1.0.0",
            "description": "Notification microservice (Python / FastAPI)",
            "team": "Equipe AWD",
        }
    }


app.include_router(notification.router)

# TODO (students): if you add other routers, include them here.


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=True)
