import os
import streamlit as st
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(page_title="Accounting AI Agent", page_icon="📊")
st.title("📊 Enterprise Accounting & Tax AI Assistant")

# 1. API Key Setup
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
if not api_key:
    st.info("Please add your free Google Gemini API key in the sidebar to begin.")
    st.stop()

# 2. Dynamic Repository File Loader
@st.cache_resource
def initialize_knowledge_base():
    docs = []
    kb_dir = "./knowledge_base/"
    
    if os.path.exists(kb_dir):
        # Load PDF files
        pdf_loader = DirectoryLoader(kb_dir, glob="**/*.pdf", loader_cls=PyPDFLoader)
        docs.extend(pdf_loader.load())
        
        # Load TXT files
        txt_loader = DirectoryLoader(kb_dir, glob="**/*.txt", loader_cls=TextLoader)
        docs.extend(txt_loader.load())
        
        # Load CSV files
        csv_loader = DirectoryLoader(kb_dir, glob="**/*.csv", loader_cls=CSVLoader)
        docs.extend(csv_loader.load())

    if not docs:
        st.warning("No files found in /knowledge_base/. Upload PDF, TXT, or CSV files to GitHub.")
        st.stop()
        
    # Chunk long documents into digestible contexts
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    splits = text_splitter.split_documents(docs)
    
    # Embed text using a lightweight model running on free CPU resources
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 4})

# 3. Setup Accounting RAG Chain
retriever = initialize_knowledge_base()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key, temperature=0.1)

system_prompt = (
    "You are an expert CPA and financial consultant specialized in US GAAP, IFRS, "
    "IRS Regulations, and Sarbanes-Oxley (SOX) compliance.\n"
    "Use the following pieces of retrieved context to answer the user's question. "
    "If you do not know the answer or if it falls outside accounting/tax scope, state that clearly.\n"
    "Always cite relevant accounting standard codes (e.g., ASC 606, IFRS 15, Internal Revenue Code) where applicable.\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# 4. Interactive Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask about revenue recognition, tax treatment, SOX controls..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response = rag_chain.invoke({"input": user_input})
        answer = response["answer"]
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
