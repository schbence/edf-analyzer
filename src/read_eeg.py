# -*- coding: utf-8 -*-
import numpy as np
import biosig
import os, sys
import pyeeg

G_REM, G_NREM1, G_NREM2, G_NREM3,G_NREM4, G_WAKE, G_M, G_U = 0, 1, 2, 3, 4, 5, 6, 9 
REM, NREM1, NREM2, NREM3,NREM4, WAKE=G_REM, G_NREM1, G_NREM2, G_NREM3,G_NREM4, G_WAKE
SLEEPSTAGE_NAME2CODE={'WAKE':WAKE, 'NREM1':NREM1, 'NREM2':NREM2, 'NREM3':NREM3, 'NREM4':NREM4, 'REM':REM}
SLEEPSTAGE_CODE2NAME={WAKE:'WAKE', NREM1:'NREM1', NREM2:'NREM2', NREM3:'NREM3', NREM4:'NREM4', REM:'REM'}
SLEEPSTAGENAMES = ['REM','NREM1', 'NREM2', 'NREM3', 'NREM4', 'WAKE', 'M', 'U']
SLEEPSTAGES = {'WAKE':WAKE, 'NREM1':NREM1, 'NREM2':NREM2, 'NREM3':NREM3, 'NREM4':NREM4, 'REM':REM, 'M':G_M, 'U':G_U}
DEFAULTFS = 256. # default sampling frequency value. To be used when there is a missmatch between the EDF structure and the capabilities of the Biosig library.
DEFAULT_ARTEFACT_CUTOFF = 0

SLEEPTIME_SEP = ';'
#SLEEPTIME_SEP = ','

EEG2ARTEFACT = {'Fp1':'ArtiFFT Fp1-A2', 
                    'Fp2':'ArtiFFT Fp2-A1', 
                    'F3' :'ArtiFFT F3-A2', 
                    'F4' :'ArtiFFT F4-A1', 
                    'C3' :'ArtiFFT C3-A2', 
                    'C4' :'ArtiFFT C4-A1', 
                    'T3' :'ArtiFFT T3-A2', 
                    'T4' :'ArtiFFT T4-A1', 
                    'P3' :'ArtiFFT P3-A2', 
                    'P4' :'ArtiFFT P4-A1', 
                    'O1' :'ArtiFFT O1-A2', 
                    'O2' :'ArtiFFT O2-A1'} 

CHANNELS = ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'T3', 'T4', 'P3', 'P4', 'O1', 'O2', 
            'A1', 'A2', 
            'LOC A2', 'ROC A1', 
            'EMG', 
            'ECG', 
            'Hypnogram', 
            'ArtiFFT Fp1-A2', 'ArtiFFT Fp2-A1', 'ArtiFFT F3-A2', 'ArtiFFT F4-A1', 
            'ArtiFFT C3-A2', 'ArtiFFT C4-A1', 'ArtiFFT P3-A2', 'ArtiFFT P4-A1', 
            'ArtiFFT O1-A2', 'ArtiFFT O2-A1', 'ArtiFFT T3-A2', 'ArtiFFT T4-A1']

EEG_CHANNELS = CHANNELS[:12]

CHANNEL_ALTERNATIVES = {'Fp1':['Fp1'], 'Fp2':['Fp2'], 'F3':['F3'], 'F4':['F4'], 'C3':['C3'], 'C4':['C4'], 'T3':['T3'], 'T4':['T4'], 'P3':['P3'], 'P4':['P4'], 'O1':['O1'], 'O2':['O2'], 'A1':['A1'], 'A2':['A2'], 'LOC A2':['LOC A2'], 'ROC A1':['ROC A1'], 'EMG':['EMG1 EMG2'], 'ECG':['ECG1 ECG2'], 'Hypnogram':['Hypnogram'], 'ArtiFFT Fp1-A2':['ArtiFFT Fp1-A2'], 'ArtiFFT Fp2-A1':['ArtiFFT Fp2-A1'], 'ArtiFFT F3-A2':['ArtiFFT F3-A2'], 'ArtiFFT F4-A1':['ArtiFFT F4-A1'], 'ArtiFFT C3-A2':['ArtiFFT C3-A2'], 'ArtiFFT C4-A1':['ArtiFFT C4-A1'], 'ArtiFFT P3-A2':['ArtiFFT P3-A2'], 'ArtiFFT P4-A1':['ArtiFFT P4-A1'], 'ArtiFFT O1-A2':['ArtiFFT O1-A2'], 'ArtiFFT O2-A1':['ArtiFFT O2-A1'], 'ArtiFFT T3-A2':['ArtiFFT T3-A2'], 'ArtiFFT T4-A1':['ArtiFFT T4-A1'], 'Hypnogram':['Hypnogram']}

