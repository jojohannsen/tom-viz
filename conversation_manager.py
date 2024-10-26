class ConversationManager:
    def __init__(self, conversation):
        """
        Initialize the conversation manager with a conversation string.
        Parse the conversation into a list of entries.
        Entries can be dialogue, character definitions, or scenes.
        """
        self.all_entries = []
        self.current_pos = 0
        self.current_conversation = ""
        self._participants = []
        self.characters = {}  # Store characters as a dictionary: name -> description
        self.scenes = []       # Store scenes as a list of descriptions
        
        # Parse the input conversation
        for line in conversation.strip().split('\n'):
            if ':' in line:
                # Check if line is a Character or Scene description
                parts = line.split(':', 1)  # Split up to 2 parts to handle 'Character' and 'Scene'
                if parts[0] == "Character" or parts[0] == "Scene":
                    entry_type = parts[0].strip()
                    name = parts[1].split()[0].strip()
                    text = parts[1]
                    
                    if entry_type == "Character":
                        self.make_character(name, text)
                    elif entry_type == "Scene":
                        self.make_scene(text)
                    else:
                        self._process_dialogue(entry_type, name)
                else:
                    # Handle regular dialogue lines like "Joe: Hi Bob"
                    name, text = map(str.strip, parts)
                    self._process_dialogue(name, text)
        offset = 0
        for c in self.characters:
            self._prepend_dialogue(f"Character: {c}", self.characters[c], offset)
            offset += 1
        for s in self.scenes:
            self._prepend_dialogue(f"Scene", s, offset)
            offset += 1

    def _prepend_dialogue(self, name, text, offset):
        self.all_entries.insert(offset, (name, text))

    def _process_dialogue(self, name, text):
        """
        Helper function to process a regular dialogue line.
        """
        self.all_entries.append((name, text))
        
        # Add participant if not already in list
        if name not in self._participants:
            self._participants.append(name)
    
    def make_character(self, name, description):
        """
        Process a character definition and store it.
        """
        self.characters[name] = description
    
    def make_scene(self, description):
        """
        Process a scene description and store it.
        """
        self.scenes.append(description)
    
    def participants(self):
        """
        Return the list of participants in order of first appearance.
        """
        return self._participants
    
    def next(self):
        """
        Return the next (name, text) tuple in the conversation.
        Returns None if at the end of the conversation.
        Updates the current conversation string.
        """
        if self.current_pos >= len(self.all_entries):
            return None
        
        name, text = self.all_entries[self.current_pos]
        self.current_pos += 1
        self.current_conversation += f"{name}: {text}\n"
        return name, text
    
    def so_far(self):
        """
        Return the conversation up to the current point.
        """
        return self.current_conversation.strip()
    
    def get_characters(self):
        """
        Return the stored characters.
        """
        return self.characters
    
    def get_scenes(self):
        """
        Return the stored scenes.
        """
        return self.scenes
