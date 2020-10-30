from flask import Blueprint, render_template, request
from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
import website.directory.repository as repo
import website.directory.memory_repository as mem
import website.movie_genre.services as services
from website.domainmodel.model import Genre

movies_blueprint = Blueprint(
    'all_movies_bp', __name__)


@movies_blueprint.route('/gen', methods=['GET'])
def movies_by_genre():
    a_genre = request.args.get('genre')
    a_genre = a_genre[0:len(a_genre) - 1]
    a_genre = Genre(a_genre)
    all_movies = services.get_all_movies_genre(repo.repo_instance, a_genre)
    print(all_movies)
    a_movie = all_movies[0]
    print(a_movie[0].title)
    return render_template(
        'movies/all_movies.html',
        all_movies=all_movies,
        title=a_genre.genre_name
    )


@movies_blueprint.route('/search', methods=['GET'])
def movies_by_search():
    a_parameter = request.args.get('parameter')
    a_search = request.args.get('search_parameter')
    if a_parameter == 'Title':
        movies = services.get_movies_by_title(repo.repo_instance, a_search)
    if a_parameter == 'Director':
        movies = services.get_movies_by_director(repo.repo_instance, a_search)
    if a_parameter == 'Actor':
        movies = services.get_movies_by_actor(repo.repo_instance, a_search)

    return render_template(
        'movies/all_movies.html',
        all_movies=movies,
        title=a_search,
    )
