import customtkinter
from tkinter import PhotoImage
from tkinter.filedialog import askopenfilename
from SoundManager import SoundManager
from MessageWindow import MessageWindow
from SettingsManager import SettingsManager


# Window for creating new audios.
class NewAudioGUI(customtkinter.CTkToplevel):
    def __init__(self, master, soundManager:SoundManager, settingsManager:SettingsManager, on_close=None):

        # Call Super Constructor
        super().__init__(master)

        

        # Constants
        self.HOVER_COLOR_MULTIPLIER=0.5         # The amount we tint a color on hover
        self.DEFAULT_AUDIO_COLOR="#373bb8"      # The default color widgets are INITed to on startup

        # Instance Variables
        self.settingsManager = settingsManager  # The settings manager for app settings
        self.soundManager = soundManager        # The sound manager that adds/ deletes sounds
        self.on_close = on_close                # The method to call when the window is closed

        # Setup GUI
        self._setupWindow()
        self._setupTabs()
        self._setupFileTab()
        self._setupColorButtons()
        self._setupDoneButton()

        self._setupDefaultWidgetColors()



    def _setupWindow(self):
        # Setup
        self.wm_iconbitmap(self.settingsManager.getAppIconPath(".ico"))
        self.iconphoto(True,PhotoImage(file = self.settingsManager.getAppIconPath(".png")))
        self.focus()
        self.protocol("WM_DELETE_WINDOW", self._closeWindow) # set the function that happens when the window is closed
        self.title("Add Audio")
        self.lift()
        self.attributes('-topmost', True)
        self.after(0, lambda: self.attributes('-topmost', False))

        # Wait for the window to display, then set as the only useable window
        # Note: this is technically a bug as the user has 10ms to fuck shit up, but idgaf
        self.after(10, self.grab_set)

        
    def _setupTabs(self):
        self.importFromTabview = customtkinter.CTkTabview(master=self)
        self.importFromTabview.add("Import from file")
        #self.importFromTabview.add("Import from YouTube")
        self.importFromTabview.pack(anchor="center", padx=10, pady=(0,10))

    def _setupFileTab(self):
        #import from file widgits
        self.filePathLabel = customtkinter.CTkLabel(self.importFromTabview.tab("Import from file"), text="File Path:",font=('bitter',12,"bold"))
        self.filePathLabel.grid(row=0, columnspan=1, pady = (0,0), sticky="w")
        self.fileInfoLabel = customtkinter.CTkLabel(self.importFromTabview.tab("Import from file"), text="'Note: a copy of the audio file will be made, so the original can be moved or deleated afterwards.'",font=('bitter', 11))
        self.fileInfoLabel.grid(row=1, columnspan=1, padx=5 ,pady=(0,0), sticky="w")
        self.filePathTextEntry = customtkinter.CTkEntry(self.importFromTabview.tab("Import from file"), placeholder_text="Path to File (.wav)")
        self.filePathTextEntry.grid(row=2, column=0, padx=5, pady=3, sticky="nsew")
        self.fileBrowseBtn = customtkinter.CTkButton(self.importFromTabview.tab("Import from file"), text="Browse", command=self._browseForFile,width=70)
        self.fileBrowseBtn.grid(row=2, column=1,padx=0)

        # title widgets
        self.fileTitleLabel = customtkinter.CTkLabel(self.importFromTabview.tab("Import from file"), text="Audio Tile:",font=('bitter',12,"bold"))
        self.fileTitleLabel.grid(row=3, columnspan=1, pady = (10,0), sticky="w")
        self.fileTitleEntry = customtkinter.CTkEntry(self.importFromTabview.tab("Import from file"), placeholder_text="Give this audio a title")
        self.fileTitleEntry.grid(row=4, column=0, padx=5, pady=(0,5), sticky="nsew")

        #color widgets
        self.fileColorLabel = customtkinter.CTkLabel(self.importFromTabview.tab("Import from file"), text="Audio Button Color:",font=('bitter',12,"bold"))
        self.fileColorLabel.grid(row=5, columnspan=1, pady = (10,0), sticky="w")
        self.fileRedSlider = customtkinter.CTkSlider(self.importFromTabview.tab("Import from file"), command=self._updateColors,from_=0, to=255, number_of_steps=255,height=15,button_color="#FF0000",button_hover_color="#800000")
        self.fileRedSlider.set(55)
        self.fileRedSlider.grid(row=6, column=0, sticky="nsew",pady=2)
        self.fileGreenSlider = customtkinter.CTkSlider(self.importFromTabview.tab("Import from file"), command=self._updateColors,from_=0, to=255, number_of_steps=255,height=15,button_color="#00FF00",button_hover_color="#008000")
        self.fileGreenSlider.set(59)
        self.fileGreenSlider.grid(row=7, column=0, sticky="nsew",pady=2)
        self.fileBlueSlider = customtkinter.CTkSlider(self.importFromTabview.tab("Import from file"), command=self._updateColors,from_=0, to=255, number_of_steps=255,height=15,button_color="#0000FF",button_hover_color="#000080")
        self.fileBlueSlider.set(184)
        self.fileBlueSlider.grid(row=8, column=0, sticky="nsew",pady=2)
        self.fileHexRGBEntry = customtkinter.CTkEntry(self.importFromTabview.tab("Import from file"), width=70)
        self.fileHexRGBEntry.bind('<Return>',self._textColorEntered)
        self.fileHexRGBEntry.insert(0,"#373bb8")
        self.fileHexRGBEntry.grid(row = 6,rowspan=3, column=1, padx=5, pady=(0,5), sticky="nsew")


        # Save colors Widgits
        self.colorSaveFrame = customtkinter.CTkFrame(self.importFromTabview.tab("Import from file"), height=10, fg_color="transparent")
        self.colorSaveFrame.grid(row=9,column=0, columnspan=2, pady=(20,0), sticky="nsew")

        self.colorSaveFrame.grid_columnconfigure(0, weight=1)
        self.saveColorButton = customtkinter.CTkButton(self.colorSaveFrame, height=10, text="Save Current Color", fg_color=['#F9F9FA', '#343638'], hover_color=['#bababb', '#27282a'], text_color=['gray10', '#DCE4EE'], command=self._saveColor)
        self.saveColorButton.grid(row=0,column=0,padx=2, sticky="nsew")

        self.colorSaveFrame.grid_columnconfigure(1, weight=1)
        self.deleteColorButton = customtkinter.CTkButton(self.colorSaveFrame, height=10, text="Remove Current Color", fg_color=['#F9F9FA', '#343638'], hover_color=['#bababb', '#27282a'], text_color=['gray10', '#DCE4EE'], command=self._deleteColor)
        self.deleteColorButton.grid(row=0,column=1,padx=2, sticky="nsew")


    def _setupColorButtons(self):

        self.colorScrollFrame = customtkinter.CTkScrollableFrame(self.importFromTabview.tab("Import from file"), height=35, fg_color="transparent", orientation="horizontal")
        self.colorScrollFrame.grid(row=10, column=0, columnspan=2, pady=(0,10), sticky="nsew")

        colors = self.soundManager.getSavedColors()
        column = 0

        for color in colors:
            action = lambda x = color: self._setWidgetColors(x)
            customtkinter.CTkButton(self.colorScrollFrame,
                                     height=25, 
                                     width=25, 
                                     text="", 
                                     fg_color=color,
                                     hover_color=self.darken_hex(color),
                                     command = action
                                     ).grid(row=0,column=column, padx=2,pady=5)
            column+=1

    def _setupDoneButton(self):
        #action = lambda x = 1: self.createNewAudio(x) #x=1 indicates that this is import from youtube
        self.doneButton = customtkinter.CTkButton(self.importFromTabview.tab("Import from file"), text="Done", command=self._createSound)
        self.doneButton.grid(row=9,column =0, columnspan=2,padx=0,pady=(58,10))

