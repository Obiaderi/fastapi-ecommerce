from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pizza_app.database import get_database_session
from pizza_app.models import OrderModel, UserModel

from pizza_app.schemas import OrderSchema, OrderStatusSchema

router = APIRouter(
    prefix='/orders',
    tags=['Orders']
)


@router.get('/')
async def hello(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    return {'msg': 'I don show again'}


@router.post('/order', status_code=status.HTTP_201_CREATED)
async def place_an_order(order: OrderSchema, Authorize: AuthJWT = Depends(), db: Session = Depends(get_database_session)):

    """
        ## Placing an Order
        This requires the following
        - quantity : integer
        - pizza_size: str

    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    current_user = Authorize.get_jwt_subject()

    user = db.query(UserModel).filter(
        UserModel.username == current_user).first()

    # Mapping request to database model instance
    new_order = OrderModel(
        quantity=order.quantity,
        pizza_size=order.pizza_size
    )

    new_order.user = user
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


@router.get('/orders')
async def list_all_orders(Authorize: AuthJWT = Depends(), db: Session = Depends(get_database_session)):

    """
        ## List all orders
        This lists all  orders made. It can be accessed by superusers

    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    current_user = Authorize.get_jwt_subject()
    user = db.query(UserModel).filter(
        UserModel.username == current_user).first()

    if user.is_staff:
        orders = db.query(OrderModel).all()
        return jsonable_encoder(orders)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a Superuser")


@router.get('/orders/{id}')
async def get_order_by_id(id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_database_session)):
    """
        ## Get an order by its ID
        This gets an order by its ID and is only accessed by a superuser


    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    user = Authorize.get_jwt_subject()

    current_user = db.query(UserModel).filter(
        UserModel.username == user).first()

    if current_user.is_staff:
        order = db.query(OrderModel).filter(OrderModel.id == id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with the given ID: {id} is not available")

        return jsonable_encoder(order)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not alowed to carry out request"
    )


@router.get('/user/orders')
async def get_user_orders(Authorize: AuthJWT = Depends(), db: Session = Depends(get_database_session)):
    """
        ## Get a current user's orders
        This lists the orders made by the currently logged in users

    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    user = Authorize.get_jwt_subject()

    current_user = db.query(UserModel).filter(
        UserModel.username == user).first()

    return jsonable_encoder(current_user.orders)


@router.get('/user/order/{id}/')
async def get_specific_order(id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_database_session)):
    """
        ## Get a specific order by the currently logged in user
        This returns an order by ID for the currently logged in user

    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token"
                            )

    subject = Authorize.get_jwt_subject()

    current_user = db.query(UserModel).filter(
        UserModel.username == subject).first()

    orders = current_user.orders

    for o in orders:
        if o.id == id:
            return jsonable_encoder(o)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="No order with such id"
                        )

# Updating Order


@router.put('/order/update/{id}/')
async def update_order(id: int, request: OrderSchema, Authorize: AuthJWT = Depends(), db: Session = Depends(get_database_session)):
    """
        ## Updating an order
        This udates an order and requires the following fields
        - quantity : integer
        - pizza_size: str

    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    order_to_update = db.query(OrderModel).filter(OrderModel.id == id).first()

    order_to_update.quantity = request.quantity
    order_to_update.pizza_size = request.pizza_size

    db.commit()
    db.refresh(order_to_update)

    return jsonable_encoder(order_to_update)


# Updating Order Status by SuperAdmin
@router.patch('/order/update/{id}/')
async def update_order_status(id: int,
                              request: OrderStatusSchema,
                              Authorize: AuthJWT = Depends(), db: Session = Depends(get_database_session)):

    """
        ## Update an order's status
        This is for updating an order's status and requires ` order_status ` in str format
    """
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    username = Authorize.get_jwt_subject()

    current_user = db.query(UserModel).filter(
        UserModel.username == username).first()

    if current_user.is_staff:
        order_to_update = db.query(OrderModel).filter(
            OrderModel.id == id).first()

        if not order_to_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"No Order with the given id {id}")

        order_to_update.order_status = request.order_status

        db.commit()
        db.refresh(order_to_update)

        # response={
        #         "id":order_to_update.id,
        #         "quantity":order_to_update.quantity,
        #         "pizza_size":order_to_update.pizza_size,
        #         "order_status":order_to_update.order_status,
        #     }

        return jsonable_encoder(order_to_update)


@router.delete('/order/delete/{id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_an_order(id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_database_session)):

    """
        ## Delete an Order
        This deletes an order by its ID
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    order_to_delete = db.query(OrderModel).filter(OrderModel.id == id).first()
    if not order_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No Order with the given id {id}")

    db.delete(order_to_delete)

    db.commit()

    return order_to_delete
