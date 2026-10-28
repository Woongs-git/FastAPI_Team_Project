#models 패키지가 import 되는 순간 -> __init__.py 실행 -> 
#현재 패키지 기준으로 user.py에서 User클래스 가져와
from .user import User
from .book import Book
