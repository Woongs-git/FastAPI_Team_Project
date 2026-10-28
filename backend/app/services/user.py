from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User
from app.db.schemas.users import UserCreate, UserLogin
from fastapi import HTTPException
from app.db.crud import UserCrud
from app.core.jwt_handler import (get_password_hash, verify_password, create_refresh_token, create_access_token)


#crud는 UserCrud에서 처리하고, 비즈니스 규칙(유효성검사, 비밀번호해시, 예외처리 등)을 추가
class UserService:

    #회원가입시 , 같은 이름 있는지 없는지 확인하려고 일단 이름 넣고 db조회함
    @staticmethod
    async def signup(db:AsyncSession, user:UserCreate) -> User:

        if await UserCrud.get_by_username(db, user.username):
            raise HTTPException(status_code=400, detail="이미 사용 중인 사용자 이름이다.")

        hashed_pw=get_password_hash(user.password)
        user_info=UserCreate(username=user.username, password=hashed_pw, email=user.email)

        try:
            db_user=await UserCrud.create(db, user_info)
            await db.commit()
            await db.refresh(db_user)
            return db_user

        except Exception:
            await db.rollback()
            raise HTTPException(status_code=401, detail="잘못된 이메일 또는 비밀번호")


    
    @staticmethod
    async def login(db:AsyncSession, user:UserLogin) -> tuple:
        db_user=await UserCrud.get_by_email(db, user.email)
        if not db_user or not verify_password(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="잘못된 이메일 또는 비밀번호")


        refresh_token=create_refresh_token(db_user.user_id)
        access_token=create_access_token(db_user.user_id)

        #db에 리프레시 토큰 저장
        updated_user=await UserCrud.update_refresh_token_by_id(db, db_user.user_id, refresh_token)
        await db.commit()
        await db.refresh(updated_user)
        return updated_user, access_token, refresh_token



    @staticmethod
    async def get_user(db:AsyncSession, user_id:int) -> User:
        db_user=await UserCrud.get_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user

        

