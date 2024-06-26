import time

from sqlalchemy import select, update

from fast_zero.models import User


def test_create_user(session):
    user = User(username='test', email='test@test.com', password='password')

    session.add(user)
    session.commit()

    query = session.scalar(select(User).where(User.id == 1))

    assert query is not None


def test_fields_updated_at_and_created_at(session):
    user = User(username='test2', email='test2@test.com', password='password')

    session.add(user)
    session.commit()

    time.sleep(1)

    session.execute(
        update(User).where(User.id == user.id).values(password='password2')
    )

    session.commit()

    query = session.scalar(
        select(User).where(User.id == user.id)
    )

    assert query.updated_at != query.created_at
