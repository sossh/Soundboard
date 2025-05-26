import json
from sounddevice import query_devices

# Settings managaer that does the file i/o for saving and editing settings.
class SettingsManager():
    def __init__(self, settingsFilePath):
        self.SETTINGS_FILE_PATH = settingsFilePath
        self.JSON_INDENTS = 1
        self.ASSETS_FOLDER_PATH = None
        self.ASSETS_FOLDER_PATH = self.getAssetFolderPath()

#====================== Settings Getter Methods =====================#
    def getAssetFolderPath(self):
        if(self.ASSETS_FOLDER_PATH is None):
            with open(self.SETTINGS_FILE_PATH, "r") as f:
                return json.load(f)["assets_folder_path"]
        else:
            return self.ASSETS_FOLDER_PATH
        
    def getInputDeviceName(self)->str:
        '''Get the name of the input device in the settings file.'''
        with open(self.SETTINGS_FILE_PATH, "r") as f:
            configData = json.load(f)           
            return configData["input_device"]
        
    def getOutputDeviceName(self)->str:
        '''Get the name of the output device in the settings file.'''
        with open(self.SETTINGS_FILE_PATH, "r") as f:
            configData = json.load(f)
            return configData["output_device"]
        
    def getVirtualDeviceName(self)->str:
        '''Get the name of the virtual device in the settings file.'''
        with open(self.SETTINGS_FILE_PATH, "r") as f:
            configData = json.load(f)            
            return configData["virtual_device"]
        
    def getAppTitle(self)->str:
        '''Gets the apps title.'''
        with open(self.SETTINGS_FILE_PATH, "r") as f:
            configData = json.load(f)            
            return configData["app_title"]
        
    def getAppIconPath(self, fileFormat)->str:
        '''Get the apps icon path in the specified format, ex: (.ico, .png)'''
        with open(self.SETTINGS_FILE_PATH, "r") as f:
            configData = json.load(f)            
            return self.ASSETS_FOLDER_PATH + configData["icon_path"][fileFormat]
        
    def getNumWelcomeMessages(self)->int:
        '''Returns the number of welcome messages stored in the settings file'''
        with open(self.SETTINGS_FILE_PATH, "r") as f:
            return len(json.load(f)["welcome_messages"])
        
        
    def getWelcomeMessage(self, index:int)->dict:
        '''Gets the welcome message at the specified index (indexes are 0 to n-1)'''
        with open(self.SETTINGS_FILE_PATH, "r") as f:
            return json.load(f)["welcome_messages"][index]
        
    def getShowMessageOnStartup(self)->bool:
        '''Returns true if we should show the welcome message on startup'''
        with open(self.SETTINGS_FILE_PATH, "r") as f:
            return json.load(f)["showWelcomeMessageOnStart"]
        
    def getHotkey(self, type:str):
        '''Gets the hotkey for toggling audio'''
        with open(self.SETTINGS_FILE_PATH, "r") as f:
            return json.load(f)["hotkeys"][type]
        
    def getImagePath(self, imageName)->str:
        '''Returns the path to an image stored in the assets folder'''
        with open(self.SETTINGS_FILE_PATH, "r") as f:
            return self.ASSETS_FOLDER_PATH + imageName
        
    
    
            
        


#================== Settings Setter Methods =======================#
    def setInputDeviceName(self, newDevice:str):
        '''Change the name of the input device in the settings file.'''
        with open(self.SETTINGS_FILE_PATH, "r") as f:
            configData = json.load(f)
            configData["input_device"] = newDevice

        with open(self.SETTINGS_FILE_PATH, "w") as f:
            json.dump(configData, f, indent=self.JSON_INDENTS)

    def setOutputDeviceName(self, newDevice:str):
        '''Change the name of the output device in the settings file.'''
        with open(self.SETTINGS_FILE_PATH, "r") as f:
            configData = json.load(f)
            configData["output_device"] = newDevice

        with open(self.SETTINGS_FILE_PATH, "w") as f:
            json.dump(configData, f, indent=self.JSON_INDENTS)

    def setVirtualDeviceName(self, newDevice:str):
        '''Change the name of the virtual device in the settings file.'''
        with open(self.SETTINGS_FILE_PATH, "r") as f:
            configData = json.load(f)
            configData["virtual_device"] = newDevice

        with open(self.SETTINGS_FILE_PATH, "w") as f:
            json.dump(configData, f, indent=self.JSON_INDENTS)

    def setShowMessageOnStartup(self, value:bool):
        '''Sets if the help and anouncements menu show appear on startup'''
        with open(self.SETTINGS_FILE_PATH, "r") as f:
            configData = json.load(f)
            configData["showWelcomeMessageOnStart"] = value

        with open(self.SETTINGS_FILE_PATH, "w") as f:
            json.dump(configData, f, indent=self.JSON_INDENTS)

    def setHotkey(self, type:str, newKey:str):
        '''Gets the hotkey for toggling audio'''

        with open(self.SETTINGS_FILE_PATH, "r") as f:
            configData = json.load(f)
            configData["hotkeys"][type] = newKey

        with open(self.SETTINGS_FILE_PATH, "w") as f:
            json.dump(configData, f, indent=self.JSON_INDENTS)

    
            


#==================== Misc Methods =================#
    def getAllInputDeviceNames(self)->list:
        '''Returns a list of all input audio devices + "default" so you can use the default device set by the os'''
        deviceList = []
        deviceList.append("default")
        for device in query_devices():
            if((device['max_input_channels'] > 0) and (device['hostapi'] == 0)):
                deviceList.append(device['name'])
                

        return deviceList
    
    def getAllOutputDeviceNames(self)->list:
        '''Returns a list of all input audio devices + "default" so you can use the default device set by the os'''
        deviceList = []
        deviceList.append("default")
        for device in query_devices():
            if((device['max_output_channels'] > 0) and (device['hostapi'] == 0)):
                deviceList.append(device['name'])
                

        return deviceList
    

   

   

