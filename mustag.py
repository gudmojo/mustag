import os
import codecs
import sys
import json

class Mustag:

	def __init__(self):
		self.basedir = 'c:\\mp3_experiment'
		self.meta_extension = '.mustag'
		self.library = dict()

	# find all db files in basedir and load them into memory
	def load_meta_from_disk(self):
		for root, dirs, files in os.walk(self.basedir):
			for file in files:
				if file.endswith(self.meta_extension):
					filepath = os.path.join(root, file)
					self.library_add(filepath, file)

	# load legal tags from file, including color

	# when triggered: import music from basedir
	def import_music(self):
		for root, dirs, files in os.walk(self.basedir):
			for file in files:
				if file.endswith(".mp3"):
					filepath = os.path.join(root, file)
					print(filepath.encode('unicode-escape'))
					item = self.library_add(filepath, file)
					self.create_metamusic(item)

	def library_add(self, filepath, file):
		item = {
			'filename': file,
			'filepath': filepath,
			'tags': []
		}
		self.library[filepath] = item
		return item

	def create_metamusic(self, item):
		metafilename = item['filepath'] + self.meta_extension
		f = open(metafilename, 'w')
		jsonstr = json.dumps(item)
		f.write(jsonstr)
		f.close()

	# when triggered: reload legal tags from file

	# show a list of all songs and the tags on them

	# show a detail view of a song with buttons to toggle each tag

	# perform screen: toggle tags and songs will be randomly selected