MISSING_ARTEFACT = []
#-------------------------------------------------------------------------------
class DataObjectManager:
    
    """
        Observation for Guildford data:
        
        Example for calling the function:
            
            C3 = manager.read_channel('C3')
            
        Reads the data from the specified channel 
        
        Guildford data sampling frequency can be 200 - 256 
        So when using any algorithm check the sampling frequency by calling the samplfreq
    """
    
        
    def __init__(self,  filename):
        self.__filename = filename
        #self.__hypdata = None
        #self.__artdata = None
        #self.__data = None
        self.__channels = []
        self.__epoch = None
        self.__HDR = None
        #self.__has_read_data = False
        if not os.path.isfile(self.__filename):
                raise IOError('file ' + self.__filename + ' cannot be opened!')
        self.__HDR = biosig.constructHDR(0, 0)
        self.__HDR = biosig.sopen(self.__filename, "r", self.__HDR)        
        self.__Fs = np.zeros(self.__HDR.NS)         
        for i in range(self.__HDR.NS):
            self.__Fs[i] = self.__HDR.CHANNEL[i].SPR
            channel = self.__HDR.CHANNEL[i].Label
            nullpos = channel.find('\x00')
            if nullpos != -1:
                 channel = channel[:nullpos]
            self.__channels.append(channel)
            self.__HDR.CHANNEL[i].OnOff = 0
            
    #     rescale  data if hyp or art length doesn't match data
        
    
    def channels(self):
        return self.__channels
        
    def closefile(self):
        biosig.sclose(self.__HDR)
        #biosig.destructHDR(self.__HDR)
    
    def read_channel(self, channel):
        """
        to avoid SEGMENTATION FAULT all channels have to be read one by one
        we set the OnOff option (this option turns reading of a channel on  or off) of all channels 0
        if we want to read the channel we set its OnOff option to 1 this means reading is on and we read the data
        after we read the channel's data we must set it again to 0, or else we get segmentation fault
        """
        #print "Debug: self.__channels=", self.__channels, " channel=", channel
        self.__HDR.CHANNEL[self.__channels.index(channel)].OnOff = 1
        channeldata = np.array(biosig.sread(0, self.__HDR.NRec, self.__HDR), dtype=np.float32)[0]
        self.__HDR.CHANNEL[self.__channels.index(channel)].OnOff = 0
        return channeldata
    
    def samplfreq(self):
        return self.__Fs
                
    def __repr__(self):
        s  = "Filename: " + self.__filename + "\n"
        #s += "Hyp filename: " + self.__hypfilename + "\n"
        #s += "Art filename: " + self.__artfilename + "\n"
        s += "Channels (" + str(len(self.__channels)) + "): " + str(self.__channels) + "\n"
        s += "Sampling freq: " + str(self.__Fs) + "\n"
        return s
  
    


#-------------------------------------------------------------------------------
#
# TODO: implement the protection from multiple reading of the same file
#
#-------------------------------------------------------------------------------

def __get_real_channel__(searched_channel, real_channels):
  for channel in CHANNEL_ALTERNATIVES[searched_channel]:
    if channel in real_channels:
      return channel
  print 'Error:',searched_channel,'or its alternatives,',CHANNEL_ALTERNATIVES[searched_channel],'not found in',real_channels


