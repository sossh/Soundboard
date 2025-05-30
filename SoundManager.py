import json
from os import remove, path as osPath
from shutil import copyfile
from Sound import Sound


class SoundManager:

    def __init__(self, soundFilePath):
        self.SOUND_FILE_PATH = soundFilePath
        self.SOUNDS_FOLDER_PATH = None
        self.SOUNDS_FOLDER_PATH = self.getSoundsFolderPath()
        self.ACCEPTED_FILE_FORMATS = ".wav"
        self.JSON_INDENTS = 0

    def getSoundsFolderPath(self):
        
        if self.SOUNDS_FOLDER_PATH is None:
            with open(self.SOUND_FILE_PATH, "r") as f:
                
                self.SOUNDS_FOLDER_PATH = json.load(f)["sounds_folder_path"]
                return self.SOUNDS_FOLDER_PATH
        else:
            
            return self.SOUNDS_FOLDER_PATH

    def getAllSounds(self):
        '''Returns a list of all sounds in the soundsFile'''
        soundList = []

        with open(self.SOUND_FILE_PATH, "r") as f:
            soundsData = json.load(f)["sounds"]

            # Add all sounds to the list
            for index, sound in enumerate(soundsData):
                # Make sure the file actually exists before adding it
                if(self.fileExists(self.getSoundsFolderPath() + sound["filepath"])):
                    soundList.append(Sound(sound["name"], self.getSoundsFolderPath()+sound["filepath"], index, sound["border_color"], sound["hover_color"]))

        return soundList
    
    def getSoundsFiltered(self, filter:str):
        '''Returns a list of all sounds that have the filter term in the soundsFile'''

        # check if we have no filter
        if(filter == ""):
            return self.getAllSounds()

        soundList = []
        filterLower = filter.lower()

        with open(self.SOUND_FILE_PATH, "r") as f:
            soundsData = json.load(f)["sounds"]

            # Add all sounds to the list
            for index, sound in enumerate(soundsData):

                # If the filter matches the sounds name and the sound file actually exists
                if((filterLower in sound["name"].lower() or 
                    filterLower == sound["border_color"].lower() or 
                    filterLower == sound["hover_color"][1:].lower()) and
                    self.fileExists(self.getSoundsFolderPath()+sound["filepath"])):

                    soundList.append(Sound(sound["name"], self.getSoundsFolderPath()+sound["filepath"], index, sound["border_color"], sound["hover_color"]))

        return soundList
    
    def getSoundByIndex(self, index:int):
        '''Gets data for a sound based on its index in the index in the soundFile'''
        with open(self.SOUND_FILE_PATH, "r") as f:
            soundsData = json.load(f)['sounds']

            if(index<=len(soundsData)): 
                # Build and return a sound object
                if(self.fileExists(self.getSoundsFolderPath()+soundsData[index]['filepath'])):
                    return Sound(soundsData[index]['name'], self.getSoundsFolderPath()+soundsData[index]['filepath'], index, soundsData[index]["border_color"], soundsData[index]["hover_color"])
        
        # If that index isn't in the sound file then return none
        return None
        
    def getSoundByPath(self, path:str):
        '''Gets data for a sound based on its index in the filepath'''
        with open(self.SOUND_FILE_PATH, "r") as f:
            soundsData = json.load(f)['sounds']

            # Find the sound
            for index, sound in enumerate(soundsData):
                if self.getSoundsFolderPath()+sound["filepath"] == path:
                    # Build and return a sound object
                    if(self.fileExists(self.getSoundsFolderPath()+sound["filepath"])):
                        return Sound(sound["name"], self.getSoundsFolderPath()+sound["filepath"], index, sound["border_color"], sound["hover_color"])
                    
                    break
                
        # If that path isn't in a sound then return none
        return None
    
    def getNumSounds(self):
        '''Returns the number of audios currently in the soundsFile'''
        with open(self.SOUND_FILE_PATH, "r") as f:
            sounds = 0
            try:
                sounds = int(json.load(f)['numSounds'])
            except:
                pass
            return sounds


    def deleteAudio(self, sound:Sound, deleteFile=True):
        '''Deletes an audio. Removes it from the soundfile, and deletes it out of the sound folder. NOTE: You must reset the indexes after deleting.'''

        # Remove the audio from the sound file
        with open(self.SOUND_FILE_PATH, "r") as file:
            soundsData = json.load(file)
            soundsData["sounds"].pop(sound.getIndex())
            soundsData["numSounds"] = len(soundsData["sounds"])

        # Reupload the sound file
        with open(self.SOUND_FILE_PATH, "w") as file:
            json.dump(soundsData, file, indent=self.JSON_INDENTS)

        if(deleteFile):
            # Remove the actual sound file from the folder
            remove(sound.getPath())

    def isValidEditAudio(self, title:str, path:str, borderCol:str, hoverCol:str):
        '''Returns "" empty string if a audio with theses valuses is valid, if it is invalid returns an error message.'''

        # Get the file name and remove all non-ascii
        filename = osPath.basename(path)
        filename = filename.encode("ascii", "ignore").decode()

        # Make sure the file exists
        if(not self.fileExists(path)):
            return 'The file at "'+path+'" does not exist, so audio cannot be edited.'
        
        # Make sure the file is a .wav
        if(filename.find(".wav") == -1):
            return 'The file is not in a accepted format '+self.ACCEPTED_FILE_FORMATS+'.'
        
        # Make sure border col is valid
        if(len(borderCol) != 7 or borderCol[0] != "#"):
            return "The color set is not valid."
        
        # Make sure hover col is valid
        if(len(hoverCol) != 7 or hoverCol[0] != "#"):
            return "The color set is not valid."
        
        return ""
        



    def isValidNewAudio(self, title:str, path:str, borderCol:str, hoverCol:str)->str:
        '''Returns "" empty string if a audio with theses valuses is valid, if it is invalid returns an error message.'''

        # Get the file name and remove all non-ascii
        filename = osPath.basename(path)
        filename = filename.encode("ascii", "ignore").decode()

        # Make sure the file to import exists
        if(not self.fileExists(path)):
            return 'The file at "'+path+'" does not exist, so no audio was created.'
        

        # Make sure no no sound with the filename currently exists
        if(self.fileExists(self.SOUNDS_FOLDER_PATH+filename)):
            return 'A Sound with the filename "'+filename+'" already exits in the soundboard.'
        
        # Make sure the file is a .wav
        if(filename.find(".wav") == -1):
            return 'The file is not in a accepted format '+self.ACCEPTED_FILE_FORMATS+'.'
        
        # Make sure border col is valid
        if(len(borderCol) != 7 and borderCol[0] != "#"):
            return "The color set is not valid."
        
        # Make sure hover col is valid
        if(len(hoverCol) != 7 and hoverCol[0] != "#"):
            return "The color set is not valid."
        
        return ""
    

    def editAudio(self, sound:Sound, title:str, borderCol:str, hoverCol:str)->str:
        '''Edits an audios name, colors, etc. Does this by deleting the audio then adding it back'''

        # Get Audio Data before we delete it
        path = sound.getPath()
        path = path.encode("ascii", "ignore").decode()
        index = sound.getIndex()

        # Check for validity
        errorMessage = self.isValidEditAudio(title, path, borderCol, hoverCol)

        if errorMessage == "":

            # Delete the audio but dont delete the file
            self.deleteAudio(sound, deleteFile=False)

            # Replace the audio in the position it was in before
            self._addAudioNoChecks(title, path, borderCol, hoverCol, index)

        return errorMessage

    

    def addAudio(self, title:str, path:str, borderCol:str, hoverCol:str, index=-1)->str:
        '''Adds an audio to the sounds file, and moves it to the sound folder if its not already there. Returns the reason audio isn't added if there was an issue.'''

        errorMessage = self.isValidNewAudio(title, path, borderCol, hoverCol)

        if errorMessage == "":
            self._addAudioNoChecks(title, path, borderCol, hoverCol, index)

        return errorMessage

    

            


    def fileExists(self, fileName) -> bool:
        '''Returns true if there is a file at the given path'''
        print(fileName)
        return osPath.isfile(fileName)
    
    def soundExists(self, sound:Sound) -> bool:
        '''Returns True if the sound exists in the soundsFile'''
        for toCompare in self.getAllSounds():
            if(sound == toCompare):
                return True

        return False
    
    def filenameTaken(self, filename:str) -> bool:
        '''Returns true if an audio with a certain file name already exists in the sounds file'''

        filepath = str(self.SOUNDS_FOLDER_PATH+filename)
        for toCompare in self.getAllSounds():
            if(filepath == toCompare.getPath()):
                return True
            
        return False
    
