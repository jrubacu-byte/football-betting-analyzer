from fastapi import FastAPI
from backend.routes.analysis_routes import router

app = FastAPI(title="Football Betting Analyzer")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
