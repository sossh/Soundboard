import customtkinter
from PIL import Image
from tkinter import PhotoImage
import time

# Import Objects
from Soundboard import Soundboard
from Sound import Sound
from SoundManager import SoundManager
from SettingsManager import SettingsManager
from HotkeyManager import HotkeyManager
from NewAudioGUI import NewAudioGUI
from EditAudioGUI import EditAudioGUI
from SettingsGUI import SettingsGUI
from WelcomeWindow import WelcomeWindow
from MessageWindow import MessageWindow



customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class SoundboardGUI(customtkinter.CTk):
    def __init__(self, configFilePath, soundsFilePath):
        super().__init__()

        # Init Constants
        self.CONFIG_FILE_PATH = configFilePath # The file that contains the data for SettingsManager.
        self.AUDIO_FILE_PATH  = soundsFilePath # The file that contains the data for SoundManager.
        self.WINDOW_WIDTH = 1100               # Default Width of the Soundboard
        self.WINDOW_HEIGHT = 350               # Default Height of the Soundboard
        self.BUTTON_WIDTH = 140                # The Default width of a audio button. Does not respect this as max size so dont always belive this.
        self.RIGHT_FRAME_WIDTH = 900           # The Default width of the right frame.
        self.HOTKEY_VOLUME_CHNAGE_AMOUNT = 5   # The % Amount the hotky will change the volume by.
        self.AP_BUTTON_COLOUR = "#1f6aa5"    # The color the audio players button will be
        self.numButtonsPerRow = 0              # The number of buttons per row currently active
        self.oldButtonWidth = 0                # The width of buttons, needs to be dynamic because of screen sizes

        ## Init Settings and Sound Manager ##
        self.settingsManager = SettingsManager(self.CONFIG_FILE_PATH)
        self.hotkeyManager = HotkeyManager()
        self.soundManager = SoundManager(self.AUDIO_FILE_PATH)

        # Get the Audio Devices we will use
        self.inputDevice = self.settingsManager.getInputDeviceName()
        self.outputDevice = self.settingsManager.getOutputDeviceName()
        self.virtualDevice = self.settingsManager.getVirtualDeviceName()

        ## Init the Audio Player ##
        self.soundPlayer = Soundboard(self.inputDevice, self.outputDevice, self.virtualDevice)
        
        ## Init Data Instance Variables(settings) ##
        self.restartOnClose = False                          # True if the program should restart when its closed.
        self.updateSliderPosition = True                     # Stops slider from moving when user it moving it.
        self.alreadyRedrawingSounds = False                  # Used to stop a redraw when we already are doing it.
        self.maxVolume = self.settingsManager.getMaxVolume() # The maximum volume multiplier that the user can set


        ## Init GUI Elements ##
        self._setupWindow()
        self._setupAudioPlayerPanel()
        self._setupRightPanel()


        # Setup the update loop(handles GUI updates)
        self.fps = 15
        self.update_interval = int(1000 / self.fps)
        self.update_id = self.after(self.update_interval, self.updateGUI)

        # Wait a little for Widgets to populate.
        self.after(10,self._displaySounds)

        # Init Hotkeys
        self._initHotkeys()

        self._resizeWindow()

        # Check if we should display the help and anouncements window
        if(self.settingsManager.getShowMessageOnStartup()):
            WelcomeWindow(self, self.settingsManager)

        # Check if the Virtual Device Exists.
        if(not self.soundPlayer.virtualDeviceExists()):
            MessageWindow(self, self.settingsManager, "Audio Device not found: Cable Input (VB-Audio Virtual Cable)")
        
        

    def _setupWindow(self):
        '''Configures the main window(sets up App title/icon)'''

        # Create and setup the main window
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.iconphoto(True,PhotoImage(file = self.settingsManager.getAppIconPath(".png")))
        self.title(self.settingsManager.getAppTitle())
        self.protocol("WM_DELETE_WINDOW", self._closeApp)
        self.wm_iconbitmap(self.settingsManager.getAppIconPath(".ico"))
        self.lift()
        self.attributes('-topmost', True)
        self.after(0, lambda: self.attributes('-topmost', False))

        self.grid_rowconfigure(0, weight=1)     # Allow both to stretch vertically
        self.grid_columnconfigure(0, weight=0)  # Set so audioPlayerFrame, doesn't horizontally
        self.grid_columnconfigure(1, weight=1)  # Set so rightFrame takes remaining space

    def _resizeWindow(self):
        '''Resizes the window after startup is done'''
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")

    def _setupAudioPlayerPanel(self):
        '''Setup the frame that contains the audio player(stuff on the left)'''

        # Create audio player frame
        self.audioPlayerFrame = customtkinter.CTkFrame(self)
        self.audioPlayerFrame.grid(row=0, column=0, sticky="nsew")
        self.audioPlayerFrame.grid_rowconfigure(0, weight=0)  # titleFrame
        self.audioPlayerFrame.grid_rowconfigure(1, weight=0)  # playFrame
        self.audioPlayerFrame.grid_rowconfigure(2, weight=0)  # volumeFrame
        self.audioPlayerFrame.grid_rowconfigure(3, weight=0)  # loopFrame
        self.audioPlayerFrame.grid_rowconfigure(4, weight=0)  # deleteFrame
        self.audioPlayerFrame.grid_columnconfigure(0, weight=1)

        # Create title frame(contains the title of a song)
        self.titleFrame = customtkinter.CTkFrame(self.audioPlayerFrame, fg_color="transparent")
        self.titleFrame.grid(row=0, column=0, sticky="nsew")
        self.audioTitleLabel = customtkinter.CTkLabel(self.titleFrame, text="_", fg_color="transparent", font=('bitter', 15, 'bold'))#(30 chars max)
        self.audioTitleLabel.grid(row=0, column=0,padx=(5, 5),pady=(10, 5))

        # Create frame that holds play button and audio position slider
        self.playFrame = customtkinter.CTkFrame(self.audioPlayerFrame, fg_color="transparent")
        self.playFrame.grid(row=1, column=0, sticky="nsew")
        self.playFrame.grid_columnconfigure(2, weight=1)
        self.playFrame.grid_rowconfigure(1, weight=1)
        self.currPosLabel = customtkinter.CTkLabel(self.playFrame, text="00:00", fg_color="transparent")
        self.currPosLabel.grid(row=0, column=0, padx=(5,3), sticky="e")
        self.audioPosSlider = customtkinter.CTkSlider(self.playFrame, state="disabled", from_=0, to=1, number_of_steps=10000)
        self.audioPosSlider.set(0)
        self.audioPosSlider.bind("<ButtonPress-1>", self._editSliderPosition)
        self.audioPosSlider.bind("<ButtonRelease-1>", self._setAudioPosition)
        self.audioPosSlider.grid(row=0, column=1, padx=(2,2),pady=(10, 15), sticky="nsew")
        self.audioLengthLabel = customtkinter.CTkLabel(self.playFrame, text="00:00", fg_color="transparent")
        self.audioLengthLabel.grid(row=0, column=2, padx=(3,5), sticky="w")
        self.playPauseBtn = customtkinter.CTkButton(self.playFrame, text="Play", command=self._toggleAudio)
        self.playPauseBtn.grid(row=1, column=1,padx=0)

        # Create volume slider frame
        self.volumeFrame = customtkinter.CTkFrame(self.audioPlayerFrame, fg_color="transparent")
        self.volumeFrame.grid(row=2, column=0, pady=(30, 5), sticky="nsew")
        self.volumeIconImage = customtkinter.CTkImage(light_image=Image.open(self.settingsManager.getImagePath("volume.PNG")),dark_image=Image.open(self.settingsManager.getImagePath("volume.PNG")),size=(30, 30))
        self.volumeIconLabel = customtkinter.CTkLabel(self.volumeFrame, image=self.volumeIconImage, text="")
        self.volumeIconLabel.grid(row=0, column=0, padx=(10, 0), sticky="nsew")
        self.volumeSlider = customtkinter.CTkSlider(self.volumeFrame, from_=0, to=self.maxVolume, number_of_steps=100)
        self.volumeSlider.set(1)
        self.volumeSlider.bind("<ButtonRelease-1>", self._setAudioVolume)
        self.volumeSlider.grid(row=0, column=1, padx=(10, 10), pady=(10, 5), sticky="nsew")

        # Create Loop Audio switch frame
        self.loopFrame = customtkinter.CTkFrame(self.audioPlayerFrame, fg_color="transparent")
        self.loopFrame.grid(row=3, column=0, pady=(5, 5), sticky="nsew")
        self.loopFrame.grid_columnconfigure(2, weight=1)
        self.loopImage = customtkinter.CTkImage(light_image=Image.open(self.settingsManager.getImagePath("loop.PNG")),dark_image=Image.open(self.settingsManager.getImagePath("loop.PNG")),size=(30, 30))
        self.loopIconLabel = customtkinter.CTkLabel(self.loopFrame, image=self.loopImage, text="")
        self.loopIconLabel.grid(row=0, column=0,padx=(10, 0),pady=(5, 5))
        self.loopSwitch = customtkinter.CTkSwitch(self.loopFrame, text="", command=self._setLoop, state="disabled", onvalue="on", offvalue="off")
        self.loopSwitch.grid(row=0, column=1,padx=(10, 10),pady=(10, 5))

        # Create Button Menu
        self.menuFrame = customtkinter.CTkFrame(self.audioPlayerFrame, fg_color="transparent")
        self.menuFrame.grid(row=4, column=0, columnspan=3, sticky="nsew")
        self.menuFrame.grid_columnconfigure(1, weight=1)

        # Create delete audio frame(the button that lets you delete an audio)
        self.deleteButtonFrame = customtkinter.CTkFrame(self.menuFrame, fg_color="transparent")
        self.deleteButtonFrame.grid(row=0, column=0, pady=(0, 5), sticky="nsew")
        self.deleteImage = customtkinter.CTkImage(light_image=Image.open(self.settingsManager.getImagePath("trash.PNG")),dark_image=Image.open(self.settingsManager.getImagePath("trash.PNG")),size=(30, 30))
        self.deleteIconLabel = customtkinter.CTkLabel(self.deleteButtonFrame, image=self.deleteImage, text="")
        self.deleteIconLabel.grid(row=0, column=0,padx=(10, 0),pady=(5, 5))
        self.deleteBtn = customtkinter.CTkButton(self.deleteButtonFrame, text="Delete", command=self._deleteAudio,width=70,fg_color="transparent",border_width=2, border_color=self.AP_BUTTON_COLOUR)
        self.deleteBtn.grid(row=0, column=1,padx=(10, 10),pady=(5, 5))

        # Create the Edit button
        self.editButtonFrame = customtkinter.CTkFrame(self.menuFrame, fg_color="transparent")
        self.editButtonFrame.grid(row=0, column=2, pady=(0, 5), sticky="nsew")
        self.editImage = customtkinter.CTkImage(light_image=Image.open(self.settingsManager.getImagePath("edit.PNG")),dark_image=Image.open(self.settingsManager.getImagePath("edit.PNG")),size=(30, 30))
        self.editIconLabel = customtkinter.CTkLabel(self.editButtonFrame, image=self.editImage, text="")
        self.editIconLabel.grid(row=0, column=0,padx=(10, 0),pady=(5, 5),sticky="e")
        self.editBtn = customtkinter.CTkButton(self.editButtonFrame, text="Edit", command=self._editAudio,width=70,fg_color="transparent",border_width=2, border_color=self.AP_BUTTON_COLOUR)
        self.editBtn.grid(row=0, column=1,padx=(10, 10),pady=(5, 5),sticky="w")

        # Create the Settings Button
        self.settingsButtonFrame = customtkinter.CTkFrame(self.menuFrame, fg_color="transparent")
        self.settingsButtonFrame.grid(row=1, column=0, pady=(0, 5), sticky="nsew")

        self.settingsImage = customtkinter.CTkImage(light_image=Image.open(self.settingsManager.getImagePath("settings.PNG")),dark_image=Image.open(self.settingsManager.getImagePath("settings.PNG")),size=(30, 30))
        self.settingsIconLabel = customtkinter.CTkLabel(self.settingsButtonFrame, image=self.settingsImage, text="")
        self.settingsIconLabel.grid(row=0, column=0,padx=(10, 0),pady=(20, 5),sticky="w")
        self.settingsBtn = customtkinter.CTkButton(self.settingsButtonFrame, text="Settings", command=self._openSettingsMenu,width=70,fg_color="transparent",border_width=2, border_color=['#a2a2a2', "#7c7c7c"], hover_color=['#7c7c7c', '#565656'])
        self.settingsBtn.grid(row=0, column=1 ,padx=(10, 10),pady=(20, 5))

        # Create the Help And Anouncements Button
        self.helpButtonFrame = customtkinter.CTkFrame(self.menuFrame, fg_color="transparent")
        self.helpButtonFrame.grid(row=1, column=2, pady=(0, 5), sticky="nsew")
        self.helpImage = customtkinter.CTkImage(light_image=Image.open(self.settingsManager.getImagePath("help.PNG")),dark_image=Image.open(self.settingsManager.getImagePath("help.PNG")),size=(30, 30))
        self.helpIconLabel = customtkinter.CTkLabel(self.helpButtonFrame, image=self.helpImage, text="")
        self.helpIconLabel.grid(row=0, column=0,padx=(10, 0),pady=(20, 5),sticky="e")
        self.helpBtn = customtkinter.CTkButton(self.helpButtonFrame, text="Help", command=self._openHelpAnouncmentsMenu,width=70,fg_color="transparent",border_width=2, border_color=['#a2a2a2', "#7c7c7c"], hover_color=['#7c7c7c', '#565656'])
        self.helpBtn.grid(row=0, column=1,padx=(10, 10),pady=(20, 5),sticky="w")


    def _setupRightPanel(self):
        '''Inits all widgets on the right panel.'''
         #create right frame
        self.rightFrame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.rightFrame.grid(row=0, column=1, sticky="nsew")
        self.rightFrame.grid_rowconfigure(1, weight=1)
        self.rightFrame.grid_columnconfigure(0, weight=1)
        

        #create search bar and add new audio frame
        self.searchFrame = customtkinter.CTkFrame(self.rightFrame,fg_color="transparent")
        self.searchFrame.grid(row=0, column=0, sticky="nsew",pady=(5,10))
        self.searchFrame.grid_columnconfigure(0, weight=1)
        self.searchFrame.grid_columnconfigure(1, weight=0)
        self.searchFrame.grid_columnconfigure(2, weight=0)
        self.searchBarEntry = customtkinter.CTkEntry(self.searchFrame, placeholder_text="Search Filter", width=400)
        self.searchBarEntry.grid(row=0, column=0, padx=5, pady=3, sticky="nsew")
        self.searchBarEntry.bind('<Return>', command=self._displaySounds)
        self.searchBtn = customtkinter.CTkButton(self.searchFrame, text="Go", command=self._displaySounds, width=40)
        self.searchBtn.grid(row=0, column=1,padx=0)

        self.addNewAudioBtn = customtkinter.CTkButton(self.searchFrame, command=self._addAudio, text="New Audio", width=100)
        self.addNewAudioBtn.grid(row=0, column=2,padx=(65,5), sticky="e")

        self.audioScrollFrame = customtkinter.CTkScrollableFrame(self.rightFrame, fg_color="transparent")
        self.audioScrollFrame.grid(row=1, column=0, sticky="nsew")


