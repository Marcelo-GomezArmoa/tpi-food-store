"""Router for Producto endpoints."""
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.core.database import get_session
from app.producto.schema import (
    ProductoCreate,
    ProductoRead,
    ProductoUpdate,
    AsignarCategoria
)
from app.categoria.schema import CategoriaRead
from app.producto import service
from app.modules.usuarios.dependencies import (
    get_current_active_user,
    require_role,
)


router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)


# ============================================================================
# ENDPOINTS CRUD PARA PRODUCTOS
# ============================================================================

@router.get(
    "",
    response_model=list[ProductoRead],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_user)],
)
async def listar_productos(
    session: Session = Depends(get_session)
) -> list[ProductoRead]:
    """
    Obtiene la lista de todos los productos.
    
    Returns:
        Lista de productos
    """
    return await service.get_productos(session)


@router.get(
    "/{producto_id}",
    response_model=ProductoRead,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_user)],
)
async def obtener_producto(
    producto_id: int,
    session: Session = Depends(get_session)
) -> ProductoRead:
    """
    Obtiene un producto específico por su ID.
    
    Args:
        producto_id: ID del producto
        
    Returns:
        El producto solicitado
        
    Raises:
        HTTPException: Si el producto no existe (404)
    """
    return await service.get_producto_by_id(session, producto_id)


@router.post(
    "",
    response_model=ProductoRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(["admin"]))],
)
async def crear_producto(
    producto_data: ProductoCreate,
    session: Session = Depends(get_session)
) -> ProductoRead:
    """
    Crea un nuevo producto.
    
    Args:
        producto_data: Datos del producto a crear
        
    Returns:
        El producto creado
        
    Raises:
        HTTPException: Si hay error en la creación (400)
    """
    return await service.create_producto(session, producto_data)


@router.put(
    "/{producto_id}",
    response_model=ProductoRead,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_role(["admin"]))],
)
async def actualizar_producto(
    producto_id: int,
    producto_data: ProductoUpdate,
    session: Session = Depends(get_session)
) -> ProductoRead:
    """
    Actualiza un producto existente de forma parcial o total.
    
    Args:
        producto_id: ID del producto a actualizar
        producto_data: Datos a actualizar
        
    Returns:
        El producto actualizado
        
    Raises:
        HTTPException: Si el producto no existe (404)
        HTTPException: Si hay error en la actualización (400)
    """
    return await service.update_producto(session, producto_id, producto_data)


@router.delete(
    "/{producto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(["admin"]))],
)
async def eliminar_producto(
    producto_id: int,
    session: Session = Depends(get_session)
) -> None:
    """
    Elimina un producto existente.
    
    Args:
        producto_id: ID del producto a eliminar
        
    Raises:
        HTTPException: Si el producto no existe (404)
    """
    await service.delete_producto(session, producto_id)


# ============================================================================
# ENDPOINTS PARA LA RELACIÓN MUCHOS A MUCHOS (Producto-Categoria)
# ============================================================================

@router.post(
    "/{producto_id}/categorias",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(["admin"]))],
)
async def asignar_categoria_a_producto(
    producto_id: int,
    datos: AsignarCategoria,
    session: Session = Depends(get_session)
) -> dict:
    """
    Asocia una categoría a un producto.
    
    Args:
        producto_id: ID del producto
        datos: Datos con el ID de la categoría
        
    Returns:
        Mensaje de confirmación
        
    Raises:
        HTTPException: Si producto o categoría no existen (404)
        HTTPException: Si la relación ya existe (400)
    """
    return await service.asignar_categoria_a_producto(
        session,
        producto_id,
        datos.categoria_id
    )


@router.get(
    "/{producto_id}/categorias",
    response_model=list[CategoriaRead],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_user)],
)
async def obtener_categorias_del_producto(
    producto_id: int,
    session: Session = Depends(get_session)
) -> list[CategoriaRead]:
    """
    Obtiene todas las categorías asociadas a un producto.
    
    Args:
        producto_id: ID del producto
        
    Returns:
        Lista de categorías del producto
        
    Raises:
        HTTPException: Si el producto no existe (404)
    """
    return await service.obtener_categorias_de_producto(session, producto_id)


@router.delete(
    "/{producto_id}/categorias/{categoria_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_role(["admin"]))],
)
async def quitar_categoria_del_producto(
    producto_id: int,
    categoria_id: int,
    session: Session = Depends(get_session)
) -> dict:
    """
    Desvincula una categoría de un producto.
    
    Args:
        producto_id: ID del producto
        categoria_id: ID de la categoría a desvincular
        
    Returns:
        Mensaje de confirmación
        
    Raises:
        HTTPException: Si producto o categoría no existen (404)
        HTTPException: Si la relación no existe (404)
    """
    return await service.quitar_categoria_de_producto(
        session,
        producto_id,
        categoria_id
    )
