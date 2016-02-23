#!/usr/bin/python
import wx, wx.html
import mustag
import playerpanel
import songdetailspanel
import songlistpanel


class MainPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
        self.create_menu()
        self.library = mustag.Mustag()
        self.library.load_legal_tags()
        self.library.load_meta_from_disk()
        self.SetSizer(self.create_main_sizer())
        self.song_activated_listeners = []
        self.add_song_activated_listener(self.player_panel.on_song_activated)
        self.add_song_activated_listener(self.song_details_panel.on_song_activated)
        self.legal_tags_refresh_listeners = []
        self.add_legal_tags_refresh_listeners(self.player_panel.on_legal_tags_refresh)
        self.add_legal_tags_refresh_listeners(self.song_details_panel.on_legal_tags_refresh)
        self.Layout()

    def add_song_activated_listener(self, listener):
        self.song_activated_listeners.append(listener)

    def add_legal_tags_refresh_listeners(self, listener):
        self.legal_tags_refresh_listeners.append(listener)

    def activate_song_handler(self, song):
        for listener in self.song_activated_listeners:
            listener(song)

    def legal_tags_refresh(self):
        for listener in self.legal_tags_refresh_listeners:
            listener()


    def create_main_sizer(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.create_top_half(), 0, wx.ALL, 5)
        self.player_panel = playerpanel.PlayerPanel(self, self.library, self.activate_song_handler)
        main_sizer.Add(self.player_panel, 0, wx.ALL, 5)
        return main_sizer

    def create_top_half(self):
        top_half_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.song_list_panel = songlistpanel.SongListPanel(self, self.library, self.activate_song_handler)
        top_half_sizer.Add(self.song_list_panel, 0, wx.ALL, 5)
        self.song_details_panel = songdetailspanel.SongDetailsPanel(self, self.library)
        top_half_sizer.Add(self.song_details_panel, 0, wx.ALL, 5)
        return top_half_sizer

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
        self.library.load_legal_tags()
        self.legal_tags_refresh()

    def create_player_taglist(self):
        sizer = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Player taglist:'), wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="Songlist"), 0, wx.ALL, 5)
        return sizer


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "the mustag", pos=(10,10), size=(1500,800))
        panel = MainPanel(self)


app = wx.App(redirect=False)
top = MainFrame()
top.Show()
app.MainLoop()