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
import mustag

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')


class MainPanel(wx.Panel):
	""""""
 
	#----------------------------------------------------------------------
	def __init__(self, parent):
		"""Constructor"""
		wx.Panel.__init__(self, parent=parent)
 
		self.frame = parent
		self.currentVolume = 50
		self.createMenu()
		self.layoutControls()
		self.library = mustag.Mustag()
		self.library.load_meta_from_disk()
		self.loadMusic('c:\\mp3_experiment\\WALK THE MOON - Shut Up and Dance.mp3')
  
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
		import_music_menu_item = fileMenu.Append(wx.NewId(), "&Import music", "Import music")
		reload_settings_file_menu_item = fileMenu.Append(wx.NewId(), "&Reload settings", "Reload settings")
		menubar.Append(fileMenu, '&File')
		self.frame.SetMenuBar(menubar)
		self.frame.Bind(wx.EVT_MENU, self.onImportMusic, import_music_menu_item)
		self.frame.Bind(wx.EVT_MENU, self.onReloadSettingsFile, reload_settings_file_menu_item)
 
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
	def loadLibrary(self, musicFile):
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
	def onImportMusic(self, event):
		"""
		Not implemented!
		"""
		pass
 
	#----------------------------------------------------------------------
	def onReloadSettingsFile(self, event):
		"""
		Not implemented!
		"""
		pass
 
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
class MainFrame(wx.Frame):
 
	#----------------------------------------------------------------------
	def __init__(self):
		wx.Frame.__init__(self, None, wx.ID_ANY, "the mustag", pos=(10,10), size=(1500,800))
		panel = MainPanel(self)



app = wx.App(redirect=False)   # Error messages go to popup window
#top = Frame("<<project>>")
top = MainFrame()
top.Show()
app.MainLoop()