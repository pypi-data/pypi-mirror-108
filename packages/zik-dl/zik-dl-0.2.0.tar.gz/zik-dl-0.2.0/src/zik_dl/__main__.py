from .arguments import Arguments
from .downloader import Downloader
from .files_manager import FilesManager


def main(argv=None):
    args = Arguments(argv)
    args.check()
    Downloader(args).download()
    FilesManager(args).manage()
