import csv
import os
from website.domainmodel.model import  Movie, Actor, Genre, Director



class MovieFileCSVReader:
    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__dataset_of_movies = set()
        self.__dataset_of_actors = set()
        self.__dataset_of_directors = set()
        self.__dataset_of_genres = set()

    def read_csv_file(self):
        with open(os.path.join(self.__file_name, 'Data1000Movies.csv'), mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)

            index = 0
            for row in movie_file_reader:
                title = row['Title']
                release_year = int(row['Year'])
                movie = Movie(title, release_year)

                if movie not in self.__dataset_of_movies:
                    self.__dataset_of_movies.add(movie)
                actors = row['Actors'].split(",")
                for actor in actors:
                    a_actor = Actor(actor)
                    movie.add_actor(a_actor)
                    if a_actor not in self.__dataset_of_actors:
                        self.__dataset_of_actors.add(a_actor)
                metascore = row['Metascore']
                movie.metascore = str(metascore)
                num_of_ratings = row['Votes']
                movie.num_of_ratings = float(num_of_ratings)
                director = row["Director"]
                director1 = Director(director)
                movie.director = director1
                description = row["Description"]
                movie.description = description
                rating = row["Rating"]

                runtime = row["Runtime (Minutes)"]

                movie.runtime_minutes = int(runtime)
                movie.rating = float(rating)
                if director1 not in self.__dataset_of_directors:
                    self.__dataset_of_directors.add(director1)
                genres = row["Genre"].split(",")
                for genre in genres:
                    a_genre = Genre(genre)
                    movie.add_genre(a_genre)
                    if a_genre not in self.__dataset_of_genres:
                        self.__dataset_of_genres.add(a_genre)
                index += 1


    @property
    def dataset_of_movies(self):
        return self.__dataset_of_movies

    @property
    def dataset_of_actors(self):
        return self.__dataset_of_actors

    @property
    def dataset_of_directors(self):
        return self.__dataset_of_directors

    @property
    def dataset_of_genres(self):
        return self.__dataset_of_genres
