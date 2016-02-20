import os
import json


class Mustag:

    def __init__(self):
        self.basedir = 'c:\\mp3_experiment'
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
                    print(file_path.encode('unicode-escape'))
                    item = self.library_add(file_path, file_name)
                    self.create_music_metadata(item)

    def library_add(self, file_path, file_name):
        item = {
            'filename': file_name,
            'filepath': file_path,
            'tags': []
        }
        self.collection[file_path] = item
        return item

    def library_add_from_metafile(self, file_path):
        f = open(file_path, 'r')
        str = f.read()
        item = json.loads(str)
        self.collection[file_path] = item
        return item

    def create_music_metadata(self, item):
        metadata_filename = item['filepath'] + self.meta_extension
        f = open(metadata_filename, 'w')
        json_str = json.dumps(item)
        f.write(json_str)
        f.close()

    # when triggered: reload legal tags from file

    # show a list of all songs and the tags on them

    # show a detail view of a song with buttons to toggle each tag

    # perform screen: toggle tags and songs will be randomly selected
