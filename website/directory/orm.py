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
    Column('password', String(255), nullable=False),
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.id')),
    Column('rating',Integer, nullable=False),
    Column('comment', String(1024), nullable=False),
    Column('timestamp', DateTime)
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('release', Integer, nullable=False),
    Column('description', String(1024), nullable=False),
    Column('director', ForeignKey('directors.id')),
    Column('runtime', Integer, nullable=False),
    Column('rating', Float, nullable=False),
    Column('metascore', String(255)),
    Column('num_of_ratings', Float),
    Column('image_hyperlink', String(255), nullable=False)
)

movie_actors = Table(
    'movie_actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('actor_id', ForeignKey('actors.id'))
)

movie_genres = Table(
    'movie_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('genre_id', ForeignKey('genres.id'))
)

actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(255)),
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False)
)



directors = Table(
    'directors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False),
)



def map_model_to_tables():
    mapper(model.User, users, properties={
        '_user_name': users.c.user_name,
        '_password': users.c.password,
        '_reviews': relationship(model.Review, backref='_user')
    })

    movies_mapper = mapper(model.Movie, movies, properties={
        '_id': movies.c.id,
        '_title': movies.c.title,
        'release': movies.c.release,
        '_description': movies.c.description,
        '_runtime_minutes': movies.c.runtime,
        '_rating': movies.c.rating,
        '_metascore': movies.c.metascore,
        '_num_of_ratings': movies.c.num_of_ratings,
        '_reviews': relationship(model.Review, backref='_movie'),
        '_image': movies.c.image_hyperlink,

    })
    mapper(model.Review, reviews, properties={
        '_review_text': reviews.c.comment,
        '_rating':reviews.c.rating,
    })
    mapper(model.Actor, actors, properties={
        'actor_full_name': actors.c.full_name,
        '_actor_movie':relationship(
            movies_mapper,
            secondary=movie_actors,
            backref="_actors"
        )
    })
    mapper(model.Genre, genres, properties={
        'genre_name': genres.c.name,
        '_genre_movie':relationship(
            movies_mapper,
            secondary=movie_genres,
            backref="_genres"
        )
    })
    mapper(model.Director, directors, properties={
        '_Director__director_full_name': directors.c.name,
    })