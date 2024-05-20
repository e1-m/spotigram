from time import sleep
from spotify import SpotifyClient
from telethon import TelegramClient


def main():
    spotify_client = SpotifyClient()
    while True:
        sleep(1)


if __name__ == '__main__':
    main()
