"""Service layer for Producto module with CRUD operations and relationships."""
from datetime import datetime, timezone

from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status
from app.producto.model import Producto, ProductoCategoria
from app.producto.schema import ProductoCreate, ProductoUpdate
from app.categoria.model import Categoria


# ============================================================================
# FUNCIONES CRUD PARA PRODUCTOS
# ============================================================================

async def get_productos(session: Session) -> list[Producto]:
    """
    Obtiene todos los productos de la base de datos.
    
    Args:
        session: Sesión de base de datos
        
    Returns:
        Lista de todos los productos
    """
    statement = select(Producto).where(Producto.deleted_at.is_(None))
    return list(session.exec(statement).all())


async def get_producto_by_id(session: Session, producto_id: int) -> Producto:
    """
    Obtiene un producto por su ID.
    
    Args:
        session: Sesión de base de datos
        producto_id: ID del producto a buscar
        
    Returns:
        El producto encontrado
        
    Raises:
        HTTPException: Si el producto no existe (status 404)
    """
    producto = session.exec(
        select(Producto).where(
            Producto.id == producto_id,
            Producto.deleted_at.is_(None),
        )
    ).first()
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    return producto


async def create_producto(session: Session, producto_data: ProductoCreate) -> Producto:
    """
    Crea un nuevo producto.
    
    Args:
        session: Sesión de base de datos
        producto_data: Datos del producto a crear
        
    Returns:
        El producto creado
        
    Raises:
        HTTPException: Si hay error en la creación (status 400)
    """
    try:
        producto = Producto(**producto_data.model_dump())
        session.add(producto)
        session.commit()
        session.refresh(producto)
        return producto
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad al crear el producto"
        )
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear el producto: {str(e)}"
        )


async def update_producto(
    session: Session,
    producto_id: int,
    producto_data: ProductoUpdate
) -> Producto:
    """
    Actualiza un producto existente de forma parcial o total.
    
    Args:
        session: Sesión de base de datos
        producto_id: ID del producto a actualizar
        producto_data: Datos parciales o totales de actualización
        
    Returns:
        El producto actualizado
        
    Raises:
        HTTPException: Si el producto no existe (status 404)
        HTTPException: Si hay error en la actualización (status 400)
    """
    producto = session.exec(
        select(Producto).where(
            Producto.id == producto_id,
            Producto.deleted_at.is_(None),
        )
    ).first()
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    
    try:
        update_data = producto_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(producto, field, value)
        
        session.add(producto)
        session.commit()
        session.refresh(producto)
        return producto
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad al actualizar el producto"
        )
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar el producto: {str(e)}"
        )


async def delete_producto(session: Session, producto_id: int) -> None:
    """
    Elimina un producto existente.
    
    Args:
        session: Sesión de base de datos
        producto_id: ID del producto a eliminar
        
    Raises:
        HTTPException: Si el producto no existe (status 404)
        HTTPException: Si una restricción de integridad impide eliminarlo (status 409)
    """
    producto = session.exec(
        select(Producto).where(
            Producto.id == producto_id,
            Producto.deleted_at.is_(None),
        )
    ).first()
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    
    try:
        producto.deleted_at = datetime.now(timezone.utc)
        session.add(producto)
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar el producto por una restricción de integridad",
        ) from exc


# ============================================================================
# FUNCIONES PARA LA RELACIÓN MUCHOS A MUCHOS (Producto-Categoria)
# ============================================================================

async def asignar_categoria_a_producto(
    session: Session,
    producto_id: int,
    categoria_id: int
) -> dict:
    """
    Asocia una categoría a un producto (evitando duplicados).
    
    Args:
        session: Sesión de base de datos
        producto_id: ID del producto
        categoria_id: ID de la categoría
        
    Returns:
        Diccionario con mensaje de confirmación
        
    Raises:
        HTTPException: Si producto o categoría no existen (status 404)
        HTTPException: Si la relación ya existe (status 400)
        HTTPException: Si hay error en la operación (status 400)
    """
    # Verificar que el producto existe
    producto = session.exec(
        select(Producto).where(
            Producto.id == producto_id,
            Producto.deleted_at.is_(None),
        )
    ).first()
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    
    # Verificar que la categoría existe
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
    
    # Verificar que la relación no existe
    statement = select(ProductoCategoria).where(
        ProductoCategoria.producto_id == producto_id,
        ProductoCategoria.categoria_id == categoria_id
    )
    relacion_existente = session.exec(statement).first()
    
    if relacion_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El producto ya está asociado a esta categoría"
        )
    
    try:
        relacion = ProductoCategoria(
            producto_id=producto_id,
            categoria_id=categoria_id
        )
        session.add(relacion)
        session.commit()
        return {
            "mensaje": "Categoría asignada al producto correctamente",
            "producto_id": producto_id,
            "categoria_id": categoria_id
        }
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al asignar categoría: {str(e)}"
        )


async def obtener_categorias_de_producto(
    session: Session,
    producto_id: int
) -> list[Categoria]:
    """
    Obtiene todas las categorías asociadas a un producto.
    
    Args:
        session: Sesión de base de datos
        producto_id: ID del producto
        
    Returns:
        Lista de categorías del producto
        
    Raises:
        HTTPException: Si el producto no existe (status 404)
    """
    producto = session.exec(
        select(Producto).where(
            Producto.id == producto_id,
            Producto.deleted_at.is_(None),
        )
    ).first()
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    
    return [
        categoria
        for categoria in producto.categorias
        if categoria.deleted_at is None
    ]


async def quitar_categoria_de_producto(
    session: Session,
    producto_id: int,
    categoria_id: int
) -> dict:
    """
    Desvincula una categoría de un producto.
    
    Args:
        session: Sesión de base de datos
        producto_id: ID del producto
        categoria_id: ID de la categoría
        
    Returns:
        Diccionario con mensaje de confirmación
        
    Raises:
        HTTPException: Si producto o categoría no existen (status 404)
        HTTPException: Si la relación no existe (status 404)
        HTTPException: Si hay error en la operación (status 400)
    """
    # Verificar que el producto existe
    producto = session.exec(
        select(Producto).where(
            Producto.id == producto_id,
            Producto.deleted_at.is_(None),
        )
    ).first()
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    
    # Verificar que la categoría existe
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
    
    # Buscar la relación
    statement = select(ProductoCategoria).where(
        ProductoCategoria.producto_id == producto_id,
        ProductoCategoria.categoria_id == categoria_id
    )
    relacion = session.exec(statement).first()
    
    if not relacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El producto no está asociado a esta categoría"
        )
    
    try:
        session.delete(relacion)
        session.commit()
        return {
            "mensaje": "Categoría desvinculada del producto correctamente",
            "producto_id": producto_id,
            "categoria_id": categoria_id
        }
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al desvincular categoría: {str(e)}"
        )
