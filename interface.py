#!/usr/bin/env python

import wx
import ape
import os

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

	def load(self, datactrl, namectrl, lenctrl, actrl, cctrl):
		def on_load(event):
			dlg = wx.FileDialog(self, message="Choose a file", wildcard="Plasmid files (.ape)|*.ape", style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST|wx.FD_CHANGE_DIR)
			result = dlg.ShowModal()
			if result == wx.ID_OK:
				bp = ape.readBP(os.path.join(dlg.GetDirectory(), dlg.GetFilename()))
				namectrl.SetLabel(label=dlg.GetFilename())
				lenctrl.SetLabel(label=str(len(bp)) + " base pairs")
				actrl.SetLabel(label=str(bp.count('A') + bp.count('a')) + " adenine")
				cctrl.SetLabel(label=str(bp.count('C') + bp.count('c')) + " cytosine")
				datactrl.SetValue(bp)
			dlg.Destroy()
		return on_load

	def save(self, datactrl):
		def on_save(event):
			dlg = wx.FileDialog(self, message="Choose a file", wildcard="Plasmid files (.ape)|*.ape", style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT|wx.FD_CHANGE_DIR)
			result = dlg.ShowModal()
			if result == wx.ID_OK:
				ape.writeBP(os.path.join(dlg.GetDirectory(), dlg.GetFilename()), datactrl.GetValue())
			dlg.Destroy()
		return on_save


	def CreateLayout(self):
		# Change text with wx.StaticText#SetLabel()

		templateLoadButton = wx.Button(self, label="Load Template Strand")
		templateSaveButton = wx.Button(self, label="Save Template Strand")
		templateFileName = wx.StaticText(self, label="no file", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
		templateLength = wx.StaticText(self, label="0 base pairs", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
		templateACount = wx.StaticText(self, label="0 adenine", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
		templateCCount = wx.StaticText(self, label="0 cytosine", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
		templateData = wx.TextCtrl(self, style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_CHARWRAP)

		templateLoadButton.Bind(wx.EVT_BUTTON, self.load(datactrl=templateData, namectrl=templateFileName, lenctrl=templateLength, actrl=templateACount, cctrl=templateCCount))
		templateSaveButton.Bind(wx.EVT_BUTTON, self.save(datactrl=templateData))

		templateSizer = wx.StaticBoxSizer(wx.StaticBox(self, label="Template Strand", style=wx.ALIGN_CENTER), wx.VERTICAL)
		templateSizer.Add(templateLoadButton, 0, wx.EXPAND)
		templateSizer.Add(templateSaveButton, 0, wx.EXPAND)
		templateSizer.Add(templateFileName, 0, wx.EXPAND)
		templateSizer.Add(templateLength, 0, wx.EXPAND)
		templateSizer.Add(templateACount, 0, wx.EXPAND)
		templateSizer.Add(templateCCount, 0, wx.EXPAND)
		templateSizer.Add(templateData, 1, wx.EXPAND)

		fPrimerLoadButton = wx.Button(self, label="Load Initialization Primer")
		fPrimerSaveButton = wx.Button(self, label="Save Initialization Primer")
		fPrimerFileName = wx.StaticText(self, label="no file", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
		fPrimerLength = wx.StaticText(self, label="0 base pairs", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
		fPrimerACount = wx.StaticText(self, label="0 adenine", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
		fPrimerCCount = wx.StaticText(self, label="0 cytosine", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
		fPrimerData = wx.TextCtrl(self, style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_CHARWRAP)

		fPrimerLoadButton.Bind(wx.EVT_BUTTON, self.load(datactrl=fPrimerData, namectrl=fPrimerFileName, lenctrl=fPrimerLength, actrl=fPrimerACount, cctrl=fPrimerCCount))
		fPrimerSaveButton.Bind(wx.EVT_BUTTON, self.save(datactrl=fPrimerData))

		fPrimerSizer = wx.StaticBoxSizer(wx.StaticBox(self, label="Initialization Primer", style=wx.ALIGN_CENTER), wx.VERTICAL)
		fPrimerSizer.Add(fPrimerLoadButton, 0, wx.EXPAND)
		fPrimerSizer.Add(fPrimerSaveButton, 0, wx.EXPAND)
		fPrimerSizer.Add(fPrimerFileName, 0, wx.EXPAND)
		fPrimerSizer.Add(fPrimerLength, 0, wx.EXPAND)
		fPrimerSizer.Add(fPrimerACount, 0, wx.EXPAND)
		fPrimerSizer.Add(fPrimerCCount, 0, wx.EXPAND)
		fPrimerSizer.Add(fPrimerData, 1, wx.EXPAND)

		rPrimerLoadButton = wx.Button(self, label="Load Termination Primer")
		rPrimerSaveButton = wx.Button(self, label="Save Termination Primer")
		rPrimerFileName = wx.StaticText(self, label="no file", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
		rPrimerLength = wx.StaticText(self, label="0 base pairs", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
		rPrimerACount = wx.StaticText(self, label="0 adenine", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
		rPrimerCCount = wx.StaticText(self, label="0 cytosine", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
		rPrimerData = wx.TextCtrl(self, style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_CHARWRAP)

		rPrimerLoadButton.Bind(wx.EVT_BUTTON, self.load(datactrl=rPrimerData, namectrl=rPrimerFileName, lenctrl=rPrimerLength, actrl=rPrimerACount, cctrl=rPrimerCCount))
		rPrimerSaveButton.Bind(wx.EVT_BUTTON, self.save(datactrl=rPrimerData))

		rPrimerSizer = wx.StaticBoxSizer(wx.StaticBox(self, label="Termination Primer", style=wx.ALIGN_CENTER), wx.VERTICAL)
		rPrimerSizer.Add(rPrimerLoadButton, 0, wx.EXPAND)
		rPrimerSizer.Add(rPrimerSaveButton, 0, wx.EXPAND)
		rPrimerSizer.Add(rPrimerFileName, 0, wx.EXPAND)
		rPrimerSizer.Add(rPrimerLength, 0, wx.EXPAND)
		rPrimerSizer.Add(rPrimerACount, 0, wx.EXPAND)
		rPrimerSizer.Add(rPrimerCCount, 0, wx.EXPAND)
		rPrimerSizer.Add(rPrimerData, 1, wx.EXPAND)

		outputLoadButton = wx.Button(self, label="Load PCR Output")
		outputSaveButton = wx.Button(self, label="Save PCR Output")
		outputFileName = wx.StaticText(self, label="no file", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
		outputLength = wx.StaticText(self, label="0 base pairs", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
		outputACount = wx.StaticText(self, label="0 adenine", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
		outputCCount = wx.StaticText(self, label="0 cytosine", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
		outputData = wx.TextCtrl(self, style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_CHARWRAP)

		outputLoadButton.Bind(wx.EVT_BUTTON, self.load(datactrl=outputData, namectrl=outputFileName, lenctrl=outputLength, actrl=outputACount, cctrl=outputCCount))
		outputSaveButton.Bind(wx.EVT_BUTTON, self.save(datactrl=outputData))

		outputSizer = wx.StaticBoxSizer(wx.StaticBox(self, label="PCR Output Strand", style=wx.ALIGN_CENTER), wx.VERTICAL)
		outputSizer.Add(outputLoadButton, 0, wx.EXPAND)
		outputSizer.Add(outputSaveButton, 0, wx.EXPAND)
		outputSizer.Add(outputFileName, 0, wx.EXPAND)
		outputSizer.Add(outputLength, 0, wx.EXPAND)
		outputSizer.Add(outputACount, 0, wx.EXPAND)
		outputSizer.Add(outputCCount, 0, wx.EXPAND)
		outputSizer.Add(outputData, 1, wx.EXPAND)

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