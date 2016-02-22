import wx


class SongListPanel(wx.Panel):
    def __init__(self, parent, library):
        wx.Panel.__init__(self, parent=parent)
        self.library = library
        self.song_activated_listeners = []
        sizer = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Collection:'), wx.VERTICAL)
        sizer.Add(self.create_filter_section(), 0, wx.ALL, 5)
        sizer.Add(self.create_songlist_section(), 0, wx.ALL, 5)
        self.SetSizer(sizer)
        self.populate_collection_ui()

    def create_filter_section(self):
        component = wx.CheckBox(self, label="Filter")
        return component

    def create_songlist_section(self):
        self.list_ctrl = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.list_ctrl.InsertColumn(0, 'Filename', width=500)
        self.list_ctrl.InsertColumn(1, 'Genre', width=175)
        self.list_ctrl.InsertColumn(2, 'Tags', width=125)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_activate_song_in_list, self.list_ctrl)
        return self.list_ctrl

    def on_activate_song_in_list(self, event):
        id = event.GetItem().Id
        item = self.items_by_id[id]
        for listener in self.song_activated_listeners:
            listener(item)
        event.Skip()

    def populate_collection_ui(self):
        rowix = 0
        self.items_by_id = dict()
        for item in self.library.collection.values():
            self.items_by_id[rowix] = item
            filename = item['filename']
            file_path = item['filepath']
            self.list_ctrl.InsertStringItem(rowix, filename)
            genre = item['genre']
            self.list_ctrl.SetStringItem(rowix, 1, genre)
            self.list_ctrl.SetStringItem(rowix, 2, "USA")
            rowix += 1

    def add_song_activated_listener(self, listener):
        self.song_activated_listeners.append(listener)