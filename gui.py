#!/usr/bin/python
import wx, wx.html
import wx.media
import wx.lib.buttons as buttons
import os
import mustag

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')


class MainPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
 
        self.frame = parent
        self.currentVolume = 50
        self.create_menu()
        self.layout_controls()
        self.library = mustag.Mustag()
        self.library.load_meta_from_disk()
        self.load_music('c:\\mp3_experiment\\WALK THE MOON - Shut Up and Dance.mp3')
  
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer)
        self.timer.Start(100)
 
    def layout_controls(self):
        try:
            self.mediaPlayer = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER)
        except NotImplementedError:
            self.Destroy()
            raise
 
        # create playback slider
        self.playbackSlider = wx.Slider(self, size=wx.DefaultSize)
        self.Bind(wx.EVT_SLIDER, self.on_seek, self.playbackSlider)
 
        self.volumeCtrl = wx.Slider(self, style=wx.SL_VERTICAL|wx.SL_INVERSE)
        self.volumeCtrl.SetRange(0, 100)
        self.volumeCtrl.SetValue(self.currentVolume)
        self.volumeCtrl.Bind(wx.EVT_SLIDER, self.on_set_volume)
 
        # Create sizers
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        audioSizer = self.build_audio_bar()
 
        # layout widgets
        main_sizer.Add(self.playbackSlider, 1, wx.ALL|wx.EXPAND, 5)
        h_sizer.Add(audioSizer, 0, wx.ALL|wx.CENTER, 5)
        h_sizer.Add(self.volumeCtrl, 0, wx.ALL, 5)
        main_sizer.Add(h_sizer)
 
        self.SetSizer(main_sizer)
        self.Layout()

    def build_audio_bar(self):
        audio_bar_sizer = wx.BoxSizer(wx.HORIZONTAL)
 
        self.build_btn({'bitmap': 'player_prev.png', 'handler': self.on_skip_prev_song, 'name': 'prev'}, audio_bar_sizer)
 
        # create play/pause toggle button
        img = wx.Bitmap(os.path.join(bitmapDir, "player_play.png"))
        self.playPauseBtn = buttons.GenBitmapToggleButton(self, bitmap=img, name="play")
        self.playPauseBtn.Enable(False)
 
        img = wx.Bitmap(os.path.join(bitmapDir, "player_pause.png"))
        self.playPauseBtn.SetBitmapSelected(img)
        self.playPauseBtn.SetInitialSize()
 
        self.playPauseBtn.Bind(wx.EVT_BUTTON, self.on_play_song)
        audio_bar_sizer.Add(self.playPauseBtn, 0, wx.LEFT, 3)
 
        btn_data = [{'bitmap':'player_stop.png',
                    'handler':self.on_stop, 'name': 'stop'},
                    {'bitmap':'player_next.png',
                     'handler':self.on_skip_song_forward, 'name': 'next'}]
        for btn in btn_data:
            self.build_btn(btn, audio_bar_sizer)
 
        return audio_bar_sizer

    def build_btn(self, btnDict, sizer):
        bmp = btnDict['bitmap']
        handler = btnDict['handler']
 
        img = wx.Bitmap(os.path.join(bitmapDir, bmp))
        btn = buttons.GenBitmapButton(self, bitmap=img, name=btnDict['name'])
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

    def load_library(self, musicFile):
        if not self.mediaPlayer.Load(musicFile):
            wx.MessageBox("Unable to load %s: Unsupported format?" % musicFile,
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
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
 

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "the mustag", pos=(10,10), size=(1500,800))
        panel = MainPanel(self)


app = wx.App(redirect=False)
top = MainFrame()
top.Show()
app.MainLoop()