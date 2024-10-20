from fasthtml.common import *
from fastcore.meta import delegates

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
                    Th(RightArrow(), 'other', cls="human human1-color"),
                    Th(RightArrow(), 'self', cls="human human2-color"),
                    Th(RightArrow(), 'other', cls="human human2-color")
                )
            ),
            Tbody(
                Tr(Td('happy', cls='row-header'), Td(cls='human human1-color'), Td(cls='human human1-color'), Td(cls='human human2-color'), Td(cls='human human2-color')),
                Tr(Td('sad', cls='row-header'), Td(cls='human human1-color'), Td(cls='human human1-color'), Td(cls='human human2-color'), Td(cls='human human2-color')),
                Tr(Td('sees positively', cls='row-header'), Td(cls='human human1-color'), Td(cls='human human1-color'), Td(cls='human human2-color'), Td(cls='human human2-color')),
                Tr(Td('sees negatively', cls='row-header'), Td(cls='human human1-color'), Td(cls='human human1-color'), Td(cls='human human2-color'), Td(cls='human human2-color')),
                Tr(Td('life experience', cls='row-header'), Td(cls='human human1-color'), Td(cls='human human1-color'), Td(cls='human human2-color'), Td(cls='human human2-color')),
                Tr(Td('introduces topic', cls='row-header'), Td(cls='human human1-color'), Td(cls='human human1-color'), Td(cls='human human2-color'), Td(cls='human human2-color'))
            )
        ),
        cls='table-container'
    )

@rt('/') 
def get():
    return JJTitled("Chat Agent Demo",
        Div(
            Header(I("Theory of Mind - Violation of Expectation")),
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

serve()
