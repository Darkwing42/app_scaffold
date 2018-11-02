from flask_scripts import Manager
import os
from flask_migrate import Migrate, MigrateCommand
from src import create_app
from src.db import db

app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()
