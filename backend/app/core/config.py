import os

from dotenv import load_dotenv

# Переход к корневой директории проекта
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# Путь к файлу .env
dotenv_path = os.path.join(base_dir, '.env')

# Загрузка переменных из файла .env
load_dotenv(dotenv_path)

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "True"
TEST = os.getenv("TEST") == "True"

DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
TEST_DATABASE_URL = "sqlite:///./test.db"
