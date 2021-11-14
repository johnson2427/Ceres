from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config

SQL_DATABASE_URL = f"postgresql://{config.SQL_USER}:{config.SQL_PASSWORD}@{config.HOST}:{config.SQL_PORT}/{config.SQL_DB}"
engine = create_engine(SQL_DATABASE_URL, pool_pre_ping=True, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
