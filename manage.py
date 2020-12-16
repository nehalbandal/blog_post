from blog_post import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand

manager = Manager(create_app)  # Script manager
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()