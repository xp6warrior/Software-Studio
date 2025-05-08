from sqlmodel import create_engine

DATABASE_URL = "postgresql://root:root@db/postgres"
engine = create_engine(DATABASE_URL, echo=True)
