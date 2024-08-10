import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv('SECRET_KEY'))
print(os.getenv('DB_USER'))
print(os.getenv('DB_PASSWORD'))
print(os.getenv('DB_HOST'))
print(os.getenv('DB_NAME'))

SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{password}@{host}/{db_name}'.format(**{
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'db_name': os.getenv('DB_NAME'),
        })

print(SQLALCHEMY_DATABASE_URI)
