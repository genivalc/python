import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS

def carregar_pdf_e_criar_vectorstore(
    pdf_path: str,
    vectorstore_dir: str = "./vectorstore",
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
    force_rebuild: bool = False
):
    
   # Se o vetor já existir e não quiser forçar a reconstrução, carregue-o
    if os.path.exists(vectorstore_dir) and not force_rebuild:
        print(f"🔁 Carregando vectorstore existente de {vectorstore_dir}")
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        return FAISS.load_local(vectorstore_dir, embeddings, allow_dangerous_deserialization=True)

    print(f"📄 Carregando e processando PDF: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    print(f"✂️ Dividindo documento em chunks: tamanho={chunk_size}, overlap={chunk_overlap}")
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(docs)

    print("🔎 Gerando embeddings e criando vectorstore")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    print(f"💾 Salvando vectorstore em {vectorstore_dir}")
    vectorstore.save_local(vectorstore_dir)

    return vectorstore