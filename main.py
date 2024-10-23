from fasthtml.common import *
from fastcore.meta import delegates
import os

app, rt = fast_app()

participants = ["You", "AI Agent"]
current_conversation = []
current_line = 0

@delegates(ft_hx, keep=True)
def JJTitled(title:str="FastHTML app", *args, cls="container", **kwargs)->FT:
    "An HTML partial containing a `Title`, and `H1`, and any provided children"
    return Title(title), Main(*args, cls=cls, **kwargs)

def RightArrow():
    return "→ "

def ChatContainer():
    return Div(
        Div(
            Div(
                Button('test', id='next-line', cls='participants-buttons', hx_get='/next', hx_target='#chat-messages', hx_swap='beforeend'),
                Span('  '),
                Button('Update Table', id='update-table', cls='participants-buttons', onclick='updateParticipantsUI()'),
                Span('  Participants:', cls='participants-label'),
                ParticipantsButtons(participants[0], participants[1]),
                cls='participants-container'
            ),
            cls='chat-header'
        ),
        Div(
            Div('Hello! How can I assist you today?', data_sender=participants[1], cls='message agent-message'),
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

def AttributeTable():
    return Div(
        Table(
            ParticipantTableHeader(participants[0], participants[1]),
            Tbody(
                Tr(Td('experiences', cls='row-header'), Td(cls='human human1-color'), Td(cls='human human1-color'), Td(cls='human human2-color'), Td(cls='human human2-color')),
                Tr(Td('interests', cls='row-header'), Td(cls='human human1-color'), Td(cls='human human1-color'), Td(cls='human human2-color'), Td(cls='human human2-color')),
                Tr(Td('family', cls='row-header'), Td(cls='human human1-color'), Td(cls='human human1-color'), Td(cls='human human2-color'), Td(cls='human human2-color')),
                Tr(Td('friends', cls='row-header'), Td(cls='human human1-color'), Td(cls='human human1-color'), Td(cls='human human2-color'), Td(cls='human human2-color')),
                Tr(Td('pets', cls='row-header'), Td(cls='human human1-color'), Td(cls='human human1-color'), Td(cls='human human2-color'), Td(cls='human human2-color')),
                Tr(Td('community', cls='row-header'), Td(cls='human human1-color'), Td(cls='human human1-color'), Td(cls='human human2-color'), Td(cls='human human2-color'))
            )
        ),
        cls='table-container'
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
        hx_swap_oob="outerHTML"
    )

@rt('/') 
def get():
    return JJTitled("Chat Agent Demo",
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

@rt('/load')
def load_file(filename:str):
    if not filename:
        return {'error': 'Filename not provided'}, 400
    
    file_path = os.path.join('data', filename)
    if not os.path.exists(file_path):
        return {'error': 'File not found'}, 404
    
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return {'content': content}
    except Exception as e:
        return {'error': f'Error reading file: {str(e)}'}, 500

@rt('/next')
def next_line():
    global current_conversation, current_line, participants
    print("next_line")
    if not current_conversation:
        # Load conversation_1.txt if no conversation is loaded
        file_path = os.path.join('data', 'conversation_1.txt')
        try:
            with open(file_path, 'r') as file:
                current_conversation = file.readlines()
            participants[0] = current_conversation[0].split(':')[0].strip()
            participants[1] = current_conversation[1].split(':')[0].strip()
            current_line = 0
        except Exception as e:
            return {'error': f'Error reading file: {str(e)}'}, 500
    
    if current_line < len(current_conversation):
        line = current_conversation[current_line].strip()
        speaker, content = line.split(':', 1)
        is_user = speaker == participants[0]
        print(f"speaker: {speaker}, content: {content}, is_user: {is_user}")
        print("p0=", participants[0], "p1=", participants[1])
        message_class = 'user-message' if is_user else 'agent-message'
        
        result = Div(content.strip(), cls=f"message {message_class}", data_sender=speaker)
        current_line += 1
        return result,ParticipantsButtons(participants[0], participants[1])#,ParticipantTableHeader(participants[0], participants[1])
    else:
        return Div("Conversation ended", cls="message system-message")

def ParticipantsButtons(participant1, participant2):
    return Div(
        Button(participant1, id='user-name', cls='participants-buttons', hx_get='/update-participants', hx_target='#participants-container', hx_swap='outerHTML'),
        Button(participant2, id='agent-name', cls='participants-buttons', hx_get='/update-participants', hx_target='#participants-container', hx_swap='outerHTML'),
        id='participants-container',
        cls='participants',
        hx_swap_oob="outerHTML"
    )

@rt('/update-participants')
def update_participants():
    return ParticipantsButtons(participants[0], participants[1])

serve()
