from human_model import Human, HumanMind

class Prompts:
    SELF_PERCEPTION = """
    Given the following conversation between {participant1_name} and {participant2_name}:

    {example_conversation}

    You are tasked with extracting {participant1_name}'s view of themselves. 
    Focus on {participant1_name}'s self-perception, not how others see them. 
    Based on the conversation, provide the following information about {participant1_name}:

    1. Experiences (list 2-3 significant life events or experiences that have shaped {participant1_name}):
    2. Interests (list 2-3 hobbies, passions, or topics that {participant1_name} finds engaging or enjoyable):
    3. Family (list any family members or family-related information important to {participant1_name}):
    4. Friends (list any close friends or social connections that are significant to {participant1_name}):
    5. Pets (list any pets owned by {participant1_name} or animals they have a strong connection with):
    6. Community (list any groups, organizations, or communities {participant1_name} is part of or identifies with):
    """

    OTHER_PERCEPTION = """
    Given the following conversation between {participant1_name} and {participant2_name}:

    {example_conversation}

    You are tasked with extracting {participant1_name}'s view of {participant2_name}. 
    Focus on how {participant1_name} perceives {participant2_name}, 
    not on {participant2_name}'s actual traits or self-perception. 
    Based on the conversation, provide the following information about 
    how {participant1_name} views {participant2_name}:

    1. Experiences (list 2-3 significant life events or experiences that {participant1_name} believes have shaped {participant2_name}):
    2. Interests (list 2-3 hobbies, passions, or topics that {participant1_name} thinks {participant2_name} finds engaging or enjoyable):
    3. Family (list any family members or family-related information that {participant1_name} believes is important to {participant2_name}):
    4. Friends (list any close friends or social connections that {participant1_name} thinks are significant to {participant2_name}):
    5. Pets (list any pets {participant1_name} believes {participant2_name} owns or has a strong connection with):
    6. Community (list any groups, organizations, or communities {participant1_name} thinks {participant2_name} is part of or identifies with):
    """

def generate_human_description(human: Human) -> str:
    """Generate a description of a human based on their attributes."""
    description = f"{human.name} is a person with the following characteristics:\n"
    
    if human.experiences:
        description += f"Experiences: {', '.join(human.experiences)}\n"
    
    if human.interests:
        description += f"Interests: {', '.join(human.interests)}\n"
    
    if human.family:
        description += f"Family: {', '.join(human.family)}\n"
    
    if human.friends:
        description += f"Friends: {', '.join(human.friends)}\n"
    
    if human.pets:
        description += f"Pets: {', '.join(human.pets)}\n"
    
    if human.community:
        description += f"Community involvement: {', '.join(human.community)}\n"
    
    return description.strip()

def generate_mental_model_prompt(human_mind: HumanMind, other_name: str) -> str:
    """Generate a prompt for the mental model of another person."""
    self_description = generate_human_description(human_mind)
    other_mental_model = human_mind.mental_models.get(other_name, Human(name=other_name))
    other_description = generate_human_description(other_mental_model)
    
    prompt = f"""
    You are {human_mind.name}. Here's what you know about yourself:
    {self_description}

    You are thinking about {other_name}. Here's what you believe about {other_name}:
    {other_description}

    Based on this information, how do you think {other_name} perceives you? 
    Consider their experiences, interests, and social connections. 
    How might these factors influence their view of you?
    """
    
    return prompt.strip()

def generate_conversation_prompt(human1: Human, human2: Human, context: str = "") -> str:
    """Generate a prompt for a conversation between two humans."""
    h1_description = generate_human_description(human1)
    h2_description = generate_human_description(human2)
    
    prompt = f"""
    {human1.name}'s characteristics:
    {h1_description}

    {human2.name}'s characteristics:
    {h2_description}

    Context: {context}

    Generate a conversation between {human1.name} and {human2.name}. 
    Consider their experiences, interests, and social connections. 
    How might these factors influence their interaction?

    {human1.name}: 
    """
    
    return prompt.strip()

# You can add more prompt generation functions as needed
