from fastapi import FastAPI
import uvicorn
from Backend.api.mongodb import mongodb_router

app = FastAPI(title="FastAPI + MongoDB Example")

# include router
app.include_router(mongodb_router, prefix="/items", tags=["items"])

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI with MongoDB"}

if __name__ == "__main__":
    uvicorn.run("Backend.main:app", host="0.0.0.0", port=8001)