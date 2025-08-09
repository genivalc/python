# 🚗 RAG Car Agent - Especialista Automotivo

Sistema RAG (Retrieval-Augmented Generation) otimizado para consultas automotivas com chunking semântico e arquitetura modular.

## 🏗️ Arquitetura

```
project/
├── data_ingestion/          # Processamento de documentos
│   ├── pdf_loader.py       # Carregamento otimizado de PDFs
│   └── chunker.py          # Chunking semântico inteligente
├── retriever/              # Sistema de recuperação
│   ├── vector_store.py     # Gerenciamento do vector store
│   └── retriever_agent.py  # Agente de recuperação
├── generator/              # Geração de respostas
│   └── generator_agent.py  # Agente gerador com rastreabilidade
├── utils/                  # Utilitários
│   └── logging_utils.py    # Sistema de logging
├── config.py              # Configurações centralizadas
└── main.py               # Orquestração principal
```

## ✨ Principais Melhorias

### 1. **Chunking Semântico Inteligente**
- Divisão baseada em estruturas lógicas (seções, parágrafos)
- Overlap dinâmico para preservar contexto
- Fallback para chunking tradicional quando necessário

### 2. **Arquitetura RAG Modular**
- **Retriever**: Busca inteligente com filtragem por relevância
- **Generator**: Geração baseada estritamente no contexto recuperado
- Separação clara de responsabilidades

### 3. **Configuração Centralizada**
- Parâmetros configuráveis em `config.py`
- Fácil ajuste de modelos e thresholds
- Gerenciamento de variáveis de ambiente

### 4. **Rastreabilidade**
- Fontes utilizadas na resposta
- Logging detalhado de operações
- Contexto recuperado disponível para auditoria

## 🚀 Como Usar

1. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

2. **Configurar API Key:**
```bash
# No arquivo .env
GOOGLE_API_KEY=sua_chave_aqui
```

3. **Executar:**
```bash
python main.py
```

## ⚙️ Configurações

Ajuste parâmetros em `config.py`:

```python
# Chunking
MIN_CHUNK_SIZE: int = 200
MAX_CHUNK_SIZE: int = 1000
CHUNK_OVERLAP: int = 100

# Retrieval
RETRIEVAL_K: int = 5
SIMILARITY_THRESHOLD: float = 0.7
```

## 🔧 Funcionalidades

- ✅ Chunking semântico baseado em estrutura
- ✅ Busca por similaridade com threshold
- ✅ Filtragem de duplicatas
- ✅ Rastreabilidade de fontes
- ✅ Logging estruturado
- ✅ Configuração modular
- ✅ Arquitetura escalável