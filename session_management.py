from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:hinade2019@localhost/cashback')
connection = engine.connect()
session = sessionmaker(bind=connection)()