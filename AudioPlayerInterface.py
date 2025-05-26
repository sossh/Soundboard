from abc import ABC, abstractmethod
from Sound import Sound
from time import sleep


# Abstract Class Interface for starting/stoping/loading audio
class AudioPlayerInterface(ABC):
    
    @abstractmethod
    def playSound(self):
        '''Start playing audio.'''
        pass

    @abstractmethod
    def stopSound(self):
        '''Stops playing audio.'''
        pass

    @abstractmethod
    def toggleSound(self):
        '''Plays audio if audio is stopped, or Stops audio when audio is playing'''
        pass
    
    @abstractmethod
    def isActive(self):
        '''Returns true if there is audio currently playing, else returns false.'''
        pass
    
    @abstractmethod
    def loadSound(self, sound:Sound):
        '''Load in a audio and prep it to be played.'''
        pass

    @abstractmethod
    def getSound(self):
        '''Returns the audio currently loaded in the soundboard.'''
        pass

    @abstractmethod
    def isSoundLoaded(self):
        '''Returns true if there is a sound loaded in the soundboard'''
        pass
    
    @abstractmethod
    def getAudioPosition(self):
        '''Gets the current position(in secconds) the playing audio is at.'''
        pass
    
    @abstractmethod
    def setStartingPosition(self, position):
        '''Sets the position in secconds to start the audio at.'''
        pass
    
    @abstractmethod
    def setVolume(self, volume):
        '''This method takes in a volume multiplier beween 0-1.'''
        pass

    @abstractmethod
    def getVolume(self):
        '''Returns the volume level (between 0-1) that the audio player is currently using.'''
        pass
    
    @abstractmethod
    def setLooping(self, loopAudio:bool):
        '''If True, the audio will continuously loop after reaching the end.'''
        pass

    @abstractmethod
    def close(self):
        '''Close the Audio Player.'''
        pass

    