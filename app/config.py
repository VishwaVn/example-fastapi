from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


# class Settings(BaseSettings):
#     database_password: str = "localhost"
#     database_username: str = "mysql"
#     secret_key: str = "121e3234tty3444"


settings = Settings()
