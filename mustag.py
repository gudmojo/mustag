import os
import json
import io
from eyed3 import id3


class Mustag:

    def __init__(self):
        self.basedir = u'c:\\mp3_experiment'
        self.meta_extension = '.mustag'
        self.collection = dict()

    # find all db files in basedir and load them into memory
    def load_meta_from_disk(self):
        for root, dirs, files in os.walk(self.basedir):
            for file in files:
                if file.endswith(self.meta_extension):
                    file_path = os.path.join(root, file)
                    self.library_add_from_metafile(file_path)

    # load legal tags from file, including color

    # when triggered: import music from basedir
    def import_music(self):
        for root, dirs, files in os.walk(self.basedir):
            for file_name in files:
                if file_name.endswith(".mp3"):
                    file_path = os.path.join(root, file_name)
                    #print(file_path.encode('unicode-escape'))
                    item = self.library_add(file_path, file_name)
                    self.write_metadata_to_file(item)

    def library_add(self, file_path, file_name):
        item = {
            'filename': file_name,
            'filepath': file_path,
            'tags': []
        }
        self.collection[file_path] = item
        return item

    def library_add_from_metafile(self, file_path):
        f = io.open(file_path, 'r', encoding='utf8')
        str = f.read()
        f.close()
        item = json.loads(str)
        item['genre'] = self.get_genre(item['filepath'])
        self.collection[file_path] = item
        return item

    def get_genre(self, filepath):
        try:
            tag = id3.Tag()
            tag.parse(filepath)
            genre = tag.genre.name
            return genre
        except:
            return "ERROR"

    def write_metadata_to_file(self, song):
        metadata_filename = song['filepath'] + self.meta_extension
        f = io.open(metadata_filename, 'w', encoding='utf8')
        json_str = unicode(json.dumps(song, ensure_ascii=False))
        f.write(json_str)
        f.close()

    # when triggered: reload legal tags from file

    # show a list of all songs and the tags on them

    # show a detail view of a song with buttons to toggle each tag

    # perform screen: toggle tags and songs will be randomly selected

    def load_legal_tags(self):
        f = io.open("legaltags.json", 'r', encoding='utf8')
        str = f.read()
        f.close()
        self.legal_tags = json.loads(str)

    def get_legal_tags(self):
        active = self.legal_tags['active_taglist']
        return self.legal_tags['taglists'][active]


if __name__ == "__main__":
    t = Mustag()
    t.import_music()