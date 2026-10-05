from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schemas, security
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/registro", status_code=status.HTTP_201_CREATED, response_model=schemas.UsuarioOut)
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # 1. Verificar si el correo ya existe
    usuario_existente_email = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if usuario_existente_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya está registrado")

    # 2. Verificar si el documento ya existe
    usuario_existente_doc = db.query(models.Usuario).filter(models.Usuario.documento == usuario.documento).first()
    if usuario_existente_doc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El número de documento ya está registrado")
    
    # 3. Encriptar la contraseña
    hashed_pwd = security.hash_password(usuario.password)
    
    # 4. Guardar el usuario en la base de datos (con los campos del hotel)
    nuevo_usuario = models.Usuario(
        documento=usuario.documento,
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        email=usuario.email,
        telefono=usuario.telefono,
        password=hashed_pwd,
        rol_id=usuario.rol_id  # 3 por defecto: CLIENTE
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return nuevo_usuario

@router.post("/login", response_model=schemas.Token)
def login(credenciales: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Buscar al usuario por email (OAuth2 envía el email en el campo 'username')
    usuario = db.query(models.Usuario).filter(models.Usuario.email == credenciales.username).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Credenciales incorrectas"
        )
        
    # 2. Verificar si la cuenta está activa
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El usuario se encuentra inactivo"
        )

    # 3. Verificar la contraseña (usando el campo 'password' de nuestro modelo)
    if not security.verify_password(credenciales.password, usuario.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Credenciales incorrectas"
        )
        
    # 4. Generar el Token JWT con el payload adecuado para Angular
    access_token = security.create_access_token(
        data={
            "sub": str(usuario.id),
            "email": usuario.email,
            "rol_id": usuario.rol_id,
            "nombre": f"{usuario.nombre} {usuario.apellido}"
        }
    )
    
    return {"access_token": access_token, "token_type": "bearer"}