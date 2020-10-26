"""Initialize Flask app."""

import os

from flask import Flask, session

import website.directory.repository as repo
from website.directory.memory_repository import MemoryRepository, populate


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)
    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = os.path.join('website', 'datafilereaders', 'datafiles')

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    populate(data_path, repo.repo_instance)

    # Build the application - these steps require an application context.
    with app.app_context():
        # Register blueprints.
        from .Home import home
        app.register_blueprint(home.home_blueprint)

        from .movie_genre import movie_genre
        app.register_blueprint(movie_genre.movies_blueprint)

        from .movie_info import movie_info
        app.register_blueprint(movie_info.movie_info_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

    return app
