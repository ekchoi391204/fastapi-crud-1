from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    app_name: str = "CRUD System"
    app_version: str = "1.0.0"
    server_name: str = "crud-app"
    server_ip: str = ""
    secret_key: str = "change-this-secret-key-before-production"
    access_token_expire_minutes: int = 60
    cookie_secure: bool = False

    mysql_host: str = "mydb-svc"
    mysql_port: int = 3306
    mysql_database: str = "frodo"
    mysql_user: str = "frodo"
    mysql_password: str = "Frodo5020!!"

    admin_username: str = "admin"
    admin_password: str = "frodo1234"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def database_url(self) -> URL:
        return URL.create(
            drivername="mysql+pymysql",
            username=self.mysql_user,
            password=self.mysql_password,
            host=self.mysql_host,
            port=self.mysql_port,
            database=self.mysql_database,
            query={"charset": "utf8mb4"},
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
