from sqlalchemy import select

from App.models import User


def test_create_user(session):
    new_user = User(
        username='Helton', password='secret', email='helton@gmail.com'
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'Helton'))

    assert user.username == 'Helton'