#-------------------------------------------------------------------------------
def read_file(filename, eeg=[], artefact=True, reference=False, ecg=False, emg=False, oculogram=False, hypno=False, resamplefreq=None):
    """
    Parameters
    ----------
    eeg - list of channel codes, any subset of ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'T3', 'T4', 'P3', 'P4', 'O1', 'O2']
        BEWARE! no precaution is taken against faulty input (invalid channel codes, etc.)
    
    Return
    ------
    eegdata - time x channel type of two-dimensional Numpy array with 
        eeg, reference, oculogram, emg and ecg data as requested and in this order
    artdata - time x channel type of two-dimensional Numpy array with 
        the artefact information for the corresponding EEG channels
    hypnodata - hypno data as Numpy array
    sampling rates - Numpy array for all channels

    if artefact and/or hypnogram are not requested empty arrays are returned
    """
    datafile = os.path.split(filename)[1].replace('.edf','')
    try:
    	manager = DataObjectManager(filename)
    except IOError as err:
	print 'read error: ' + str(err)
	return
    real_channels = manager.channels()
    import copy
    channels = copy.copy(eeg)
    if eeg == [] :    
        channels += ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'T3', 'T4', 'P3', 'P4', 'O1', 'O2']
    artefact_channels = []    
    if artefact:
        for eegname in channels:
            artefact_channels.append(EEG2ARTEFACT[eegname])
    if reference:
        channels += ['A1', 'A2']
    if oculogram:
        channels += ['LOC A2', 'ROC A1']
    if emg:
        channels += ['EMG']
    if ecg:
        channels += ['ECG']
    if hypno:
        hypno_channels = ['Hypnogram']
    else:
        hypno_channels = []
								
    # copied over from cambridge3.read_file								
    sampling_rates = [DEFAULTFS]*len(channels + artefact_channels + hypno_channels)
#    sampling_rates = []
#    if len(manager.samplfreq()) != len(channels + artefact_channels + hypno_channels):   WARNING! THIS PART IS NOT DONE PROPERLY. CHECK THE CASE hypno=False
#        sampling_rates += [DEFAULTFS]*len(channels + artefact_channels + hypno_channels)
#        print 'Warning: sampling frequencies not read properly. Got: ', manager.samplfreq(), ". Using: ", sampling_rates, " instead"
#    else:
#        for channel in channels + artefact_channels + hypno_channels:    
#            sampling_rates.append(manager.samplfreq()[all_channels.index(channel)])
    eegdata = manager.read_channel(__get_real_channel__(channels[0], real_channels))
    for channel in channels[1:]:
        eegdata = np.column_stack((eegdata, manager.read_channel(__get_real_channel__(channel, real_channels))))
    artdata = np.array([])        
    if artefact:
         if datafile in MISSING_ARTEFACT:
              artdata = np.zeros(eegdata.shape, dtype=np.int32)
         else:
              artdata = manager.read_channel(__get_real_channel__(artefact_channels[0], real_channels))
              for channel in artefact_channels[1:]:
                   artdata = np.column_stack((artdata, manager.read_channel(__get_real_channel__(channel, real_channels))))        
    else:
         artdata = np.array([])
    hypnodata = np.array([])
    if hypno:
        hypdata = manager.read_channel(__get_real_channel__(hypno_channels[0], real_channels))
    else:
	hypdata = np.array([])
    # TODO: consider the possibility of always returning a one row 2D array (reshaped vector) 
    # even for a single channel
    # have to retest everything if changing
    manager.closefile()
    if type(resamplefreq) == type(0.0):
        eegdata = pyeeg.datatools.resampling(eegdata, sampling_rates[0], resamplefreq)
	if artefact:
             artdata = pyeeg.datatools.resampling(artdata, sampling_rates[0], resamplefreq, stepped=True)
	if hypno:
             hypdata = pyeeg.datatools.resampling(hypdata, sampling_rates[0], resamplefreq, stepped=True)
        sampling_rates = [resamplefreq]*len(sampling_rates)
    print resamplefreq
    return eegdata.astype(np.float32), artdata.astype(np.int16), hypdata.astype(np.int16), np.array(sampling_rates, dtype=np.float32), (channels, artefact_channels, hypno_channels)
    # end of copy over from cambridge3.read_file								
								
#								
#    Original								
#								
#    sampling_rates = []
#    if len(manager.samplfreq()) != len(channels + artefact_channels + hypno_channels):
#        sampling_rates += [DEFAULTFS]*len(channels + artefact_channels + hypno_channels)
#        print 'Warning: sampling frequencies not read properly. Got: ', manager.samplfreq(), ". Using: ", sampling_rates, " instead"
#    else:
#        for channel in channels + artefact_channels + hypno_channels:    
#            sampling_rates.append(manager.samplfreq()[CHANNELS.index(channel)])
#    eegdata = manager.read_channel(channels[0])
#    for channel in channels[1:]:
#        eegdata = np.column_stack((eegdata, manager.read_channel(channel)))
#    artdata = np.array([])        
#    if artefact:
#        artdata = manager.read_channel(artefact_channels[0])
#        for channel in artefact_channels[1:]:
#            artdata = np.column_stack((artdata, manager.read_channel(channel)))        
#    hypnodata = np.array([])
#    if hypno:
#        hypdata = manager.read_channel(__get_real_channel__(hypno_channels[0], real_channels))
#    else:
#        hypdata = np.array([])
#    # TODO: consider the possibility of always returning a one row 2D array (reshaped vector) 
#    # even for a single channel
#    # have to retest everything if changing
#    manager.closefile()
#    if resamplefreq != None:
#        eegdata = pyeeg.datatools.resampling(eegdata, sampling_rates[0], resamplefreq)
#	if artefact:
#             artdata = pyeeg.datatools.resampling(artdata, sampling_rates[0], resamplefreq, stepped=True)
#	if hypno:
#             hypdata = pyeeg.datatools.resampling(hypdata, sampling_rates[0], resamplefreq, stepped=True)
#        sampling_rates = [resamplefreq]*len(sampling_rates)
#				
#    return eegdata.astype(np.float32), artdata.astype(np.int16), hypdata.astype(np.int16), np.array(sampling_rates, dtype=np.int16), (channels, artefact_channels, hypno_channels)

