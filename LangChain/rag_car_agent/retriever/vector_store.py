import os
from typing import List
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import config

class VectorStoreManager:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(model=config.EMBEDDING_MODEL)
        self.vectorstore = None
    
    def create_or_load(self, documents: List[Document], force_rebuild: bool = False) -> FAISS:
        """Cria ou carrega vectorstore existente"""
        if os.path.exists(config.VECTORSTORE_DIR) and not force_rebuild:
            print(f"🔁 Carregando vectorstore existente")
            self.vectorstore = FAISS.load_local(
                config.VECTORSTORE_DIR, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
        else:
            print(f"🔎 Criando novo vectorstore")
            self.vectorstore = FAISS.from_documents(documents, self.embeddings)
            self._save_vectorstore()
        
        return self.vectorstore
    
    def _save_vectorstore(self):
        """Salva vectorstore no disco"""
        os.makedirs(os.path.dirname(config.VECTORSTORE_DIR), exist_ok=True)
        self.vectorstore.save_local(config.VECTORSTORE_DIR)
        print(f"💾 Vectorstore salvo em {config.VECTORSTORE_DIR}")
    
    def get_vectorstore(self) -> FAISS:
        """Retorna vectorstore atual"""
        if self.vectorstore is None:
            raise ValueError("Vectorstore não foi inicializado")
        return self.vectorstore