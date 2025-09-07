import streamlit as st
from chatbot_backend import workflow 
from langchain_core.messages import HumanMessage
import uuid


# *************************************** Utility funtions **********************************
def generate_thread_id():
    thread_id=uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id=generate_thread_id()
    st.session_state['thread_id']=thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['messages']=[]

def add_thread(thread_id, title="New Chat"):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'][thread_id] = title

def load_conversation(thread_id):
    return workflow.get_state(config={'configurable':{'thread_id':thread_id}}).values['messages']
# *************************************** Session Setup *****************************************


# st.session_state-> dict-> does not refresh dictionary
if 'messages' not in st.session_state:
    st.session_state['messages']=[]
if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generate_thread_id()
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads']={}


add_thread(st.session_state['thread_id'])
# **************************************** Sidebar UI **********************************************

st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button('New Chat'):
    reset_chat()


st.sidebar.header("My conversations")

for thread_id, title in reversed(list(st.session_state['chat_threads'].items())):
    if st.sidebar.button(title, key=thread_id):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id=thread_id)

        temp_msg=[]
        for m in messages:
            role = 'user' if isinstance(m, HumanMessage) else 'assistant'
            temp_msg.append({'role':role, 'content': m.content})
        st.session_state['messages'] = temp_msg


# **************************************** Main UI ************************************************
# loading the conversatin history
for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input=st.chat_input("Type your message")

if user_input:
    # first add the message to messages history
    st.session_state['messages'].append({'role':'user', 'content':user_input})

    # update thread title if it's still "New Chat"
    if st.session_state['chat_threads'][st.session_state['thread_id']] == "New Chat":
        st.session_state['chat_threads'][st.session_state['thread_id']] = user_input[:30]  # truncate for neatness
        st.rerun() 

    with st.chat_message('user'):
        st.text(user_input)

    config={'configurable':{'thread_id':st.session_state['thread_id']}}
    
    with st.chat_message('assistant'):
        ai_message=st.write_stream(
            message_chunk.content for message_chunk, metadata in workflow.stream(
                {'messages':[HumanMessage(content=user_input)]},
                config=config,
                stream_mode="messages"
            )
    )
    st.session_state['messages'].append({'role':'assistant', 'content':ai_message})
    