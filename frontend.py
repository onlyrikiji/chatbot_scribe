import streamlit as st
from backend import handle_userinput, get_pdf_text, get_text_chunks, get_vectorstore, get_conversation_chain
from htmlTemplates import css, bot_template, user_template
from dotenv import load_dotenv
import os


def main():
    st.set_page_config(page_title="SCRIBE!", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    
    # Add your project logo
    logo = st.image("https://i.ibb.co/44w9sk1/extralong.png", use_column_width=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Review with your own PDF using SCRIBE! :books:")

    # Sidebar
    with st.sidebar:
        # Add your project logo
        logo = st.image("https://i.ibb.co/k3Jt1km/scribe.png", use_column_width=True)

        st.subheader("Add your PDF reviewer here!")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)

    user_question = st.text_input("Ask a question based on your PDF reviewer:")
    
    if user_question:
        st.session_state.chat_history = handle_userinput(user_question, st.session_state.conversation)

        # Display chat history
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

if __name__ == '__main__':
    main()
