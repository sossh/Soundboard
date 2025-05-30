import customtkinter
from tkinter import PhotoImage
from SettingsManager import SettingsManager
from HotkeyManager import HotkeyManager

# A window for editing settings
class SettingsGUI(customtkinter.CTkToplevel):
    def __init__(self, master, settingsManager:SettingsManager, on_close=None):

        # Call Super Constructor
        super().__init__(master)

        # Init Constants
        self.WINDOW_WIDTH = 400
        self.WINDOW_HEIGHT = 450

        # Init Instance Vars
        self.settingsManager = settingsManager
        self.on_close = on_close
        self.hotkeyEntryList = []
        

        # Setup GUI
        self._setupWindow()
        self._setupSettingsPanel()
        self._resizeWindow()


    def _setupWindow(self):
        '''Sets up the window that other gui components go in.'''
        # Setup
        #self.wm_iconbitmap(self.settingsManager.getAppIconPath(".ico"))
        self.iconphoto(True,PhotoImage(file = self.settingsManager.getAppIconPath(".png")))
        self.focus()
        self.protocol("WM_DELETE_WINDOW", self._on_close) # set the function that happens when the window is closed
        self.title("Settings")
        self.lift()
        self.attributes('-topmost', True)
        self.after(0, lambda: self.attributes('-topmost', False))

        # Wait for the window to display, then set as the only useable window
        # Note: this is technically a bug as the user has 10ms to fuck shit up, but idgaf
        self.after(10, self.grab_set)

    def _resizeWindow(self):
        '''Resize the window'''
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")

    def _setupSettingsPanel(self):
        '''Setup where settings will be stored.'''

        # Setup the frame that holds all settings
        self.grid_columnconfigure(0, weight=1)
        self.settingsFrame = customtkinter.CTkScrollableFrame(self, fg_color="transparent")
        self.settingsFrame.pack(padx=10, pady=10, expand=True, fill="both")
        
        

        # Setup Audio Device Settings
        self._setupAudioDeviceSettings()

        # Setup Hotkey Settings
        self._setupHotkeySettings()

        # Setup the button that saves your changes
        self.doneButton = customtkinter.CTkButton(self.settingsFrame, text="Save Changes and Restart", command=self._saveAndExit)
        self.doneButton.pack(anchor="center", pady = 1)


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

        currRow = 1
        hotkeys = self.settingsManager.getAllHotkeys()
        for hotkeyType in hotkeys.keys():

            # Create stuff for editing the toggle audio hotkey
            toggleHotkeyLabel = customtkinter.CTkLabel(self.hotkeyFrame, text=f"{hotkeyType} Hotkey:",font=('bitter',12))
            toggleHotkeyLabel.grid(row=currRow, column=0, pady = 5, padx=(0,3), sticky="w")

            # Create the entry that hold the key
            toggleHotkeyEntry = customtkinter.CTkEntry(self.hotkeyFrame, placeholder_text="Enter a key or its name.", width=150)
            toggleHotkeyEntry.grid(row=currRow, column=1, padx=5, pady=3, sticky="nsew")
            key = hotkeys[hotkeyType]
            if(key is None):
                key = ""
            toggleHotkeyEntry.insert(0, key)

            # Add the hotkey to the list so it can be accessed later
            self.hotkeyEntryList.append(toggleHotkeyEntry)

            # Move to the next row
            currRow +=1











#=========== GUI Command Methods =============#

    def _saveAndExit(self):
        '''Ran after the done button has been pressed, saves all changes and updates the settings file.'''

        # Get and Set input device
        self.settingsManager.setInputDeviceName(self.inputDeviceOptionMenu.get())

        # Get and Set output device
        self.settingsManager.setOutputDeviceName(self.outputDeviceOptionMenu.get())

        # Get and Set virtual device
        self.settingsManager.setVirtualDeviceName(self.virtualDeviceOptionMenu.get())


        # Get all hotkeys and set them in order
        hotkeys = self.settingsManager.getAllHotkeys()
        for keyEntry, hotkeyType in zip(self.hotkeyEntryList, hotkeys.keys()):

            # Get the key in this hotkeys entry
            newKey = keyEntry.get()

            # If the key is valid then set it
            if((HotkeyManager.isValidKey(newKey) or newKey=="") and newKey != hotkeys[hotkeyType]):
                self.settingsManager.setHotkey(hotkeyType, newKey)


        # Restart the soundboard
        self._on_close(restart=True)

    def _on_close(self, restart=False):
        '''Called before we close the window.'''

        self.destroy()
        if(restart):
            self.on_close()

        

    



        

