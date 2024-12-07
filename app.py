import torch
import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from transformers import pipeline

st.set_page_config(page_title="Gemini_Student", page_icon=":material/edit:")
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM,AutoTokenizer

from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM,AutoTokenizer
import google.generativeai as genai
import os
from dotenv import load_dotenv
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Initialize the text-generation pipeline (without the device argument)


# Streamlit app UI
st.title("Chat with Llama Models")

def generate_chat(user_input):
    """Generate chatbot responses using the Llama model."""
    
    # Define the user input message format
    config = PeftConfig.from_pretrained("gyanbardhan123/llama-3.2-1b-iiitn")
    base_model = AutoModelForCausalLM.from_pretrained("unsloth/llama-3.2-3b-instruct-bnb-4bit")
    loc=r"C:\Users\HPC LAB\Desktop\Disha_BT21CSE194_161\lora_model"
    model = PeftModel.from_pretrained(base_model, loc)
    tokenizer = AutoTokenizer.from_pretrained("unsloth/llama-3.2-3b-instruct-bnb-4bit")
    messages = [
    {"role": "user", "content": user_input},
    ]
    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize = True,
        add_generation_prompt = True, # Must add for generation
        return_tensors = "pt",
    ).to("cuda")

    # Generate the response using the Llama model
    generated_ids = model.generate(
        input_ids=inputs,  # Ensure input_ids are sent to the correct device (CUDA)
        max_new_tokens=512,
        use_cache=True,
        temperature=0.2,
        min_p=0.1
        )

    # Decode the generated IDs to text. We need to consider the first (or relevant) output in the batch.
    generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

    
    
    return generated_text

def generate_chat_rag(user_input):
    from langchain_google_genai import ChatGoogleGenerativeAI


    from langchain import PromptTemplate
    from langchain.chains import RetrievalQA
    from langchain.vectorstores import Pinecone as PC
    import pinecone
    from pinecone import Pinecone
    from langchain.prompts import PromptTemplate
    
    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    # Load environment variables
    load_dotenv()
    if user_input:
        # Append user message to history

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
        return result


prompt_template = """
        Summarize based on Context ,Response1,Response2 
        Context: {context}
        Response1: {response1}
        Response2: {response2}
        Only return the helpful answer below and nothing else.
        Helpful answer:
        """
# Text input for user message
user_input = st.text_input("Type your message here...", key="user_input")

# Respond button to trigger the chat
if st.button("Submit"):
    if user_input:
        # Generate the response based on the user input
        response1 = generate_chat(user_input)
        response2= generate_chat_rag(user_input)
        model=genai.GenerativeModel('gemini-1.5-pro-latest')
        chat=model.start_chat(history=[])
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []
        from langchain import PromptTemplate
        context=user_input
        input = PromptTemplate(template=prompt_template, input_variables=["context", "response1","response2"])
        

        submit=st.button("Submit")

        if submit and input:


            response=chat.send_message(input,stream=True)
            st.session_state['chat_history'].append(("You", input))
            st.subheader("The Response is")
            for chunk in response:
                st.write(chunk.text)
                st.session_state['chat_history'].append(("Bot", chunk.text))


        st.subheader("The Chat History is")

        for role, text in st.session_state['chat_history']:
            st.write(f"{role}: {text}")