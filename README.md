# **Disha - Chatbot IIIT Nagpur**

Welcome to the Disha Chatbot GitHub repository! This project is an innovative solution designed to streamline the user experience for navigating the IIIT Nagpur website. Built with cutting-edge Machine Learning (ML), Natural Language Processing (NLP), and Large Language Models (LLMs), Disha provides instant, user-friendly responses to a variety of queries.

---

## **Features**

### **Human-like Interaction**
- Enables natural and intuitive conversations.
- Provides accurate and contextual answers to queries about IIIT Nagpur.

### **Voice Input**
- [OpenAI - Whisper-small-en](https://huggingface.co/openai/whisper-small.en)

### **Data Processing and Structuring**
- Extracts text and images from IIIT Nagpur’s website using OCR.
- Structures data into a comprehensive JSON format for training.

### **Unified and Accurate Responses**
- Combines fine-tuned LLMs and Retrieval-Augmented Generation (RAG) for precise answers.
- Responses are verified for maximum reliability.

### **Evaluation Metrics**
- Measures output quality using BLEU, ROUGE-L, Semantic Similarity, and Human Score metrics.

---

## **Key Technologies**

### **Machine Learning Models**
- **LLaMA-3.2-1B**: Fine-tuned with rank values R-8, R-16, R-32, and Phi-3.5.
- **Phi-3.5-mini**
- **PEFT Techniques**: Efficient fine-tuning with LoRA and QLoRA.

### **Retrieval-Augmented Generation (RAG)**
- Retrieves accurate, contextually relevant data from external databases.
- Utilizes:
  - **Pinecone**: Vector database for optimized search and retrieval.
  - **LangChain**: For seamless data pipelines.
  - **Google Gemini API**: Provides accurate, summarized answers.

---

## **Evaluation Metrics Table**

| **Model**           | **BLEU**   | **ROUGE-L** | **Semantic Similarity** | **Human Evaluation** | **Trained Parameters** |
|----------------------|------------|-------------|--------------------------|-----------------------|-------------------------|
| LLAMA-3.2-1b (R=8)  | 0.925700   | 0.964550    | 0.998106                | 0.934744             | 12,156,928             |
| LLAMA-3.2-1b (R=16) | 0.925950   | 0.964757    | 0.998106                | 0.942012             | 24,313,856             |
| LLAMA-3.2-1b (R=32) | 0.924404   | 0.963656    | 0.998096                | 0.946338             | 48,627,712             |
| Phi 3.5 Mini         | 0.785048   | 0.886750    | 0.998205                | 0.852504             | 29,884,416             |
| RAG                  | 0.964902   | 0.996087    | 0.995800                | 0.967379             | 0                       |

---

## **Trained Models**
- LLaMA-3.2-1b r=8 [Link](https://huggingface.co/gyanbardhan123/llama-3.2-1b-r8-iiitn)
- LLaMA-3.2-1b r=16 [Link](https://huggingface.co/gyanbardhan123/llama-3.2-1b-iiitn/tree/main)
- LLaMA-3.2-1b r=32 [Link](https://huggingface.co/gyanbardhan123/llama-3.2-1b-r32-iiitn/tree/main)
- Phi-3.5-mini [Link](https://huggingface.co/gyanbardhan123/phi-3.5-mini/tree/main)

---

## **[Web Interface - Hugging Face](https://huggingface.co/spaces/gyanbardhan123/Disha_RAG)**

---

## **Architecture Overview**

### **Unified Intelligence**
- Integrates RAG and fine-tuned LLMs for robust performance.

### **Context Preservation**
- Ensures all critical details are included in responses.

### **Natural Flow**
- Delivers user-friendly, conversational interactions.

---

## **Future Plans**
- Expand language support beyond Hindi and English.
- Enhance scalability for larger datasets and more complex queries.
- Integrate additional evaluation metrics to improve accuracy.

---

Feel free to fork, contribute, and enhance Disha for broader applications!
