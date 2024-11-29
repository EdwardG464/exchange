from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_user: str
    db_pass: str
    db_host: str
    db_port: str
    db_name: str

    secret_jwt: str
    algorithm_jwt: str
    access_token_expire_minutes: int

    currency_data_api_key: str

    @property
    def get_database_url(self):
        return f'postgresql+psycopg2://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()