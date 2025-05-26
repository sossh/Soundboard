import sounddevice as sd
from numpy import zeros, pad, column_stack
from threading import Thread, Event
from AudioPlayer import AudioPlayer

# Concrete Class that allows you to play audio through an output device on your computer.
class LocalSoundPlayer(AudioPlayer):

    def __init__(self, outputDevice:str|None=None):

        # Call Super Constructor
        super().__init__()

        # Init the device to play audio to
        self.outputDevice = self._getAudioDevice(outputDevice)  #Try to find the device the user wants
        if(self.outputDevice is None):
            self.outputDevice = self._getDefaultDevice(False)   # Get the default output device


        # Setup the event to close the audio player
        self._stopEvent = Event()

        # Init the audio playing thread
        self._thread = None
        self._startAudioThread()

    def playSound(self):
        '''Start playing audio, by setting a flag and allowing audio to pass'''
        if(self._isReady()):

            # Set to active 
            self._audioPlaying = True

            # Set the audio position to start at
            self.audioPosition = self.audioStartPosition


    def stopSound(self):
        '''Stops audio from playing if a sound is loaded'''
        # Make sure a sound is loaded
        if(self.isSoundLoaded()):

            # Set to inactive
            self._audioPlaying = False

            # Save the position we stopped at so we can start there later
            self.audioStartPosition = self.audioPosition

            # Can cause an error where we try to start playing past the file
            if(self.audioPosition >= self.audio.getDuration()*self.sampleRate):
                self.audioStartPosition = 0

    def close(self):
        '''Close the Audio player and stop all output thread'''

        # Just incase sound is still playing
        self.stopSound()

        # Set the exit event so stop playing
        self._stopEvent.set()        

        # Wait for the thread to finish
        if self._thread is not None:
            self._thread.join()      

                     



    def _startAudioThread(self):
        '''Starts the thread that manages audio playing'''
        self._thread = Thread(target=self._audioLoop, args=(), daemon=True)
        self._thread.start()
        

    def _audioLoop(self):
        '''Loop that plays audio, self._audioCallback() is called for each buffer.'''
        with sd.OutputStream(device=self.outputDevice,
                            samplerate=self.sampleRate,
                            channels=2, 
                            dtype='float32', callback=self._audioCallback) as stream:
            # Wait until stop signal is set
            self._stopEvent.wait()  


    def _audioCallback(self, data, frames, time, status):
        '''Callback function for mixing microphone + file output'''

        # If no audio is loaded or playback is inactive, fill with silence
        if not self.isActive() or self.audioData is None:
            data[:] = zeros((frames, data.shape[1]), dtype=data.dtype)
            return
        
        start = self.audioPosition
        end = start + frames
        chunk = self.audioData[start:end]

        # Update the audio position 
        self.audioPosition = end

        # Check if we have gone past the end of the audio
        if(end > len(self.audioData)):
            if(self.loopAudio):
                chunk = self.audioData[0:frames]  # Start from the beginning if we've reached the end
                self.audioPosition = frames # Start the position at the new chunk
            else:
                self.stopSound()   # Stops audio from playing
                data[:] = zeros((frames, data.shape[1]), dtype=data.dtype)
                return             # Audio has stopped so leave early
            
        # If the chunk isn't long enough pad with zeros
        if chunk.shape[0] < frames:
            chunk = pad(chunk, ((0, frames - chunk.shape[0]), (0, 0)), 'constant')

        # If chunk is 1D (mono), duplicate it for stereo output
        if chunk.ndim == 1:
            chunk = column_stack([chunk, chunk])
        

        data[:] = chunk * self.audioVolume


    
