import streamlit as st
import whisper
from audio_recorder_streamlit import audio_recorder
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone as PC
import pinecone
from pinecone import Pinecone
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv()

# Load the Whisper model (English version)
model = whisper.load_model("small.en")  # You can choose 'small', 'medium', or 'large'

# Function to transcribe audio from bytes (wav or mp3)
def transcribe_with_whisper(audio_bytes):
    # Save the audio_bytes to a temporary file
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_bytes)

    # Load the audio file
    result = model.transcribe("temp_audio.wav")
    return result["text"]

# Streamlit app
def main():
    st.title("Disha - IIITN Chatbot")
    st.markdown("*A chatbot guiding IIIT Nagpur users with direction and information.*")

    # Initialize session state for conversation history
    if "history" not in st.session_state:
        st.session_state.history = []

    # Display chat history above input (with a placeholder for smooth rendering)
    chat_container = st.empty()

    # Audio recording section and input field will be at the bottom
    col1, col2 = st.columns([1, 7])  # Create two columns, one for the input and one for the button

    # Audio recorder icon (speech icon in the first column)
    with col1:
        # Custom audio recording button
        audio_bytes = audio_recorder(key="audio_recorder_no_text")

    # Input text field (in the second column)
    with col2:
        text_input = st.chat_input("Ask a question...")

    user_input = None
    # Handle voice input (only if audio is recorded)
    if audio_bytes:
        user_input = transcribe_with_whisper(audio_bytes)
        # Reset audio bytes after processing
        audio_bytes = None

    # Handle text input
    if text_input:
        user_input = text_input

    # If there is any user input (audio or text)
    if user_input:
        # Append user message to history
        st.session_state.history.append({"role": "user", "content": user_input})

        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        pineconekey = os.getenv("PINECONE_API_KEY")
        pc = Pinecone(api_key=pineconekey)
        index_name = "iiitn"

        docsearch = PC.from_existing_index(index_name=index_name, embedding=embeddings)
        
        prompt_template=""" 
            You are an intelligent assistant designed to provide accurate and helpful information.  
            You must strictly adhere to the following rules:  
            1. Use the provided context to answer the user's question.  
            2. If you don't know the answer, just say "Sorry Try again with another command or try using other option (voice/text)", don't try to make up an answer.
            3. Keep your responses concise and focused.  
            4. Ensure your answers are user-friendly and directly address the question. 
             
            Context: {context}  
            Question: {question}  
            Helpful answer: """
        
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

        llm = ChatGoogleGenerativeAI(model="models/gemini-1.0-pro", temperature=0.9)

        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=docsearch.as_retriever(search_kwargs={'k': 3}),
            return_source_documents=True,
            chain_type_kwargs={
                "prompt": PROMPT # Passing ModelQA as input
            }
        )

        result = qa({"query": user_input})

        # Append bot response to history
        st.session_state.history.append({"role": "bot", "content": result["result"]})

    # Display conversation history in reverse order with user-bot pairs
    if st.session_state.history:
        for i in range(len(st.session_state.history)-1, -1, -1):
            message = st.session_state.history[i]
            
            # Display user message first
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            
            # Display bot message next
            if message["role"] == "bot":
                with st.chat_message("bot"):
                    st.write(message["content"])

if __name__ == "__main__":
    main()
