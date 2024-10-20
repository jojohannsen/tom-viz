from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from prompts import Prompts
from human_model import Human, Info, Incentives

# Initialize the LLMs
openai_llm = ChatOpenAI(model="gpt-4")
anthropic_llm = ChatAnthropic(model="claude-2")

# Create prompt templates
self_prompt = PromptTemplate(
    input_variables=["participant1_name", "participant2_name", "example_conversation"],
    template=Prompts.SELF_PERCEPTION
)

other_prompt = PromptTemplate(
    input_variables=["participant1_name", "participant2_name", "example_conversation"],
    template=Prompts.OTHER_PERCEPTION
)

# Create chains for OpenAI with structured output
openai_self_chain = self_prompt | openai_llm.with_structured_output(Human)
openai_other_chain = other_prompt | openai_llm.with_structured_output(Human)

# Create chains for Anthropic with structured output
anthropic_self_chain = self_prompt | anthropic_llm.with_structured_output(Human)
anthropic_other_chain = other_prompt | anthropic_llm.with_structured_output(Human)

# Wrapper functions to use the chains
def use_openai_self_chain(participant1_name, participant2_name, example_conversation):
    return openai_self_chain.invoke({
        "participant1_name": participant1_name,
        "participant2_name": participant2_name,
        "example_conversation": example_conversation
    })

def use_openai_other_chain(participant1_name, participant2_name, example_conversation):
    return openai_other_chain.invoke({
        "participant1_name": participant1_name,
        "participant2_name": participant2_name,
        "example_conversation": example_conversation
    })

def use_anthropic_self_chain(participant1_name, participant2_name, example_conversation):
    return anthropic_self_chain.invoke({
        "participant1_name": participant1_name,
        "participant2_name": participant2_name,
        "example_conversation": example_conversation
    })

def use_anthropic_other_chain(participant1_name, participant2_name, example_conversation):
    return anthropic_other_chain.invoke({
        "participant1_name": participant1_name,
        "participant2_name": participant2_name,
        "example_conversation": example_conversation
    })
