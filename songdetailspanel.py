import wx


class SongDetailsPanel(wx.Panel):
    def __init__(self, parent, library):
        wx.Panel.__init__(self, parent=parent)
        self.library = library
        self.selected_song = None
        sizer = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Song details:'), wx.VERTICAL)
        self.filename_label = wx.StaticText(self, label="Filename")
        self.genre_label = wx.StaticText(self, label="Genre")
        sizer.Add(self.filename_label, 0, wx.ALL, 5)
        sizer.Add(self.genre_label, 0, wx.ALL, 5)
        sizer.Add(self.create_details_tag_area(), 0, wx.ALL, 5)
        self.SetSizer(sizer)

    def create_details_tag_area(self):
        sizer = wx.GridSizer(cols=2, vgap=0, hgap=0)
        tags = self.library.get_legal_tags()
        self.tag_checkboxes = dict()
        for tag in tags:
            tagname = tag['name']
            check_box = wx.CheckBox(self, label=tagname)
            self.tag_checkboxes[tagname] = check_box
            sizer.Add(check_box, 0, wx.ALL, 5)
            self.Bind(wx.EVT_CHECKBOX, self.on_song_details_tag_check, check_box)
        return sizer

    def show_song_details(self):
        song = self.selected_song
        self.filename_label.Label = song['filename']
        self.genre_label.Label = song['genre']
        for checkbox in self.tag_checkboxes.values():
            checkbox.Value = checkbox.Label in self.selected_song['tags']

    def on_song_details_tag_check(self, event):
        checkbox_ctrl = event.EventObject
        tag = checkbox_ctrl.Label
        checked = checkbox_ctrl.Value
        song = self.selected_song
        taglist = song['tags']
        if checked:
            taglist.append(tag)
        else:
            while True:
                try:
                    taglist.remove(tag)
                except ValueError:
                    break
        self.library.write_metadata_to_file(song)

    def on_song_activated(self, song):
        self.selected_song = song
        self.show_song_details()
