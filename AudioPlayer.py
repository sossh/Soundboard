from abc import abstractmethod
import sounddevice as sd
from Sound import Sound
from AudioPlayerInterface import AudioPlayerInterface

# Abstaract Class that provides common functionalities for AudioPlayers
class AudioPlayer(AudioPlayerInterface):
    def __init__(self):

        # State of Player
        self._audioPlaying = False      # Will be set to true when audio is started, set to false when audio stops

        # Volume Settings
        self.MAX_VOLUME = 1             # Max Volume Multiplier
        self.MIN_VOLUME = 0             # Min Volume Multiplier
        self.audioVolume = 1            # Volume multiplier between 0-1

        # Misc Settings
        self.loopAudio = False          # True if audio should keep looping false if not

        # Data for the sound loaded
        self.audioPosition = 0          # The audio position we are currently at on the sound
        self.audio = None               # The Sound loaded into the soundboard 
        self.audioData = None           # The Audio Data of the sound(to be played)
        self.sampleRate = 0             # The sample rate of the Audio Data
        self.audioStartPosition = 0     # The position the audio will start at
        self.audioDefaultPosition = 0   # The position audioStartPosition will be set to(lets you crop audio) 

        self._reset()   # Reset all settings



    @abstractmethod
    def playSound(self):
        '''Start playing audio.'''
        pass

    @abstractmethod
    def stopSound(self):
        '''Stops playing audio.'''
        pass

    def toggleSound(self):
        '''Plays audio if audio is stopped, or Stops audio when audio is playing'''
        # If audio is playing stop it
        if(self.isActive()):
            self.stopSound()
        # If audio is stopped play it
        else:
            self.playSound()
        
    def isActive(self):
        '''Returns true if there is audio currently playing, else returns false.'''
        return (self._audioPlaying) and self.isSoundLoaded()

    def loadSound(self, sound:Sound):
        '''Load in a audio and prep it to be played.'''
        self._reset()   # Reset the AP to its initial state

        self.audio = sound
        self.audioData = sound.getAudioData()
        self.sampleRate = sound.getSampleRate()
        #SETUP AUDIO CROPPING
        self.audioPosition = 0
        self.audioDefaultPosition = 0

    def getSound(self) -> Sound:
        '''Returns the Sound currently loaded in the soundboard.'''
        return self.audio

    def isSoundLoaded(self):
        '''Returns true if there is a sound loaded in the soundboard'''
        return (self.audio is not None) and (self.sampleRate is not None) and (self.audioData is not None)
    
    def getAudioPosition(self):
        '''Gets the current position(in secconds) the playing audio is at.'''
        # If the audio is playing calculate the position
        # If the audio isn't playing return where it will start at if it is played
        if(self.isActive()):
            pos = self.audioPosition/self.sampleRate

            # Shouldnt ever be needed but check if we are still in bounds of the audio
            if(pos > self.audio.getDuration()):
                pos = self.audioStartPosition/self.sampleRate

        # Audio isnt playing so return the start position
        else:
            pos = self.audioStartPosition/self.sampleRate

        return pos
    
    def setStartingPosition(self, position):
        '''Sets the position in secconds to start the audio at.'''
        if(self.isSoundLoaded()):
            self.audioStartPosition = int(self.sampleRate * position)

    def setVolume(self, volume):
        '''This method takes in a volume multiplier beween 0-1.'''

        # Make sure audio is not less than 0
        if(volume<self.MIN_VOLUME): self.audioVolume = self.MIN_VOLUME
        # Make sure audio is not too loud
        elif(volume>self.MAX_VOLUME): self.audioVolume = self.MAX_VOLUME
        # Set volume
        else: self.audioVolume = volume

    def getVolume(self):
        '''Returns the volume level (between 0-1) that the audio player is currently using.'''
        return self.audioVolume
    
    def setLooping(self, loopAudio:bool):
        '''If True, the audio will continuously loop after reaching the end.'''
        self.loopAudio = loopAudio

#============== Private Internal Mehtods =================#
    def _getDefaultDevice(self, isInput:bool):
        '''Gets the id of the default audio device. True for input, False for output.'''
        device = 0
        if(isInput):
            device = sd.default.device[0]
        else:
            device = sd.default.device[1]

        return device

    def _getAudioDevice(self, deviceName:str)->int:
        '''Gets the id of the audio device with the given name. "default" or None will return device'''
        if(deviceName is not None):
            deviceLower = deviceName.lower()
            if(deviceLower != "default"):

                # Find the output device with the right name
                for i, device in enumerate(sd.query_devices()):
                    if(device['name'].lower() in deviceLower or device['name'].lower() == deviceLower):  
                        return i
            
        # If we are here return none, so it will be overwritten with the default
        return None
    
    def _isReady(self):
        '''Returns true if we are ready to start playing audio'''
        return (not self.audio is None) and (self._audioPlaying == False)

    def _reset(self):
        '''Reset the soundboard to its original state, used commonly for unloading sounds.'''
        # State
        self._audioPlaying = False      # Will be set to true when audio is started, set to false when audio stops

        # Volume Settings
        self.MAX_VOLUME = 1             # Max Volume Multiplier
        self.MIN_VOLUME = 0             # Min Volume Multiplier
        self.audioVolume = 1            # Volume multiplier between 0-1

        # Misc Settings
        self.loopAudio = False          # True if audio should keep looping false if not

        # Data for the sound loaded
        self.audioPosition = 0          # The audio position we are currently at on the sound
        self.audio = None               # The Sound loaded into the soundboard 
        self.audioData = None           # The Audio Data of the sound(to be played)
        self.sampleRate = None          # The sample rate of the Audio Data
        self.audioStartPosition = 0     # The position the audio will start at
        self.audioDefaultPosition = 0   # The position audioStartPosition will be set to(lets you crop audio) 
    