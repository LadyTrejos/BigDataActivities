from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

# dialecto://usuariodb:pwdb@ip:puerto/base_datos
motor = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/PQRSalud")
print(database_exists(motor.url))
if not database_exists(motor.url):
    create_database(motor.url)
print(database_exists(motor.url))


Session = sessionmaker(bind=motor)
session = Session()
Base = declarative_base()
