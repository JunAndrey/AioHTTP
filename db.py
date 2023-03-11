from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from config import PG_DSN
from sqlalchemy_utils import UUIDType, EmailType


engine = create_async_engine(PG_DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


class Announcement(Base):
    __tablename__ = "announcements"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    creation_date = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("app_user.id", ondelete="CASCADE"))
    user = relationship("User", backref="owner_posts", foreign_keys=[user_id], lazy="joined")

    def __repr__(self):
        return "<Announcement: {}>".format(self.id)


class User(Base):
    __tablename__ = "app_user"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    users_email = Column(EmailType, unique=True)

    # token = Column(UUIDType, default=uuid.uuid4())
    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return "<User: {}>".format(self.username)
