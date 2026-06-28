from fastapi import FastAPI
from app.api.dashboard import router as dashboard_router
from app.api.logs import router as logs_router
from app.api.anomaly import router as anomaly_router

app = FastAPI(
    title="LogSentinel API",
    version="1.0.0",
    description="Backend API for LogSentinel Web Application"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to LogSentinel API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "backend": "running"
    }


app.include_router(dashboard_router)
app.include_router(logs_router)
app.include_router(anomaly_router)