from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pizza_app.database import get_database_session
from pizza_app.models import OrderModel, UserModel, UserTextModel

from pizza_app.schemas import CrudTextSchema, OrderSchema, OrderStatusSchema

router = APIRouter(
    prefix='/crud',
    tags=['Crud Text']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_crud(crud: CrudTextSchema,  db: Session = Depends(get_database_session)):

    new_crud = UserTextModel(
        name=crud.name,
        language=crud.language
    )

    db.add(new_crud)
    db.commit()
    db.refresh(new_crud)

    return new_crud


@router.get('/')
async def list_all_cruds(db: Session = Depends(get_database_session)):

    cruds = db.query(UserTextModel).all()
    return jsonable_encoder(cruds)


@router.get('/{id}')
async def get_crud_by_id(id: int, db: Session = Depends(get_database_session)):

    order = db.query(UserTextModel).filter(UserTextModel.id == id).first()

    return jsonable_encoder(order)


@router.put('/update/{id}/')
async def update_crud(id: int, request: CrudTextSchema, db: Session = Depends(get_database_session)):

    crud_to_update = db.query(UserTextModel).filter(
        UserTextModel.id == id).first()

    crud_to_update.name = request.name
    crud_to_update.language = request.language

    db.commit()
    db.refresh(crud_to_update)

    return jsonable_encoder(crud_to_update)


@router.delete('/delete/{id}/')
async def delete_crud(id: int, db: Session = Depends(get_database_session)):

    crud_to_delete = db.query(UserTextModel).filter(
        UserTextModel.id == id).first()

    db.delete(crud_to_delete)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
