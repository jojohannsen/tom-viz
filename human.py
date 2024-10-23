from typing import Dict, List, Optional
from pydantic import BaseModel, Field

# Core data models
class HumanView(BaseModel):
    """Represents one person's view of another person (or themselves)"""
    name: str = Field(..., description="Name of the person being viewed")
    myself: bool = Field(..., description="True if this is a self-view")
    attributes: List[str] = Field(default_factory=list, description="List of words or phrases or facts describing or associated with this human")

class Human(BaseModel):
    """Represents a person and their mental model of others"""
    name: str = Field(..., description="Name of the person")
    society: Dict[str, HumanView] = Field(..., description="Mental model of self and others")

    @property
    def myself(self) -> Optional[List[str]]:
        """Get this person's self-view attributes"""
        view = self.society.get(self.name)
        return view.attributes if view and view.myself else None

    def __getitem__(self, key: str) -> Optional[HumanView]:
        """Get this person's view of someone else"""
        return self.society.get(key)

    def get_or_create_view(self, name: str) -> HumanView:
        """Get or create a view of another person"""
        if name not in self.society:
            self.society[name] = HumanView(
                name=name,
                myself=False, 
                attributes=[]
            )
        return self.society[name]

class PromptGenerator:
    """Generates prompts for updating mental models based on conversations"""

    @staticmethod
    def view_update(person_a: Human, person_b: str, conversation: str) -> str:
        """Generate prompt to update person_a's view of person_b"""
        current_view = person_a.society[person_b].attributes if person_b in person_a.society else []
        
        return f"""
        Based on the following conversation, identify what {person_a.name} learns about {person_b}.
        List concrete facts and attributes that {person_a.name} discovers about {person_b}.
        Include only new information not already in {person_a.name}'s current view.
        
        Current view:
        {current_view}
        
        Conversation:
        {conversation}
        
        What new attributes should be added to {person_a.name}'s view of {person_b}?
        Please provide a list of individual facts or traits, one per line.
        """

    @staticmethod
    def self_view_update(person: Human, conversation: str) -> str:
        """Generate prompt to update person's self-view"""
        return f"""
        Based on the following conversation, identify any new information {person.name} reveals or learns about themselves.
        List only new concrete facts and attributes not already in their self-view.
        
        Current self-view:
        {person.myself}
        
        Conversation:
        {conversation}
        
        What new attributes should be added to {person.name}'s self-view?
        Please provide a list of individual facts or traits, one per line.
        """

# Example usage:
def create_example_human(name: str, attributes: List[str] = None) -> Human:
    """Create a Human instance with default empty society"""
    return Human(
        name=name,
        society={
            name: HumanView(
                name=name,
                myself=True,
                attributes=attributes or []
            )
        }
    )

# Helper functions for working with the models
def update_view(human: Human, target: str, new_attributes: List[str]) -> None:
    """Update a human's view of another person (or themselves)"""
    view = human.get_or_create_view(target)
    view.attributes = list(set(view.attributes + new_attributes))

def format_view(view: HumanView) -> List[str]:
    """Format a view's attributes as a list"""
    return view.attributes
