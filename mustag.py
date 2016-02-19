import os
import codecs
import sys
import json

basedir = 'c:\\mp3_experiment'
meta_extension = '.mustag'

library = dict()

# find all db files in basedir and load them into memory
def load_meta_from_disk():
    for root, dirs, files in os.walk(basedir):
        for file in files:
            if file.endswith(meta_extension):
                filepath = os.path.join(root, file)
                library_add(filepath, file)

# load legal tags from file, including color

# when triggered: import music from basedir
def import_music():
    for root, dirs, files in os.walk(basedir):
        for file in files:
            if file.endswith(".mp3"):
                filepath = os.path.join(root, file)
                print(filepath.encode('unicode-escape'))
                item = library_add(filepath, file)
                create_metamusic(item)

def library_add(filepath, file):
    item = {
        'filename': file,
        'filepath': filepath,
        'tags': []
    }
    library[filepath] = item
    return item

def create_metamusic(item):
    metafilename = item['filepath'] + meta_extension
    f = open(metafilename, 'w')
    jsonstr = json.dumps(item)
    f.write(jsonstr)
    f.close()

# when triggered: reload legal tags from file

# show a list of all songs and the tags on them

# show a detail view of a song with buttons to toggle each tag

# perform screen: toggle tags and songs will be randomly selected



# temp hack bootstrap
load_meta_from_disk()
print(json.dumps(library))