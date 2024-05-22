from schemas import Track
from src.config import settings


def form_listening_string(track: Track):
    string = f"Listening to {track.name} by {track.artists} on Spotify:\n"
    return string + track.link if len(string + track.link) <= settings.BIO_CHAR_LIMIT else string
