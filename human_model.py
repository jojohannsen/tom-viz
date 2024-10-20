from __future__ import annotations
from typing import List, Dict
from pydantic import BaseModel, Field
from itertools import count

# Global id generator
id_generator = count(1)

class Info(BaseModel):
    """
    Represents the contents of a human's mind, including their personality traits,
    topics they view positively or negatively, and their interests.
    """
    
    personality: List[str] = Field(
        default_factory=list,
        description="A list of personality traits that describe the human."
    )
    positive_topics: List[str] = Field(
        default_factory=list,
        description="Topics or subjects that the human views positively or enjoys discussing."
    )
    negative_topics: List[str] = Field(
        default_factory=list,
        description="Topics or subjects that the human views negatively or dislikes discussing."
    )
    interests: List[str] = Field(
        default_factory=list,
        description="A list of the human's interests, hobbies, or areas of expertise."
    )

class Incentives(BaseModel):
    """
    Represents the social connections and interactions of a human,
    including their relationships and conversation patterns.
    """

    relationships: List[str] = Field(
        default_factory=list,
        description="Names of other humans with whom this human has a significant relationship."
    )
    speaks_positively_of: List[str] = Field(
        default_factory=list,
        description="Names of humans about whom this human tends to speak positively."
    )
    speaks_negatively_of: List[str] = Field(
        default_factory=list,
        description="Names of humans about whom this human tends to speak negatively."
    )
    positive_conversations_with: List[str] = Field(
        default_factory=list,
        description="Names of humans with whom this human tends to have positive conversations."
    )
    negative_conversations_with: List[str] = Field(
        default_factory=list,
        description="Names of humans with whom this human tends to have negative conversations."
    )

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
    info: Info = Field(
        default_factory=Info,
        description="The mental model of the human, including personality, topics, and interests."
    )
    incentives: Incentives = Field(
        default_factory=Incentives,
        description="The social connections and interaction patterns of the human."
    )
    life_experiences: List[str] = Field(
        default_factory=list,
        description="A list of significant life events, stories, or experiences that shape the human's perspective."
    )

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
        # Initialize the self mental model with the human's known info, incentives, and life experiences
        self.update_mental_model(self.name, self.info, self.incentives, self.life_experiences)

    def update_mental_model(self, participant_name: str, info: Info = None, incentives: Incentives = None, life_experiences: List[str] = None):
        """
        Update the mental model for a specific participant.
        """
        if participant_name not in self.mental_models:
            # For self, use own values; for others, use empty Info, Incentives, and life_experiences
            if participant_name == self.name:
                new_info = self.info.model_copy()
                new_incentives = self.incentives.model_copy()
                new_life_experiences = self.life_experiences.copy()
            else:
                new_info = Info()
                new_incentives = Incentives()
                new_life_experiences = []
            
            self.mental_models[participant_name] = Human(
                name=participant_name,
                info=new_info,
                incentives=new_incentives,
                life_experiences=new_life_experiences
            )
        
        if info:
            self.mental_models[participant_name].info = info
        if incentives:
            self.mental_models[participant_name].incentives = incentives
        if life_experiences is not None:
            self.mental_models[participant_name].life_experiences = life_experiences

    class Config:
        arbitrary_types_allowed = True
