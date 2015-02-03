#!/usr/bin/env python

import wx
import ape

class PCRSimulatorFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, title="PCR Simulator", size=(840, 400), name="PCR Simulator")

		#self.icon = wx.Icon("res/icon.png", wx.BITMAP_TYPE_ANY)
		#self.SetIcon(self.icon)

		#self.CreateMenuBar() # Access with self.GetMenuBar()
		#self.CreateToolBar(wx.TB_HORIZONTAL|wx.TB_FLAT|wx.TB_TEXT) # Access with self.GetToolBar()
		self.CreateStatusBar() # Access with self.GetStatusBar()

		self.SetBackgroundColour(wx.WHITE)

		self.SetAutoLayout(True)
		self.CreateLayout()
		self.Layout()

		self.Show(True)


	def CreateMenuBar(self):

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


	def CreateLayout(self):
		# Change text with wx.StaticText#SetLabel()

		self.templateLoadButton = wx.Button(self, label="Load Template Strand")
		self.templateSaveButton = wx.Button(self, label="Save Template Strand")
		self.templateFileName = wx.StaticText(self, label="Empty file", style=wx.ALIGN_CENTER)
		self.templateLength = wx.StaticText(self, label="0 base pairs", style=wx.ALIGN_CENTER)
		self.templateACount = wx.StaticText(self, label="0 adenine", style=wx.ALIGN_CENTER)
		self.templateCCount = wx.StaticText(self, label="0 cytosine", style=wx.ALIGN_CENTER)
		self.templateData = wx.TextCtrl(self, style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_CHARWRAP)

		templateSizer = wx.StaticBoxSizer(wx.StaticBox(self, label="Template Strand", style=wx.ALIGN_CENTER), wx.VERTICAL)
		templateSizer.Add(self.templateLoadButton, 0, wx.EXPAND)
		templateSizer.Add(self.templateSaveButton, 0, wx.EXPAND)
		templateSizer.Add(self.templateFileName, 0, wx.EXPAND)
		templateSizer.Add(self.templateLength, 0, wx.EXPAND)
		templateSizer.Add(self.templateACount, 0, wx.EXPAND)
		templateSizer.Add(self.templateCCount, 0, wx.EXPAND)
		templateSizer.Add(self.templateData, 1, wx.EXPAND)

		self.fPrimerLoadButton = wx.Button(self, label="Load Initialization Primer")
		self.fPrimerSaveButton = wx.Button(self, label="Save Initialization Primer")
		self.fPrimerFileName = wx.StaticText(self, label="Empty file", style=wx.ALIGN_CENTER)
		self.fPrimerLength = wx.StaticText(self, label="0 base pairs", style=wx.ALIGN_CENTER)
		self.fPrimerACount = wx.StaticText(self, label="0 adenine", style=wx.ALIGN_CENTER)
		self.fPrimerCCount = wx.StaticText(self, label="0 cytosine", style=wx.ALIGN_CENTER)
		self.fPrimerData = wx.TextCtrl(self, style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_CHARWRAP)

		fPrimerSizer = wx.StaticBoxSizer(wx.StaticBox(self, label="Initialization Primer", style=wx.ALIGN_CENTER), wx.VERTICAL)
		fPrimerSizer.Add(self.fPrimerLoadButton, 0, wx.EXPAND)
		fPrimerSizer.Add(self.fPrimerSaveButton, 0, wx.EXPAND)
		fPrimerSizer.Add(self.fPrimerFileName, 0, wx.EXPAND)
		fPrimerSizer.Add(self.fPrimerLength, 0, wx.EXPAND)
		fPrimerSizer.Add(self.fPrimerACount, 0, wx.EXPAND)
		fPrimerSizer.Add(self.fPrimerCCount, 0, wx.EXPAND)
		fPrimerSizer.Add(self.fPrimerData, 1, wx.EXPAND)

		self.rPrimerLoadButton = wx.Button(self, label="Load Termination Primer")
		self.rPrimerSaveButton = wx.Button(self, label="Save Termination Primer")
		self.rPrimerFileName = wx.StaticText(self, label="Empty file", style=wx.ALIGN_CENTER)
		self.rPrimerLength = wx.StaticText(self, label="0 base pairs", style=wx.ALIGN_CENTER)
		self.rPrimerACount = wx.StaticText(self, label="0 adenine", style=wx.ALIGN_CENTER)
		self.rPrimerCCount = wx.StaticText(self, label="0 cytosine", style=wx.ALIGN_CENTER)
		self.rPrimerData = wx.TextCtrl(self, style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_CHARWRAP)

		def testfn1(event):
			self.rPrimerData.SetValue(ape.readBP('input.ape'))

		def testfn2(event):
			ape.writeBP('output.ape', self.rPrimerData.GetValue())

		self.rPrimerLoadButton.Bind(wx.EVT_BUTTON, testfn1)
		self.rPrimerSaveButton.Bind(wx.EVT_BUTTON, testfn2)

		rPrimerSizer = wx.StaticBoxSizer(wx.StaticBox(self, label="Termination Primer", style=wx.ALIGN_CENTER), wx.VERTICAL)
		rPrimerSizer.Add(self.rPrimerLoadButton, 0, wx.EXPAND)
		rPrimerSizer.Add(self.rPrimerSaveButton, 0, wx.EXPAND)
		rPrimerSizer.Add(self.rPrimerFileName, 0, wx.EXPAND)
		rPrimerSizer.Add(self.rPrimerLength, 0, wx.EXPAND)
		rPrimerSizer.Add(self.rPrimerACount, 0, wx.EXPAND)
		rPrimerSizer.Add(self.rPrimerCCount, 0, wx.EXPAND)
		rPrimerSizer.Add(self.rPrimerData, 1, wx.EXPAND)

		self.outputLoadButton = wx.Button(self, label="Load PCR Output")
		self.outputSaveButton = wx.Button(self, label="Save PCR Output")
		self.outputFileName = wx.StaticText(self, label="Empty file", style=wx.ALIGN_CENTER)
		self.outputLength = wx.StaticText(self, label="0 base pairs", style=wx.ALIGN_CENTER)
		self.outputACount = wx.StaticText(self, label="0 adenine", style=wx.ALIGN_CENTER)
		self.outputCCount = wx.StaticText(self, label="0 cytosine", style=wx.ALIGN_CENTER)
		self.outputData = wx.TextCtrl(self, style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_CHARWRAP)

		outputSizer = wx.StaticBoxSizer(wx.StaticBox(self, label="PCR Output Strand", style=wx.ALIGN_CENTER), wx.VERTICAL)
		outputSizer.Add(self.outputLoadButton, 0, wx.EXPAND)
		outputSizer.Add(self.outputSaveButton, 0, wx.EXPAND)
		outputSizer.Add(self.outputFileName, 0, wx.EXPAND)
		outputSizer.Add(self.outputLength, 0, wx.EXPAND)
		outputSizer.Add(self.outputACount, 0, wx.EXPAND)
		outputSizer.Add(self.outputCCount, 0, wx.EXPAND)
		outputSizer.Add(self.outputData, 1, wx.EXPAND)

		self.generatePrimers = wx.Button(self, label="Generate Primers")
		self.generateOutput = wx.Button(self, label="Generate PCR Output")
		self.verifyOutput = wx.Button(self, label="Verify PCR Output")

		actionSizer = wx.BoxSizer(wx.VERTICAL)
		actionSizer.AddStretchSpacer()
		actionSizer.Add(self.generatePrimers, 1, wx.EXPAND)
		actionSizer.Add(self.generateOutput, 1, wx.EXPAND)
		actionSizer.Add(self.verifyOutput, 1, wx.EXPAND)

		sizer = wx.FlexGridSizer(1, 5, 5, 5)
		sizer.AddGrowableRow(0)
		sizer.AddGrowableCol(0)
		sizer.AddGrowableCol(1)
		sizer.AddGrowableCol(2)
		sizer.AddGrowableCol(3)
		sizer.Add(templateSizer, 1, wx.EXPAND)
		sizer.Add(fPrimerSizer, 1, wx.EXPAND)
		sizer.Add(rPrimerSizer, 1, wx.EXPAND)
		sizer.Add(outputSizer, 1, wx.EXPAND)
		sizer.Add(actionSizer, 1)

		self.SetSizer(sizer)




class PCRSimulatorApp(wx.App):
	def OnInit(self):
		self.frame = PCRSimulatorFrame()
		self.frame.Show()
		self.SetTopWindow(self.frame)
		return True