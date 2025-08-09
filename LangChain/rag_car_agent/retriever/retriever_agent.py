from typing import List, Dict, Any
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from config import config

class RetrieverAgent:
    def __init__(self, vectorstore: FAISS):
        self.vectorstore = vectorstore
        self.retriever = vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": config.RETRIEVAL_K,
                "score_threshold": config.SIMILARITY_THRESHOLD
            }
        )
    
    def retrieve_context(self, query: str) -> List[Document]:
        """Recupera documentos relevantes para a query"""
        print(f"🔍 Buscando contexto para: {query[:50]}...")
        
        # Busca por similaridade
        relevant_docs = self.retriever.get_relevant_documents(query)
        
        # Filtra e ranqueia resultados
        filtered_docs = self._filter_and_rank(relevant_docs, query)
        
        print(f"📋 Encontrados {len(filtered_docs)} páginas relevantes") 

        return filtered_docs
    
    def _filter_and_rank(self, docs: List[Document], query: str) -> List[Document]:
        """Filtra e ranqueia documentos por relevância"""
        # Remove duplicatas baseado no conteúdo
        unique_docs = []
        seen_content = set()
        
        for doc in docs:
            content_hash = hash(doc.page_content[:100])
            if content_hash not in seen_content:
                seen_content.add(content_hash)
                unique_docs.append(doc)
        
        return unique_docs[:config.RETRIEVAL_K]
    
    def get_context_string(self, query: str) -> str:
        """Retorna contexto como string formatada"""
        docs = self.retrieve_context(query)
        
        context_parts = []
        for doc in docs:
            page_num = doc.metadata.get('page', 'N/A')
            context_parts.append(f"[Página {page_num + 1}]\n{doc.page_content}\n")
    
        return "\n".join(context_parts)