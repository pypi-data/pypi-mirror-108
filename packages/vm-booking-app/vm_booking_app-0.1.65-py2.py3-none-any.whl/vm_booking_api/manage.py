from flask_migrate import Migrate
from flask_script import Manager

from . import app, db

migrate = Migrate(app, db)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
