import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.compra import Compra
from models.revendedor import Revendedor

DB_USER='dev'
DB_PASSWORD='hinade2019'
DB_SERVER='localhost'

class DBSessionManagement(object):
    """Class for management of db session"""
    
    def __init__(self):
        self.engine = create_engine(
            'mysql+pymysql://{user}:{password}@{server}'.format(
            user=DB_USER, password=DB_PASSWORD,
            server=DB_SERVER), echo=False)
    
    def get_db_session(self):
        self.engine.execute('USE `{db_name}`'.format(db_name=os.environ.get('DB_NAME')))
        connection = self.engine.connect()
        return sessionmaker(bind=connection)()
    
    def generate_db(self):
        self.engine.execute('DROP DATABASE IF EXISTS `{db_name}`'.format(
            db_name=os.environ.get('DB_NAME')))
        self.engine.execute('CREATE DATABASE IF NOT EXISTS `{db_name}`'.format(
            db_name=os.environ.get('DB_NAME')))
        self.engine.execute('USE `{db_name}`'.format(db_name=os.environ.get('DB_NAME')))
        Revendedor.metadata.create_all(self.engine)
        Compra.metadata.create_all(self.engine)

    def drop_db(self):
        self.engine.execute('DROP DATABASE IF EXISTS `{db_name}`'.format(
            db_name=os.environ.get('DB_NAME')
        ))
        self.engine.execute('COMMIT')        
