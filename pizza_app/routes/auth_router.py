
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from pizza_app.database import get_database_session
from pizza_app.hash import Hash
from pizza_app.models import UserModel
from pizza_app.schemas import LoginSchema, SignupSchema

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

# session = SessionLocal(bind=engine)


@router.get('/')
async def hello(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    return {'msg': 'I don show again'}


@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def sign_up(request: SignupSchema, db: Session = Depends(get_database_session)):

    """
        ## Create a user
        This requires the following
        ```
                username:int
                email:str
                password:str
                is_staff:bool
                is_active:bool

        ```

    """

    db_email = db.query(UserModel).filter(
        UserModel.email == request.email).first()
    if db_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with {request.email} already exist")
    db_username = db.query(UserModel).filter(
        UserModel.username == request.username).first()
    if db_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with {request.username} already exist")
    new_user = UserModel(
        username=request.username,
        email=request.email,
        password=Hash.hash_password(request.password),
        is_active=request.is_active,
        is_staff=request.is_staff
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post('/login', status_code=status.HTTP_200_OK)
async def login_user(request: LoginSchema, Authorize: AuthJWT = Depends(), db: Session = Depends(get_database_session)):

    """     
        ## Login a user
        This requires
            ```
                username:str
                password:str
            ```
        and returns a token pair `access` and `refresh`
    """

    db_user = db.query(UserModel).filter(
        UserModel.username == request.username).first()

    if db_user and Hash.verify(request.password, db_user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(
            subject=db_user.username)

        response = {
            "access": access_token,
            "refresh": refresh_token
        }

        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid Username or Password ")


# Refreshing Token
@router.get('/refresh')
async def refresh_token(Authorize: AuthJWT = Depends()):

    """
    ## Create a fresh token
    This creates a fresh token. It requires an refresh token.
    """

    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Please provide a valid refresh token")

    # Get current user identity
    current_user = Authorize.get_jwt_subject()

    new_access_token = Authorize.create_access_token(subject=current_user)
    return jsonable_encoder({"access_token": new_access_token})
