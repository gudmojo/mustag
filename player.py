import wx, wx.media
import wx.lib.buttons as buttons
import os

DIR_NAME = os.path.dirname(os.path.abspath(__file__))
BITMAP_DIR = os.path.join(DIR_NAME, 'bitmaps')


class PlayerPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
        try:
            self.mediaPlayer = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER, szBackend=wx.media.MEDIABACKEND_WMP10)
        except NotImplementedError:
            self.Destroy()
            raise
        self.currentVolume = 50
        self.Bind(wx.media.EVT_MEDIA_LOADED, self.on_song_is_loaded)
        self.SetSizer(self.create_player_area_sizer())
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer)
        self.timer.Start(100)

    def on_song_is_loaded(self, event):
        self.play_it()

    def on_skip_song_forward(self, event):
        pass

    def on_pause_song(self):
        self.mediaPlayer.Pause()

    def on_play_song(self, event):
        if not event.GetIsDown():
            self.on_pause_song()
            return

        self.play_it()
        event.Skip()

    def play_it(self):
        if not self.mediaPlayer.Play():
            wx.MessageBox("Unable to Play media : Unsupported format?",
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mediaPlayer.SetInitialSize()
            self.GetSizer().Layout()
            self.playbackSlider.SetRange(0, self.mediaPlayer.Length())


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

    def load_music(self, music_file):
        if not self.mediaPlayer.Load(music_file):
            wx.MessageBox("Unable to load %s: Unsupported format?" % music_file, "ERROR", wx.ICON_ERROR | wx.OK)
        else:
            self.mediaPlayer.SetInitialSize()
            self.GetSizer().Layout()
            self.playbackSlider.SetRange(0, self.mediaPlayer.Length())
            self.playPauseBtn.Enable(True)

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
