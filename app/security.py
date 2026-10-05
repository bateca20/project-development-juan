import os
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
# ------------------------------------------------------------------
# CONFIGURACIÓN DE JWT Y SEGURIDAD
# Nota: En producción, SECRET_KEY debe obtenerse desde variables de entorno (.env)
# ------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas de validez para el token

# Configuración de hashing con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ------------------------------------------------------------------
# FUNCIONES DE CONTRASEÑAS (HASHING Y VERIFICACIÓN)
# ------------------------------------------------------------------

def hash_password(password: str) -> str:
    """Genera un hash seguro a partir de la contraseña en texto plano."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña ingresada coincide con el hash almacenado."""
    return pwd_context.verify(plain_password, hashed_password)

# ------------------------------------------------------------------
# GESTIÓN DE TOKENS JWT (CREACIÓN Y DECODIFICACIÓN)
# ------------------------------------------------------------------

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT adjuntando la expiración y la información del usuario
    (sub: ID o Email, rol_id, etc.).
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodifica y valida un token JWT enviado en los headers HTTP.
    Devuelve el payload si es válido o None si ha expirado/es inválido.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
