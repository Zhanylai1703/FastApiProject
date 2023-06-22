from core.db import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Float, Enum, Boolean
from sqlalchemy.sql.sqltypes import Enum
from sqlalchemy.ext.declarative import declarative_base


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String)


class UserType(Enum):
    PRODUCER = 'PRODUCER'
    CONSUMER = 'CONSUMER'


class GenderType(Enum):
    F = 'F'
    M = 'M'
    O = 'O'


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    date = Column(DateTime)
    type = Column(Enum(UserType.PRODUCER, UserType.CONSUMER, name='usertype'),  default=UserType.CONSUMER)
    city = relationship('City')
    city_id = Column(Integer, ForeignKey('cities.id'))
    gender = Column(Enum(GenderType.F, GenderType.M, GenderType.O, name='gendertype'), default=GenderType.O)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(length=100))


class Post(Base):
    __tablename__ = 'microblog_posts'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String(length=100))
    text = Column(Text)
    date = Column(DateTime)
    price = Column(Float)
    user = relationship('User')
    user_id = Column(Integer, ForeignKey('user.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category')
    image = Column(String)
    hashtags = relationship(
        "Hashtag", secondary='post_hashtags', back_populates='posts'
    )


class Hashtag(Base):
    __tablename__ = 'hashtags'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(length=25))
    posts = relationship(
        "Post", secondary='post_hashtags', back_populates='hashtags'
    )
