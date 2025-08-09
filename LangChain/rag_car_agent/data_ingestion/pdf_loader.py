import os
from typing import List
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader
from .chunker import SemanticChunker
from config import config

class PDFProcessor:
    def __init__(self):
        self.chunker = SemanticChunker(
            min_chunk_size=config.MIN_CHUNK_SIZE,
            max_chunk_size=config.MAX_CHUNK_SIZE,
            overlap=config.CHUNK_OVERLAP
        )
    
    def load_and_process(self, pdf_path: str) -> List[Document]:
        """Carrega PDF e aplica chunking semântico"""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF não encontrado: {pdf_path}")
        
        print(f"📄 Carregando PDF: {pdf_path}")
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        
        print(f"✂️ Aplicando chunking semântico")
        chunks = self.chunker.chunk_documents(documents)
        
        print(f"📊 Gerados {len(chunks)} chunks semânticos")
        return chunks