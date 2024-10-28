from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    TELEGRAM_API_ID: int
    TELEGRAM_API_HASH: str

    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str

    PHONE: str
    PASSWORD: str

    DEFAULT_BIO: str = ''
    DEFAULT_EMOJI_STATUS_ID: int = 0
    SPOTIFY_EMOJI_STATUS_ID: int = 5346074681004801565

    CHECK_TRACK_PERIOD: int = 3

    SESSIONS_PATH: str = 'sessions/'
    SCOPE: str = 'user-read-playback-state user-read-currently-playing'
    REDIRECT_URL: str = 'http://localhost:8888/callback'
    BIO_CHAR_LIMIT: int = 140

    USE_TRAY: bool


settings = Settings()
