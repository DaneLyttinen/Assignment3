from sqlalchemy import select, inspect
from website.directory.orm import metadata


def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['actors','genres', 'movies', 'reviews', 'directors', 'users']
