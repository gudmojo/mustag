#!/usr/bin/python
# -*- coding: <<encoding>> -*-
#-------------------------------------------------------------------------------
#   <<project>>
# 
#-------------------------------------------------------------------------------

import wx, wx.html
import sys
import wx.media
import wx.lib.buttons as buttons
import os

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')

aboutText = """<p>Sorry, there is no information about this program. It is
running on version %(wxpy)s of <b>wxPython</b> and %(python)s of <b>Python</b>.
See <a href="http://wiki.wxpython.org">wxPython Wiki</a></p>""" 

class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, size=(600,400)):
        wx.html.HtmlWindow.__init__(self,parent, id, size=size)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())
        
class AboutBox(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "About <<project>>",
            style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|
                wx.TAB_TRAVERSAL)
        hwin = HtmlWindow(self, -1, size=(400,200))
        vers = {}
        vers["python"] = sys.version.split()[0]
        vers["wxpy"] = wx.VERSION_STRING
        hwin.SetPage(aboutText % vers)
        btn = hwin.FindWindowById(wx.ID_OK)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth()+25, irep.GetHeight()+10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()

class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, pos=(150,150), size=(350,200))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        menuBar = wx.MenuBar()
        menu = wx.Menu()
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.OnClose, m_exit)
        menuBar.Append(menu, "&File")
        menu = wx.Menu()
        m_about = menu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, m_about)
        menuBar.Append(menu, "&Help")
        self.SetMenuBar(menuBar)
        
        self.statusbar = self.CreateStatusBar()

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        
        m_text = wx.StaticText(panel, -1, "Hello World!")
        m_text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        m_text.SetSize(m_text.GetBestSize())
        box.Add(m_text, 0, wx.ALL, 10)
        
        m_close = wx.Button(panel, wx.ID_CLOSE, "Close")
        m_close.Bind(wx.EVT_BUTTON, self.OnClose)
        box.Add(m_close, 0, wx.ALL, 10)
        
        panel.SetSizer(box)
        panel.Layout()

    def OnClose(self, event):
        dlg = wx.MessageDialog(self, 
            "Do you really want to close this application?",
            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()

    def OnAbout(self, event):
        dlg = AboutBox()
        dlg.ShowModal()
        dlg.Destroy()  

		
		
		
		
		
		
		
		
		
		
		
class MediaPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
 
        self.frame = parent
        self.currentVolume = 50
        self.createMenu()
        self.layoutControls()
 
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()
 
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer)
        self.timer.Start(100)
 
    #----------------------------------------------------------------------
    def layoutControls(self):
        """
        Create and layout the widgets
        """
 
        try:
            self.mediaPlayer = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER)
        except NotImplementedError:
            self.Destroy()
            raise
 
        # create playback slider
        self.playbackSlider = wx.Slider(self, size=wx.DefaultSize)
        self.Bind(wx.EVT_SLIDER, self.onSeek, self.playbackSlider)
 
        self.volumeCtrl = wx.Slider(self, style=wx.SL_VERTICAL|wx.SL_INVERSE)
        self.volumeCtrl.SetRange(0, 100)
        self.volumeCtrl.SetValue(self.currentVolume)
        self.volumeCtrl.Bind(wx.EVT_SLIDER, self.onSetVolume)
 
        # Create sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        audioSizer = self.buildAudioBar()
 
        # layout widgets
        mainSizer.Add(self.playbackSlider, 1, wx.ALL|wx.EXPAND, 5)
        hSizer.Add(audioSizer, 0, wx.ALL|wx.CENTER, 5)
        hSizer.Add(self.volumeCtrl, 0, wx.ALL, 5)
        mainSizer.Add(hSizer)
 
        self.SetSizer(mainSizer)
        self.Layout()
 
    #----------------------------------------------------------------------
    def buildAudioBar(self):
        """
        Builds the audio bar controls
        """
        audioBarSizer = wx.BoxSizer(wx.HORIZONTAL)
 
        self.buildBtn({'bitmap':'player_prev.png', 'handler':self.onPrev,
                       'name':'prev'},
                      audioBarSizer)
 
        # create play/pause toggle button
        img = wx.Bitmap(os.path.join(bitmapDir, "player_play.png"))
        self.playPauseBtn = buttons.GenBitmapToggleButton(self, bitmap=img, name="play")
        self.playPauseBtn.Enable(False)
 
        img = wx.Bitmap(os.path.join(bitmapDir, "player_pause.png"))
        self.playPauseBtn.SetBitmapSelected(img)
        self.playPauseBtn.SetInitialSize()
 
        self.playPauseBtn.Bind(wx.EVT_BUTTON, self.onPlay)
        audioBarSizer.Add(self.playPauseBtn, 0, wx.LEFT, 3)
 
        btnData = [{'bitmap':'player_stop.png',
                    'handler':self.onStop, 'name':'stop'},
                    {'bitmap':'player_next.png',
                     'handler':self.onNext, 'name':'next'}]
        for btn in btnData:
            self.buildBtn(btn, audioBarSizer)
 
        return audioBarSizer
 
    #----------------------------------------------------------------------
    def buildBtn(self, btnDict, sizer):
        """"""
        bmp = btnDict['bitmap']
        handler = btnDict['handler']
 
        img = wx.Bitmap(os.path.join(bitmapDir, bmp))
        btn = buttons.GenBitmapButton(self, bitmap=img, name=btnDict['name'])
        btn.SetInitialSize()
        btn.Bind(wx.EVT_BUTTON, handler)
        sizer.Add(btn, 0, wx.LEFT, 3)
 
    #----------------------------------------------------------------------
    def createMenu(self):
        """
        Creates a menu
        """
        menubar = wx.MenuBar()
 
        fileMenu = wx.Menu()
        open_file_menu_item = fileMenu.Append(wx.NewId(), "&Open", "Open a File")
        menubar.Append(fileMenu, '&File')
        self.frame.SetMenuBar(menubar)
        self.frame.Bind(wx.EVT_MENU, self.onBrowse, open_file_menu_item)
 
    #----------------------------------------------------------------------
    def loadMusic(self, musicFile):
        """
        Load the music into the MediaCtrl or display an error dialog
        if the user tries to load an unsupported file type
        """
        if not self.mediaPlayer.Load(musicFile):
            wx.MessageBox("Unable to load %s: Unsupported format?" % musicFile,
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mediaPlayer.SetInitialSize()
            self.GetSizer().Layout()
            self.playbackSlider.SetRange(0, self.mediaPlayer.Length())
            self.playPauseBtn.Enable(True)
 
    #----------------------------------------------------------------------
    def onBrowse(self, event):
        """
        Opens file dialog to browse for music
        """
        wildcard = "MP3 (*.mp3)|*.mp3|"     \
                   "WAV (*.wav)|*.wav"
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.currentFolder, 
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.currentFolder = os.path.dirname(path)
            self.loadMusic(path)
        dlg.Destroy()
 
    #----------------------------------------------------------------------
    def onNext(self, event):
        """
        Not implemented!
        """
        pass
 
    #----------------------------------------------------------------------
    def onPause(self):
        """
        Pauses the music
        """
        self.mediaPlayer.Pause()
 
    #----------------------------------------------------------------------
    def onPlay(self, event):
        """
        Plays the music
        """
        if not event.GetIsDown():
            self.onPause()
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
 
    #----------------------------------------------------------------------
    def onPrev(self, event):
        """
        Not implemented!
        """
        pass
 
    #----------------------------------------------------------------------
    def onSeek(self, event):
        """
        Seeks the media file according to the amount the slider has
        been adjusted.
        """
        offset = self.playbackSlider.GetValue()
        self.mediaPlayer.Seek(offset)
 
    #----------------------------------------------------------------------
    def onSetVolume(self, event):
        """
        Sets the volume of the music player
        """
        self.currentVolume = self.volumeCtrl.GetValue()
        print "setting volume to: %s" % int(self.currentVolume)
        self.mediaPlayer.SetVolume(self.currentVolume)
 
    #----------------------------------------------------------------------
    def onStop(self, event):
        """
        Stops the music and resets the play button
        """
        self.mediaPlayer.Stop()
        self.playPauseBtn.SetToggle(False)
 
    #----------------------------------------------------------------------
    def onTimer(self, event):
        """
        Keeps the player slider updated
        """
        offset = self.mediaPlayer.Tell()
        self.playbackSlider.SetValue(offset)
 
########################################################################
class MediaFrame(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Python Music Player")
        panel = MediaPanel(self)
		
		
		
app = wx.App(redirect=False)   # Error messages go to popup window
#top = Frame("<<project>>")
top = MediaFrame()
top.Show()
app.MainLoop()