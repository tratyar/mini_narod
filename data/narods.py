import sqlalchemy
from .db_session import SqlAlchemyBase


class Narods(SqlAlchemyBase):
    __tablename__ = 'narods'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    info = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    region = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    history = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    traditions = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    kitchen = sqlalchemy.Column(sqlalchemy.String, nullable=True)