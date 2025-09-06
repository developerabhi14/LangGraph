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
    response=workflow.invoke({'messages':[HumanMessage(content=user_input)]}, config=config)
    ai_message=response['messages'][-1].content
    st.session_state['messages'].append({'role':'assistant', 'content':ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)