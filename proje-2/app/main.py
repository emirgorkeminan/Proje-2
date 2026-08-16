import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.config import settings
from app.routers import recipe

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Ayarları (Gerektiğinde dış erişimler için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Router'ını ekle
app.include_router(recipe.router, prefix=settings.API_V1_STR)

# Ana sayfada frontend arayüzünü sun
@app.get("/", include_in_schema=False)
async def serve_frontend():
    frontend_path = os.path.join(os.getcwd(), "frontend", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"message": "AI Destekli Yemek Tarifi Asistanı API Çalışıyor! Dokümantasyon için /docs adresine gidin."}