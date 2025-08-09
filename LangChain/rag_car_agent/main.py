from data_ingestion import PDFProcessor
from retriever import VectorStoreManager, RetrieverAgent
from generator import GeneratorAgent
from utils import setup_logging
from config import config

def main():
    # Setup logging
    logger = setup_logging()
    logger.info("🚀 Iniciando RAG Car Agent")
    
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
        
        # 4. Loop interativo
        print("\n🚗 RAG Car Agent - Especialista Automotivo")
        print("Digite suas perguntas sobre carros e manutenção!")
        print("(Digite 'sair' para encerrar)\n")
        
        while True:
            pergunta = input("❓ Sua pergunta: ")
            
            if pergunta.lower() in ["sair", "exit", "quit"]:
                print("👋 Até logo!")
                break
            
            if not pergunta.strip():
                continue
            
            # Gera resposta usando arquitetura RAG
            resultado = generator_agent.generate_response(pergunta)
            
            print(f"\n🤖 Resposta: {resultado['answer']}")
            
            if resultado['context_used']:
                print(f"\n📚 Fontes: {', '.join(resultado['sources'])}")
            
            print("-" * 50)
    
    except Exception as e:
        logger.error(f"❌ Erro: {e}")
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()