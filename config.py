from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    API_ID: int
    API_HASH: str
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    PHONE: str
    PASSWORD: str
    SCOPE: str = 'user-read-playback-state user-read-currently-playing'
    REDIRECT_URL: str = 'http://localhost:8888/callback'


settings = Settings()
