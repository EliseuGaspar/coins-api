import logging
from os.path import join

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.log import configure_global_logging, logg

configure_global_logging()


sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
sqlalchemy_logger.setLevel(logging.INFO)
sqlalchemy_logger.addHandler(logg.logger.handlers[0])
sqlalchemy_logger.propagate = True

db_path: str = join("src", "storage", "database", "db.sqlite3")

engine = create_engine(f"sqlite:///{db_path}")
session = sessionmaker(bind=engine)
base = declarative_base()
