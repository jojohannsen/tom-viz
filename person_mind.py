from pydantic import BaseModel, Field
from typing import List, Optional

class PersonalHistory(BaseModel):
    """
    Contains information about a person's background and significant life events.
    """
    upbringing: Optional[str] = Field(
        None,
        description="Information about the person's early life."
    )
    education: Optional[str] = Field(
        None,
        description="Educational background."
    )
    significant_life_events: Optional[List[str]] = Field(
        None,
        description="Key events that have shaped the person."
    )

class Emotion(BaseModel):
    """
    Captures the emotional aspects of a person, including current state and expressions.
    """
    current_state: Optional[str] = Field(
        None,
        description="The person's current emotional state."
    )
    expressions: Optional[List[str]] = Field(
        None,
        description="Common emotional expressions."
    )
    empathy_levels: Optional[str] = Field(
        None,
        description="The person's ability to understand others' feelings."
    )

class RelationshipDynamics(BaseModel):
    """
    Details the person's relationships with family, friends, and colleagues.
    """
    family: Optional[str] = Field(
        None,
        description="Relationship with family members."
    )
    friends: Optional[str] = Field(
        None,
        description="Friendships and social circle."
    )
    colleagues: Optional[str] = Field(
        None,
        description="Professional relationships."
    )
    social_network: Optional[str] = Field(
        None,
        description="The person's broader social connections."
    )
    support_systems: Optional[str] = Field(
        None,
        description="Sources of support in the person's life."
    )

class InterpersonalFacts(BaseModel):
    """
    Represents various facts and insights gained from interpersonal interactions with a person.
    """
    personal_beliefs_and_values: Optional[List[str]] = Field(
        None,
        description="A list of the person's core principles and ethics."
    )
    false_beliefs_and_misconceptions: Optional[List[str]] = Field(
        None,
        description="Misunderstandings or incorrect assumptions the person holds."
    )
    personal_history_and_background: Optional[PersonalHistory] = Field(
        None,
        description="Information about the person's upbringing, education, and significant life events."
    )
    interests_and_hobbies: Optional[List[str]] = Field(
        None,
        description="Activities the person enjoys."
    )
    emotions_and_feelings: Optional[Emotion] = Field(
        None,
        description="Emotional aspects, including current state and expressions."
    )
    goals_and_aspirations: Optional[List[str]] = Field(
        None,
        description="Future plans and ambitions."
    )
    opinions_and_perspectives: Optional[List[str]] = Field(
        None,
        description="The person's viewpoints on various topics."
    )
    cultural_and_social_norms: Optional[List[str]] = Field(
        None,
        description="Cultural practices and social expectations influencing the person."
    )
    personal_challenges_and_struggles: Optional[List[str]] = Field(
        None,
        description="Difficulties or obstacles the person is facing."
    )
    skills_and_expertise: Optional[List[str]] = Field(
        None,
        description="Professional skills and talents."
    )
    relationship_dynamics: Optional[RelationshipDynamics] = Field(
        None,
        description="Details about the person's relationships with others."
    )
    preferences_and_tastes: Optional[List[str]] = Field(
        None,
        description="Likes and dislikes in various areas."
    )
    body_language_and_non_verbal_communication: Optional[List[str]] = Field(
        None,
        description="Common non-verbal cues and gestures."
    )
    values_alignment_and_compatibility: Optional[str] = Field(
        None,
        description="How the person's values align with others."
    )
    shared_experiences_and_memories: Optional[List[str]] = Field(
        None,
        description="Past events shared with others."
    )
    feedback_and_reflections: Optional[List[str]] = Field(
        None,
        description="Feedback given or received, personal reflections."
    )
