# Dependency
from app.extensions.db import DbSession


def get_db():
    db = DbSession()
    try:
        yield db
    finally:
        db.close()
