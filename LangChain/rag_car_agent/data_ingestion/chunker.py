from typing import List
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re

class SemanticChunker:
    def __init__(self, min_chunk_size: int = 200, max_chunk_size: int = 1000, overlap: int = 100):
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
        
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Aplica chunking semântico baseado na estrutura do documento"""
        chunks = []
        
        for doc in documents:
            semantic_chunks = self._semantic_split(doc.page_content)
            
            for i, chunk_text in enumerate(semantic_chunks):
                if len(chunk_text.strip()) >= self.min_chunk_size:
                    chunk = Document(
                        page_content=chunk_text,
                        metadata={
                            **doc.metadata,
                            "chunk_id": i,
                            "chunk_type": "semantic"
                        }
                    )
                    chunks.append(chunk)
        
        return chunks
    
    def _semantic_split(self, text: str) -> List[str]:
        """Divide texto baseado em estruturas semânticas"""
        # Padrões para identificar estruturas semânticas
        section_pattern = r'\n\s*(?:\d+\.|\w+\.|\•|\-)\s+'
        paragraph_pattern = r'\n\s*\n'
        
        # Primeiro, tenta dividir por seções
        sections = re.split(section_pattern, text)
        
        chunks = []
        for section in sections:
            if len(section) <= self.max_chunk_size:
                chunks.append(section.strip())
            else:
                # Se seção muito grande, divide por parágrafos
                paragraphs = re.split(paragraph_pattern, section)
                current_chunk = ""
                
                for para in paragraphs:
                    if len(current_chunk + para) <= self.max_chunk_size:
                        current_chunk += para + "\n\n"
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = para + "\n\n"
                
                if current_chunk:
                    chunks.append(current_chunk.strip())
        
        # Fallback para chunking tradicional se necessário
        final_chunks = []
        for chunk in chunks:
            if len(chunk) > self.max_chunk_size:
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=self.max_chunk_size,
                    chunk_overlap=self.overlap
                )
                sub_chunks = splitter.split_text(chunk)
                final_chunks.extend(sub_chunks)
            else:
                final_chunks.append(chunk)
        
        return final_chunks