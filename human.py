from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
import os
import pickle
from datetime import datetime

# Core data models
class HumanView(BaseModel):
    """Represents one person's view of another person (or themselves)"""
    name: str = Field(..., description="Name of the person being viewed")
    myself: bool = Field(default=False, description="True if this is a self-view")
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

    def generate_other_view_update_prompt(self, other_person: str, conversation: str) -> str:
        """Generate prompt to update this person's view of another person"""
        current_view = self.society[other_person].attributes if other_person in self.society else []
        
        return f"""
        Based on the following conversation, identify what {self.name} learns about {other_person}.
        List concrete facts and attributes that {self.name} discovers about {other_person}.
        Include only new information not already in {self.name}'s current view of {other_person}.
        
        <HUMAN_VIEW>
        {current_view}
        </HUMAN_VIEW>
        
        <CONVERSATION>
        {conversation}
        </CONVERSATION>
        
        What new attributes should be added to {self.name}'s view of {other_person}?
        Please provide a list of individual facts or traits to populate the attributes field of the HumanView.
        """

    def update_other_view(self, other_person: str, prompt: str):
        """Update this person's view of another person"""
        print("UPDATE OTHER VIEW")
        # Create ChatOpenAI instance with gpt-4
        gpt4 = ChatOpenAI(model_name="gpt-4o", temperature=0).with_structured_output(HumanView)

        # Create ChatAnthropic instance with claude-3-sonnet-20240229
        claude = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0).with_structured_output(HumanView)

        # Create a ChatPromptTemplate
        chat_prompt = ChatPromptTemplate.from_template(
            "Based on the following information, create a HumanView for {name}:\n\n{prompt}"
        )

        # Create chains for each model
        gpt4_chain = chat_prompt | gpt4 
        claude_chain = chat_prompt | claude 

        # Prepare the input
        chain_input = {
            "name": other_person,
            "prompt": prompt
        }

        # Invoke each chain with the prepared input
        gpt4_result = invoke_and_save(gpt4_chain, chain_input, "GPT4", other_person)
        claude_result = invoke_and_save(claude_chain, chain_input, "Claude", other_person)

        # Update self-view only if we have valid results
        if gpt4_result:
            print(f"Updating {other_person}'s view with GPT-4 attributes: {gpt4_result.attributes}")
            print("current view: ", self.society[other_person].attributes)
            self.society[other_person].attributes = self.merge_attributes(self.society[other_person].attributes, gpt4_result.attributes)
            print("new view: ", self.society[other_person].attributes)        
        if claude_result:
            print(f"Updating {other_person}'s view with Claude 3.5 Sonnet attributes: {claude_result.attributes}")
            print("current view: ", self.society[other_person].attributes)
            self.society[other_person].attributes = self.merge_attributes(self.society[other_person].attributes, claude_result.attributes)
            print("new view: ", self.society[other_person].attributes)

        return self


    def update_self_view(self, prompt: str):
        """Update this person's self-view"""
        print("UPDATE SELF VIEW")
        # Create ChatOpenAI instance with gpt-4
        gpt4 = ChatOpenAI(model_name="gpt-4o", temperature=0).with_structured_output(HumanView)

        # Create ChatAnthropic instance with claude-3-sonnet-20240229
        claude = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0).with_structured_output(HumanView)

        # Create a ChatPromptTemplate
        chat_prompt = ChatPromptTemplate.from_template(
            "Based on the following information, create a HumanView for {name}:\n\n{prompt}"
        )

        # Create chains for each model
        gpt4_chain = chat_prompt | gpt4     
        claude_chain = chat_prompt | claude 

        # Prepare the input
        chain_input = {
            "name": self.name,
            "prompt": prompt
        }

        # Invoke each chain with the prepared input
        gpt4_result = invoke_and_save(gpt4_chain, chain_input, "GPT4", self.name)
        claude_result = invoke_and_save(claude_chain, chain_input, "Claude", self.name)

        # Update self-view only if we have valid results
        if gpt4_result:
            self.society[self.name].attributes = self.merge_attributes(self.society[self.name].attributes, gpt4_result.attributes)
        
        if claude_result:
            self.society[self.name].attributes = self.merge_attributes(self.society[self.name].attributes, claude_result.attributes)

        return self

    def merge_attributes(self, current_attributes: List[str], new_attributes: List[str]) -> List[str]:
        """Merge two lists of attributes, removing duplicates"""
        return list(set(current_attributes + new_attributes))

    def generate_self_view_update_prompt(self, conversation: str) -> str:
        """Generate prompt to update this person's self-view"""
        return f"""
        Based on the following conversation, identify any new information {self.name} reveals or learns about themselves.
        List only new concrete facts and attributes not already in their self-view: 
        
        <HUMAN_VIEW>
        {self.myself}
        </HUMAN_VIEW>
        
        <CONVERSATION>
        {conversation}
        </CONVERSATION>

        What new attributes should be added to {self.name}'s self-view?
Please provide a list of individual facts or traits to populate the attributes field of the HumanView.
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

def invoke_and_save(chain, chain_input, model_name, other_person):
    # Create the directory if it doesn't exist
    os.makedirs('tests/pickle', exist_ok=True)

    # Generate a unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tests/pickle/{model_name}_{other_person}_{timestamp}.pkl"

    try:
        result = chain.invoke(chain_input)
        print(f"{model_name} Result for {other_person}:")
        print(type(result))
        
        # Save the input and result to a pickle file
        with open(filename, 'wb') as f:
            pickle.dump({'input': chain_input, 'output': result}, f)
        
        return result
    except Exception as e:
        print(f"Error with {model_name} invocation: {type(e)}")
        
        # Save the input and exception to a pickle file
        with open(filename, 'wb') as f:
            pickle.dump({'input': chain_input, 'error': str(e)}, f)
        
        return None
