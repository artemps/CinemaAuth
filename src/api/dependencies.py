from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends

from models import User
from services import (
    SecurityService,
    UserService,
    get_security_service,
    get_user_service,
)


async def authenticated_user(
    security_service: SecurityService = Depends(get_security_service),
    user: UserService = Depends(get_user_service),
    auth: AuthJWT = Depends(),
) -> User:
    await auth.jwt_required()
    login = await auth.get_jwt_subject()
    await security_service.authenticate(auth, login)
    user = await user.get(login=login)
    return user
