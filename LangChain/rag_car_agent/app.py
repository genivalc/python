# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import logging
from typing import Dict, Any

from data_ingestion import PDFProcessor
from retriever import VectorStoreManager, RetrieverAgent
from generator import GeneratorAgent
from utils import setup_logging
from config import config

# Modelos Pydantic
class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str
    sources: list[str]
    context_used: bool

# Variáveis globais para os agentes
retriever_agent = None
generator_agent = None
logger = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    global retriever_agent, generator_agent, logger
    
    # Inicialização
    logger = setup_logging()
    logger.info("🚀 Iniciando RAG Car Agent API")
    
    try:
        # 1. Processamento de documentos
        pdf_processor = PDFProcessor()
        documents = pdf_processor.load_and_process(config.PDF_PATH)
        
        # 2. Criação/carregamento do vector store
        vector_manager = VectorStoreManager()
        vectorstore = vector_manager.create_or_load(documents, force_rebuild=False)
        
        # 3. Inicialização dos agentes RAG
        retriever_agent = RetrieverAgent(vectorstore)
        generator_agent = GeneratorAgent(retriever_agent)
        
        logger.info("✅ Sistema RAG inicializado com sucesso")
        
        yield
        
    except Exception as e:
        logger.error(f"❌ Erro na inicialização: {e}")
        raise
    
    # Cleanup (se necessário)
    logger.info("🔄 Finalizando aplicação")

# Criação da aplicação FastAPI
app = FastAPI(
    title="RAG Car Agent API",
    description="Sistema RAG especializado em consultas automotivas",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """Endpoint de status"""
    return {"message": "🚗 RAG Car Agent API - Especialista Automotivo"}

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest) -> QuestionResponse:
    """Processa pergunta usando arquitetura RAG"""
    global generator_agent, logger
    
    if generator_agent is None:
        raise HTTPException(status_code=503, detail="Sistema ainda não inicializado")
    
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Pergunta não pode estar vazia")
    
    try:
        logger.info(f"📝 Processando pergunta: {request.question}")
        
        # Gera resposta usando arquitetura RAG
        resultado = generator_agent.generate_response(request.question)
        
        logger.info(f"✅ Resposta gerada com {len(resultado['sources'])} fontes")
        
        return QuestionResponse(
            answer=resultado['answer'],
            sources=resultado['sources'],
            context_used=resultado['context_used']
        )
        
    except Exception as e:
        logger.error(f"❌ Erro ao processar pergunta: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
