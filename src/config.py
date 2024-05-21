from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    API_ID: int
    API_HASH: str
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    PHONE: str
    PASSWORD: str
    DEFAULT_BIO: str
    SPOTIFY_EMOJI_STATUS_ID: int
    DEFAULT_EMOJI_STATUS_ID: int
    SCOPE: str = 'user-read-playback-state user-read-currently-playing'
    REDIRECT_URL: str = 'http://localhost:8888/callback'
    BIO_CHAR_LIMIT: int = 140


settings = Settings()
