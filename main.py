from fasthtml.common import *
from fastcore.meta import delegates
import os
from llms import create_named_participants
from human import Human, HumanView
from conversation_manager import ConversationManager  # Import ConversationManager

os.environ['LANGCHAIN_PROJECT'] = 'theory-of-mind-2'

app, rt = fast_app()

# Add these global variables at the top of the file
participants = ["You", "AI Agent"]
conversation_manager = None
current_line = 0
human1 = None
human2 = None

@delegates(ft_hx, keep=True)
def JJTitled(title:str, *args, cls="container", **kwargs)->FT:
    "An HTML partial containing a `Title`, and `H1`, and any provided children"
    return Title(title), Main(*args, cls=cls, **kwargs)

def RightArrow():
    return "→ "

def ConversationSelector(span_text: str, button_text: str):
    return Div(
        Span(span_text, cls='participants-label'),
        Button(button_text, id='next-line', cls='participants-buttons', hx_get='/next', hx_target='#chat-messages', hx_swap='beforeend'),
        cls='participants-container',
        id='conversation-selector',
        hx_swap_oob='outerHTML'
    )

def ChatContainer():
    return Div(
        Div(
            ConversationSelector('Conversations:', 'Bob-Shirley'),
            cls='chat-header'
        ),
        Div(
            Div('Select a conversation to begin.', data_sender=participants[1], cls='message agent-message'),
            id='chat-messages',
            cls='chat-messages'
        ),
        Div(
            Input(type='text', id='user-input', placeholder='Type your message...'),
            Button('Send', id='send-button'),
            cls='chat-input'
        ),
        cls='chat-container left-column'
    )

def AttributeList(human_view: HumanView, color: str) -> FT:
    """
    Create a FastHTML Pre component with newline-separated attributes from a HumanView.
    """
    return Pre('\n'.join(human_view.attributes), cls=f'attribute-list {color}')

def AttributeTable():
    global human1, human2
    if human1 is None or human2 is None:
        # Initialize with an empty dictionary for society
        human1 = Human(name=participants[0], society={})
        human2 = Human(name=participants[1], society={})
    
    def get_human_view(human, name):
        return human.society.get(name, HumanView(name=name, myself=(human.name == name)))
    
    thoughts = Div(
        Span('thoughts'),
        Button('update', 
               id='update-table-btn', 
               cls='participants-buttons', 
               hx_get='/conversation', 
               hx_target='#attribute-table', 
               hx_swap='outerHTML'),
        cls='thoughts-container'
    )
    return Div(
         Table(
            ParticipantTableHeader(participants[0], participants[1]),
            Tbody(
                Tr(Td(thoughts, cls='row-header'), 
                   Td(AttributeList(get_human_view(human1, human1.name), 'self-color'), cls='human human1-color', id='human1-self-view'), 
                   Td(AttributeList(get_human_view(human1, human2.name), 'other-color'), cls='human human1-color', id='human1-other-view'), 
                   Td(AttributeList(get_human_view(human2, human2.name), 'self-color'), cls='human human2-color', id='human2-self-view'), 
                   Td(AttributeList(get_human_view(human2, human1.name), 'other-color'), cls='human human2-color', id='human2-other-view')),
                # Tr(Td('experiences', cls='row-header'), Td(cls='human human1-color'), Td(cls='human human1-color'), Td(cls='human human2-color'), Td(cls='human human2-color')),
                # Tr(Td('interests', cls='row-header'), Td(cls='human human1-color'), Td(cls='human human1-color'), Td(cls='human human2-color'), Td(cls='human human2-color')),
                # Tr(Td('family', cls='row-header'), Td(cls='human human1-color'), Td(cls='human human1-color'), Td(cls='human human2-color'), Td(cls='human human2-color')),
                # Tr(Td('friends', cls='row-header'), Td(cls='human human1-color'), Td(cls='human human1-color'), Td(cls='human human2-color'), Td(cls='human human2-color')),
                # Tr(Td('pets', cls='row-header'), Td(cls='human human1-color'), Td(cls='human human1-color'), Td(cls='human human2-color'), Td(cls='human human2-color')),
                # Tr(Td('community', cls='row-header'), Td(cls='human human1-color'), Td(cls='human human1-color'), Td(cls='human human2-color'), Td(cls='human human2-color'))
            )
        ),
        cls='table-container',
        id='attribute-table'
    )

