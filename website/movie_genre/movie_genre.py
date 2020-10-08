from flask import Blueprint, render_template, request
from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
import website.directory.repository as repo
import website.directory.memory_repository as mem
import website.Home.services as services
from website.domainmodel.genre import Genre

movies_blueprint = Blueprint(
    'all_movies_bp', __name__)


@movies_blueprint.route('/gen', methods=['GET'])
def movies_by_genre():
    a_genre = request.args.get('genre')
    a_genre = a_genre[0:len(a_genre)-1]
    a_genre = Genre(a_genre)
    all_movies = services.get_all_movies_genre(repo.repo_instance, a_genre)
    print(all_movies)
    return render_template(
        'movies/all_movies.html',
        all_movies=all_movies,
        genre=a_genre
    )