#======== Private Sound Methods ===========#

    def _addAudioNoChecks(self, title:str, path:str, borderCol:str, hoverCol:str, index=-1):
        '''Adds an audio with the given parameters, without checking for validity, CHECK SOMEWHERE ELSE!'''
  
        # Get the file name and remove all non-ascii
        filename = osPath.basename(path)
        filename = filename.encode("ascii", "ignore").decode()
        
        # Move the file to the sounds folder if they are not the same
        if(path != self.SOUNDS_FOLDER_PATH+filename):
            copyfile(path,self.SOUNDS_FOLDER_PATH+filename)

        # Add the sound to the sounds file
        with open(self.SOUND_FILE_PATH, "r") as f:
            data = json.load(f)


        # Add it to the audio file
        if(index >=0 and index < self.getNumSounds()):
            data["sounds"].insert(index, {"name":title, "filepath":filename, "border_color":borderCol, "hover_color":hoverCol})
        else:
            data["sounds"].append({"name":title, "filepath":filename, "border_color":borderCol, "hover_color":hoverCol})
        

        # Update the Number of sounds in the file
        data["numSounds"] = len(data["sounds"])
        

        # Write to file
        with open(self.SOUND_FILE_PATH, "w") as file:
                json.dump(data, file, indent=self.JSON_INDENTS)
    
