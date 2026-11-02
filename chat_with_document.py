# Chat with Document - Support for TXT, PDF, and DOCX

import streamlit as st
import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

st.title('💬 Chat with Document')

# File Upload (TXT, PDF, DOCX)
uploaded_file = st.file_uploader("📤 Upload a document", type=['txt', 'pdf', 'docx'])
add_file = st.button("➕ Add File")

if uploaded_file and add_file:
    # Determine file type and select loader
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    try:
        # Save to temp file because loaders need a file path
        temp_path = f"./temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Select Loader
        if file_extension == 'pdf':
            loader = PyPDFLoader(temp_path)
        elif file_extension == 'docx':
            loader = Docx2txtLoader(temp_path)
        else: # txt
            loader = TextLoader(temp_path)

        # Load and Split
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)

        # Setup Embeddings & Vector Store
        embeddings = OllamaEmbeddings(model='nomic-embed-text')
        vector_store = Chroma.from_documents(chunks, embeddings)
        retriever = vector_store.as_retriever(search_kwargs={"k":5})

        # Setup LLM & Chain
        llm = ChatOllama(model="llama3.2:3b")
        
        template = """Answer the question based ONLY on the following context. If the answer is not in the context, say 'I don't know based on the document:
        Context: {context}
        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)
        
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        # Save chain to session state
        st.session_state.chain = chain
        st.success(f'✅ {uploaded_file.name} processed! ({len(chunks)} chunks)')
        
        # Cleanup temp file
        os.remove(temp_path)
        
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        if os.path.exists(temp_path):
            os.remove(temp_path)

# Chat Interface
if 'chain' in st.session_state:
    st.divider()
    question = st.text_input('🔍 Ask a question about the document:')
    
    if question:
        with st.spinner("Thinking..."):
            try:
                chain = st.session_state.chain
                response = chain.invoke(question)
                st.markdown(f"**Answer:** {response}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Make sure Ollama is running and the models are pulled.")
else:
    st.info("👆 Please upload a TXT, PDF, or DOCX file and click 'Add File' to start.")