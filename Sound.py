import soundfile as sf

# Class for storing/obtaining soundfile data.
class Sound:

    # Constructor
    def __init__(self, title:str, path:str, index:int, borderCol:str, hoverCol:str):
        self._title = title
        self._path = path
        self._index = index
        self._borderCol = borderCol
        self._hoverCol = hoverCol

    def __eq__(self, otherSound):
        '''Compares if this sounds has equal instance variables'''
        if isinstance(otherSound, self.__class__):
            return (self._title == otherSound._title 
                    and self._path == otherSound._path
                    and self._index == otherSound._index
                    and self._borderCol == otherSound._borderCol
                    and self._hoverCol == self._hoverCol)
        else:
            return None

    def getPath(self)->str:
        '''Returns the path to the file.'''
        return self._path
    
    def getTitle(self)->str:
        '''Returns the title of the audio.'''
        return self._title
    
    def getIndex(self)->int:
        '''Returns the sound index of the audio in the soundFile'''
        return self._index
    
    def getBorderColor(self)->str:
        '''Returns the border color associated with this sound.'''
        return self._borderCol
    
    def getHoverColor(self)->str:
        '''Returns the hover color associated with this sound.'''
        return self._hoverCol
    
    def getAudioData(self):
        '''Returns the Audio Data of this audio.'''
        return sf.read(self.getPath(), dtype='float32')[0]

    def getSampleRate(self):
        '''Returns the Sample rate of this audio.'''
        return sf.read(self.getPath(), dtype='float32')[1]
    
    def getDuration(self)->float:
        '''Returns the duration(secconds) of the audio.'''
        return self.getAudioData().shape[0] / self.getSampleRate()
    