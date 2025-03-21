from fastapi import FastAPI

app = FastAPI(
    title="DuoKani WaniLingo",
    docs_url="/docs",  # This will be /api/docs
    openapi_url="/openapi.json",  # This will be /api/openapi.json
    root_path="/api"  # This tells FastAPI all routes are under /api
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
