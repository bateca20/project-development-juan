from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, habitaciones, reservas

app = FastAPI(
    title="API - Sistema de Administración Hotelera",
    version="1.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir Routers
app.include_router(auth.router)
app.include_router(habitaciones.router)
app.include_router(reservas.router)

@app.get("/")
def read_root():
    return {"mensaje": "¡API Hotelera funcionando correctamente!"}