def ParticipantTableHeader(participant1, participant2):
    return Thead(
        Tr(
            Th('', rowspan=2, cls="row-header"),
            Th(Span(participant1, id='table-participant1', cls='human1-color'), colspan=2, cls="human human1-color"),
            Th(Span(participant2, id='table-participant2', cls='human2-color'), colspan=2, cls="human human2-color")
        ),
        Tr(
            Th(RightArrow(), 'self', cls="human human1-color"),
            Th(RightArrow(), participant2, id="h1-other", cls="human human1-color"),
            Th(RightArrow(), 'self', cls="human human2-color"),
            Th(RightArrow(), participant1, id="h2-other", cls="human human2-color")
        ),
        id='participant-table-header',
    )


@rt('/') 
def get():
    return JJTitled("Theory of Mind",
        Div(
            Header(I("Theory of Mind - Reasoning about what others are thinking")),
            Div(
                ChatContainer(),
                AttributeTable(),
                cls='main-container'
            ),
            cls='page-container'
        ),
        Script(src='https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js'),
        Script(src='/static/scripts.js'),
        Link(rel="stylesheet", href="/static/styles.css")
    )

@rt('/next')
def next_line():
    global conversation_manager, current_line, participants

    if not conversation_manager or current_line >= len(conversation_manager.all_entries):
        # Reset everything and start over
        file_path = os.path.join('data', 'conversation_1.txt')
        try:
            with open(file_path, 'r') as file:
                conversation_text = file.read()
            conversation_manager = ConversationManager(conversation_text)
            participants = conversation_manager.participants()
            current_line = 0
            return (
                Div("Conversation...", cls="message system-message"),
                ParticipantsButtons(participants[0], participants[1])
            )
        except Exception as e:
            return {'error': f'Error reading file: {str(e)}'}, 500
    
    name, content = conversation_manager.next()
    is_user = name == participants[0]
    message_class = 'user-message' if is_user else 'agent-message'
    message_class = 'intro-message' if name.startswith('Character') or name.startswith('Scene') else message_class
    
    result = Div(content.strip(), cls=f"message {message_class}", data_sender=name)
    current_line += 1
    
    if current_line >= len(conversation_manager.all_entries):
        return (
            result,
            Div("Conversation ended. Click 'Next' to start over.", cls="message system-message")
        )
    else:
        return result, ConversationSelector(f'{participants[0]}-{participants[1]}', 'Next')

def ParticipantsButtons(participant1, participant2):
    trigger_script = Script(
        "document.dispatchEvent(new CustomEvent('analyze-conversation'));"
    )
    return Div(
        Button(participant1, id='user-name', cls='participants-buttons', hx_get='/update-participants', hx_target='#participants-container', hx_swap='outerHTML'),
        Button(participant2, id='agent-name', cls='participants-buttons', hx_get='/update-participants', hx_target='#participants-container', hx_swap='outerHTML'),
        trigger_script,
        id='participants-container',
        cls='participants',
        hx_swap_oob="outerHTML"
    )

@rt('/update-participants')
def update_participants():
    return ParticipantsButtons(participants[0], participants[1])

@rt('/conversation')
def get():
    global conversation_manager, current_line, participants, human1, human2
    
    if not conversation_manager:
        return {'error': 'No conversation loaded'}, 400
    
    conversation = conversation_manager.so_far()
    print(conversation)
    
    participant_generator = create_named_participants(conversation, participants)
    
    # human1: Human
    human1 = next(participant_generator)
    # human2: Human
    human2 = next(participant_generator)
    print("HUMANS: ", human1.name, human2.name)
    human1_self_prompt = human1.generate_self_view_update_prompt(conversation)
    human1 = human1.update_self_view(human1_self_prompt)
    print("HUMAN 1 (self view): ", human1.society[human1.name].attributes)

    human2_self_prompt = human2.generate_self_view_update_prompt(conversation)
    human2 = human2.update_self_view(human2_self_prompt)
    print("HUMAN 2 (self view): ", human2.society[human2.name].attributes)
    
    human1_other_prompt = human1.generate_other_view_update_prompt(human2.name, conversation)
    human1 = human1.update_other_view(human2.name, human1_other_prompt)
    print("HUMAN 1 (other view): ", human1.society[human2.name].attributes)
    human2_other_prompt = human2.generate_other_view_update_prompt(human1.name, conversation)
    human2 = human2.update_other_view(human1.name, human2_other_prompt)
    print("HUMAN 2 (other view): ", human2.society[human1.name].attributes)
    
    table = AttributeTable()
    
    return table

serve()
