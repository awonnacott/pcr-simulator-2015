#!/usr/bin/env python

import wx
import ape
import os
import genomics

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

	def load(self, onWrite, nameCtrl):
		def onLoad(event):
			dlg = wx.FileDialog(self, message="Choose a file", wildcard="Plasmid files (.ape, .str)|*.ape;*.str", style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST|wx.FD_CHANGE_DIR)
			result = dlg.ShowModal()
			if result == wx.ID_OK:
				onWrite(bp=ape.readBP(os.path.join(dlg.GetDirectory(), dlg.GetFilename())))
				nameCtrl.SetLabel(label=dlg.GetFilename())
			dlg.Destroy()
		return onLoad

	def save(self, dataCtrl):
		def onSave(event):
			dlg = wx.FileDialog(self, message="Choose a file", wildcard="Plasmid files (.ape, .str)|*.ape;*.str", style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT|wx.FD_CHANGE_DIR)
			result = dlg.ShowModal()
			if result == wx.ID_OK:
				ape.writeBP(filename=os.path.join(dlg.GetDirectory(), dlg.GetFilename()), bp=dataCtrl.GetValue())
			dlg.Destroy()
		return onSave

	def writeCtrl(self, dataCtrl, nameCtrl, lengthCtrl, aCtrl, cCtrl):
		def onWrite(bp):
			nameCtrl.SetLabel("unsaved file")
			lengthCtrl.SetLabel(label=str(len(bp)) + " base pairs")
			aCtrl.SetLabel(label=str(bp.count('A') + bp.count('a')) + " adenine")
			cCtrl.SetLabel(label=str(bp.count('C') + bp.count('c')) + " cytosine")
			dataCtrl.SetValue(value=bp)
		return onWrite

	def generatePrimers(self, templateDataCtrl, outputDataCtrl, fPrimerOnWrite, rPrimerOnWrite):
		def onGeneratePrimers(event):
			templateBP = templateDataCtrl.GetValue()
			outputBP = outputDataCtrl.GetValue()
			fPrimerBP, rPrimerBP = genomics.generatePrimers(template=templateBP, output=outputBP)
			fPrimerOnWrite(bp=fPrimerBP)
			rPrimerOnWrite(bp=rPrimerBP)
		return onGeneratePrimers

	def simulatePCR(self, templateDataCtrl, fPrimerDataCtrl, rPrimerDataCtrl, outputOnWrite):
		def onSimulatePCR(event):
			templateBP = templateDataCtrl.GetValue()
			fPrimerBP = fPrimerDataCtrl.GetValue()
			rPrimerBP = rPrimerDataCtrl.GetValue()
			outputBP = genomics.simulatePCR(template=templateBP, fPrimer=fPrimerBP, rPrimer=rPrimerBP)
			outputOnWrite(bp=outputBP)
		return onSimulatePCR

	def verifyPrimers(self, templateDataCtrl, fPrimerDataCtrl, rPrimerDataCtrl, outputDataCtrl):
		def onVerifyPrimers(event):
			templateBP = templateDataCtrl.GetValue()
			fPrimerBP = fPrimerDataCtrl.GetValue()
			rPrimerBP = rPrimerDataCtrl.GetValue()
			outputBP = outputDataCtrl.GetValue()
			checkPass, simOutputBP = genomics.verifyPrimers(template=templateBP, fPrimer=fPrimerBP, rPrimer=rPrimerBP, output=outputBP)
			if checkPass:
				resultMDialog = wx.MessageDialog(self, message='Output verified: primers work', caption='Primer verification pass', style=wx.OK|wx.ICON_INFORMATION)
				resultMDialog.ShowModal()
			else:
				resultTEDialog = wx.TextEntryDialog(self, message='Output verified: primers fail\nSimulation yielded:', caption='Primer verification fail', style=wx.OK|wx.TE_MULTILINE|wx.TE_CHARWRAP|wx.TE_READONLY)
				resultTEDialog.SetValue(value=simOutputBP)
				resultTEDialog.ShowModal()
		return onVerifyPrimers

	def CreateLayout(self):
		# Change text with wx.StaticText#SetLabel()

		templateLoadButton = wx.Button(self, label="Load Template Strand")
		templateSaveButton = wx.Button(self, label="Save Template Strand")
		templateFileName = wx.StaticText(self, label="no file", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
		templateLength = wx.StaticText(self, label="0 base pairs", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
		templateACount = wx.StaticText(self, label="0 adenine", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
		templateCCount = wx.StaticText(self, label="0 cytosine", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
		templateData = wx.TextCtrl(self, style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_CHARWRAP)

		templateOnWrite = self.writeCtrl(dataCtrl=templateData, nameCtrl=templateFileName, lengthCtrl=templateLength, aCtrl=templateACount, cCtrl=templateCCount)
		templateLoadButton.Bind(wx.EVT_BUTTON, self.load(onWrite=templateOnWrite, nameCtrl=templateFileName))
		templateSaveButton.Bind(wx.EVT_BUTTON, self.save(dataCtrl=templateData))

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

		fPrimerOnWrite = self.writeCtrl(dataCtrl=fPrimerData, nameCtrl=fPrimerFileName, lengthCtrl=fPrimerLength, aCtrl=fPrimerACount, cCtrl=fPrimerCCount)
		fPrimerLoadButton.Bind(wx.EVT_BUTTON, self.load(onWrite=fPrimerOnWrite, nameCtrl=fPrimerFileName))
		fPrimerSaveButton.Bind(wx.EVT_BUTTON, self.save(dataCtrl=fPrimerData))

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

		rPrimerOnWrite = self.writeCtrl(dataCtrl=rPrimerData, nameCtrl=rPrimerFileName, lengthCtrl=rPrimerLength, aCtrl=rPrimerACount, cCtrl=rPrimerCCount)
		rPrimerLoadButton.Bind(wx.EVT_BUTTON, self.load(onWrite=rPrimerOnWrite, nameCtrl=rPrimerFileName))
		rPrimerSaveButton.Bind(wx.EVT_BUTTON, self.save(dataCtrl=rPrimerData))

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

		outputOnWrite = self.writeCtrl(dataCtrl=outputData, nameCtrl=outputFileName, lengthCtrl=outputLength, aCtrl=outputACount, cCtrl=outputCCount)
		outputLoadButton.Bind(wx.EVT_BUTTON, self.load(onWrite=outputOnWrite, nameCtrl=outputFileName))
		outputSaveButton.Bind(wx.EVT_BUTTON, self.save(dataCtrl=outputData))

		outputSizer = wx.StaticBoxSizer(wx.StaticBox(self, label="PCR Output Strand", style=wx.ALIGN_CENTER), wx.VERTICAL)
		outputSizer.Add(outputLoadButton, 0, wx.EXPAND)
		outputSizer.Add(outputSaveButton, 0, wx.EXPAND)
		outputSizer.Add(outputFileName, 0, wx.EXPAND)
		outputSizer.Add(outputLength, 0, wx.EXPAND)
		outputSizer.Add(outputACount, 0, wx.EXPAND)
		outputSizer.Add(outputCCount, 0, wx.EXPAND)
		outputSizer.Add(outputData, 1, wx.EXPAND)

		generatePrimers = wx.Button(self, label="Generate Primers")
		simulatePCR = wx.Button(self, label="Simulate PCR")
		verifyPrimers = wx.Button(self, label="Verify Primers")

		generatePrimers.Bind(wx.EVT_BUTTON, self.generatePrimers(templateDataCtrl=templateData, outputDataCtrl=outputData, fPrimerOnWrite=fPrimerOnWrite, rPrimerOnWrite=rPrimerOnWrite))
		simulatePCR.Bind(wx.EVT_BUTTON, self.simulatePCR(templateDataCtrl=templateData, fPrimerDataCtrl=fPrimerData, rPrimerDataCtrl=rPrimerData, outputOnWrite=outputOnWrite))
		verifyPrimers.Bind(wx.EVT_BUTTON, self.verifyPrimers(templateDataCtrl=templateData, fPrimerDataCtrl=fPrimerData, rPrimerDataCtrl=rPrimerData, outputDataCtrl=outputData))

		actionSizer = wx.BoxSizer(wx.VERTICAL)
		actionSizer.AddStretchSpacer()
		actionSizer.Add(generatePrimers, 1, wx.EXPAND)
		actionSizer.Add(simulatePCR, 1, wx.EXPAND)
		actionSizer.Add(verifyPrimers, 1, wx.EXPAND)

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