#-------------------------------------------------------------------------------
def simplify_artefact(artdata, **inparams):
    """
    Artefact values (integers) are scaled to the binary {0, 1} set (1 - artefact, 0 - no artefact).
    
    input
    -----
    artdata: Numpy array of dimension one or two (of Ntime x Nchannels)
    Artefact values can be 0 (no artefact) or several integer values depending
    on the type of artefact and method of detection
    
    
    merge:        boolean value specifying the combination of several art channels into a single ones (we have an artefact if any of the channels have artefacts)
    keep_dim:     when *merge* is True then it specifies whether the output is a single vector or a matrix of the same shape as *artdata*
    lower_cutoff: only elements above this value are considered artefacts
    
    output
    ------
    one or two dimensional Numpy array of 0s and 1s
    if *merge* is True and *artdata* is two dimensional and *keep_dim* is False then all channels are merged into a single one
    if *merge* is True and *artdata* is two dimensional and *keep_dim* is True then the merged channel from the case above is used for all channels  
    if *merge* is False or *artdata* is one dimensional then the output array is of the same size as the input one
    """
    params = {'merge':False, 'keep_dim':False, 'lower_cutoff': DEFAULT_ARTEFACT_CUTOFF}
    params.update(inparams)
    merge, keep_dim, lower_cutoff = params['merge'], params['keep_dim'], params['lower_cutoff']
    if artdata.ndim == 1:
        ind = np.where(artdata <= lower_cutoff)[0]
    elif artdata.ndim == 2:
        ind = np.where(artdata <= lower_cutoff)
    else:
        print 'simplify_artefact error: input data can be of dimension 1 or 2. It is ', artdata.ndim
        return
    artdata = np.ones(artdata.shape, dtype=np.int16)
    artdata[ind] = 0
    #artdata = artdata/artdata
    #artdata[np.where(np.isnan(artdata))] = 0
    if merge and artdata.ndim ==2:
        if keep_dim:
            return np.tile(1 - (1 - artdata).prod(axis=1), artdata.shape[1]).reshape(artdata.shape[1], -1).T
        else:
            return 1 - (1 - artdata).prod(axis=1)
    return artdata



#-------------------------------------------------------------------------------
def refere(eeg, channels, mode='contralateral'):
        """
	EEG channels are referred to the appropriate reference channels 
	It is assumed that A1 and A2 are part of the array 
	It modifies the EEG 'in loco'	
	Parameters
	----------
	eeg - 2D (time x channel type) array of EEG data (Numpy array) including the reference channels
	channels - list of channel codes in the same order as in *eeg* 

	Output
	------
	It doesn't  return anything. The data in *eeg* will be changed. 
	"""
	bipolar_map = {'Fp1':'Fp2', 'Fp2':'Fp2', 'F3':'F4', 'F4':'F4', 'C3':'C4', 'C4':'C4', 'T3':'T4', 'T4':'T4', 'P3':'P4', 'P4':'P4', 'O1':'O2', 'O2':'O2'}
	if mode not in ['monopolar', 'contralateral', 'bipolar', 'linked', 'average']:
		print 'WARNING - refere(): parameter "mode" can only be "monopolar", "contralateral", "bipolar" or "linked". Using "contralateral"!'
		mode = 'contralateral'
	if mode == 'linked':		
		reference = (eeg[:,channels.index('A1')] + eeg[:,channels.index('A2')])/2.
	if mode == 'average':
		reference = np.zeros(len(eeg), dtype=np.float32)
		chcounter = 0
		for channel in range(len(channels)):
			if (channels[channel] in EEG_CHANNELS):
				reference += eeg[:, channel]
				chcounter += 1
		reference /= chcounter
	for channel in range(len(channels)):
		if (channels[channel] in EEG_CHANNELS):
			# mindenkit referalunk kiveve magukat a referencia csatornakat
			if mode == 'contralateral':
				if (channels[channel] in ['Fp2', 'F4', 'C4', 'T4', 'P4', 'O2']):
					ref_channel = channels.index('A1')
				elif (channels[channel] in ['Fp1', 'F3', 'C3', 'T3', 'P3', 'O1']):
					ref_channel = channels.index('A2')
				else:
					print "Error: what kind of channel is this: ", channels[channel], " cannot reference!!!!"
				reference = eeg[:, ref_channel]
				print "channel ", channels[channel], " referenced to ", channels[ref_channel]
			if mode == 'bipolar':
				ref_channel = channels.index(bipolar_map[channels[channel]])
				reference   = eeg[:, ref_channel]
				print "channel ", channels[channel], " referenced to ", channels[ref_channel]
			eeg[:, channel] -= reference
	
	
