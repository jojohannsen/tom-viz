class ConversationManager:
    def __init__(self, conversation):
        """
        Initialize the conversation manager with a conversation string.
        Parse the conversation into a list of (name, text) tuples.
        """
        self.all_entries = []
        self.current_pos = 0
        self.current_conversation = ""
        self._participants = []
        
        # Parse the input conversation
        for line in conversation.strip().split('\n'):
            if ':' in line:
                name, text = line.split(':', 1)
                name = name.strip()
                text = text.strip()
                self.all_entries.append((name, text))
                
                # Add participant if not already in list
                if name not in self._participants:
                    self._participants.append(name)
    
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
        self.current_conversation += f"{name}: {text}\n"
        self.current_pos += 1
        
        return name, text
    
    def so_far(self):
        """
        Return the conversation up to the current point.
        """
        return self.current_conversation.strip()
