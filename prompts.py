class Prompts:
    SELF_PERCEPTION = """
    Given the following conversation between {participant1_name} and {participant2_name}:

    {example_conversation}

    You are tasked with extracting {participant1_name}'s view of himself. 
    Focus on {participant1_name}'s self-perception, not how others see him. 
    Based on the conversation, provide the following information about {participant1_name}:

    1. Personality traits (list 3-5 traits):
    2. Positive topics (list 2-3 topics {participant1_name} views positively or enjoys discussing):
    3. Negative topics (list 2-3 topics {participant1_name} views negatively or dislikes discussing):
    4. Interests (list 2-3 of {participant1_name}'s interests, hobbies, or areas of expertise):
    5. Relationships (list any significant relationships mentioned):
    6. Speaks positively of (list any individuals {participant1_name} speaks positively about):
    7. Speaks negatively of (list any individuals {participant1_name} speaks negatively about):
    8. Has positive conversations with (based on this conversation):
    9. Has negative conversations with (based on this conversation):
    10. Life experiences (list 2-3 significant life events or stories that have shaped {participant1_name}):
    """

    OTHER_PERCEPTION = """
    Given the following conversation between {participant1_name} and {participant2_name}:

    {example_conversation}

    You are tasked with extracting {participant1_name}'s view of {participant2_name}. 
    Focus on how {participant1_name} perceives {participant2_name}, 
    not on {participant2_name}'s actual traits or self-perception. 
    Based on the conversation, provide the following information about 
    how {participant1_name} views {participant2_name}:

    1. Personality traits (list 3-5 traits {participant1_name} might attribute to {participant2_name}):
    2. Positive topics (list 2-3 topics {participant1_name} thinks {participant2_name} views positively or enjoys discussing):
    3. Negative topics (list 2-3 topics {participant1_name} thinks {participant2_name} views negatively or dislikes discussing):
    4. Interests (list 2-3 interests, hobbies, or areas of expertise {participant1_name} might attribute to {participant2_name}):
    5. Relationships (list any significant relationships of {participant2_name} mentioned by {participant1_name}):
    6. Speaks positively of (list any individuals {participant1_name} notices {participant2_name} speaking positively about):
    7. Speaks negatively of (list any individuals {participant1_name} notices {participant2_name} speaking negatively about):
    8. Has positive conversations with (based on {participant1_name}'s perception in this conversation):
    9. Has negative conversations with (based on {participant1_name}'s perception in this conversation):
    10. Life experiences (list 2-3 significant life events or stories that {participant1_name} might attribute to {participant2_name}):
    """