#================ GUI Update/Control Methods ================#
    def updateGUI(self):
        '''Method called within the mainloop that updates GUI'''

        # Set the ID to none so we dont try to cancel while we are in this method
        self.update_id = None
        
        if self.soundPlayer.isActive(): 
            self.playPauseBtn.configure(text="Pause")
        else:
            self.playPauseBtn.configure(text="Play")

        # Check if the user is editing the slider, dont change it if we are
        if self.updateSliderPosition and self.soundPlayer.isSoundLoaded(): 
            currPos = self.soundPlayer.getAudioPosition()
            
            self.audioPosSlider.set(currPos)
            self.currPosLabel.configure(text=time.strftime("%M:%S", time.gmtime(currPos)))

        # Check if we need to update the layout of buttons
        self.audioScrollFrame.update_idletasks()
        currFrameWidth = self.audioScrollFrame.winfo_width()
        
        if(self.numButtonsPerRow != self.getNumButtonsPerRow(currFrameWidth, self.oldButtonWidth)):
            
            # Schedule A Resize in 100ms
            if(not self.alreadyRedrawingSounds and self.resizeID is None):
                self.alreadyRedrawingSounds = True
                self.resizeID = self.after(100, self._displaySounds)


        # Schedule the next update
        self.update_id = self.after(self.update_interval, self.updateGUI)

    def shouldRestartSoundboard(self)->bool:
        '''Returns True if we should restart the soundboard after it has closed, used for changing settings. Use to check after mainloop ends.'''
        restart = False

        # Check if we should restart then set to false
        if(self.restartOnClose):
            restart = True
            self.restartOnClose = False

        return restart
    
    def _closeApp(self):
        '''Close the app'''

        # Stop the update event
        if(self.update_id):
            self.after_cancel(self.update_id)

        # Close the Soundboard
        self.soundPlayer.close()

        # Close hotkeys
        self.hotkeyManager.deactivateHotkeys()

        # Destroy all gui widgets
        self.destroy()

    def _restartApp(self):
        '''Set the restart flag and close the app'''

        # Set it so we restart when we close
        self.restartOnClose = True

        # Stop Audio
        self.soundPlayer.stopSound()

        # Close the app so it can be restarted
        self._closeApp()

    def _initHotkeys(self):
        '''Inits hotkeys with the SettingsManager and adds them to the HotkeyManager'''

        # Init the hotkey for toggling Audio
        self.hotkeyManager.addHotkey(self.settingsManager.getHotkey("Toggle Audio"), self._toggleAudio)

        # Init the hotkey Increasing Volume
        self.hotkeyManager.addHotkey(self.settingsManager.getHotkey("Volume Up"), self._volumeUp)

        # Start activate all hotkeys
        self.hotkeyManager.activateHotkeys()


