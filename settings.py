from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


class DBConfig(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    name: str

    class Config:
        env_prefix = "DB_"

    @property
    def dsn(self):
        """
        A property method that generates a PostgreSQL DSN using user, password, host, port, and name.
        Returns a formatted string representing the PostgreSQL DSN.
        """
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Settings(BaseSettings):
    db: DBConfig


def get_settings():
    """
    Get the settings by instantiating a Settings object with the database configuration.
    """
    return Settings(
        db=DBConfig()
    )

