from fastapi import (APIRouter, Depends,
                     HTTPException, Request)

from app.repo.base import Repository
from app.repo.user_repo import UserRepo
from app.schemas.user import UserCreate, UserFromDB
from app.services.depends import get_repo

router = APIRouter()

@router.post("/signup/", response_model=UserFromDB)
async def signup_account(user_data: UserCreate, request: Request, repo: Repository = Depends(get_repo)):
	user: UserFromDB = await repo.get_repo(UserRepo).get_by_email(email=user_data.email)
	if user:
		raise HTTPException(status_code=400, detail="The user with this username already exists")

	user: UserFromDB = await repo.get_repo(UserRepo).user_add(user_data=user_data)
	#url for activate account

	print(request.url_for("activate_account", user_id = user.id, activate_code="caefrg"))
	"""
	генерируем UUID-код для активации аккаунта (храним в БД?)
	отправляем пользователю ссылочку для активации аккаунта (или достаточно просто user_id?)
	"""
	return user


@router.post("/activate/{user_id}/{activate_code}")
async def activate_account(user_id: int, activate_code: str):
	print(activate_code)