#================== GUI Behaviour Methods =============================#

    def _toggleAudio(self):
        '''Used so we can set the button to display the correct text faster.'''

        # We are just about to stop audio, set before stopping because it looks better
        if self.playPauseBtn.cget("text") == "Pause" and self.soundPlayer.isActive():
            self.playPauseBtn.configure(text="Play")
    
        # Toggle the audio
        self.soundPlayer.toggleSound()

    def _volumeUp(self):
        '''Increases Volulme by HOTKEY_VOLUME_CHNAGE_AMOUNT points'''
        # Check if audio is currently playing
        isActive = self.soundPlayer.isActive()

        # Stops the audio from playing
        self.soundPlayer.stopSound()

        # Get the volume to set the audio to, and set it
        vol = self.volumeSlider.get()
        vol += vol*(self.HOTKEY_VOLUME_CHNAGE_AMOUNT/100)
        self.volumeSlider.set(vol)
        self.soundPlayer.setVolume(vol)

        # Restart the audio if it was playing
        if(isActive):
            self.soundPlayer.playSound()


    def _editSliderPosition(self, pos):
        '''Stops updateGUI() from changing the sliders position while the user is editing it'''
        self.updateSliderPosition = False

    def _setAudioPosition(self, event):
        '''Sets the audio postion to the position of the position slider.'''
        if(self.soundPlayer.isSoundLoaded()):

            # Check if audio is currently playing
            isActive = self.soundPlayer.isActive()

            # Get the position to set the audio to
            pos = self.audioPosSlider.get()

            # Change the audio position
            self.soundPlayer.stopSound()
            self.soundPlayer.setStartingPosition(pos)
            
            # Restart the audio if it was playing
            if(isActive):
                self.soundPlayer.playSound()

            # A new audio position has been set, so allow the GUI to update again
            self.updateSliderPosition = True

    def _setAudioVolume(self, event):
        '''Sets the audio volume to the position of the volume slider.'''

        # Check if audio is currently playing
        isActive = self.soundPlayer.isActive()

        # Stops the audio from playing
        self.soundPlayer.stopSound()

        # Get the volume to set the audio to, and set it
        vol = self.volumeSlider.get()
        self.soundPlayer.setVolume(vol)

         # Restart the audio if it was playing
        if(isActive):
            self.soundPlayer.playSound()

    def _setLoop(self):
        '''Enable looping for the soundboard.'''
        # Don't let the user try to loop when no sound is loaded
        if not self.soundPlayer.isSoundLoaded():
            self.loopSwitch.deselect()
            return
        
        # If the switch is set to on then loop audio
        loop = self.loopSwitch.get() == "on"
        self.soundPlayer.setLooping(loop)
    
    def _deleteAudio(self):
        '''Delete the currend audio loaded in the sound player.'''
        audioToDelete = self.soundPlayer.getSound()

        # If an audio is loaded we will delete it
        if(audioToDelete != None):

            # Stop the audio from from playing
            self.soundPlayer.stopSound()

            # Reset the Audio Player
            self.soundPlayer.reset()

            # Reset the GUI Components
            self.unloadSound()

            # Delete the aduio
            self.soundManager.deleteAudio(audioToDelete)

            # Re-Init the Sounds
            self._displaySounds()

