from datetime import date, datetime

import pytest

from website.directory.database_repository import SqlAlchemyRepository
from website.domainmodel.model import User,Genre,Movie,Director,Actor,Review,make_review
from website.directory.repository import RepositoryException

def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user