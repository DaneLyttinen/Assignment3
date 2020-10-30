from datetime import datetime





class Genre:
    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.genre_name = None
        else:
            self.genre_name = genre_name.strip()

    def __repr__(self):
        return f"<Genre {self.genre_name}>"

    def __eq__(self, other):
        return other.genre_name == self.genre_name

    def __lt__(self, other):
        return self.genre_name[0] < other.genre_name[0]

    def __hash__(self):
        return hash(self.genre_name)



class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    def __repr__(self):
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other):
        return other.__director_full_name == self.__director_full_name

    def __lt__(self, other):
        return self.__director_full_name[0] < other.__director_full_name[0]

    def __hash__(self):
        return hash(self.__director_full_name)


class Actor:
    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.actor_full_name = None
        else:
            self.actor_full_name = actor_full_name.strip()
        self.colleague_list = []

    def __repr__(self):
        return f"<Actor {self.actor_full_name}>"

    def __eq__(self, other):
        return other.actor_full_name == self.actor_full_name

    def __lt__(self, other):
        return self.actor_full_name[0] < other.actor_full_name[0]

    def __hash__(self):
        return hash(self.actor_full_name)

    def check_if_this_actor_worked_with(self, colleague):
        if colleague in self.colleague_list or self in colleague.colleague_list:
            return True
        else:
            return False

    def add_actor_colleague(self, colleague):
        self.colleague_list.append(colleague)
        colleague.colleague_list.append(self)

class Movie:
    def __init__(self, title: str, release: int):


        if title == "" or type(title) is not str:
            self._title = None
        else:
            self._title = title.strip()
        if release == "" or type(release) is not int or release < 1900:
            self.release = None
        else:
            self.release = release

        self._description: str
        self._director: Director
        self._actors = []
        self._genres = []
        self._runtime_minutes: int
        self._rating: float
        self._metascore: str
        self._num_of_ratings: float
        self._reviews = []
        self._image: str

    def __repr__(self):
        return f"<Movie {self._title}, {self.release}>"

    def __eq__(self, other):
        return other.title == self.title and other.release == self.release

    def __lt__(self, other):
        return self.__repr__() < other.__repr__()

    def __hash__(self):
        return hash((self.title, self.release))

    @property
    def actors(self):
        return self._actors

    @property
    def genres(self):
        return self._genres

    def add_actor(self, actor):
        if type(actor) is Actor and actor not in self._actors:
            self._actors.append(actor)

    def remove_actor(self, actor):
        if actor in self._actors:
            self._actors.remove(actor)
        else:
            pass

    def add_genre(self, genre):
        if type(genre) is Genre and genre not in self._genres:
            self._genres.append(genre)

    def remove_genre(self, genre):
        if genre in self._genres:
            self._genres.remove(genre)
        else:
            pass

    @property
    def metascore(self):
        return self._metascore

    @metascore.setter
    def metascore(self, value):
        if type(value) is str:
            self._metascore = value


    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        if type(value) is str:
            self._image = value


    @property
    def reviews(self):
        return self._reviews


    def add_review(self, review):
        if type(review) is Review and review not in self._reviews:
            self._reviews.append(review)

    @property
    def num_of_ratings(self):
        return self._num_of_ratings

    @num_of_ratings.setter
    def num_of_ratings(self, value):
        if type(value) is float:
            self._num_of_ratings = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if type(value) is str:
            self._title = value.strip()

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if type(value) is float and 0 <= value <= 10:
            self._rating = value

    @property
    def description(self):
        return self._description.strip()

    @description.setter
    def description(self, desc):
        if type(desc) is str:
            self._description = desc.strip()

    @actors.setter
    def actors(self, ac):
        if ac not in self._actors and type(ac) is Actor:
            self._actors.append(ac)
        else:
            pass

    @genres.setter
    def genres(self, value):
        if value not in self._genres and type(value) is Genre:
            self._genres.append(value)
        else:
            pass

    @property
    def runtime_minutes(self):
        return self._runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, value):
        if value > 0 and type(value) is int:
            self._runtime_minutes = value
        else:
            raise ValueError

    @property
    def director(self) -> Director:
        return self._director

    @director.setter
    def director(self, value):
        if type(value) is Director:
            self._director = value


