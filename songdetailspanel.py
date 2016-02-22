import wx


class SongDetailsPanel(wx.Panel):
    def __init__(self, parent, library):
        wx.Panel.__init__(self, parent=parent)
        self.library = library
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
        for tag in tags:
            check_box = wx.CheckBox(self, label=tag['name'])
            sizer.Add(check_box, 0, wx.ALL, 5)
            self.Bind(wx.EVT_CHECKBOX, self.on_song_details_tag_check, check_box)
        return sizer

    def show_song_details(self, song):
        self.filename_label.Label = song['filename']
        self.genre_label.Label = song['genre']

    def on_song_details_tag_check(self, event):
        checkbox_ctrl = event.EventObject
        print checkbox_ctrl.Label + " " + str(checkbox_ctrl.Value)

    def on_song_activated(self, song):
        self.show_song_details(song)
