from argparse import ArgumentParser
from dataclasses import dataclass


@dataclass(init=False)
class Arguments:
    url: str = None
    artist: str = None
    album: str = None

    def __init__(self, argv=None):
        parser = ArgumentParser(
            description="Command-line program to download music from YouTube and other websites."
        )
        parser.add_argument("url", help="URL of the song/album to download")
        parser.add_argument("--artist", help="artist name")
        parser.add_argument("--album", help="album name")

        args = parser.parse_args(argv)
        self.url = args.url
        if args.artist:
            self.artist = args.artist
        if args.album:
            self.album = args.album

    def check(self):
        """
        Checks the value and compatibility of arguments.
        """
        # Nothing todo yet
