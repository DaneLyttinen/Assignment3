from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey, Float
)
from sqlalchemy.orm import mapper, relationship

from website.domainmodel import model

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movie.id')),
    Column('rating',Integer, nullable=False),
    Column('comment', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('release', Integer, nullable=False),
    Column('description', String(1024), nullable=False),
    Column('runtime', Integer, nullable=False),
    Column('rating', Integer, nullable=False),
    Column('metascore', Integer, nullable=False),
    Column('num_of_ratings', Float, nullable=False),
    Column('image_hyperlink', String(255), nullable=False)
)

actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(255), nullable=False),
    Column('colleague_list', String(255), nullable=False)
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False)
)

directors = Table(
    'directors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False)
)

def map_model_to_tables():
    mapper(model.User, users, properties={
        '_username': users.c.user_name,
        '_password': users.c.password,
        '_reviews': relationship(model.Review, backref='_user')
    })
    mapper(model.Review, reviews, properties={
        '_comment': reviews.c.comment,
        '_rating':reviews.c.rating
    })
    movies_mapper = mapper(model.Movie, movies, properties={
        '_id': movies.c.id,
        '_title': movies.c.title,
        '_release': movies.c.release,
        '_description': movies.c.description,
        '_director':relationship(model.Director, backref="_movie"),
        '_actors':relationship(model.Actor, backref='_movie'),
        '_genres':relationship(model.Genre, backref='_movie'),
        '_runtime': movies.c.runtime,
        '_rating': movies.c.rating,
        '_metascore': movies.c.metascore,
        '_num_of_ratings': movies.c.num_if_ratings,
        '_reviews': relationship(model.Review, backref='_movie'),
        '_image_hyperlink': movies.c.image_hyperlink,
    })
    mapper(model.Actor, actors, properties={
        '_comment': reviews.c.comment,
        '_rating':reviews.c.rating
    })