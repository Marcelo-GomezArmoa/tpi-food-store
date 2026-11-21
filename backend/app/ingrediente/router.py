from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session

from app.core.database import get_session
from app.ingrediente.schema import (
    IngredienteCreate,
    IngredienteRead,
    IngredienteUpdate,
)
from app.ingrediente.service import IngredienteService
from app.modules.usuarios.dependencies import (
    get_current_active_user,
    require_role,
)


router = APIRouter(prefix="/ingredientes", tags=["ingredientes"])


@router.get(
    "",
    response_model=list[IngredienteRead],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_user)],
)
def listar_ingredientes(
    session: Session = Depends(get_session),
) -> list[IngredienteRead]:
    return IngredienteService(session).listar()


@router.post(
    "",
    response_model=IngredienteRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(["admin"]))],
)
def crear_ingrediente(
    datos: IngredienteCreate,
    session: Session = Depends(get_session),
) -> IngredienteRead:
    return IngredienteService(session).crear(datos)


@router.put(
    "/{ingrediente_id}",
    response_model=IngredienteRead,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_role(["admin"]))],
)
def actualizar_ingrediente(
    ingrediente_id: int,
    datos: IngredienteUpdate,
    session: Session = Depends(get_session),
) -> IngredienteRead:
    ingrediente = IngredienteService(session).actualizar(ingrediente_id, datos)
    if ingrediente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ingrediente con ID {ingrediente_id} no encontrado",
        )
    return ingrediente


@router.delete(
    "/{ingrediente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(["admin"]))],
)
def eliminar_ingrediente(
    ingrediente_id: int,
    session: Session = Depends(get_session),
) -> Response:
    eliminado = IngredienteService(session).eliminar(ingrediente_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ingrediente con ID {ingrediente_id} no encontrado",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
