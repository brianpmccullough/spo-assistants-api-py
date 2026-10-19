from fastapi import FastAPI

app = FastAPI(title="Site Assistant API")

@app.get("/health")
def health() -> dict[str, str]:
    return { "status": "ok....." }
