from gen_graph import gen_graph
from human_model import Human, HumanMind, Info, Incentives
from pydantic import BaseModel, Field
from typing import Dict, List, Set, Annotated
import operator
from prompts import Prompts
from llms import use_openai_self_chain, use_openai_other_chain, use_anthropic_self_chain, use_anthropic_other_chain

class ConversationState(BaseModel):
    """
    Represents the state of a conversation.
    """
    participants: Dict[str, Human] = Field(
        default_factory=dict,
        description="The participants in the conversation, with names as keys and Human objects as values."
    )
    conversation_history: Annotated[List[(str, str)], operator.add] = Field(
        default_factory=list,
        description="The history of the conversation."
    )
    current_speaker: Human = Field(
        description="The human who is currently speaking."
    )
    conversation_text: object = Field(
        description="Generator yielding person and their current thought."
    )

def conversation(lines: List[str]):
    for line in lines:
        yield Human(name=line.split(":")[0], thought=line.split(":")[1])

def load_conversation(state: ConversationState):
    lines = open("data/conversation.txt").readlines()
    human_names: Set[str] = set(line.split(":")[0] for line in lines)
    p = {}
    for name in human_names:
        human = HumanMind(name=name)
        # Initialize empty mental models for all other participants
        for other_name in human_names:
            if other_name != name:
                human.update_mental_model(other_name)
        p[name] = human
    return {"conversation_text": conversation(lines), "participants": p }

def converse(state: ConversationState):
    person, text = next(state.conversation_text)
    return { "conversation_history": [(person, text)], "current_speaker": state.participants[person] }
    
def update_listener_minds(state: ConversationState):
    speaker = state.current_speaker
    last_message = state.conversation_history[-1]
    for listener_name, listener in state.participants.items():
        # Get existing mental model for the speaker, and update what the listener thinks of them
        existing_model = listener.mental_models.get(speaker.name)
        updated_view = update_listener_perception(last_message, speaker.name, listener_name, existing_model)
        listener.update_mental_model(speaker.name, updated_view.info, updated_view.incentives)
    return {"participants": state.participants}

def update_listener_perception(message: str, speaker_name: str, listener_name: str, existing_model: Human = None) -> Human:
    # Determine which chain to use, this is how the speaker sees themselves and others
    if speaker_name == listener_name:
        chain = use_openai_self_chain  # or use_anthropic_self_chain
    else:
        chain = use_openai_other_chain  # or use_anthropic_other_chain

    # Use the chain to extract info and incentives
    listener_view = chain(speaker_name, listener_name, message)

    return listener_view

graph_spec = """
START(ConversationState) => load_conversation

load_conversation => human_speaks

human_speaks => update_listener_minds

"""
