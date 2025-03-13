# config.py
DB_NAME = "myDatabase"
COLLECTION = "dystopianNovels"


class Config:
    MONGO_URI = f"mongodb://localhost:27017/{DB_NAME}"
    SECRET_KEY = "your-secret-key"  # Change this to a random secret
