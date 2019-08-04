import datetime

from sqlalchemy import Column, Integer, String, DateTime, sql, Boolean, false, desc

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

    status_posted = Column(Boolean, default=False, index=True)
    status_send_tg = Column(Boolean, server_default=false(), index=True, nullable=False)

    @classmethod
    async def filter(cls, limit: int = 10):
        return await cls.query.order_by(desc(cls.id)).limit(limit=limit).gino.all()
