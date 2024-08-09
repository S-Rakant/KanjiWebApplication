import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class LocalConfig:
    DEBUG=True

    KANJIALIVE_API_URL=os.getenv('KANJIALIVE_API_URL')
    X_RAPID_KEY=os.getenv('X-RAPID_KEY')
    FILEPATH_KANJI_DATA=os.getenv('FILEPATH_KANJI_DATA')
    SECRET_KEY=os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'db_name': os.getenv('DB_NAME'),
    })
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=180)
