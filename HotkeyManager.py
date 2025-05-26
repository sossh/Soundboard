from pynput import keyboard

# Manages hotkeys after they have been created
# Hotkeys mut be entered into this class with the addHotkey() Mehtod
# Does not import hotkeys from anywhere
class HotkeyManager:
    special_keys = {keyboard.Key.alt: 'alt',
                        keyboard.Key.alt_l: 'alt_l',
                        keyboard.Key.alt_r: 'alt_r',
                        keyboard.Key.alt_gr: 'alt_gr',
                        keyboard.Key.backspace: 'backspace',
                        keyboard.Key.caps_lock: 'caps_lock',
                        keyboard.Key.cmd: 'cmd_l',
                        keyboard.Key.cmd_r: 'cmd_r',
                        keyboard.Key.ctrl_l: 'ctrl_l',
                        keyboard.Key.ctrl_r: 'ctrl_r',
                        keyboard.Key.delete: 'delete',
                        keyboard.Key.down: 'down',
                        keyboard.Key.end: 'end',
                        keyboard.Key.enter: 'enter',
                        keyboard.Key.esc: 'esc',
                        keyboard.Key.f1: 'f1',
                        keyboard.Key.f2: 'f2',
                        keyboard.Key.f3: 'f3',
                        keyboard.Key.f4: 'f4',
                        keyboard.Key.f5: 'f5',
                        keyboard.Key.f6: 'f6',
                        keyboard.Key.f7: 'f7',
                        keyboard.Key.f8: 'f8',
                        keyboard.Key.f9: 'f9',
                        keyboard.Key.f10: 'f10',
                        keyboard.Key.f11: 'f11',
                        keyboard.Key.f12: 'f12',
                        keyboard.Key.f13: 'f13',
                        keyboard.Key.f14: 'f14',
                        keyboard.Key.f15: 'f15',
                        keyboard.Key.f16: 'f16',
                        keyboard.Key.f17: 'f17',
                        keyboard.Key.f18: 'f18',
                        keyboard.Key.f19: 'f19',
                        keyboard.Key.f20: 'f20',
                        keyboard.Key.home: 'home',
                        keyboard.Key.left: 'left',
                        keyboard.Key.page_down: 'page_down',
                        keyboard.Key.page_up: 'page_up',
                        keyboard.Key.right: 'right',
                        keyboard.Key.shift: 'shift_l',
                        keyboard.Key.shift_r: 'shift_r',
                        keyboard.Key.space: 'space',
                        keyboard.Key.tab: 'tab',
                        keyboard.Key.up: 'up',
                        keyboard.Key.media_play_pause: 'media_play_pause',
                        keyboard.Key.media_volume_mute: 'media_volume_mute',
                        keyboard.Key.media_volume_down: 'media_volume_down',
                        keyboard.Key.media_volume_up: 'media_volume_up',
                        keyboard.Key.media_previous: 'media_previous',
                        keyboard.Key.media_next: 'media_next',
                        keyboard.Key.insert: 'insert',
                        keyboard.Key.menu: 'menu',
                        keyboard.Key.num_lock: 'num_lock',
                        keyboard.Key.pause: 'pause',
                        keyboard.Key.print_screen: 'print_screen',
                        keyboard.Key.scroll_lock: 'scroll_lock'}
    def __init__(self):
        
        # Init instance vars.
        self.hotkeyDict = {}
        self.listener = None
        

    def activateHotkeys(self):
        '''Starts the Hotkey listener.'''

        # Create and start the listener
        self.listener = keyboard.Listener(on_press=self._onKeyPressed)
        self.listener.start()
        
    def deactivateHotkeys(self):
        '''Stops the hotkey listener'''

        # Make sure the listener is not null then stop it
        if self.listener is not None:
            self.listener.stop()

    def addHotkey(self, hotkey:str, method):
        '''Adds a hotkey to the dictionary of all hotkeys. Will not add if key is None. Runs the given method when the given key is pressed'''

        # Chcek if key/method is valid and the key not being used already
        if(self.isValidKey(hotkey) and (method is not None) and (self.hotkeyDict.get(hotkey) is None)):

            # Add the method to the hotkeyDict
            self.hotkeyDict[hotkey] = method

    @staticmethod
    def isValidKey(keyStr: str) -> bool:
        '''Returns True if the given string is a valid key'''

        keyStr = keyStr.lower().strip()
        # Check if it is a special key
        if len(keyStr) == 1 and keyStr.isprintable():
            return True  # typable character like 'a', '1', etc.
        if keyStr in HotkeyManager.special_keys.values():
            return True
        return False
    

#========== Private Internal Methods ============#
    def _onKeyPressed(self, key):
        keyStr = self._getKeyStr(key)
        
        # Check if a hotkey with this key exists
        if(self.hotkeyDict.get(keyStr) is not None):
            
            # Call the method given by the hotkey
            method = self.hotkeyDict.get(keyStr)
            method()
            

    def _getKeyStr(self, key:keyboard.Key)->str:
        '''Converts a pynput.keyboard.Key Object into a key string, returns None if the key doesn't exist.'''

        # Default Value
        keyStr = None
        try:
            # If the key has a char value use that its str
            keyStr = str(key.char)
            keyStr = keyStr.lower()
        except:
            # If the key is a special key then use the table
            keyStr = self.special_keys[key]

        return keyStr

    

