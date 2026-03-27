from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "ContractGuard AI Backend Running"}