from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from entities.user import UserCreate
from ..dependencies.providers import user_provider, UserProvider


router = APIRouter()

@router.post("/register")
async def register(
    user: UserCreate,
    provider: Annotated[UserProvider, Depends(user_provider)],
):
    provider.create_user(user) # No logic on interface layer, only call the provider
    return {"message": "User created!"} # You should use a response model here instead of a dict
