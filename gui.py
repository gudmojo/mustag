#!/usr/bin/python
import wx, wx.html
import wx.media
import wx.lib.buttons as buttons
import os
import mustag
from eyed3 import id3

DIR_NAME = os.path.dirname(os.path.abspath(__file__))
BITMAP_DIR = os.path.join(DIR_NAME, 'bitmaps')


class MainPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
 
        self.frame = parent
        self.currentVolume = 50
        self.create_menu()
        self.layout_controls()
        self.library = mustag.Mustag()
        self.library.load_meta_from_disk()
        self.populate_collection_ui()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer)
        self.timer.Start(100)

    def populate_collection_ui(self):
        rowix = 0
        self.items_by_id = dict()
        for item in self.library.collection.values():
            self.items_by_id[rowix] = item
            filename = item['filename']
            file_path = item['filepath']
            self.list_ctrl.InsertStringItem(rowix, filename)
            genre = self.get_genre(file_path)
            self.list_ctrl.SetStringItem(rowix, 1, genre)
            self.list_ctrl.SetStringItem(rowix, 2, "USA")
            rowix += 1

    def get_genre(self, filepath):
        try:
            tag = id3.Tag()
            tag.parse(filepath)
            genre = tag.genre.name
            return genre
        except:
            return "ERROR"

    def layout_controls(self):
        try:
            self.mediaPlayer = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER, szBackend=wx.media.MEDIABACKEND_WMP10)
        except NotImplementedError:
            self.Destroy()
            raise
        self.Bind(wx.media.EVT_MEDIA_LOADED, self.on_song_is_loaded)
 
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
        top_half_sizer.Add(self.create_song_details_sizer(), 0, wx.ALL, 5)
        return top_half_sizer

    def create_list_area_sizer(self):
        list_area_sizer = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Collection:'), wx.VERTICAL)
        list_area_sizer.Add(self.create_filter_section(), 0, wx.ALL, 5)
        list_area_sizer.Add(self.create_songlist_section(), 0, wx.ALL, 5)
        return list_area_sizer

    def create_song_details_sizer(self):
        sizer = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Song details:'), wx.VERTICAL)
        self.song_details = dict()
        self.song_details['filename'] = wx.StaticText(self, label="Filename")
        self.song_details['genre'] = wx.StaticText(self, label="Genre")
        self.song_details['tags'] = wx.StaticText(self, label="Tags of this song")
        sizer.Add(self.song_details['filename'], 0, wx.ALL, 5)
        sizer.Add(self.song_details['genre'], 0, wx.ALL, 5)
        sizer.Add(self.song_details['tags'], 0, wx.ALL, 5)
        return sizer

    def create_bottom_half(self):
        bottom_half_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bottom_half_sizer.Add(self.create_player_area_sizer(), 0, wx.ALL, 5)
        bottom_half_sizer.Add(self.create_player_taglist(), 0, wx.ALL, 5)
        return bottom_half_sizer

    def create_player_area_sizer(self):
        player_sizer = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Player:'), wx.VERTICAL)

        self.playbackSlider = wx.Slider(self, size=wx.DefaultSize)
        self.Bind(wx.EVT_SLIDER, self.on_seek, self.playbackSlider)

        self.volumeCtrl = wx.Slider(self, style=wx.SL_VERTICAL | wx.SL_INVERSE)
        self.volumeCtrl.SetRange(0, 100)
        self.volumeCtrl.SetValue(self.currentVolume)
        self.volumeCtrl.Bind(wx.EVT_SLIDER, self.on_set_volume)

        player_sizer.Add(self.playbackSlider, 1, wx.ALL | wx.EXPAND, 5)
        audio_sizer = self.build_audio_bar()
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h_sizer.Add(audio_sizer, 0, wx.ALL|wx.CENTER, 5)
        h_sizer.Add(self.volumeCtrl, 0, wx.ALL, 5)
        player_sizer.Add(h_sizer)
        return player_sizer

    def build_audio_bar(self):
        audio_bar_sizer = wx.BoxSizer(wx.HORIZONTAL)
 
        self.build_btn({'bitmap': 'player_prev.png', 'handler': self.on_skip_prev_song, 'name': 'prev'},
                       audio_bar_sizer)
 
        # create play/pause toggle button
        img = wx.Bitmap(os.path.join(BITMAP_DIR, "player_play.png"))
        self.playPauseBtn = buttons.GenBitmapToggleButton(self, bitmap=img, name="play")
        self.playPauseBtn.Enable(False)
 
        img = wx.Bitmap(os.path.join(BITMAP_DIR, "player_pause.png"))
        self.playPauseBtn.SetBitmapSelected(img)
        self.playPauseBtn.SetInitialSize()
 
        self.playPauseBtn.Bind(wx.EVT_BUTTON, self.on_play_song)
        audio_bar_sizer.Add(self.playPauseBtn, 0, wx.LEFT, 3)
 
        btn_data = [{'bitmap': 'player_stop.png',
                    'handler': self.on_stop, 'name': 'stop'},
                    {'bitmap': 'player_next.png',
                     'handler': self.on_skip_song_forward, 'name': 'next'}]
        for btn in btn_data:
            self.build_btn(btn, audio_bar_sizer)
 
        return audio_bar_sizer

    def build_btn(self, btn_dict, sizer):
        bmp = btn_dict['bitmap']
        handler = btn_dict['handler']
 
        img = wx.Bitmap(os.path.join(BITMAP_DIR, bmp))
        btn = buttons.GenBitmapButton(self, bitmap=img, name=btn_dict['name'])
        btn.SetInitialSize()
        btn.Bind(wx.EVT_BUTTON, handler)
        sizer.Add(btn, 0, wx.LEFT, 3)

    def create_menu(self):
        menu_bar = wx.MenuBar()
 
        file_menu = wx.Menu()
        import_music_menu_item = file_menu.Append(wx.NewId(), "&Import music", "Import music")
        reload_settings_file_menu_item = file_menu.Append(wx.NewId(), "&Reload settings", "Reload settings")
        menu_bar.Append(file_menu, '&File')
        self.frame.SetMenuBar(menu_bar)
        self.frame.Bind(wx.EVT_MENU, self.on_import_music, import_music_menu_item)
        self.frame.Bind(wx.EVT_MENU, self.on_reload_settings_file, reload_settings_file_menu_item)

    def load_music(self, music_file):
        if not self.mediaPlayer.Load(music_file):
            wx.MessageBox("Unable to load %s: Unsupported format?" % music_file, "ERROR", wx.ICON_ERROR | wx.OK)
        else:
            self.mediaPlayer.SetInitialSize()
            self.GetSizer().Layout()
            self.playbackSlider.SetRange(0, self.mediaPlayer.Length())
            self.playPauseBtn.Enable(True)

    def on_import_music(self, event):
        pass

    def on_reload_settings_file(self, event):
        pass
 
    def on_skip_song_forward(self, event):
        pass

    def on_pause_song(self):
        self.mediaPlayer.Pause()

    def on_play_song(self, event):
        if not event.GetIsDown():
            self.on_pause_song()
            return

        if not self.mediaPlayer.Play():
            wx.MessageBox("Unable to Play media : Unsupported format?",
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mediaPlayer.SetInitialSize()
            self.GetSizer().Layout()
            self.playbackSlider.SetRange(0, self.mediaPlayer.Length())
 
        event.Skip()

    def on_song_is_loaded(self, event):
        self.mediaPlayer.Play()
 
    def on_skip_prev_song(self, event):
        pass

    def on_seek(self, event):
        offset = self.playbackSlider.GetValue()
        self.mediaPlayer.Seek(offset)
 
    def on_set_volume(self, event):
        self.currentVolume = self.volumeCtrl.GetValue()
        print "setting volume to: %s" % int(self.currentVolume)
        self.mediaPlayer.SetVolume(self.currentVolume)
 
    def on_stop(self, event):
        self.mediaPlayer.Stop()
        self.playPauseBtn.SetToggle(False)
 
    def on_timer(self, event):
        # Keep the player slider updated
        offset = self.mediaPlayer.Tell()
        self.playbackSlider.SetValue(offset)

    def on_activate_song_in_list(self, event):
        id = event.GetItem().Id
        item = self.items_by_id[id]
        self.load_music(item['filepath'])
        self.playPauseBtn.SetValue(True)
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
        self.song_details['filename'].Label = item['filename']
        self.song_details['genre'].Label = item['genre']


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "the mustag", pos=(10,10), size=(1500,800))
        panel = MainPanel(self)


app = wx.App(redirect=False)
top = MainFrame()
top.Show()
app.MainLoop()