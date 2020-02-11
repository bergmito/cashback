from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.revendedor import Revendedor
from models.compra import Compra

engine = create_engine('mysql+pymysql://root:hinade2019@localhost')
engine.execute('DROP DATABASE IF EXISTS `cashback`')
engine.execute('CREATE DATABASE IF NOT EXISTS `{0}`'.format('cashback'))
engine.execute('USE `cashback`')
Revendedor.metadata.create_all(engine)
Compra.metadata.create_all(engine)