import eyed3
from vagalume import lyrics

class Mp3Tagger:
    def __init__(self, path, title, artist, genre, id3_version=(2,3,0)):
        self.path = path
        self.title = title
        self.artist = artist
        self.genre = genre
        self.id3_version = id3_version

    def edit_tags(self):
        mp3 = eyed3.load(self.path)
        mp3.tag.title = self.title
        mp3.tag.artist = self.artist
        mp3.tag.genre = self.genre
        mp3.tag.lyrics.set(self._get_lyric())
        mp3.tag.save(version=self.id3_version)

    def _get_lyric(self):
        result = lyrics.find(self.artist, self.title)
        if result.is_not_found():
            return ''
        else:
            return result.song.lyric
