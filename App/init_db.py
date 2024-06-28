from App.database import engine, Base
from App.models import User


Base.metadata.create_all(bind=engine)