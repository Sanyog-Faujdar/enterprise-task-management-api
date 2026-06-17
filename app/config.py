from dotenv import load_dotenv
import os

load_dotenv()

class Config():
    
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    
    USER = os.getenv("DB_USER")
    PASSWORD = os.getenv("DB_PASSWORD")
    HOST = os.getenv("DB_HOST")
    PORT = os.getenv("DB_PORT")
    NAME = os.getenv("DB_NAME")
    SQLALCHEMY_DATABASE_URI =  f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
