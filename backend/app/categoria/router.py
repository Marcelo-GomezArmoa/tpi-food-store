"""Router for Categoria endpoints."""
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.core.database import get_session
from app.categoria.schema import CategoriaCreate, CategoriaRead, CategoriaUpdate
from app.categoria import service
from app.modules.usuarios.dependencies import (
    get_current_active_user,
    require_role,
)


router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)


@router.get(
    "",
    response_model=list[CategoriaRead],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_user)],
)
async def listar_categorias(
    session: Session = Depends(get_session)
) -> list[CategoriaRead]:
    """
    Obtiene la lista de todas las categorías.
    
    Returns:
        Lista de categorías
    """
    return await service.get_categorias(session)


@router.get(
    "/{categoria_id}",
    response_model=CategoriaRead,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_user)],
)
async def obtener_categoria(
    categoria_id: int,
    session: Session = Depends(get_session)
) -> CategoriaRead:
    """
    Obtiene una categoría específica por su ID.
    
    Args:
        categoria_id: ID de la categoría
        
    Returns:
        La categoría solicitada
        
    Raises:
        HTTPException: Si la categoría no existe (404)
    """
    return await service.get_categoria_by_id(session, categoria_id)


@router.post(
    "",
    response_model=CategoriaRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(["admin"]))],
)
async def crear_categoria(
    categoria_data: CategoriaCreate,
    session: Session = Depends(get_session)
) -> CategoriaRead:
    """
    Crea una nueva categoría.
    
    Args:
        categoria_data: Datos de la categoría a crear
        
    Returns:
        La categoría creada
        
    Raises:
        HTTPException: Si el nombre ya existe (400)
    """
    return await service.create_categoria(session, categoria_data)


@router.put(
    "/{categoria_id}",
    response_model=CategoriaRead,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_role(["admin"]))],
)
async def actualizar_categoria(
    categoria_id: int,
    categoria_data: CategoriaUpdate,
    session: Session = Depends(get_session)
) -> CategoriaRead:
    """
    Actualiza una categoría existente de forma parcial o total.
    
    Args:
        categoria_id: ID de la categoría a actualizar
        categoria_data: Datos a actualizar
        
    Returns:
        La categoría actualizada
        
    Raises:
        HTTPException: Si la categoría no existe (404)
        HTTPException: Si el nombre ya existe (400)
    """
    return await service.update_categoria(session, categoria_id, categoria_data)


@router.delete(
    "/{categoria_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(["admin"]))],
)
async def eliminar_categoria(
    categoria_id: int,
    session: Session = Depends(get_session)
) -> None:
    """
    Elimina una categoría existente.
    
    Args:
        categoria_id: ID de la categoría a eliminar
        
    Raises:
        HTTPException: Si la categoría no existe (404)
    """
    await service.delete_categoria(session, categoria_id)
