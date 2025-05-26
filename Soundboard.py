from Sound import Sound
from AudioPlayerInterface import AudioPlayerInterface
from LocalSoundPlayer import LocalSoundPlayer
from MicPassthroughPlayer import MicPassthroughPlayer

# Basically just a container class to run 2 audio players at the same time.
# 1 for playing audio Locally, and another for playing audio through Microphone.
class Soundboard(AudioPlayerInterface):
    def __init__(self, inputDevice:str|None=None, outputDevice:str|None=None, virtualDevice:str|None=None):

        # Create Audio Player for playing audio Locally.
        self.localSoundPlayer = LocalSoundPlayer(outputDevice)

        # Create Audio Player for playing audio through Microphone.
        self.micPassPlayer    = MicPassthroughPlayer(inputDevice, virtualDevice)

    def playSound(self):
        '''Start playing audio.'''
        self.localSoundPlayer.playSound()
        self.micPassPlayer.playSound()

    def stopSound(self):
        '''Stops playing audio.'''
        self.localSoundPlayer.stopSound()
        self.micPassPlayer.stopSound()

    def toggleSound(self):
        '''Plays sound if it is off, Stops sound if it is on.'''
        self.localSoundPlayer.toggleSound()
        self.micPassPlayer.toggleSound()
    
    def isActive(self):
        '''Returns true if there is audio currently playing, else returns false.'''
        return self.localSoundPlayer.isActive() and self.micPassPlayer.isActive()
    
    def loadSound(self, sound:Sound):
        '''Load in a audio and prep it to be played.'''
        self.localSoundPlayer.loadSound(sound)
        self.micPassPlayer.loadSound(sound)

    def reset(self):
        '''Reset the Soundboard to its original state'''
        self.localSoundPlayer._reset()
        self.micPassPlayer._reset()

    def close(self):
        '''Close the Soundboard.'''
        self.localSoundPlayer.close()
        self.micPassPlayer.close()

    def getSound(self) -> Sound:
        '''Returns the audio currently loaded in the soundboard.'''
        return self.localSoundPlayer.getSound()

    def isSoundLoaded(self):
        '''Returns true if there is a sound loaded in the soundboard'''
        return self.localSoundPlayer.isSoundLoaded() and self.micPassPlayer.isSoundLoaded()
    
    def getAudioPosition(self):
        '''Gets the current position(in secconds) the playing audio is at.'''

        # Return the position for the local player, so it matches up with what the user is hearing.
        return self.localSoundPlayer.getAudioPosition()
    
    def setStartingPosition(self, position):
        '''Sets the position in secconds to start the audio at.'''
        self.localSoundPlayer.setStartingPosition(position)
        self.micPassPlayer.setStartingPosition(position)
    
    def setVolume(self, volume):
        '''This method takes in a volume multiplier beween 0-1.'''
        self.localSoundPlayer.setVolume(volume)
        self.micPassPlayer.setVolume(volume)

    def getVolume(self):
        '''Returns the volume level (between 0-1) that the audio player is currently using.'''
        # Maybe add a feature to have individual audio per player in the future
        
        # Check if the audio is at the same volume for each player, if not set them to be the same
        if(self.localSoundPlayer.getVolume() != self.micPassPlayer.getVolume()):
            self.setVolume(self.localSoundPlayer.getVolume())

        # Return the local audio volume
        return self.localSoundPlayer.getVolume()

    def setLooping(self, loopAudio:bool):
        '''If True, the audio will continuously loop after reaching the end.'''
        self.localSoundPlayer.setLooping(loopAudio)
        self.micPassPlayer.setLooping(loopAudio)

    def virtualDeviceExists(self):
        '''Returns true if the virtual device is not None.'''
        return self.micPassPlayer.virtualDeviceExists()

