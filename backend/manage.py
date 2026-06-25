from app import create_app
from extensions import db
import os

# The app will automatically use FLASK_ENV to select the appropriate configuration
app = create_app()

if __name__ == "__main__":
    env = os.getenv("FLASK_ENV", "development")
    print(f"Running in {env} environment...")
    
    with app.app_context():
        db.create_all()
        print("Database schema has been created or updated.")
