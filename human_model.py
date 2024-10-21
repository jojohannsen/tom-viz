from __future__ import annotations
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from itertools import count

# Global id generator
id_generator = count(1)

class Human(BaseModel):
    """
    Represents a human entity with their basic information, mental model (Info),
    social interactions (Incentives), and life experiences.
    """

    id: int = Field(
        default_factory=lambda: next(id_generator),
        description="Unique identifier for the human, automatically generated."
    )
    name: str = Field(
        description="The name of the human."
    )
    experiences: List[str] = Field(
        default_factory=list,
        description="Significant life events or experiences that have shaped the person."
    )
    interests: List[str] = Field(
        default_factory=list,
        description="Hobbies, passions, or topics that the person finds engaging or enjoyable."
    )
    family: List[str] = Field(
        default_factory=list,
        description="Family members or family-related information important to the person."
    )
    friends: List[str] = Field(
        default_factory=list,
        description="Close friends or social connections that are significant to the person."
    )
    pets: List[str] = Field(
        default_factory=list,
        description="Pets owned by the person or animals they have a strong connection with."
    )
    community: List[str] = Field(
        default_factory=list,
        description="Groups, organizations, or communities the person is part of or identifies with."
    )

    def to_dict(self):
        return {
            "name": self.name,
            "experiences": self.experiences,
            "interests": self.interests,
            "family": self.family,
            "friends": self.friends,
            "pets": self.pets,
            "community": self.community
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


class HumanMind(Human):
    """
    Extends the Human class to include mental models of other humans.
    """

    mental_models: Dict[str, Human] = Field(
        default_factory=dict,
        description="Mental models of all participants, including self. Keys are participant names."
    )

    def __init__(self, **data):
        super().__init__(**data)
        # Initialize the self mental model with the human's known attributes
        self.update_mental_model(self.name)

    def update_mental_model(self, participant_name: str, **attributes):
        """
        Update the mental model for a specific participant.
        """
        if participant_name not in self.mental_models:
            # For self, use own values; for others, use empty lists
            if participant_name == self.name:
                new_human = self.model_copy(deep=True)
            else:
                new_human = Human(name=participant_name)
            
            self.mental_models[participant_name] = new_human
        
        # Update attributes if provided
        for attr, value in attributes.items():
            if hasattr(self.mental_models[participant_name], attr):
                setattr(self.mental_models[participant_name], attr, value)

    class Config:
        arbitrary_types_allowed = True
