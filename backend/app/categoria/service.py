"""Service layer for Categoria module with CRUD operations."""
from datetime import datetime, timezone

from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.categoria.model import Categoria
from app.categoria.schema import CategoriaCreate, CategoriaUpdate


async def get_categorias(session: Session) -> list[Categoria]:
    """
    Obtiene todas las categorías de la base de datos.
    
    Args:
        session: Sesión de base de datos
        
    Returns:
        Lista de todas las categorías
    """
    statement = select(Categoria).where(Categoria.deleted_at.is_(None))
    return list(session.exec(statement).all())


async def get_categoria_by_id(session: Session, categoria_id: int) -> Categoria:
    """
    Obtiene una categoría por su ID.
    
    Args:
        session: Sesión de base de datos
        categoria_id: ID de la categoría a buscar
        
    Returns:
        La categoría encontrada
        
    Raises:
        HTTPException: Si la categoría no existe (status 404)
    """
    categoria = session.exec(
        select(Categoria).where(
            Categoria.id == categoria_id,
            Categoria.deleted_at.is_(None),
        )
    ).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {categoria_id} no encontrada"
        )
    return categoria


async def create_categoria(session: Session, categoria_data: CategoriaCreate) -> Categoria:
    """
    Crea una nueva categoría.
    
    Args:
        session: Sesión de base de datos
        categoria_data: Datos de la categoría a crear
        
    Returns:
        La categoría creada
        
    Raises:
        HTTPException: Si el nombre de la categoría ya existe (status 400)
    """
    try:
        categoria = Categoria(**categoria_data.model_dump())
        session.add(categoria)
        session.commit()
        session.refresh(categoria)
        return categoria
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La categoría con nombre '{categoria_data.nombre}' ya existe"
        )


async def update_categoria(
    session: Session,
    categoria_id: int,
    categoria_data: CategoriaUpdate
) -> Categoria:
    """
    Actualiza una categoría existente de forma parcial o total.
    
    Args:
        session: Sesión de base de datos
        categoria_id: ID de la categoría a actualizar
        categoria_data: Datos parciales o totales de actualización
        
    Returns:
        La categoría actualizada
        
    Raises:
        HTTPException: Si la categoría no existe (status 404)
        HTTPException: Si el nombre ya existe (status 400)
    """
    categoria = session.exec(
        select(Categoria).where(
            Categoria.id == categoria_id,
            Categoria.deleted_at.is_(None),
        )
    ).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {categoria_id} no encontrada"
        )
    
    try:
        update_data = categoria_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(categoria, field, value)
        
        session.add(categoria)
        session.commit()
        session.refresh(categoria)
        return categoria
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La categoría con nombre '{categoria_data.nombre}' ya existe"
        )


async def delete_categoria(session: Session, categoria_id: int) -> None:
    """
    Elimina una categoría existente.
    
    Args:
        session: Sesión de base de datos
        categoria_id: ID de la categoría a eliminar
        
    Raises:
        HTTPException: Si la categoría no existe (status 404)
    """
    categoria = session.exec(
        select(Categoria).where(
            Categoria.id == categoria_id,
            Categoria.deleted_at.is_(None),
        )
    ).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {categoria_id} no encontrada"
        )
    
    categoria.deleted_at = datetime.now(timezone.utc)
    session.add(categoria)
    session.commit()
