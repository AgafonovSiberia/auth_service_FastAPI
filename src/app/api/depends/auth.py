from app.infrastructure.repo.user_repo import UserRepo
from app.infrastructure.repo.base import SQLALchemyRepo

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class Auth:
    ...
    # async def get_current_user(
    #         self,
    #         token: str = Depends(oauth2_scheme),
    #         dao: HolderDao = Depends(dao_provider),
    # ) -> dto.User:
    #     credentials_exception = HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Could not validate credentials",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    #     try:
    #         payload = jwt.decode(token, self.secret_key, algorithms=[self.algorythm])
    #         username: str = payload.get("sub")
    #         if username is None:
    #             raise credentials_exception
    #     except JWTError:
    #         raise credentials_exception
    #     try:
    #         user = await dao.user.get_by_username(username=username)
    #     except NoUsernameFound:
    #         raise credentials_exception
    #     return user