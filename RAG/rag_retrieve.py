from langchain_google_genai import ChatGoogleGenerativeAI

import streamlit as st
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone as PC
import pinecone
from pinecone import Pinecone
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv()





# Streamlit app
def main():
    st.title("Disha - IIITN Chatbot")
    st.markdown("*A chatbot guiding IIIT Nagpur users with direction and information.*")

    # Initialize session state for conversation history
    if "history" not in st.session_state:
        st.session_state.history = []

    # User input
    user_input = st.chat_input("Ask a question...")

    if user_input:
        # Append user message to history
        st.session_state.history.append({"role": "user", "content": user_input})

        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        pineconekey = os.getenv("PINECONE_API_KEY")
        pc = Pinecone(api_key=pineconekey)
        index_name = "iiitn"

        docsearch = PC.from_existing_index(index_name=index_name, embedding=embeddings)
        #prompt_template1="""Just return the context:{context} provided for question:{question}"""
        prompt_template = """
        Use the following pieces of information to answer the user's question.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Context: {context}
        Question: {question}

        Only return the helpful answer below and nothing else.
        Helpful answer:
        """

        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

        llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro-latest", temperature=0.9)

        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )

        result = qa({"query": user_input})

        # Append bot response to history
        st.session_state.history.append({"role": "bot", "content": result["result"]})

    # Display conversation history
    for message in st.session_state.history:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        else:
            with st.chat_message("bot"):
                st.write(message["content"])

if __name__ == "__main__":
    main()