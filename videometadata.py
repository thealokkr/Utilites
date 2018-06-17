import os
import sys
import re
import tempfile
import getopt

def getVideoDetails(filepath):
    """Returns Video file metadata
    GLOBAL - Duration, bitrate
    VIDEO - codec, resolution, bitrate, fps
    AUDIO - codec, frequency, bitrate
    
    Arguments:
        filepath {[type]} -- [string]
    
    Returns:
        [Json] -- [Metadata Key-value pair in JSON format]
    """

    tmpf = tempfile.NamedTemporaryFile()
    os.system("ffmpeg -i \"%s\" 2> %s" % (filepath, tmpf.name))
    lines = tmpf.readlines()
    tmpf.close()
    metadata = {}
    
    for l in lines:

        l = l.strip()    
        if l.startswith(b'Duration'):
            metadata['duration'] = re.search(b'Duration: (.*?),', l).group(0).split(b':',1)[1].strip(b' ,')
            metadata['bitrate'] = re.search(b"bitrate: (\d+ kb/s)", l).group(0).split(b':')[1].strip()
        if l.startswith(b'Stream #0:0'):
            metadata['video'] = {}
            metadata['video']['codec'], metadata['video']['profile'] = \
                [e.strip(b' ,()') for e in re.search(b'Video: (.*? \(.*?\)),? ', l).group(0).split(b':')[1].split(b'(')]
            metadata['video']['resolution'] = re.search(b'([1-9]\d+x\d+)', l).group(1)
            metadata['video']['bitrate'] = re.search(b'(\d+ kb/s)', l).group(1)
            metadata['video']['fps'] = re.search(b'(\d+ fps)', l).group(1)
        if l.startswith(b'Stream #0:1'):
            metadata['audio'] = {}
            metadata['audio']['codec'] = re.search(b'Audio: (.*?) ', l).group(1)
            metadata['audio']['frequency'] = re.search(b', (.*? Hz),', l).group(1)
            metadata['audio']['bitrate'] = re.search(b', (\d+ kb/s)', l).group(1)
    return metadata

def allowedfilexts(ext):
    """Check if video extension is allowed to get picked up
    
    Arguments:
        ext {[string]} -- [file extension in string format.]
    
    Returns:
        [bool] -- [Whether that ext. is allowed or not]
    """
    #Add/Remove the extensions to suit your need
    ALLOWED_EXTS = ['.avi', '.divx', '.flv', '.m4v', '.mkv', '.mov', '.mpg', '.mpeg', '.wmv','.mp4']
    
    if ext.lower() in (ALLOWED_EXTS):
        return True
    else:
        return False

def displayFileProperties(filelist):    
    for file in filelist:
        print(f"file name:{file}\n")
        print(getVideoDetails(file))
        print("+++++++++++\n")
        print("+++++++++++\n")
    
#Video files path
VIDEOFILEPATH = os.getcwd() + '/video'

fileList  = [] #Video files to be processed

# Preparing the list of video files only. Presence of none video file won't cause any problem. 
for _, _, files in os.walk(VIDEOFILEPATH):
    
    for file in files:
        filePath = VIDEOFILEPATH + "/" + file
        theFile = os.path.join(VIDEOFILEPATH,file)
        
        # Pick only allowed file extensions
        fileName, fileExtension = os.path.splitext(theFile)

        if allowedfilexts(fileExtension):
            print('Adding to the  processing list',theFile)
            fileList.append(theFile)


#Time to display the video file metadata
displayFileProperties(fileList)

 


