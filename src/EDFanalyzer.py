import jpype
from numpy import *
import read_eeg,time
import sys,xml_manager
from pylab import *
from pyeeg.linear import autocorrelation
import measures

class Observer(object):
    def __init__(self):
        self.fr,self.to = 0,0
    def setData(self, data):
        self.dataObj = data

    def notif(self,msg):
        #print self.fr,self.to
        print msg
        if msg == "PLOT SIG":
            p = Plot()
            p.setData(self.dataObj)
            p.plotSignal(self.fr,self.to,self.activeChannels)
        if msg == "PLOT HIST":
            p = Plot()
            p.setData(self.dataObj)
            p.plotHist(self.fr,self.to,self.activeChannels)
        if msg == "PLOT PSD":
            p = Plot()
            p.setData(self.dataObj)
            p.plotPsd(self.fr,self.to,self.activeChannels)
        if msg == "PLOT AC":
            p = Plot()
            p.setData(self.dataObj)
            p.plotAutocorr(self.fr,self.to,self.activeChannels)
        if msg == "CALC STD":
            c = Calc()
            c.setData(self.dataObj)
            print self.fr, self.to
            c.std(self.fr,self.to,self.activeChannels)
        if msg == "CALC ENTROP":
            c = Calc()
            c.setData(self.dataObj)
            print self.fr, self.to
            c.entrop(self.fr,self.to,self.activeChannels)



    def setBounds(self,nf,nt):
        self.fr,self.to = sort([nf-10,nt-10])

    def setActiveChannels(self,chList):
        print chList
        self.activeChannels = chList



class EEGData(object):
    def __init__(self,filename):
        self.edfpath  = filename
        data          = read_eeg.read_file(filename)
        eeg           = data[0]
        self.sig      = eeg[:2000000,:].T.tolist()
        self.labels   = data[4][0]
        self.sampFreq = data[3][0]

    def getSignal(self):
        return self.sig

    def getPath(self):
        return self.edfpath

    def getLabels(self):
        return self.labels

    def getSampFreq(self):
        return self.sampFreq

    def reloadData(self,newfile):
        print "RELOADING"+newfile
        self.edfpath  = newfile
        data          = read_eeg.read_file(str(newfile))
        eeg           = data[0]
        self.sig      = eeg[:2000000,:].T.tolist()
        self.labels   = data[4][0]
        self.sampFreq = data[3][0]
        print "RELOADING DONE"

class Plot(object):
    def setData(self, data):
        self.dataObj = data
    def plotSignal(self,fr,to,activeChannels):
        leg = []
        sig = self.dataObj.getSignal()
        labs = self.dataObj.getLabels()
        for s,l,ch in zip(sig,labs,activeChannels):
            if ch:
                plot(s[fr:to],alpha=.7)
                leg.append(l)
        suptitle("Signal")
        legend(leg)
        grid()
        show()

    def plotHist(self,fr,to,activeChannels):
        leg = []
        sig = self.dataObj.getSignal()
        labs = self.dataObj.getLabels()
        sarr = array(sig)[:,fr:to]
        min,max = sarr.min(),sarr.max()
        for s,l,ch in zip(sig,labs,activeChannels):
            if ch:
                hist(s[fr:to],bins=linspace(min,max,200),alpha=.7)
                leg.append(l)
        suptitle("Histogram")
        xlabel("U [uV]")
        legend(leg)
        grid()
        show()

    def plotPsd(self,fr,to,activeChannels):
        leg  = []
        sig  = self.dataObj.getSignal()
        labs = self.dataObj.getLabels()
        fs   = self.dataObj.getSampFreq()
        for s,l,ch in zip(sig,labs,activeChannels):
            if ch:
                psd(s[fr:to],Fs=fs,alpha=.7)
                grid()
                leg.append(l)
        legend(leg)
        grid()
        show()

    def plotAutocorr(self,fr,to,activeChannels):
        leg  = []
        sig  = self.dataObj.getSignal()
        labs = self.dataObj.getLabels()
        fs   = self.dataObj.getSampFreq()
        for s,l,ch in zip(sig,labs,activeChannels):
            if ch:
                mlag = int((to-fr)/2)
                #mlag = int(fs*10)
                v,t = autocorrelation(array(s[fr:to]),maxlag = mlag)
                plot(t/fs,v,alpha=.7)
                leg.append(l)
        legend(leg)
        xlabel("Time [s]")
        ylabel("Autocorrelation")
        grid()
        show()

def measureArray(s):
    a = measures.dlArray(len(s))
    for i in range(len(s)):
        a[i] = s[i]
    return a


class Calc(object):
    def setData(self,data):
        self.dataObj = data

    def std(self,fr,to,activeChannels):
        sig = self.dataObj.getSignal()
        labs = self.dataObj.getLabels()
        for s,l,ch in zip(sig,labs,activeChannels):
            if ch:
                ss = measureArray(s[fr:to])
                print l,':',measures.STD(ss,to-fr+1)

    def entrop(self,fr,to,activeChannels):
        sig = self.dataObj.getSignal()
        labs = self.dataObj.getLabels()
        for s,l,ch in zip(sig,labs,activeChannels):
            if ch:
                ss = measureArray(s[fr:to])
                print l,':',measures.Entropy(ss,to-fr+1,50)



class projectManager(object):
    def save_project(self,savepath,pth,ch_list,viewpos,zoom,selFrom,selTo,sigH):
        xml_manager.save_project(savepath,pth,ch_list,viewpos,zoom,selFrom,selTo,sigH)
    def load_project(self,filename):
        p,ch,v,z,sf,st,sH = xml_manager.load_project(filename)
        self.path      = p
        self.channels  = ch
        self.viewpos   = v
        self.zoom      = z
        self.selFr     = sf
        self.selTo     = st
        self.sigHeight = sH

    def getPath(self):
        return self.path

    def getChannels(self):
        print 'ACTIVE CHANNELS:',self.channels
        return self.channels

    def getViewpos(self):
        return self.viewpos

    def getZoom(self):
        return self.zoom

    def getSelection(self):
        return self.selFr,self.selTo

    def getSigHeight(self):
        return self.sigHeight



def main():
    if len(sys.argv)!=2:
        print len(sys.argv)
        print "Usage " +str(sys.argv[0])+" <edf file> "
        sys.exit(0)
    else:
        fl = str(sys.argv[1])
        dataObj  = EEGData(fl)

        jpype.startJVM(jpype.getDefaultJVMPath())

        pyobs   = Observer()
        pyobs.setData(dataObj)
        jobs    = jpype.JClass("Observer")
        obsprox = jpype.JProxy(jobs, inst=pyobs)

        jdata    = jpype.JClass("EEGData")
        dataprox = jpype.JProxy(jdata,inst=dataObj)

        projObj  = projectManager()
        jproj    = jpype.JClass("ProjectManager")
        projprox = jpype.JProxy(jproj,inst=projObj)

        gui = jpype.JClass("GUI")
        print 'gui init'
        gui(obsprox,dataprox,projprox)

        time.sleep(1000)
        jpype.shutdownJVM()


if __name__ == "__main__" : main()
