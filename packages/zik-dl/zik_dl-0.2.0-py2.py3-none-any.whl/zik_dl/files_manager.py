import os
import shutil
import music_tag
from .arguments import Arguments
from .settings import TMP_DIR, UNKNOWN


class FilesManager:
    def __init__(self, args: Arguments):
        self.args = args

    def manage(self):
        for filename in os.listdir(TMP_DIR):
            filepath = os.path.join(TMP_DIR, filename)
            song_name = os.path.splitext(filename)[0]
            f = music_tag.load_file(filepath)
            f["title"] = song_name
            f["artist"] = self.args.artist
            f["album"] = self.args.album
            f.save()
            dest_dir = f"./{self.args.artist or UNKNOWN}/{self.args.album or UNKNOWN}"
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(filepath, os.path.join(dest_dir, filename))
