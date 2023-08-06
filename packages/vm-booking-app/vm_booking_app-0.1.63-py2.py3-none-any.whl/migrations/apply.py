# Python script that will apply the migrations up to head
import alembic.config
import os

from flask import current_app
from vm_booking_api import create_app, db


here = os.path.dirname(os.path.abspath(__file__))


try:
    app = current_app._get_current_object()
except RuntimeError:
    app = create_app()

alembic_args = ["--sqlalchemy.url", app.config["SQLALCHEMY_DATABASE_URI"],
                "-c", os.path.join(here, "alembic.ini"), "upgrade", "head"]
target_metadata = db.metadata


def main():
    with app.app_context():
        alembic.config.main(argv=alembic_args)
