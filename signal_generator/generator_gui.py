#!/usr/bin/env python

import Tkinter as tk
import ttk


def GenerateSignal():
	print 'generando senal'


def SaveFile():
	print 'Guardando Archivo'


def CreateGui():

	IN_XPAD = '10px'
	IN_YPAD = '10px'

	root = tk.Tk()
	root.geometry('500x350+500+100')
	root.title('ROM Signal Generator - v1.08')

	############################################################################################
	##                                      VARIABLE 										  ##
	##									   DECLARATION										  ##
	

	registerWitdh     = tk.IntVar() #IntVar, DoubleVar, StringVar
	nTxtPeriods       = tk.IntVar()
	signalSampleFreq  = tk.IntVar()
	signalFreq        = tk.IntVar()
	signalFreqMult    = tk.StringVar()
	signalFreqMultSpl = tk.StringVar()
	signalSelected    = tk.StringVar() 
	fileName 		  = tk.StringVar()
	signalList        = ('Sine', 'Square', 'Triangular', 'Pseudorandom')
	multList          = ('Hz','kHz','MHz')


	signalSelected.set(signalList[0])
	signalFreqMult.set(multList[0])
	signalFreqMultSpl.set(multList[0])

	##										END												  ##
	##								VARIABLE DECLARATION									  ##
	############################################################################################


	############################################################################################
	##                                     PARAMETERS 										  ##
	##										SECTION											  ##
	##																						  ##

	frameParam = tk.LabelFrame(root,text='Parameters',relief=tk.FLAT)
	frameParam.grid(row=0, column=1,padx='5px',pady='10px')


	lblSignal = ttk.Label(frameParam,text='Signal Selection')
	lblSignal.grid(row=0, column=0,pady=IN_YPAD,padx=IN_XPAD, sticky=tk.W)

	opSignal = tk.OptionMenu(frameParam, signalSelected, *signalList)
	opSignal.grid(row=0, column=1, columnspan=2, sticky=tk.W+tk.E)

	lblFc = ttk.Label(frameParam, text='Signal Freq. (fc)')
	lblFc.grid(row=1, column=0,pady=IN_YPAD,padx=IN_XPAD, sticky=tk.W)

	txtFc = ttk.Entry(frameParam,justify=tk.CENTER, textvariable=signalFreq, width=8)
	txtFc.grid(row=1, column=1, sticky=tk.W+tk.E)

	opSignalFreq = tk.OptionMenu(frameParam, signalFreqMult, *multList)
	opSignalFreq.grid(row=1, column=2, sticky=tk.E)

	lblDataPoints = ttk.Label(frameParam,text='Number Cycles')
	lblDataPoints.grid(row=2,column=0, pady=IN_YPAD,padx=IN_XPAD, sticky=tk.W, columnspan=2)

	txtDataPoints = ttk.Entry(frameParam,justify=tk.CENTER, textvariable=nTxtPeriods,width=8)
	txtDataPoints.grid(row=2,column=1, columnspan=2, sticky=tk.W+tk.E)

	lblFs = ttk.Label(frameParam,text='Sample Freq. (fs)')
	lblFs.grid(column=0,row=3,pady=IN_YPAD,padx=IN_XPAD, sticky=tk.W)

	txtSampleF = ttk.Entry(frameParam,justify=tk.CENTER, textvariable=signalSampleFreq,width=8)
	txtSampleF.grid(column=1,row=3, sticky=tk.W+tk.E)

	opSignalFreqSpl = tk.OptionMenu(frameParam, signalFreqMultSpl, *multList)
	opSignalFreqSpl.grid(row=3, column=2, sticky=tk.E)

	lblWb = ttk.Label(frameParam,text='Width of Register (bits)')
	lblWb.grid(row=4, column=0,pady=IN_YPAD,padx=IN_XPAD, sticky=tk.W)

	txtWidth = ttk.Entry(frameParam,justify=tk.CENTER, textvariable=registerWitdh,width=8)
	txtWidth.grid(row=4, column=1, columnspan=2, sticky=tk.W+tk.E)

	lblFileName = ttk.Label(frameParam, text='File Name for Signal')
	lblFileName.grid(row=7,column=0, sticky=tk.W, pady=IN_YPAD, padx=IN_XPAD)

	txtWidth = ttk.Entry(frameParam, justify=tk.CENTER, textvariable=fileName, width=20)
	txtWidth.grid(row=7, column=1, columnspan=2, pady=IN_YPAD)

	btnGenerate = ttk.Button(frameParam, text='Generate Signal', command=GenerateSignal, takefocus=False)
	btnGenerate.grid(row = 8, column = 0, pady='20px', sticky=tk.E+tk.W, padx=IN_XPAD)

	btnSave = ttk.Button(frameParam, text='Save Signal', command=SaveFile, takefocus=False)
	btnSave.grid(row = 8, column = 1, pady='20px', sticky=tk.E+tk.W,columnspan=2)

	##											END											  ##
	##									PARAMETERS SECTION									  ##
	############################################################################################

	
	
	
	
	
	
	
	
	
	
	
	
	root.mainloop()



if __name__ == '__main__':
	CreateGui()



