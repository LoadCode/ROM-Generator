#!/usr/bin/env python
import numpy as np
import math
import Tkinter as tk
import ttk




def GenerateSignal():

	global registerWitdh    
	global nPeriods     
	global signalSampleFreq
	global signalFreq      
	global fixedSine
	global fixedSignalString

	f  = signalFreq.get()
	fs = signalSampleFreq.get()
	n  = nPeriods.get()
	regWidth  = registerWitdh.get()

	#generate signal
	per = 1.0/f
	ts = 1.0/fs 
	t  = np.arange(0.0,n*per+ts, ts)
	floatSignal = np.around(np.sin(2*np.pi*f*t),decimals=10)
	
	########################### fixed point signal ###############################
	#Determine the needed bits for integer part
	minValBits = min(floatSignal).astype(int).bit_length()
	maxValBits = max(floatSignal).astype(int).bit_length()
	maxValBits = maxValBits if maxValBits >= minValBits else minValBits

	C2factor = 2 ** (regWidth)
	Qfactor  = 2 ** (regWidth - maxValBits - 1) #Qi,f notation, -1 for sign bit
	
	#Fixed point notation
	fixedSignal = (np.around(floatSignal*Qfactor)).astype(int)
	
	#Two's complement notation
	for i in range(len(fixedSignal)):
		fixedSignal[i] = fixedSignal[i] if fixedSignal[i] >= 0 else C2factor + fixedSignal[i]

	#Conversion to string
	fixedSignalString = ['0' for i in range(len(fixedSignal))]
	formatStr = '0%db'%regWidth
	for i in range(len(fixedSignal)):
		fixedSignalString[i] = format(fixedSignal[i], formatStr)

	GenerateVerilogFiles()
	print 'Signal Processing Complete'


	
def GenerateVerilogFiles():

	global fixedSignalString

	romFileName 	= 'rom.v'
	romTestFileName = 'rom_tb.v'
	memLength		= int(len(fixedSignalString)) - 1;
	bitAddress		= int(math.ceil(math.log(memLength, 2)));
	dataWidth		= int(len(fixedSignalString[0])) -1

	romFileContent  = """module rom (
										address , // Address input
										data    , // Data output
										read_en , // Read Enable
										ce        // Chip Enable
										);

						input  		[%d:0] address;
						output 		[%d:0] data;
						input        read_en;
						input        ce;
							
						  
						reg [%d:0]    mem [0:%d];

						assign data = (ce && read_en) ? mem[address] : %d'b0;	
						

						initial begin
						  $readmemb("data.list",mem);
						end

				endmodule"""%(bitAddress, dataWidth, dataWidth, memLength, dataWidth+1)

	romTbFile       = """ module rom_tb;
					 reg [%d:0] address;
					 reg read_en, ce;
					 wire [%d:0] data;
					 integer i;
			 
					 initial begin
						address = 0;
						read_en = 0;
						ce      = 0;
						
							for (i = 0; i <%d; i = i +1 )begin
										#5 address = i;
										read_en = 1;
										ce = 1;
										#5 read_en = 0;
										ce = 0;
										address = 0;
							end
			 			end
			 
							rom U(
							address ,	 	// Address input
							data    , 		// Data output
							read_en , 		// Read Enable
							ce        		// Chip Enable
							);

						endmodule
						 """%(bitAddress, dataWidth, memLength+1)


	fileRomTb = open(romTestFileName, 'w')
	fileRom   = open(romFileName, 'w')
	print >> fileRom,   romFileContent
	print >> fileRomTb, romTbFile


def SaveFile():
	global fixedSignalString
	fileVar = open('data.list','w')

	for item in fixedSignalString:
		print >> fileVar, item
	print str(len(fixedSignalString)) + " elements in the file"
	print 'Saved File'


def CreateGui():

	IN_XPAD = '10px'
	IN_YPAD = '10px'

	root = tk.Tk()
	root.geometry('500x350+500+100')
	root.title('ROM Signal Generator - v1.08')

	############################################################################################
	##                                      VARIABLE 										  ##
	##									   DECLARATION										  ##
	
	global registerWitdh, nPeriods, signalSampleFreq, signalFreq, signalFreqMult, signalFreqMultSpl

	registerWitdh     	= tk.IntVar() #IntVar, DoubleVar, StringVar
	nPeriods          	= tk.IntVar()
	signalSampleFreq  	= tk.IntVar()
	signalFreq        	= tk.IntVar()
	signalFreqMult      = tk.StringVar()
	signalFreqMultSpl   = tk.StringVar()
	signalSelected      = tk.StringVar() 
	fileName 		    = tk.StringVar()
	registerList		= (8,16,32,64)
	signalList          = ('Sine', 'Square', 'Triangular', 'Pseudorandom')
	multList            = ('Hz','kHz','MHz')

	nPeriods.set(1)
	signalFreq.set(1)
	signalSampleFreq.set(4)
	registerWitdh.set(registerList[0])
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
	frameParam.grid(row=0, column=0,padx='5px',pady='10px')


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

	txtDataPoints = ttk.Entry(frameParam,justify=tk.CENTER, textvariable=nPeriods,width=8)
	txtDataPoints.grid(row=2,column=1, columnspan=2, sticky=tk.W+tk.E)

	lblFs = ttk.Label(frameParam,text='Sample Freq. (fs)')
	lblFs.grid(column=0,row=3,pady=IN_YPAD,padx=IN_XPAD, sticky=tk.W)

	txtSampleF = ttk.Entry(frameParam,justify=tk.CENTER, textvariable=signalSampleFreq,width=8)
	txtSampleF.grid(column=1,row=3, sticky=tk.W+tk.E)

	opSignalFreqSpl = tk.OptionMenu(frameParam, signalFreqMultSpl, *multList)
	opSignalFreqSpl.grid(row=3, column=2, sticky=tk.E)

	lblWb = ttk.Label(frameParam,text='Width of Register (bits)')
	lblWb.grid(row=4, column=0,pady=IN_YPAD,padx=IN_XPAD, sticky=tk.W)

	txtWidth = tk.OptionMenu(frameParam, registerWitdh, *registerList)
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


	############################################################################################
	##                                     GRAPHICS 										  ##
	##									   SECTION											  ##
	##																						  ##

	##										 END 											  ##
	##									GRAPHICS SECTION									  ##
	############################################################################################






	root.mainloop()



if __name__ == '__main__':
	CreateGui()























#sources:
#		
# http://stackoverflow.com/questions/8928240/convert-base-2-binary-number-string-to-int
# http://stackoverflow.com/questions/1604464/twos-complement-in-python
# http://stackoverflow.com/questions/10411085/converting-integer-to-binary-in-python
# https://en.wikibooks.org/wiki/Floating_Point/Fixed-Point_Numbers

