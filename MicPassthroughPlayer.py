import sounddevice as sd
from numpy import pad, repeat, column_stack
from threading import Thread, Event
from AudioPlayer import AudioPlayer


# Concrete Class that plays audio through a virtural cable, and passes audio to the virtural cable.
# Allows you to set your audio device to the virtural cable and play audio through your microphone.
class MicPassthroughPlayer(AudioPlayer):
    def __init__(self, inputDevice:str|None=None, virtualDevice:str|None=None):

        # Call Super Constructor
        super().__init__()

        # Constants
        self.VIRTUAL_CABLE_NAME = "cable input (vb-audio virtual cable)"

        # Init the input device
        self.inputDevice = self._getAudioDevice(inputDevice)  #Try to find the device the user wants
        if(self.inputDevice is None):
            self.inputDevice = self._getDefaultDevice(True)   # Get the default output device

        # Init the device that handles output device to input device passthrough
        self.virtualDevice = self._getAudioDevice(virtualDevice)
        if(self.virtualDevice is None):
            self.virtualDevice = self._getAudioDevice(self.VIRTUAL_CABLE_NAME)

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
        # Make sure a sound is loaded
        if(self.isSoundLoaded()):

            # Set to inactive(will make audio stop)
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
    
    def virtualDeviceExists(self):
        '''Returns true if the virtual device is not None.'''
        return self.virtualDevice is not None


    def _startAudioThread(self):
        self._thread = Thread(target=self._mic_loop, args=(), daemon=True)
        self._thread.start()

    def _mic_loop(self):
        '''Starts stream for mic-to-virtual cable passthrough.'''
        with sd.Stream(device=(self.inputDevice, self.virtualDevice),
                    samplerate=self.sampleRate,
                    channels=(1, 2),  # 1 mic input, 2 virtual output(stereo)
                    dtype='float32',
                    callback=self._audioCallback) as stream:
            self._stopEvent.wait()

    def _audioCallback(self, indata, outdata, frames, time, status):
        '''Callback function for mixing microphone + file output'''
        

        output_channels = 2 # Stereo Audio
        mic_chunk = indata

        # Mic is mono so duplicate on 2 channels to make is "stereo"
        if mic_chunk.shape[1] == 1:
            mic_chunk = repeat(mic_chunk, 2, axis=1)
        # If the input has too many or too few channels make it match output_channels
        elif mic_chunk.shape[1] < output_channels:
            mic_chunk = pad(mic_chunk, ((0, 0), (0, output_channels - mic_chunk.shape[1])), 'constant')
        elif mic_chunk.shape[1] > output_channels:
            mic_chunk = mic_chunk[:, :output_channels]

        # Default output is mic
        output = mic_chunk
        outdata[:] = output

        # If sound is playing we mix it in with the mic input, else just output mic
        if self.isActive() and (self.virtualDevice is not None):

            # Get audio start/end positions
            start = self.audioPosition
            end = start + frames

            # Check if we have gone past the end of the audio
            if(end > len(self.audioData)):
                if(self.loopAudio):
                    chunk = self.audioData[0:frames]  # Start from the beginning if we've reached the end
                    self.audioPosition = frames # Start the position at the new chunk
                else:
                    self.stopSound()   # Stops audio from playing
                    outdata[:] = mic_chunk
                    return             # Audio has stopped so leave early
                
            # We did not go past the end of the audio so play normally
            else:
                # Get the data chunk
                chunk = self.audioData[start:end]

                # Update the audio position to be at the end of this buffer
                self.audioPosition = end

            if chunk.shape[0] < frames:
                chunk = pad(chunk, ((0, frames - chunk.shape[0]), (0, 0)), 'constant')

            # Change the volume of the output
            chunk = chunk * self.audioVolume

            # If chunk is 1D (mono), duplicate it for stereo output
            if chunk.ndim == 1:
                chunk = column_stack([chunk, chunk])

            # Mix sound and mic half and half
            output = 0.5 * mic_chunk + 0.5 * chunk

        outdata[:] = output






