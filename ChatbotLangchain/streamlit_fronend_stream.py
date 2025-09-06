import streamlit as st
from chatbot_backend import workflow 
from langchain_core.messages import HumanMessage



# st.session_state-> dict-> does not refresh dictionary
if 'messages' not in st.session_state:
    st.session_state['messages']=[]

# loading the conversatin history
for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input=st.chat_input("Type your message")

if user_input:
    # first add the message to messages history
    st.session_state['messages'].append({'role':'user', 'content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

    config={'configurable':{'thread_id':1}}
    
    with st.chat_message('assistant'):
        ai_message=st.write_stream(
            message_chunk.content for message_chunk, metadata in workflow.stream(
                {'messages':[HumanMessage(content=user_input)]},
                config=config,
                stream_mode="messages"
            )
    )
    st.session_state['messages'].append({'role':'assistant', 'content':ai_message})
    