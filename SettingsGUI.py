import customtkinter
from tkinter import PhotoImage
from SettingsManager import SettingsManager
from HotkeyManager import HotkeyManager

# A window for editing settings
class SettingsGUI(customtkinter.CTkToplevel):
    def __init__(self, master, settingsManager:SettingsManager, on_close=None):

        # Call Super Constructor
        super().__init__(master)

        # Init Instance Vars
        self.settingsManager = settingsManager
        self.on_close = on_close
        

        # Setup GUI
        self._setupWindow()
        self._setupSettingsPanel()


    def _setupWindow(self):
        '''Sets up the window that other gui components go in.'''
        # Setup
        self.wm_iconbitmap(self.settingsManager.getAppIconPath(".ico"))
        self.iconphoto(True,PhotoImage(file = self.settingsManager.getAppIconPath(".png")))
        self.focus()
        self.protocol("WM_DELETE_WINDOW", self._on_close) # set the function that happens when the window is closed
        self.title("Settings")
        self.attributes("-topmost", True)

        # Wait for the window to display, then set as the only useable window
        # Note: this is technically a bug as the user has 10ms to fuck shit up, but idgaf
        self.after(10, self.grab_set)

    def _setupSettingsPanel(self):
        '''Setup where settings will be stored.'''

        # Setup the frame that holds all settings
        self.settingsFrame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.settingsFrame.pack(anchor="center", padx=10, pady=10)
        

        # Setup Audio Device Settings
        self._setupAudioDeviceSettings()

        # Setup Hotkey Settings
        self._setupHotkeySettings()

        # Setup the button that saves your changes
        self.doneButton = customtkinter.CTkButton(self.settingsFrame, text="Save Changes and Restart", command=self._saveAndExit)
        self.doneButton.pack(anchor="center", pady = 15)


    def _setupAudioDeviceSettings(self):
        '''Setups GUI for audio device settings.'''

        # Create the frame that audio settings go inside
        self.audioDeviceFrame = customtkinter.CTkFrame(self.settingsFrame, fg_color="transparent")
        self.audioDeviceFrame.pack(anchor="center", padx=10, pady=(10,20), expand=True)
        self.audioDeviceFrame.grid_columnconfigure(1, weight=1)

        # Create the audio device settings title
        self.audioDeviceTitleLabel = customtkinter.CTkLabel(self.audioDeviceFrame, text="Audio Device Settings", font=('bitter', 15, 'bold'))
        self.audioDeviceTitleLabel.grid(row=0, pady=5)

        # Get all audio devices
        allInputDevices = self.settingsManager.getAllInputDeviceNames()
        allOutputDevices = self.settingsManager.getAllOutputDeviceNames()
        
        # Setup GUI for input device
        self.inputDeviceLabel = customtkinter.CTkLabel(self.audioDeviceFrame, text="Input Device:",font=('bitter',12))
        self.inputDeviceLabel.grid(row=1, column=0, pady = 5, padx=(0,3), sticky="w")
        self.inputDeviceOptionMenu = customtkinter.CTkOptionMenu(self.audioDeviceFrame, values=allInputDevices)
        self.inputDeviceOptionMenu.grid(row=1, column=1, pady = 5, sticky="e")
        self.inputDeviceOptionMenu.set(self.settingsManager.getInputDeviceName())

        # Setup GUI for output device
        self.outputDeviceLabel = customtkinter.CTkLabel(self.audioDeviceFrame, text="Output Device:",font=('bitter',12))
        self.outputDeviceLabel.grid(row=2, column=0, pady = 5, padx=(0,3), sticky="w")
        self.outputDeviceOptionMenu = customtkinter.CTkOptionMenu(self.audioDeviceFrame, values=allOutputDevices)
        self.outputDeviceOptionMenu.grid(row=2, column=1, pady = 5, sticky="e")
        self.outputDeviceOptionMenu.set(self.settingsManager.getOutputDeviceName())

        # Setup GUI for virtual device
        self.virtualDeviceLabel = customtkinter.CTkLabel(self.audioDeviceFrame, text="Virtual Device:",font=('bitter',12))
        self.virtualDeviceLabel.grid(row=3, column=0, pady = 5, padx=(0,3), sticky="w")
        self.virtualDeviceOptionMenu = customtkinter.CTkOptionMenu(self.audioDeviceFrame, values=allOutputDevices)
        self.virtualDeviceOptionMenu.grid(row=3, column=1, pady = 5, sticky="e")
        self.virtualDeviceOptionMenu.set(self.settingsManager.getVirtualDeviceName())

    def _setupHotkeySettings(self):
        # Create the frame that audio settings go inside
        self.hotkeyFrame = customtkinter.CTkFrame(self.settingsFrame, fg_color="transparent")
        self.hotkeyFrame.pack(anchor="center", padx=10, pady=(10,20), expand=True)
        

        # Create the audio device settings title
        self.hotkeyTitleLabel = customtkinter.CTkLabel(self.hotkeyFrame, text="Hotkey Settings", font=('bitter', 15, 'bold'))
        self.hotkeyTitleLabel.grid(row=0, pady=5)

        # Create stuff for editing the toggle audio hotkey
        self.toggleHotkeyLabel = customtkinter.CTkLabel(self.hotkeyFrame, text="Input Device:",font=('bitter',12))
        self.toggleHotkeyLabel.grid(row=1, column=0, pady = 5, padx=(0,3), sticky="nsew")

        self.toggleHotkeyEntry = customtkinter.CTkEntry(self.hotkeyFrame, placeholder_text="Enter a key or its name.", width=150)
        self.toggleHotkeyEntry.grid(row=1, column=1, padx=5, pady=3, sticky="nsew")
        key = self.settingsManager.getHotkey("toggleAudio")
        if(key is None):
            key = ""
        self.toggleHotkeyEntry.insert(0, key)






#=========== GUI Command Methods =============#

    def _saveAndExit(self):
        '''Ran after the done button has been pressed, saves all changes and updates the settings file.'''

        # Get and Set input device
        self.settingsManager.setInputDeviceName(self.inputDeviceOptionMenu.get())

        # Get and Set output device
        self.settingsManager.setOutputDeviceName(self.outputDeviceOptionMenu.get())

        # Get and Set virtual device
        self.settingsManager.setVirtualDeviceName(self.virtualDeviceOptionMenu.get())

        # Get the hotkey for toggling audio and set if it is valid
        newKey = self.toggleHotkeyEntry.get()
        if((HotkeyManager.isValidKey(newKey) or newKey=="") and newKey != self.settingsManager.getHotkey("toggleAudio")):
            self.settingsManager.setHotkey("toggleAudio", newKey)

        # Restart the soundboard
        self._on_close(restart=True)

    def _on_close(self, restart=False):
        '''Called before we close the window.'''

        self.destroy()
        if(restart):
            self.on_close()

        

    



        

