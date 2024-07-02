from fastapi import APIRouter

router = APIRouter()


import app.rest.add_to_db as add_to_db  # noqa
import app.rest.query as query  # noqa