#======== Sound Color Methods ============#
    
    def getSavedColors(self) -> list:
        '''Returns a list of colors that the user has saved'''
        with open(self.SOUND_FILE_PATH, "r") as f:
            return json.load(f)["savedColors"]
        
    def getFirstSavedColor(self) -> str|None:
        '''Retruns the first color saved in the file, returns None if no color exists'''

        returnColor = None
        with open(self.SOUND_FILE_PATH, "r") as f:
            cols = json.load(f)["savedColors"]
            if(len(cols) > 0):
                returnColor = cols[0]

        return returnColor
        
    def addSavedColor(self, hexCol:str):
        '''Adds a color to the list of saved colors'''

        # Get data for all things
        with open(self.SOUND_FILE_PATH, "r") as f:
            data = json.load(f)

        # Make sure color is valid and not duplicate
        if(len(hexCol) == 7 and hexCol[0] == "#" and (not hexCol in data["savedColors"])):
            data["savedColors"].append(hexCol)

            # Output data
            with open(self.SOUND_FILE_PATH, "w") as file:
                json.dump(data, file, indent=self.JSON_INDENTS)

        
    def removeSavedColor(self, hexCol:str):

        # Get data for all things
        with open(self.SOUND_FILE_PATH, "r") as f:
            data = json.load(f)

        # Find the item to remove if it exists
        toRemoveIndex = -1
        for i, col in enumerate(data["savedColors"]):
            if(col == hexCol):
                toRemoveIndex = i
                break
        
        # Remove the item
        if(toRemoveIndex != -1):
            data["savedColors"].pop(toRemoveIndex)
            with open(self.SOUND_FILE_PATH, "w") as file:
                json.dump(data, file, indent=self.JSON_INDENTS)




    



