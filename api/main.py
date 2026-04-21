"""
Entry point da API FastAPI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import router
from api.config import settings

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
async def root():
    return {
        "message": "Discord Lookup API",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/users/health"
    }
@app.get("/health")
async def health_check():
    """Verifica se a API está funcionando"""
    return {"status": "ok", "token_configured": settings.is_token_configured}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )