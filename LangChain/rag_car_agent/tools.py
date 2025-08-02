from langchain.tools import Tool
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

def criar_ferramenta_de_busca(vectorstore):
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", temperature=0.3)
    
    prompt = ChatPromptTemplate.from_template("""
    Responda a pergunta baseado no contexto fornecido:
    
    {context}
    
    Pergunta: {input}
    """)
    
    document_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, document_chain)

    return Tool(
        name="ManualAutomotivoTool",
        func=lambda query: chain.invoke({"input": query})["answer"],
        description="Usado para responder perguntas sobre carros, mecânica, manutenção e manuais automotivos."
    )