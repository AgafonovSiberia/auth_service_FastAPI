from fastapi import APIRouter, Depends, HTTPException

from app.schemas.user import UserCreate, User
from app.repo.base import SQLAlchemyRepo
from app.repo.user_repo import UserRepo

from app.services.depends import get_repo



router = APIRouter()


@router.post("/signup/", response_model=User)
async def root(user_data: UserCreate,  repo: SQLAlchemyRepo = Depends(get_repo)):
	user: User = await repo.get_repo(UserRepo).get_by_email(email=user_data.email)
	if user:
		raise HTTPException(status_code=400,
		                    detail="The user with this username already exists")

	user: User = await repo.get_repo(UserRepo).user_add(user_data=user_data)
	return user

