import wx


class SongDetailsPanel(wx.Panel):
    def __init__(self, parent, library):
        wx.Panel.__init__(self, parent=parent)
        self.library = library
        self.selected_song = None
        self.nosong = True
        self.main_sizer = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Song details:'), wx.VERTICAL)
        dummy = "______________________________________________________________________________________________________"
        self.filename_label = wx.StaticText(self, label=dummy)
        self.genre_label = wx.StaticText(self, label=dummy)
        self.main_sizer.Add(self.filename_label, 0, wx.ALL, 5)
        self.main_sizer.Add(self.genre_label, 0, wx.ALL, 5)
        self.tags_sizer = self.create_details_tag_area()
        self.main_sizer.Add(self.tags_sizer, 0, wx.ALL, 5)
        self.SetSizer(self.main_sizer)

    def create_details_tag_area(self):
        self.checklistbox = wx.CheckListBox(self)
        self.init_checklistbox()
        self.Bind(wx.EVT_CHECKLISTBOX, self.on_tag_check, self.checklistbox)
        return self.checklistbox

    def on_tag_check(self, event):
        song = self.selected_song
        taglist = song['tags']
        for tag in self.checklistbox.Items:
            checked = tag in self.checklistbox.GetCheckedStrings()
            if checked:
                taglist.append(tag)
            else:
                while True:
                    try:
                        taglist.remove(tag)
                    except ValueError:
                        break
        self.library.write_metadata_to_file(song)
        event.Skip()

    def init_checklistbox(self):
        self.checklistbox.Clear()
        for tag in self.library.get_legal_tags():
            self.checklistbox.Append(tag['name'])
        if not self.nosong:
            self.checklistbox.SetCheckedStrings(self.selected_song['tags'])

    def show_song_details(self):
        self.nosong = False
        song = self.selected_song
        self.filename_label.Label = song['filename']
        self.genre_label.Label = song['genre']
        self.init_checklistbox()

    def on_song_activated(self, song):
        self.selected_song = song
        self.show_song_details()

    def on_legal_tags_refresh(self):
        self.init_checklistbox()
