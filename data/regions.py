import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Regions(SqlAlchemyBase):
    __tablename__ = 'regions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    region = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    narods = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    mine = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    development = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    history = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    now_time = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    traditions = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    future_time = sqlalchemy.Column(sqlalchemy.String, nullable=True)
