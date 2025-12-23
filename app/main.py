from fastapi import FastAPI
from .router import api_router

app = FastAPI(title="Multi Agente de Ventas API")
app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {"status": "ok", "message": "API Multi Agente Comercial ONLINE"}