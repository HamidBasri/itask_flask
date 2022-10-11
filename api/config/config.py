import os
import enum

BASE_PATH = os.path.join(os.path.dirname(__file__))


class Permissions(enum.Enum):
    Developer = "Developer"
    ProjectManager = "ProjectManager"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.environ.get("DATABASE_PATH")}'
    DATABASE_PATH = os.environ.get("DATABASE_PATH")
