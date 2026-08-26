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
        
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    splits = text_splitter.split_documents(docs)
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 4})
