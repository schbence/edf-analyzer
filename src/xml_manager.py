import xml.etree.ElementTree as ET

# create the file structure

def save_project(filepath,edfpath, channels, viewpos, zooming,selectfrom,selectto,sigHeight):
    root    = ET.Element('EEG_project_state')
    path    = ET.SubElement(root, 'edfpath')
    viewp   = ET.SubElement(root, 'viewposition')
    zoom    = ET.SubElement(root, 'zooming')
    chs     = ET.SubElement(root, 'active_channels')
    sel     = ET.SubElement(root,'selector')
    selfr   = ET.SubElement(sel,'selfrom')
    selto   = ET.SubElement(sel,'selto')
    sheight = ET.SubElement(root,'signal_height')


    path.text  = str(edfpath)
    viewp.text = str(viewpos)
    zoom.text  = str(zooming)
    selfr.text = str(selectfrom)
    selto.text = str(selectto)
    sheight.text = str(sigHeight)

    for c,i in zip(channels,range(len(channels))):
        channel = ET.SubElement(chs,str('CH_'+str(i)))
        channel.text = str(c)

    mydata = ET.tostring(root)
    myfile = open(filepath+'.proj', "w")
    myfile.write(mydata)
    myfile.close()

def str2bool(x):
    if x=='True':
        return True
    if x=='False':
        return False
    print 'ERROR IN CONVERSION FROM STRING TO BOOL'

def load_project(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    pth,vp,zoom,act,sel,sh = list(root)

    edfpath   = pth.text
    viewpos   = int(vp.text)
    zooming   = int(zoom.text)
    activeCHs = map(lambda x:int(str2bool(x.text)),list(act))
    selfr,selto = map(lambda x:int(x.text),list(sel))
    sigHeight = int(sh.text)

    return edfpath,activeCHs,viewpos,zooming,selfr,selto,sigHeight



'''
##############  write example  ####################
pth = '../data/BB0008_SP3.edf'
chs = [1,0,0,0,1,0,0,1,1,0,1,0]
vp  = 125
zoo = 8
sel = [15,25]

save_project(pth,chs,vp,zoo,sel[0],sel[1])
'''

'''
################ read example ########################
pth,cp,zoo,acs,sf,st = load_project('./projdata.xml')
'''
