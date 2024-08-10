import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    # Flask
    DEBUG = False

    if not DEBUG:
        # SECRET_KEY設定
        SECRET_KEY = os.getenv('SECRET_KEY')

        # sqlalchemy設定
        SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'db_name': os.getenv('DB_NAME'),
        })
        # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db_name}'.format(**{
        #     'user': os.getenv('DB_USER'),
        #     'password': os.getenv('DB_PASSWORD'),
        #     'host': os.getenv('DB_HOST'),
        #     'db_name': os.getenv('DB_NAME'),
        # })
        PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SQLALCHEMY_ECHO = False
# print(Config.SQLALCHEMY_DATABASE_URI)
