from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from retriever.retriever_agent import RetrieverAgent
from utils.web_search import WebSearchAgent  # ADICIONAR ESTA LINHA
from config import config

class GeneratorAgent:
    def __init__(self, retriever: RetrieverAgent):
        self.retriever = retriever 
        self.web_search = WebSearchAgent()
        self.llm = ChatGoogleGenerativeAI(
            model=config.LLM_MODEL,
            temperature=config.LLM_TEMPERATURE
        )
        self.prompt = self._create_prompt()
    
    def _create_prompt(self) -> ChatPromptTemplate:
        """Cria prompt otimizado para RAG automotivo"""
        template = """Você é um especialista automotivo altamente qualificado.

CONTEXTO RECUPERADO:
{context}

INSTRUÇÕES:
1. Responda APENAS com base no contexto fornecido acima
2. Se a informação não estiver no contexto, diga claramente que não possui essa informação
3. Seja preciso, técnico e detalhado quando apropriado
4. Cite partes específicas do contexto quando relevante
5. Mantenha foco estritamente automotivo

PERGUNTA: {question}

RESPOSTA:"""
        
        return ChatPromptTemplate.from_template(template)
    
    def generate_response(self, query: str) -> Dict[str, Any]:
        """Gera resposta baseada no contexto recuperado"""
        # Recupera contexto relevante
        context = self.retriever.get_context_string(query)
        
        if not context.strip():
            print("🌐 Buscando informações na web...")
            web_results = self.web_search.search_automotive(query)
            web_context = self.web_search.format_web_results(web_results)
            
            if web_context:
                context = web_context
                sources = [f"Web {i+1}" for i in range(len(web_results))]
                
                response = self.llm.invoke(
                    self.prompt.format_messages(context=context, question=query)
                )
                
                return {
                    "answer": response.content,
                    "context_used": True,
                    "sources": sources,
                    "search_type": "web"
                }
        
        # Gera resposta usando o LLM
        print("🤖 Gerando resposta...")
        response = self.llm.invoke(
            self.prompt.format_messages(context=context, question=query)
        )
        
        # Extrai fontes utilizadas
        sources = self._extract_sources(context)
        
        return {
            "answer": response.content,
            "context_used": True,
            "sources": sources,
            "context": context[:500] + "..." if len(context) > 500 else context
        }
    
    def _extract_sources(self, context: str) -> list:
        """Extrai informações das fontes utilizadas"""
        # Simples extração de fontes baseada nos documentos
        import re
        page_pattern = r'\[Página (\d+)\]'  # Mudança aqui
        matches = re.findall(page_pattern, context)
        return [f"Página {match}" for match in matches]