from SoundboardGUI import SoundboardGUI

if __name__ == "__main__":

    keepRunning = True
    while (keepRunning):
        
        # Create the Soundboard
        app = SoundboardGUI()

        # Start the mainloop to update gui widgets
        app.mainloop()
        
        # Check if we should restart
        keepRunning = app.shouldRestartSoundboard()

