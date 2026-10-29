from fastapi import APIRouter, Depends, Response, HTTPException, status
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import UserService
from app.db.schemas.users import UserLogin, UserRead, UserCreate, UserUpdate
from app.core.jwt_handler import get_password_hash
from app.core.auth import set_auth_cookies, get_user_id

router=APIRouter(prefix="/users", tags=["User"])

#users/me로 들어가면 쿠키에서 access_token을 꺼내 검증(user_id)
@router.get("/me", response_model=UserRead)
async def get_user(user_id:int=Depends(get_user_id), db:AsyncSession=Depends(get_db)):
    return await UserService.get_user(db, user_id)


@router.post("/signup", response_model=UserRead)
async def sinnup(user:UserCreate, db:AsyncSession = Depends(get_db)):
    db_user=await UserService.signup(db, user)
    return db_user


#users/login
#response : 쿠키를 심을 응답 객체
#set_auth_cookies(response, access_token, refresh_token) : response객체에 쿠키로 토큰저장
@router.post("/login", response_model=UserRead)
async def login(user:UserLogin, response:Response, db:AsyncSession = Depends(get_db)):
    result=await UserService.login(db, user)
    db_user,access_token, refresh_token=result
    #토큰 2개를 쿠키로 응답에 붙인다.
    set_auth_cookies(response, access_token, refresh_token)
    return db_user


#로그아웃시 엑세스, 리프레시 토큰 쿠키 삭제
@router.post("/logout", response_model=bool)
async def logout(response:Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return True


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    delete_user = await UserService.delete_user(db=db, user_id=user_id)
    if not delete_user:
        raise HTTPException(status_code=404, detail="User not found")
    return None

@router.put("/{user_id}")
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    updated_user = await UserService.update_user(db=db, user_id=user_id, user=user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user