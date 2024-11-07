from track import Track
from config import settings


def build_listening_string(track: Track) -> str:
    string_without_link = f"Listening to {track.name} by {track.artists} on Spotify"
    string_with_link = string_without_link + ":\n" + track.link

    if len(string_with_link) <= settings.BIO_CHAR_LIMIT:
        return string_with_link
    elif len(string_without_link) <= settings.BIO_CHAR_LIMIT:
        return string_without_link
    else:
        return f"Listening to {track.name} on Spotify"
