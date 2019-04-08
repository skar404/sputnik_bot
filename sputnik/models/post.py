import datetime

from sqlalchemy import Column, Integer, String, DateTime, sql, Boolean

from sputnik.models.main import DataBase


class PostModel(DataBase.Model):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, autoincrement=True)

    guid = Column(String, unique=True)

    category = Column(String)
    description = Column(String)
    enclosure = Column(String)

    link = Column(String)
    post_id = Column(String)
    pub_date = Column(DateTime, default=datetime.datetime.utcnow)
    short_link = Column(String)

    text = Column(String)
    title = Column(String)

    created_at = Column(DateTime, server_default=sql.text('now()'), index=True, default=datetime.datetime.utcnow)

    is_posted = Column(Boolean, default=False, index=True)