class Review:
    def __init__(self, movie: Movie, review_text: str, rating: int):
        if type(movie) is Movie:
            self._movie = movie
        else:
            self._movie = None
        if type(review_text) is str:
            self._review_text = review_text
        else:
            self._review_text = None
        if type(rating) is int and 0 <= rating <= 10:
            self._rating = rating
        else:
            self._rating = None
        self._date = datetime
        self._user: User = None

    def __repr__(self):
        return f"{self._movie}/n" \
               f"Review: {self._review_text}>/n" \
               f"Rating: {self._rating}"

    def __eq__(self, other):
        return self._movie == other._movie and self._rating == other._rating and self._review_text == other._review_text and self._date == other._date

    @property
    def movie(self):
        return self._movie

    @movie.setter
    def movie(self, movies):
        if type(movies) is Movie:
            self._movie = movies
        else:
            self._movie = None

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        if type(user) is User and self._user is None:
            self._user = user
        else:
            pass

    @property
    def review_text(self):
        return self._review_text

    @review_text.setter
    def review_text(self, reviews):
        if type(reviews) is str:
            self._review_text = reviews
        else:
            self._review_text = None

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, ratings):
        if type(ratings) is int and 0 <= ratings <= 10:
            self._rating = ratings
        else:
            self._rating = None

    @property
    def timestamp(self):
        return self._date

    @timestamp.setter
    def timestamp(self, value):
        self._date = value


class User:
    def __init__(self, user_name: str, password: str):
        if type(user_name) is str:
            self._user_name = user_name.strip().lower()
        else:
            self._user_name = None
        if type(password) is str:
            self._password = password
        else:
            self._password = None
        self._watched_movies = []
        self._reviews = []
        self._time_spent_watching_movies_minutes = 0

    def __repr__(self):
        return f"<User {self._user_name} {self._password}>"

    def __eq__(self, other):
        return self._user_name == other._user_name

    def __lt__(self, other):
        return self.__repr__() < other.__repr__()

    def __hash__(self):
        return hash(self._user_name)

    def watch_movie(self, movie):
        if type(movie) is Movie and movie not in self._watched_movies:
            self._watched_movies.append(movie)
            self._time_spent_watching_movies_minutes += movie.runtime_minutes
        else:
            pass

    def add_review(self, review):
        if type(review) is Review and review not in self._reviews:
            self._reviews.append(review)
        else:
            pass

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, value):
        if type(value) is str:
            self._user_name = value.strip().lower()
        else:
            pass

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if type(value) is str:
            self._password = value
        else:
            pass

    @property
    def watched_movies(self):
        return self._watched_movies

    @watched_movies.setter
    def watched_movies(self, movie):
        if type(movie) is Movie and movie not in self._watched_movies:
            self._watched_movies.append(movie)
        else:
            pass

    @property
    def reviews(self):
        return self._reviews

    @reviews.setter
    def reviews(self, other):
        if type(other) is Review and other not in self._reviews:
            self._reviews.append(other)
        else:
            pass

    @property
    def time_spent_watching_movies_minutes(self):
        return self._time_spent_watching_movies_minutes

    @time_spent_watching_movies_minutes.setter
    def time_spent_watching_movies_minutes(self, other):
        if type(other) is int and other > 0:
            self._time_spent_watching_movies_minutes += other
        else:
            pass

class ReviewException(Exception):
    pass

def make_review(review_text: str, user: User, movie: Movie, rating, timestamp: datetime = datetime.today()):
    if user is None or movie is None:
        raise ReviewException
    review = Review(movie, review_text, rating)
    review.user = user
    user.add_review(review)
    movie.add_review(review)

    return review