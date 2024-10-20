from fasthtml.common import *
from fastcore.meta import delegates
import os

app, rt = fast_app()

participants = ["You", "AI Agent"]

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
                Span('Participants:', cls='participants-label'),
                Div(
                    Button(participants[0], id='user-name', cls='participants-buttons'),
                    Button(participants[1], id='agent-name', cls='participants-buttons'),
                    cls='participants'
                ),
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
            Thead(
                Tr(
                    Th('', rowspan=2, cls="row-header"),
                    Th(Span(participants[0], id='table-participant1', cls='human1-color'), colspan=2, cls="human human1-color"),
                    Th(Span(participants[1], id='table-participant2', cls='human2-color'), colspan=2, cls="human human2-color")
                ),
                Tr(
                    Th(RightArrow(), 'self', cls="human human1-color"),
                    Th(RightArrow(), participants[1], id="h1-other", cls="human human1-color"),
                    Th(RightArrow(), 'self', cls="human human2-color"),
                    Th(RightArrow(), participants[0], id="h2-other", cls="human human2-color")
                )
            ),
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

serve()
