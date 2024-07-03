from sqlalchemy import select

from App.models import Todo, User


def test_create_user(session):
    new_user = User(
        username='Helton', password='secret', email='helton@gmail.com'
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'Helton'))

    assert user.username == 'Helton'


def test_create_todo(session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos
