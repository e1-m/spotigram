from schemas import Track
from src.config import settings


def get_listening_to_track_string(track: Track) -> str:
    string_without_link = f"Listening to {track.name} by {track.artists} on Spotify"
    string_with_link = string_without_link + ":\n" + track.link
    return string_with_link if len(string_with_link) <= settings.BIO_CHAR_LIMIT else string_without_link
