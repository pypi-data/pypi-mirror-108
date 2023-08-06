# Python script that will apply the migrations up to head
import alembic.config
import os

from flask import current_app
from vm_booking_api import create_app, db

from alembic import context

config = context.config

here = os.path.dirname(os.path.abspath(__file__))

alembic_args = ["-c", os.path.join(here, "alembic.ini"), "upgrade", "head"]

try:
    app = current_app._get_current_object()
except RuntimeError:
    app = create_app()

config.set_main_option("sqlalchemy.url", app.config["SQLALCHEMY_DATABASE_URI"])
target_metadata = db.metadata


def main():
    with app.app_context():
        alembic.config.main(argv=alembic_args)
