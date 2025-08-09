from duckduckgo_search import DDGS
from typing import List, Dict
import time
import requests

class WebSearchAgent:
    def __init__(self):
        self.ddgs = DDGS()
    
    def search_automotive(self, query: str, max_results: int = 3) -> List[Dict]:
        """Busca informações automotivas na web"""
        automotive_query = f"{query} manual carro automotivo manutenção"
        
        try:
            time.sleep(1)
            results = list(self.ddgs.text(
                automotive_query, 
                max_results=max_results,
                region='br-pt'
            ))
            return results
        except Exception as e:
            print(f"Busca web indisponível: {e}")
            # Fallback: resposta genérica
            return [{
                'title': 'Informação não encontrada',
                'body': 'Não foi possível buscar informações adicionais na web no momento. Tente novamente mais tarde.'
            }]
    
    def format_web_results(self, results: List[Dict]) -> str:
        """Formata resultados da web"""
        if not results:
            return ""
        
        formatted = "INFORMAÇÕES DA WEB:\n"
        for i, result in enumerate(results, 1):
            formatted += f"[Web {i}] {result.get('title', '')}\n"
            formatted += f"{result.get('body', '')}\n\n"
        
        return formatted
