from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI

def criar_agente_com_tool(tool):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", temperature=0.3)

    # Define a regra de especialização do agente
    prompt = """
Você é um especialista automotivo. 
Responda apenas a perguntas sobre carros, mecânica, manutenção ou manuais automotivos. 
Se a pergunta não for relacionada a esse tema, diga educadamente que não pode responder.
"""

    return initialize_agent(
        tools=[tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        agent_kwargs={"system_message": prompt}
    )
