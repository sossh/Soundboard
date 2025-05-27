import customtkinter
from PIL import Image
from tkinter import PhotoImage
from SettingsManager import SettingsManager

# Window that displays information relevent to the soundboards use. ie: Setup instructions
class WelcomeWindow(customtkinter.CTkToplevel):

    def __init__(self, master, settingsManager:SettingsManager):

        # Call Super Constructor
        super().__init__(master)
        super().iconphoto(True,PhotoImage(file=settingsManager.getAppIconPath(".png")))

        # Init Constants
        self.WINDOW_WIDTH = 550
        self.WINDOW_HEIGHT = 450
        self.MESSAGE_IMAGE_SIZE = (480,270)
        self.TITLE = "Help and Announcements"

        # Init the settings manager to get Messages
        self.settingsManager = settingsManager
        self.numMessages = self.settingsManager.getNumWelcomeMessages()
        self.currPage = 1
        
        # Only create the window if we have messages to display.
        if(self.numMessages > 0):
            
            self._setupWindow()
            self._setupWidgets()
            self._resizeWindow()

            
            self._setMessage(self.currPage)




    def _setupWindow(self):

        # Setup the Window
        self.title("Help and Announcements")
        self.iconphoto(True,PhotoImage(file=self.settingsManager.getAppIconPath(".png")))
        self.focus()
        self.lift()
        self.attributes('-topmost', True)
        self.after(0, lambda: self.attributes('-topmost', False))

    def _resizeWindow(self):
        '''Resize the window after all widgets have been inited'''
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        


    def _setupWidgets(self):

        self.messageWindowFrame = customtkinter.CTkFrame(self, bg_color="transparent", fg_color="transparent")
        self.messageWindowFrame.pack(anchor="center", expand=True, padx=10, pady=10)

        self.messageTitleLabel = customtkinter.CTkLabel(self.messageWindowFrame, text="", font=('bitter', 15, 'bold'))
        self.messageTitleLabel.pack(anchor="center", expand=True, pady=(0,5))

        self.messageImageLabel = customtkinter.CTkLabel(self.messageWindowFrame, text="")
        self.messageImageLabel.pack(anchor="center", expand=True)

        self.bottomFrame = customtkinter.CTkFrame(self.messageWindowFrame, bg_color="transparent", fg_color="transparent")
        self.bottomFrame.pack(anchor="center", padx=5, pady=10)

        self.goLeftBtn = customtkinter.CTkButton(self.bottomFrame, width=30, height=30, text="<-", command=self._on_goLeftBtn_press)
        self.goLeftBtn.grid(column = 0, row=0, sticky="W")

        self.bottomFrame.grid_columnconfigure(1, weight=1)
        self.message = customtkinter.CTkLabel(self.bottomFrame, text="", width=400, wraplength=400, anchor="w", justify="left")
        self.message.grid(column = 1, row=0, padx=10)

        self.goRightBtn = customtkinter.CTkButton(self.bottomFrame, width=30, height=30, text="->", command=self._on_goRightBtn_press)
        self.goRightBtn.grid(column = 2, row=0, sticky="e")


        self.showOnStartupFrame = customtkinter.CTkFrame(self.messageWindowFrame, bg_color="transparent", fg_color="transparent")
        self.showOnStartupFrame.pack(anchor="center", padx=5)

        # Get the State of the checkbox
        cbValue = "off"
        if(self.settingsManager.getShowMessageOnStartup()):
            cbValue = "on"

        check_var = customtkinter.StringVar(value=cbValue)
        self.showOnStartupCheckbox = customtkinter.CTkCheckBox(self.showOnStartupFrame, command=self._on_startupCheckBox_set, variable=check_var, onvalue="on", offvalue="off", text="Show on Startup", checkbox_height=20, checkbox_width=20)
        self.showOnStartupCheckbox.pack(pady=2)


    def _setMessage(self, currPage:int):
        '''Set the page to the page number you want (indexes are 1-n)'''

        index = currPage-1

        if(index >= 0 and index < self.numMessages):
            message = self.settingsManager.getWelcomeMessage(index)

            messageImage = customtkinter.CTkImage(size=self.MESSAGE_IMAGE_SIZE, light_image=Image.open(self.settingsManager.getAssetFolderPath()+message["image_path"]),dark_image=Image.open(self.settingsManager.getAssetFolderPath()+message["image_path"]))
            self.messageImageLabel.configure(require_redraw=True, image=messageImage)

            self.message.configure(text=message["message"])

            self.messageTitleLabel.configure(text=message["title"])

            self.title(f"{self.TITLE} ({self.currPage}/{self.numMessages})")


#========== GUI Behaviour Methods ===========#

    def _on_goLeftBtn_press(self):
        '''Go left 1 page and display the message on that page.'''

        # Go left 1 page
        oldPage = self.currPage
        self.currPage = (self.currPage - 2) % self.numMessages + 1

        # Display new page
        if(self.currPage != oldPage):
            self._setMessage(self.currPage)
        
    def _on_goRightBtn_press(self):
        '''Go right 1 page and display the message on that page.'''
        
        # Go right 1 page
        oldPage = self.currPage
        self.currPage = (self.currPage) % self.numMessages + 1

        # Display new page
        if(self.currPage != oldPage):
            self._setMessage(self.currPage)

    def _on_startupCheckBox_set(self):
        
        showOnStartup = (self.showOnStartupCheckbox.get() == "on")
        self.settingsManager.setShowMessageOnStartup(showOnStartup)

