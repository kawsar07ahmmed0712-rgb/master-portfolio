from fastapi import FastAPI

app = FastAPI(title = "Master Portfolio API" , version="0.1.0")


@app.get("/health")
def health_check():
    return {"status":"ok"}