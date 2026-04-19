"""FastAPI application entry point"""
from fastapi import FastAPI
from api import router

app = FastAPI(
    title="/Tmp/Nonexistent.Spec",
    description="",
    version="0.1.0"
)

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
