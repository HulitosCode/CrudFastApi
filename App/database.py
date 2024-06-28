from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# URL do banco de dados PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://helton:admin@localhost:5432/fastapi"

# Criação do engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Criação do sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa
Base = declarative_base()

# Table Registry para armazenar os modelos
table_registry = Base.metadata

# Função para obter a sessão
def get_session():
    with SessionLocal() as session:
        yield session