#========== Open Windows Methods =========#

    def _addAudio(self):
        '''Opens the add audio menu so the user can create a new sound.'''

        # Stop audio if it is playing
        self.soundPlayer.stopSound()

        # Open the add audio menu
        NewAudioGUI(self, self.soundManager, self.settingsManager, on_close=self._displaySounds)

    def _editAudio(self):
        '''Opens the edit audio menu so the user can edit the currently loaded sound'''

        # Get the current audio loaded so we can edit it
        audioToEdit = self.soundPlayer.getSound()

        # Make sure we have an audio loaded
        if(audioToEdit != None):

            # Stop audio if it is playing
            self.soundPlayer.stopSound()

            # Open the edit menu
            EditAudioGUI(self, self.soundManager, self.settingsManager, audioToEdit, on_close=self._displaySounds)

    def _openSettingsMenu(self):
        '''Opens the settings window and stops audio from playing'''

        # Stop audio if it is playing
        self.soundPlayer.stopSound()

        SettingsGUI(self, self.settingsManager, on_close=self._restartApp)
        
    def _openHelpAnouncmentsMenu(self):
        '''Opens the Welcome Window.'''

        # Open the window
        WelcomeWindow(self, self.settingsManager)
    

        

        







#======================= Sound Management Methods =========================#
    def _displaySounds(self, value=None):
        '''Displays all sounds to the screen. The parameter just lets the entry call this function, it is unused.'''

        # Get data for button and frame width, so we can determine how many buttons to put per row
        currFrameWidth = 0
        buttonWidth = self.BUTTON_WIDTH
        if(self.audioScrollFrame is not None):

            # Create a test button so we can determine how many buttons will fit
            testButton = customtkinter.CTkButton(self.audioScrollFrame, text="", bg_color="transparent", fg_color="transparent")
            testButton.grid(row=0,column=0)

            # Get Data from GUI Objects
            self.audioScrollFrame.update_idletasks()
            buttonWidth = testButton.winfo_width()
            currFrameWidth = self.audioScrollFrame.winfo_width()

        # Set the frames width
        self.oldButtonWidth = buttonWidth

        # Delete the old scroll frame
        self.audioScrollFrame.destroy()

        # Create/Remake the frame that holds all of the sounds
        self.audioScrollFrame = customtkinter.CTkScrollableFrame(self.rightFrame, fg_color="transparent")
        self.audioScrollFrame.grid(row=1, column=0, sticky="nsew")

        # Determine the number of cols to make
        self.numButtonsPerRow = self.getNumButtonsPerRow(currFrameWidth, buttonWidth)
        

        filterTerm = self.searchBarEntry.get()
        soundList = self.soundManager.getSoundsFiltered(filterTerm)
        
        for i, sound in enumerate(soundList):
            col = i%self.numButtonsPerRow
            row = i//self.numButtonsPerRow
            action = lambda x = sound.getIndex(): self._loadSoundFromIndex(x)
            self.newAudioBtn = customtkinter.CTkButton(self.audioScrollFrame, command=action, width=self.BUTTON_WIDTH, text=sound.getTitle(), font=('bitter',10),fg_color="transparent",hover_color=sound.getHoverColor(), border_width=2, border_color=sound.getBorderColor())
            self.newAudioBtn.grid(row=row, column=col,padx=(5, 5),pady=(5, 5))

        # We are done redrawing the sounds
        self.alreadyRedrawingSounds = False
        self.resizeID = None

    def _loadSoundFromIndex(self, index:int):
        '''Loads a sound into the soundboard via its index in the sound file'''
        # Get the sound at that index and load it
        sound = self.soundManager.getSoundByIndex(index)
        self._loadSound(sound)

    def _loadSound(self, sound:Sound):
        '''Loads a sound and inserts its information into the interface'''

        # Load the sound into the soundplayer
        self.soundPlayer.stopSound()
        self.soundPlayer.loadSound(sound)

        # Disable looping
        self.soundPlayer.setLooping(False)

        # Edit gui elements
        self.playPauseBtn.configure(text="Play")
        self.audioPosSlider.configure(to=sound.getDuration())
        self.currPosLabel.configure(text=time.strftime("%M:%S", time.gmtime(0)))
        self.audioLengthLabel.configure(text=time.strftime("%M:%S", time.gmtime(sound.getDuration())))
        self.audioTitleLabel.configure(text=sound.getTitle())

        self.audioPosSlider.configure(state="normal")
        self.loopSwitch.configure(state="normal")
        self.loopSwitch.deselect()

    def unloadSound(self):
        '''Unloads the sound and its information from the Interface'''

        # Disable looping
        self.soundPlayer.setLooping(False)

        # Edit gui elements
        self.playPauseBtn.configure(text="Play")
        self.audioPosSlider.set(0)
        self.audioPosSlider.configure(to=0)
        self.currPosLabel.configure(text=time.strftime("%M:%S", time.gmtime(0)))
        self.audioLengthLabel.configure(text=time.strftime("%M:%S", time.gmtime(0)))
        self.audioTitleLabel.configure(text="-")

        self.audioPosSlider.configure(state="disabled")
        self.loopSwitch.configure(state="disabled")
        self.loopSwitch.deselect()


#============= Misc Private Methods ===============#
    def getNumButtonsPerRow(self, currFrameWidth:int, buttonWidth:int)->int:
        '''Returns the number of buttons that will fit on each row with given sizes'''
        return max(1, currFrameWidth // (buttonWidth+10))