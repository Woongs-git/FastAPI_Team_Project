import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, async_engine
from fastapi.concurrency import asynccontextmanager
from app.routers import user, book
from app.middleware.token_refresh import TokenRefreshMiddleware

load_dotenv(dotenv_path=".env")


# 서버 켤때/끌때 할일 정의
# 서버시작-> 테이블 생성 -> yield -> 엔진정리(db연결 정리) -> 서버종료
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  # 서버가 켜져있는동안 일시정지
    await async_engine.dispose()


# lifespan연결
app = FastAPI(lifespan=lifespan)

# 모든 연결이 미들웨어를 거치도록 함
app.add_middleware(TokenRefreshMiddleware)


# 미들웨어: 모든 요청이 api함수에 도착하기 전, 응답이 나가기 전에 거치는 확인작업!!!!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# user.py에 만든 라우터를 fastapi앱에 등록함
app.include_router(user.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)