#========= Audio Saving Methods ========#

    def _createSound(self):
        '''Create a new audio with data from gui widgets'''

        # Get Path to the file
        filepath = self.filePathTextEntry.get()

        # Get the Title of the new sound
        title = self.fileTitleEntry.get()

        # Get the Color for the new sound
        color = self.fileHexRGBEntry.get()

        # Get the darker color for the new sound
        dark = self.darken_hex(color)

        # Try to create the new audio
        message = self.soundManager.addAudio(title, filepath, color, dark)

        # Check if a sound was created
        if(message == ""):
            self._closeWindow()
        else:
            MessageWindow(self, self.settingsManager, "Audio Not Created:\n\n"+message)


    def _browseForFile(self):
        '''Opens a file explorer and sets the selected files to be the value of the text entry.'''
        fn = askopenfilename(filetypes =[('Audio Files', '*.wav')])
        if fn != "":
            self.filePathTextEntry.delete(0,len(self.filePathTextEntry.get()))
            self.filePathTextEntry.insert(0,fn)


#========= GUI Methods ================#
    
    def _closeWindow(self):
        '''Desrtoy the window, and reset the sounds for the soundboard'''
        if(self.on_close is not None):
            self.on_close()
        self.destroy()
    

#======= Color Customization Methods ========#

    def _setupDefaultWidgetColors(self)->None:
        '''Set the widget colors starting value when the window is first opened. Uses the first color saved in the soundsFile or the default set by the class.'''

        colorToSet = self.soundManager.getFirstSavedColor()
        if(colorToSet is not None):
            self._setWidgetColors(colorToSet)
        else:
            self._setWidgetColors(self.DEFAULT_AUDIO_COLOR)


    def _setWidgetColors(self, col:str)->None:
        '''Change the colors of a widget to be the given Hex color. Note "dark" is the hover color for buttons'''

        # Edit widgets
        self.fileHexRGBEntry.delete(0,len(self.fileHexRGBEntry.get()))
        self.fileHexRGBEntry.insert(0,col)

        dark = self.darken_hex(col)
        rgb = self.hex_to_rgb(col)

        self.fileBrowseBtn.configure(fg_color=col,hover_color=dark)
        self.importFromTabview.configure(segmented_button_selected_color=col,segmented_button_selected_hover_color=dark)
        self.fileHexRGBEntry.configure(text_color=col)
        self.doneButton.configure(fg_color="transparent",hover_color=dark, border_width=2, border_color=col)
        
        self.fileRedSlider.set(rgb[0])
        self.fileGreenSlider.set(rgb[1])
        self.fileBlueSlider.set(rgb[2])



    def _updateColors(self, val):
        '''Update the colors base on the position of the sliders'''
        newCol=[]
        newCol.append(int(self.fileRedSlider.get()))
        newCol.append(int(self.fileGreenSlider.get()))
        newCol.append(int(self.fileBlueSlider.get()))

        self._setWidgetColors(self.rgb_to_hex(newCol))

    def _textColorEntered(self, event):
        '''changes the text color when a user types a color into the text entry'''

        # Make sure the user enters a valid color
        try:
            col = self.fileHexRGBEntry.get()

            #update widgets
            self._setWidgetColors(col)
        except:

            # Invalid color entered so set to default
            self._setWidgetColors(self.DEFAULT_AUDIO_COLOR)

    def _saveColor(self):
        self.soundManager.addSavedColor(self.fileHexRGBEntry.get())
        self._setupColorButtons()

    def _deleteColor(self):
        self.soundManager.removeSavedColor(self.fileHexRGBEntry.get())
        self._setupColorButtons()

#=========== Utility Methods ============#
    def hex_to_rgb(self, hex:str)->list:
        if hex[0] == "#":
            hex = hex[1:]
        rgb = []
        for i in (0, 2, 4):
            decimal = int(hex[i:i+2], 16)
            rgb.append(decimal)
        
        return rgb

    def rgb_to_hex(self, rgb:list)->str:
        return '#{:02x}{:02x}{:02x}'.format(rgb[0],rgb[1],rgb[2])

    def darken_rgb(self, rgb:list,t)->list:
        return [int(rgb[0]*t), int(rgb[1]*t),int(rgb[2]*t)]
    
    def darken_hex(self, hex:str):
        return self.rgb_to_hex(self.darken_rgb(self.hex_to_rgb(hex), self.HOVER_COLOR_MULTIPLIER))


    
    