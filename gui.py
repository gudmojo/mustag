#!/usr/bin/python
import wx, wx.html
import mustag
import player


class MainPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
 
        self.frame = parent
        self.create_menu()
        self.library = mustag.Mustag()
        self.library.load_legal_tags()
        self.layout_controls()
        self.library.load_meta_from_disk()
        self.populate_collection_ui()

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

    def layout_controls(self):
        self.SetSizer(self.create_main_sizer())
        self.Layout()

    def create_main_sizer(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        # layout widgets
        main_sizer.Add(self.create_top_half(), 0, wx.ALL, 5)
        main_sizer.Add(self.create_bottom_half(), 0, wx.ALL, 5)
        return main_sizer

    def create_top_half(self):
        top_half_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_half_sizer.Add(self.create_list_area_sizer(), 0, wx.ALL, 5)
        top_half_sizer.Add(self.create_song_details_area(), 0, wx.ALL, 5)
        return top_half_sizer

    def create_list_area_sizer(self):
        list_area_sizer = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Collection:'), wx.VERTICAL)
        list_area_sizer.Add(self.create_filter_section(), 0, wx.ALL, 5)
        list_area_sizer.Add(self.create_songlist_section(), 0, wx.ALL, 5)
        return list_area_sizer

    def create_song_details_area(self):
        sizer = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Song details:'), wx.VERTICAL)
        self.song_details = dict()
        self.song_details['filename'] = wx.StaticText(self, label="Filename")
        self.song_details['genre'] = wx.StaticText(self, label="Genre")
        self.song_details['tags'] = wx.StaticText(self, label="Tags of this song")
        sizer.Add(self.song_details['filename'], 0, wx.ALL, 5)
        sizer.Add(self.song_details['genre'], 0, wx.ALL, 5)
        sizer.Add(self.song_details['tags'], 0, wx.ALL, 5)
        sizer.Add(self.create_details_tag_area(), 0, wx.ALL, 5)

        return sizer

    def create_bottom_half(self):
        bottom_half_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.player_panel = player.PlayerPanel(self)
        bottom_half_sizer.Add(self.player_panel, 0, wx.ALL, 5)
        bottom_half_sizer.Add(self.create_player_taglist(), 0, wx.ALL, 5)
        return bottom_half_sizer

    def create_menu(self):
        menu_bar = wx.MenuBar()
 
        file_menu = wx.Menu()
        import_music_menu_item = file_menu.Append(wx.NewId(), "&Import music", "Import music")
        reload_settings_file_menu_item = file_menu.Append(wx.NewId(), "&Reload settings", "Reload settings")
        menu_bar.Append(file_menu, '&File')
        self.frame.SetMenuBar(menu_bar)
        self.frame.Bind(wx.EVT_MENU, self.on_import_music, import_music_menu_item)
        self.frame.Bind(wx.EVT_MENU, self.on_reload_settings_file, reload_settings_file_menu_item)

    def on_import_music(self, event):
        pass

    def on_reload_settings_file(self, event):
        pass

    def on_activate_song_in_list(self, event):
        id = event.GetItem().Id
        item = self.items_by_id[id]
        self.player_panel.load_music(item['filepath'])
        self.player_panel.playPauseBtn.SetValue(True)
        self.show_song_details(item)
        event.Skip()

    def create_filter_section(self):
        component = wx.CheckBox(self, label="Filter")
        return component

    def create_songlist_section(self):
        self.list_ctrl = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.list_ctrl.InsertColumn(0, 'Filename', width=500)
        self.list_ctrl.InsertColumn(1, 'Genre', width=175)
        self.list_ctrl.InsertColumn(2, 'Tags', width=125)
        self.frame.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_activate_song_in_list, self.list_ctrl)

        return self.list_ctrl

    def create_player_taglist(self):
        sizer = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Player taglist:'), wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="Songlist"), 0, wx.ALL, 5)
        return sizer

    def show_song_details(self, item):
        filename = item['filename']
        self.song_details['filename'].Label = filename
        genre = item['genre']
        self.song_details['genre'].Label = genre

    def create_details_tag_area(self):
        sizer = wx.GridSizer(cols=2, vgap=0, hgap=0)
        tags = self.library.get_legal_tags()
        for tag in tags:
            check_box = wx.CheckBox(self, label=tag['name'])
            sizer.Add(check_box, 0, wx.ALL, 5)
            self.frame.Bind(wx.EVT_CHECKBOX, self.on_song_details_tag_check, check_box)
        return sizer

    def on_song_details_tag_check(self, event):
        item = event.EventObject
        print item.Label + " " + str(item.Value)


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "the mustag", pos=(10,10), size=(1500,800))
        panel = MainPanel(self)


app = wx.App(redirect=False)
top = MainFrame()
top.Show()
app.MainLoop()