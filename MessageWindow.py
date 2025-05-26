import customtkinter
from tkinter import PhotoImage
from SettingsManager import SettingsManager

# Window that displays a message to the screen
class MessageWindow(customtkinter.CTkToplevel):

    def __init__(self, master, settingsManager:SettingsManager, message:str):

        # Call Super Constructor
        super().__init__(master)

        # Init Instance Variables
        self.settingsManager = settingsManager
        
        # Setup the Window
        self.attributes("-topmost", True)
        self.title("")
        self.wm_iconbitmap(self.settingsManager.getAppIconPath(".ico"))
        self.iconphoto(True,PhotoImage(file = self.settingsManager.getAppIconPath(".png")))
        self.focus()
        self.protocol("WM_DELETE_WINDOW", self._on_close) # set the function that happens when the window is closed

        # Display the message
        self.messageLabel = customtkinter.CTkLabel(self, text=message)
        self.messageLabel.pack(anchor="center", expand=True, padx=30, pady=15)


    def _on_close(self):
        '''Method that is called when x button is pressed.'''
        self.destroy()