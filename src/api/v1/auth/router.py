import asyncio

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends, Request

from services import (
    SecurityService,
    UserService,
    get_security_service,
    get_user_service,
)
from . import schemas
from .const import ENDPOINT_DESCRIPTIONS

router = APIRouter()


@router.post("/login", description=ENDPOINT_DESCRIPTIONS["login"])
async def login(
    schema: schemas.UserLoginIn,
    request: Request,
    security_service: SecurityService = Depends(get_security_service),
    user_service: UserService = Depends(get_user_service),
    auth: AuthJWT = Depends()
) -> schemas.UserLoginOut:
    user = await user_service.get(login=schema.login)
    security_service.verify_password(schema.password, user.password)
    coro = user_service.create_login_record(
        user.id,
        user_agent=request.headers.get("User-Agent"),
        ip_address=request.client.host,
    )
    asyncio.create_task(coro)
    access_token, refresh_token = await asyncio.gather(
        security_service.create_access_token(user.login, auth),
        security_service.create_refresh_token(user.login, auth),
    )
    return schemas.UserLoginOut(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/refresh")
async def refresh(
    auth: AuthJWT = Depends(),
    security_service: SecurityService = Depends(get_security_service),
) -> schemas.UserLoginOut:
    new_tokens = await security_service.refresh_token(auth)
    return schemas.UserLoginOut(
        access_token=new_tokens.get("access_token"),
        refresh_token=new_tokens.get("refresh_token"),
        token_type="bearer",
    )


@router.post("/logout")
async def logout(
    auth: AuthJWT = Depends(),
    security_service: SecurityService = Depends(get_security_service),
) -> schemas.UserLogout():
    await security_service.logout(auth)
    return schemas.UserLogout()
