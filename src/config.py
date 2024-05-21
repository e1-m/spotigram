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
    SCOPE: str = 'user-read-playback-state user-read-currently-playing'
    REDIRECT_URL: str = 'http://localhost:8888/callback'
    SPOTIFY_EMOJI_STATUS_ID: int = 5346074681004801565
    DEFAULT_EMOJI_STATUS_ID: int = 0


settings = Settings()
