import streamlit as st
from streamlit_chatbox import *
import time
import simplejson as json
import requests
st.title("qna chatbot")
llm = FakeLLM()
chat_box = ChatBox()


with st.sidebar:
    st.subheader('start to chat using streamlit')
    streaming = st.checkbox('streaming', True)
    in_expander = st.checkbox('show messages in expander', True)
    

    st.divider()

    btns = st.container()

    


chat_box.init_session()
chat_box.output_messages()

if query := st.chat_input('input your question here'):
    response = requests.post('http://127.0.0.1:8000/qna/', json={"querie":query})
    print()
    chat_box.user_say(response.json()['response'])
    if streaming:
        generator = llm.chat_stream(query)
        elements = chat_box.ai_say(
            [
                # you can use string for Markdown output if no other parameters provided
                Markdown("thinking", in_expander=in_expander,
                         expanded=True, title="answer"),
               
            ]
        )
        
        text = ""
        for x, docs in generator:
            text += x
            chat_box.update_msg(text, element_index=0, streaming=True)
        # update the element without focus
        chat_box.update_msg(text, element_index=0, streaming=False, state="complete")
        
    else:
        text, docs = llm.chat(query)
        chat_box.ai_say(
            [
                Markdown(text, in_expander=in_expander,
                         expanded=True, title="answer"),
              
            ]
        )



btns.download_button(
    "Export Markdown",
    "".join(chat_box.export2md()),
    file_name=f"chat_history.md",
    mime="text/markdown",
)

btns.download_button(
    "Export Json",
    chat_box.to_json(),
    file_name="chat_history.json",
    mime="text/json",
)

if btns.button("clear history"):
    chat_box.init_session(clear=True)
    st.experimental_rerun()

