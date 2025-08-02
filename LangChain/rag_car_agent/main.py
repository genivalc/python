# main.py

from utils import carregar_pdf_e_criar_vectorstore
from tools import criar_ferramenta_de_busca
from agent import criar_agente_com_tool

if __name__ == "__main__":
    # Configurações
    pdf_path = "./data/argo_2023.pdf"
    vectorstore_dir = "./vectorstore/argo"
    chunk_size = 800
    chunk_overlap = 100
    k = 5
    force_rebuild = False  # Coloque True se quiser recriar embeddings
    # Passo 1: Carregar vetor
    vectorstore = carregar_pdf_e_criar_vectorstore(
        pdf_path,
        vectorstore_dir=vectorstore_dir,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        force_rebuild=force_rebuild
    )
    
    # # Passo 2: Criar tool a partir do vetor
    tool = criar_ferramenta_de_busca(vectorstore)
    
    # # Passo 3: Criar agente com a tool e regras
    agente = criar_agente_com_tool(tool)

    # Passo 4: Testar perguntas
    while True:
        pergunta = input("\nDigite sua pergunta (ou 'sair' para encerrar): ")
        if pergunta.lower() in ["sair", "exit", "quit"]:
            break
        output = agente.invoke({"input": pergunta})
        print("\nResposta:", output)

      



# ✅ Multi-documentos: suporte a múltiplos manuais de diferentes modelos/marcas.

# 🧾 Metadata nos chunks: salvar modelo/ano nas metadatas para filtro inteligente.

# 🌍 Interface web: integrar com Streamlit ou FastAPI.

# 🧪 Avaliação RAG: implemente LangChain Eval para medir a qualidade das respostas.

# 🔒 Controle de domínio por LLM: combine regras com classificadores de tópico.