#	for channel in range(len(channels)):
#		if not (channels[channel] in ['A1', 'A2']):
#			# mindenkit referalunk kiveve magukat a referencia csatornakat
#			if (channels[channel] in ['Fp2', 'F4', 'C4', 'T4', 'P4', 'O2']):
#				ref_channel = channels.index('A1')
#			elif (channels[channel] in ['Fp1', 'F3', 'C3', 'T3', 'P3', 'O1']):
#				ref_channel = channels.index('A2')
#			else:
#				print "Error: what kind of channel is this: ", channels[channel], " cannot reference!!!!"
#			eeg[:, channel] -= eeg[:, ref_channel]
#			print "channel ",channels[channel], " referenced to ", channels[ref_channel]
					 
#-------------------------------------------------------------------------------
def sleeptimeinfo(filename, timeinfofile, format=["%d-%b-%y %H:%M:%S", "%d-%b-%y %H:%M"]):
	"""
        Lights out, lights on information

	Parameters
	----------
	filename - name of the edf file without extension e.g. BB0008_SP2
	
	timeinfofile - name of the CSV file with the information

	format - can be a string like "%d-%b-%y %H:%M:%S" or a list of strings like
	         ["%d-%b-%y %H:%M:%S", "%d-%b-%y %H:%M"]
	
	Returns
	------- 
	start, lights out, lights on (triple) datetime information for *filename* from *timeinfofile*
	"""
	#print timeinfofile
	input_subject, input_night = filename.split('_SP')
	input_night = input_night[0] # the first character only (0 - 9)
	infoall = file(timeinfofile).read().split('\n');
	for row in infoall:		
		#print row.split(',')
		subject, night, startdate, starttime, offdate, offtime,  ondate, ontime = row.split(SLEEPTIME_SEP)[:8]
		ontime = ontime.strip()
		#print subject, night, ondate, ontime, offdate, offtime 
		if subject == input_subject and night == input_night:
			#print subject, night, startdate, starttime, offdate, offtime,  ondate, ontime	
			timestart, timeon, timeoff  = __gettime__(startdate + " " + starttime, format), __gettime__(ondate + " " + ontime, format), __gettime__(offdate + " " + offtime, format)
			if timestart == None or timeoff == None or timeon == None :
  				print "waketimeinfo() error: format problem?"
			return timestart, timeoff, timeon
	print "waketimeinfo() error: " + filename + " not found in " + timeinfofile


#-------------------------------------------------------------------------------
def __gettime__(timestr, format=["%d-%b-%y %H:%M:%S", "%d-%b-%y %H:%M"]):
	from datetime import datetime
	if type(format) != type([]):
		try:
			return datetime.strptime(timestr, format)
		except ValueError:
			print "__gettime__() error: " + timestr + " is not covered by the " + str(format)  + " format"
			return
	else:
		for frmt in format:				
			try:
				return datetime.strptime(timestr, frmt)
			except ValueError:
				pass			
		print "__gettime__() error: " + timestr + " is not covered by any of the following formats: " + str(format)
	
		
	
__all__ = ['G_WAKE', 'G_NREM1', 'G_NREM2', 'G_NREM3', 'G_NREM4', 'G_REM', 'simplify_artefact', 'read_file' ]
