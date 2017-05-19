import eyed3

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
        mp3.tag.save(version=self.id3_version)
