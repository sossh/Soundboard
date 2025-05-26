from NewAudioGUI import NewAudioGUI
from Sound import Sound
from SoundManager import SoundManager
from MessageWindow import MessageWindow
from SettingsManager import SettingsManager

# GUI For editing audios, currently just reuses the gui from add audio with minor changes
class EditAudioGUI(NewAudioGUI):
    def __init__(self, mainWindow, soundManager:SoundManager, settingsManager:SettingsManager, sound:Sound, on_close=None):

        # Call Super Constructor
        super().__init__(mainWindow, soundManager, settingsManager, on_close)

        # Init Instance Variables
        self.soundToEdit = sound

        # Change Window Settings
        self.title("Edit Audio")

        # Disable the options change the files path
        self.filePathTextEntry.delete(0, len(self.filePathTextEntry.get()))
        self.filePathTextEntry.insert(0, sound.getPath())
        self.filePathTextEntry.configure(state="disabled")
        self.fileBrowseBtn.configure(state="disabled")

        # Set the audio title
        self.fileTitleEntry.delete(0, len(self.fileTitleEntry.get()))
        self.fileTitleEntry.insert(0, sound.getTitle())

        # Change the command that the done button uses
        self.doneButton.configure(command=self._editAudio)

        # Change the colors
        self._setWidgetColors(sound.getBorderColor())

    

    def _editAudio(self):
        '''Edits an audio with changes made in gui widgets.'''

        # Get the new title
        newTitle = self.fileTitleEntry.get()

        # Get the new Color
        newColor =  self.fileHexRGBEntry.get()

        # Get the new hover color
        newDark = self.darken_hex(newColor)

        # Try to edit audio
        errorMessage = self.soundManager.editAudio(self.soundToEdit, newTitle, newColor, newDark)

        # Check if we got an error
        if(errorMessage == ""):
            # Close the edit window
            self._closeWindow()
        else:
            # Display the error
            MessageWindow(self, self.settingsManager, "Audio not Edited\n\n"+errorMessage)





