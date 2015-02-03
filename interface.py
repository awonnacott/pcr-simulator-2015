#!/usr/bin/env python

import wx

class PCRSimulatorFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, title="PCR Simulator", size=(640, 480), name="PCR Simulator")

		#self.icon = wx.Icon("res/icon.png", wx.BITMAP_TYPE_ANY)
		#self.SetIcon(self.icon)

		self.CreateMenuBar() # Access with self.GetMenuBar()
		self.CreateToolBar(wx.TB_HORIZONTAL|wx.TB_FLAT|wx.TB_TEXT) # Access with self.GetToolBar()
		self.CreateStatusBar() # Access with self.GetStatusBar()

		self.SetBackgroundColour(wx.WHITE)

		self.Show(True)


	def CreateMenuBar(self):
		menuFile       = wx.Menu()
		menuFileNew    = menuFile.Append(wx.ID_NEW,             "&New",            "Start a file")
		menuFileOpen   = menuFile.Append(wx.ID_OPEN,            "&Open",           "Open a file")
		menuFileRevert = menuFile.Append(wx.ID_REVERT_TO_SAVED, "Revert to Saved", "Destroy changes since the previous save")
		menuFileSave   = menuFile.Append(wx.ID_SAVE,            "&Save",           "Save this file")
		menuFileSaveAs = menuFile.Append(wx.ID_SAVEAS,          "Save &As...",     "Save this file with a new name")
		menuFileExit   = menuFile.Append(wx.ID_EXIT,            "&Exit",           "Terminate the program")
		menuFile.Bind(wx.EVT_MENU, self.onNew,    menuFileNew)
		menuFile.Bind(wx.EVT_MENU, self.onOpen,   menuFileOpen)
		menuFile.Bind(wx.EVT_MENU, self.onRevert, menuFileRevert)
		menuFile.Bind(wx.EVT_MENU, self.onSave,   menuFileSave)
		menuFile.Bind(wx.EVT_MENU, self.onSaveAs, menuFileSaveAs)
		menuFile.Bind(wx.EVT_MENU, self.onExit,   menuFileExit)

		menuEdit = wx.Menu()

		menuView = wx.Menu()

		menuBar = wx.MenuBar()
		menuBar.Append(menuFile, "&File")
		menuBar.Append(menuEdit, "&Edit")
		menuBar.Append(menuView, "&View")
		self.SetMenuBar(menuBar)

		return menuBar

	def onNew(self, event):
		return True

	def onOpen(self, event):
		return True

	def onRevert(self, event):
		return True

	def onSave(self, event):
		return True

	def onSaveAs(self, event):
		return True

	def onExit(self, event):
		return True

class PCRSimulatorApp(wx.App):
	def OnInit(self):
		self.mainFrame = PCRSimulatorFrame()
		self.mainFrame.Show()
		self.SetTopWindow(self.mainFrame)
		return True