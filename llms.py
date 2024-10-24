from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate

from human import Human, HumanView

# Initialize the LLMs
openai_llm = ChatOpenAI(model="gpt-4o")
anthropic_llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

def mk_human_views(participant, participant_names):
    return [
        HumanView(name=participant, myself=True, attributes=[]),
        *[HumanView(name=other, myself=False, attributes=[]) for other in participant_names if other != participant]
    ]

def create_named_participants(conversation, participant_names):
    for participant in participant_names:
        human = Human(name=participant, society={hv.name: hv for hv in mk_human_views(participant, participant_names)})
        yield human
