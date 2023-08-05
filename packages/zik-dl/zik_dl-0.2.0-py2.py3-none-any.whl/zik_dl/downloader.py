import shutil
from .arguments import Arguments
from yt_dlp import main as ytdlp
from .settings import TMP_DIR


class Downloader:
    def __init__(self, args: Arguments):
        self.args = args

    def download(self):
        shutil.rmtree(TMP_DIR, ignore_errors=True)
        try:
            ytdlp(["-x", "-o", TMP_DIR + r"%(title)s.%(ext)s", self.args.url])
        except SystemExit as e:
            if e.code != 0:
                raise e
