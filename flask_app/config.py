import os
# from dotenv import load_dotenv
from datetime import timedelta

# load_dotenv()

class Config:
    # Flask
    DEBUG = False

    if not DEBUG:
        # SECRET_KEY設定
        SECRET_KEY = os.environ['SECRET_KEY']
        # sqlalchemy設定
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
            'user': os.environ['DATABASE_USERNAME'],
            'password': os.environ['DATABASE_PASSWORD'],
            'host': os.environ['DATABASE_HOSTNAME'],
            'db_name': os.environ['DATABASE_NAME'],
        })
        PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SQLALCHEMY_ECHO = False
# print(Config.SQLALCHEMY_DATABASE_URI)
