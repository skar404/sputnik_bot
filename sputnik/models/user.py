import datetime

from sqlalchemy import Column, Integer, DateTime, sql, Boolean, JSON

from sputnik.models.main import DataBase


class UserModel(DataBase.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)

    telegram_id = Column(Integer, index=True, unique=True)

    created_at = Column(DateTime, server_default=sql.text('now()'), index=True, default=datetime.datetime.utcnow)

    is_active = Column(Boolean, default=False)

    info_json = Column(JSON, nullable=True)
