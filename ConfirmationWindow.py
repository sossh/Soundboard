import customtkinter as ctk

class ConfirmationWindow(ctk.CTkToplevel):
    '''Class that takes a message and up 2 callback methods, on_confirm is called on a "Yes" and on_cancel called on a "No"'''
    def __init__(self, master, message, on_confirm=None, on_cancel=None):
        # Call Super Constructor
        super().__init__(master)
        
        # Callback Methods
        self.confirmCallback = on_confirm
        self.cancelCallback = on_cancel

        self._setupWindow()
        self._setupMessageFrame()

    def _setupWindow(self):
        self.title("Confirm Deletion")
        self.geometry("300x150")
        self.resizable(False, False)
        self.grab_set() 

    def _setupMessageFrame(self):
        # Message
        self.label = ctk.CTkLabel(self, text="Would you like to delete this sound?")
        self.label.pack(pady=(20, 10))

        # Button frame
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=10)

        # Yes Button
        yes_button = ctk.CTkButton(button_frame, text="Yes", command=self._confirm)
        yes_button.pack(side="left", padx=10)

        # No Button
        no_button = ctk.CTkButton(button_frame, text="No", command=self._cancel)
        no_button.pack(side="left", padx=10)

    def _confirm(self):
        self.grab_release()
        self.destroy()
        if self.confirmCallback:
            self.confirmCallback()

    def _cancel(self):
        self.grab_release()
        self.destroy()
        if self.cancelCallback:
            self.cancelCallback()