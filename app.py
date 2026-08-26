import streamlit as st  # MUST BE AT LINE 1
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# --- Optional fix for sqlite3 on Streamlit Cloud ---
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

# --- NOW you can use @st.cache_resource ---
@st.cache_resource
def initialize_knowledge_base():
    # Your initialization code here...
    pass
