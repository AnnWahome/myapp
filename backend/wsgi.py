from flask_migrate import Migrate
from app import create_app
from extensions import db
import os

# The app will automatically use FLASK_ENV to select the appropriate configuration
app = create_app()
migrate = Migrate(app, db)

if __name__ == "__main__":
    env = os.getenv("FLASK_ENV", "development")
    print(f"Flask-Migrate initialized. Environment: {env}")
    print("Use 'flask db' commands to manage migrations.")
