from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from config import redis_client
from app import app, db

app.config.from_object(str(redis_client.get('APP_SETTINGS').decode('utf-8')))

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
