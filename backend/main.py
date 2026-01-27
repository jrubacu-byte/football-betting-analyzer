"""FastAPI Backend - Aplicación de Análisis de Apuestas Deportivas"""
from fastapi import FastAPI

app = FastAPI(
    title="Betting Analysis API",
    description="API para análisis de apuestas deportivas de fútbol",
    version="0.1.0"
)


@app.get("/ping")
async def ping():
    """Health check endpoint"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
