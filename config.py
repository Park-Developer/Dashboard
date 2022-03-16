import os

BASE_DIR=os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR,'pybo.db')) # DB 접속 주소

SQLALCHEMY_TRACK_MODIFICATIONS = False # SQLAlchemy의 이벤트를 처리하는 옵션
# => pybo.db라는 파일으 프로젝트의 루트 디렉터리에 저장하라는 것


# Initial DB Data
