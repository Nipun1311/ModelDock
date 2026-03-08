from fastapi import FastAPI

app = FastAPI(title="ModelDock API")

@app.get("/")
def root():
    return {"message": "ModelDock backend running"}