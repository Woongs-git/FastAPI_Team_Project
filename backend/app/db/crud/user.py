from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import User
from app.db.schemas.users import UserCreate, UserUpdate

#@staticmethod, @classmethod -> 인스턴스 없이 클래스에서 바로 호출
class UserCrud:
    @staticmethod
    async def get_by_id(db:AsyncSession, user_id:int) -> User | None:
        result = await db.execute(select(User).filter(User.user_id == user_id))
        return result.scalar_one_or_none() #결과가 0이면 none, 1개면 객체, 2개이상 에러


    @staticmethod
    async def create(db:AsyncSession, user:UserCreate) -> User:
        db_user=User(**user.model_dump())  #User(email=aaa@aa.com, username=hong, pasword=1234)
        db.add(db_user) #동기 (await이 없어서)
        await db.flush() #변경사항을 insert 로 db에 전송 - commit을 안해서 롤백가능함(영구반영 안함)
        return db_user

    #put, patch
    #flush() : DB에 sql 전송하는 메소드
    @staticmethod
    async def update_by_id(db:AsyncSession, user_id:int, user:UserUpdate) -> User | None:
        db_user=await db.get(User, user_id) #select *from users where user_id=(1)
        if db_user:
            update_data=user.model_dump(exclude_unset=True) #{email:"aa@aa.com", username:'bb'....}
            # db_user.username="bb"
            # db_user.email="aa@aa.com"
            #일일히 어떤필드를 수정하고 , 몇개 필드를 수정할지 미리 알수없기 때문에
            #반복문없으면 필드마다 일일이 확인해야함
            for key, value in update_data.items():
                setattr(db_user, key, value) #골라낸 필드를 자동으로 대입
            await db.flush() #수정한 내용을 DB에 전송 (update users set username='bb'...where user_id=(1))
            return db_user 
        return None


    @staticmethod
    async def delete_by_id(db:AsyncSession, user_id:int) -> User | None:
        db_user=await db.get(User, user_id)
        if db_user:
            await db.delete(db_user) #cascade때문-> 아직 로드되지 않은 자식테이블일경우 db에서 불러와야함(동기식으로 막바로 지우면안됨)
            await db.flush()  #delete from users user_id=(1)
            return db_user  #삭제된 객체반환
        return None


    @staticmethod
    async def get_by_username(db:AsyncSession, username:str) -> User | None:
        result=await db.execute(select(User).filter(User.username == username))
        return result.scalar_one_or_none()


    @staticmethod
    async def get_by_email(db:AsyncSession, email:str) -> User | None:
        result=await db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()

#리프레시 토큰 왜 DB에 저장? 재사용방지
#오래 살아있기 때문에 유출되면 내가 아닌 제 3자가 계속 새 엑세스 토큰 발급받을 수 있다.
#보안강화 -> 서버에서 검증하려고(db와 비교해서)

#사용자 로그인 -> 리프레시 토큰 발급 -> db에 저장
#엑세스토큰이 만료되면 사용자가 리프레시토큰을 전송
#서버에서 db확인 토큰일치해? 새 엑세스 토큰 발급 / 일치노노 -> 거부
    @staticmethod
    async def update_refresh_token_by_id(
        db:AsyncSession, user_id:int, refresh_token:str):

        db_user=await db.get(User, user_id) #기본키로 사용자 조회
        if db_user:
            db_user.refresh_token=refresh_token
            await db.flush()

        return db_user

    


    