from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Cargo service"
    db_url: str = Field(validation_alias='DATABASE_URL')


settings = Settings()