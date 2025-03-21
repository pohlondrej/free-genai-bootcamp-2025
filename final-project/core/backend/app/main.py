from fastapi import FastAPI

app = FastAPI(title="DuoKani WaniLingo")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
