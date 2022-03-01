from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from config import setting

# SQLALCHEMY_DATABASE_URL = 'postgres://<username>:<password>@<ip-address/hostname>/<database-name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:uxairkhan@localhost/alembic'
# SQLALCHEMY_DATABASE_URL = f'postgresql://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}'

engine  = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False , autoflush=False , bind=engine)
                
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn =  psycopg2.connect(host = 'localhost' , database = 'fastapi' , user = 'postgres' , password = 'uxairkhan' ,  cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         cursor.execute(""" SELECT * FROM posts """)
#         post = cursor.fetchall() 
#         # print(post)
#         print('Database connection was successfull')
#         break
#     except Exception as error:
#         print('Connecting to database failed')
#         print("Error : ", error )
#         time.sleep(2)