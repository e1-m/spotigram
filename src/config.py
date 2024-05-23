from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    # Telegram app API ID and hash
    API_ID: int
    API_HASH: str

    # Spotify app Client ID and secret
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str

    # Telegram credentials
    PHONE: str
    PASSWORD: str

    DEFAULT_BIO: str
    DEFAULT_EMOJI_STATUS_ID: int
    SPOTIFY_EMOJI_STATUS_ID: int

    CHECK_TRACK_PERIOD: int

    SCOPE: str = 'user-read-playback-state user-read-currently-playing'
    REDIRECT_URL: str = 'http://localhost:8888/callback'
    BIO_CHAR_LIMIT: int = 140


settings = Settings()
