from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import date

class Pet(BaseModel):
    """
    Represents a pet, either owned by self or known about others.
    """
    name: str = Field(..., description="The name of the pet")
    species: str = Field(..., description="The species of the pet (e.g., 'Dog', 'Cat')")
    breed: Optional[str] = Field(None, description="The breed of the pet, if known")
    age: Optional[float] = Field(None, description="The age of the pet in years, if known")
    is_own_pet: bool = Field(..., description="Whether this pet belongs to the person or to someone else")
    owner_name: Optional[str] = Field(None, description="The name of the pet's owner if not owned by self")
    description: str = Field(..., description="A brief description of the pet from the person's perspective")

class Memory(BaseModel):
    """
    Represents a single memory or piece of information.
    """
    content: str = Field(..., description="The content of the memory")
    date_added: date = Field(default_factory=date.today, description="The date this memory was added")

class PersonalMemory(BaseModel):
    """
    Represents the personal memory of an individual, including knowledge about self and others.
    """
    name: str = Field(..., description="The name of the person whose memory this is")
    residence: str = Field(..., description="The person's place of residence")
    pets: List[Pet] = Field(default_factory=list, description="List of pets, both owned and known about")
    memories: List[Memory] = Field(default_factory=list, description="List of memories or pieces of information")
    known_people: Dict[str, str] = Field(default_factory=dict, description="Dictionary of known people and brief descriptions")

class HumanMemory(BaseModel):
    """
    Stores personal memories for multiple individuals.
    """
    people: Dict[str, PersonalMemory] = Field(..., description="Dictionary of personal memories, keyed by person's name")

# Create instances for Bob and Shirley
bob_memory = PersonalMemory(
    name="Bob",
    residence="Apartment complex down the street",
    pets=[
        Pet(name="Rocky", species="Dog", breed="Golden Retriever", age=3, is_own_pet=True, 
            description="My friendly and playful dog. Gets anxious at the vet. Tries to bury bones in couch cushions. Brings his leash when he wants a walk."),
        Pet(name="Buffy", species="Cat", breed="Tabby", age=5, is_own_pet=False, owner_name="Shirley",
            description="Shirley's cat. She mentioned Buffy drops toy mice in her shoes.")
    ],
    memories=[
        Memory(content="I met Shirley today. She's new to the neighborhood and has a cat."),
        Memory(content="Shirley lives in the same apartment complex as me."),
        Memory(content="We talked about arranging a pet playdate.")
    ],
    known_people={
        "Shirley": "New neighbor, owns a cat named Buffy. Friendly and open to pet playdates."
    }
)

shirley_memory = PersonalMemory(
    name="Shirley",
    residence="Apartment complex down the street",
    pets=[
        Pet(name="Buffy", species="Cat", breed="Tabby", age=5, is_own_pet=True,
            description="My tabby cat. Adopted her from a shelter last year. She likes to drop her toy mouse in my shoes and meow proudly."),
        Pet(name="Rocky", species="Dog", breed="Golden Retriever", age=3, is_own_pet=False, owner_name="Bob",
            description="Bob's dog. He mentioned Rocky gets anxious at the vet.")
    ],
    memories=[
        Memory(content="I met Bob today. He's a neighbor who owns a dog."),
        Memory(content="Bob lives in the same apartment complex as me."),
        Memory(content="We discussed the possibility of a pet playdate.")
    ],
    known_people={
        "Bob": "Neighbor, owns a Golden Retriever named Rocky. Friendly and interested in pet playdates."
    }
)

# Initialize HumanMemory with Bob and Shirley's personal memories
human_memory = HumanMemory(people={
    "Bob": bob_memory,
    "Shirley": shirley_memory
})