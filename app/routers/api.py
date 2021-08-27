from datetime import datetime
from fastapi import APIRouter, HTTPException, Form, Header
from fastapi.params import Depends


from app.schemas import users as schema_users
from app.schemas import urls as schema_urls
from app.crud import users as crud_users
from app.crud import urls as crud_urls
from app.crud import refresh_sessions as crud_sessions
from app.utils.auth import AuthHandler
from app.core.url_hashing import get_url_hash


router = APIRouter()
auth_handler = AuthHandler()


@router.post("/create-url", response_model=schema_urls.UrlBase,
             status_code=201)
async def create_url(url: schema_urls.CreateUrl):
    hash_url = await get_url_hash(url.original_url)
    return await crud_urls.create_url(url, hash_url)


@router.post("/create-user-url", response_model=schema_urls.UrlBase,
             status_code=201)
async def create_user_url(url: schema_urls.CreateUrl,
                          user_id=Depends(auth_handler.auth_wrapper)):
    hash_url = await get_url_hash(url.original_url)
    return await crud_urls.create_url(url, hash_url, user_id)


@router.post("/delete-url")
async def delete_url(hash: str = Form(...),
                     user_id=Depends(auth_handler.auth_wrapper)):
    return await crud_urls.delete_url(hash, user_id)


@router.get('/user-urls', response_model=schema_urls.ListUrlStats)
async def get_user_urls(user_id=Depends(auth_handler.auth_wrapper)):
    res = await crud_urls.get_urls_by_user_id(user_id)
    return {"urls": res}


@router.post("/register", response_model=schema_users.UserBase,
             status_code=201)
async def register_user(user: schema_users.CreateUser):
    db_user = await crud_users.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400,
                            detail='User with this email already exists.')
    hashed_password = auth_handler.encode_password(user.password)
    return await crud_users.create_user(user, hashed_password)


@router.post('/login', response_model=schema_users.LoginUser)
async def login_user(email: str = Form(...),
                     password: str = Form(...),
                     user_agent=Header(None)):
    user = await crud_users.get_user_by_email(email=email)

    if not user or not auth_handler.verify_password(
        plain_password=password, hashed_password=user["hashed_password"]
    ):
        raise HTTPException(status_code=400,
                            detail='Incorrect email or password')

    access_token = auth_handler.encode_token(user["id"])
    refresh_token = auth_handler.get_refresh_token()

    await crud_sessions.create_session(user["id"], user_agent,
                                       refresh_token)

    return {'access_token': access_token, "refresh_token": refresh_token}


@router.post("/change-password")
async def change_password(password: schema_users.ChangeUserPassword,
                          user_id=Depends(auth_handler.auth_wrapper)):
    hashed_password = auth_handler.encode_password(password.password)
    return await crud_users.change_user_password(user_id, hashed_password)


@router.get('/user')
def get_user(user_id=Depends(auth_handler.auth_wrapper)):
    return {'user_id': user_id}


@router.post('/refresh-token', response_model=schema_users.LoginUser)
async def refresh_jwt_token(refresh_token: str = Form(...),
                            user_agent=Header(None)):
    session = await crud_sessions.get_session(refresh_token)
    if not session or session["user_agent"] != user_agent:
        raise HTTPException(status_code=401, detail='Invalid token')
    if session["expiration_date"] < datetime.now():
        raise HTTPException(status_code=401, detail='Token expired')

    await crud_sessions.delete_session(refresh_token)

    user = await crud_users.get_user_by_id(user_id=session["user_id"])
    token = auth_handler.encode_token(user["id"])
    refresh_token = auth_handler.get_refresh_token()
    await crud_sessions.create_session(session["user_id"], user_agent,
                                       refresh_token)

    return {'access_token': token, "refresh_token": refresh_token}
