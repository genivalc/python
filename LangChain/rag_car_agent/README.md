# 🚗 RAG Car Agent - Automotive Specialist

Advanced RAG (Retrieval-Augmented Generation) system for automotive queries with hybrid search, semantic chunking and modular architecture.

## 🎯 Key Features

- 🔍 **Hybrid Search**: Semantic + keyword + term expansion
- 🧠 **Smart Chunking**: Preserves automotive context
- 🌐 **Web Fallback**: External search when needed
- 📊 **REST API**: Complete FastAPI interface
- 🔧 **Configurable**: Adjustable parameters
- 📝 **Traceable**: Sources and detailed logs

## 🏗️ Architecture


rag_car_agent/
├── data_ingestion/ # Document processing
│ ├── pdf_loader.py # Optimized PDF loading
│ └── chunker.py # Automotive semantic chunking
├── retriever/ # Hybrid retrieval system
│ ├── vector_store.py # FAISS management
│ └── retriever_agent.py # Semantic + keyword search
├── generator/ # Response generation
│ └── generator_agent.py # LLM + traceability
├── utils/ # Utilities
│ ├── logging_utils.py # Logging system
│ └── web_search.py # Web search (DuckDuckGo)
├── data/ # PDF documents
├── vectorstore/ # FAISS indices
├── logs/ # Application logs
├── app.py # FastAPI app
├── config.py # Configuration
└── requirements.txt # Dependencies


## 🚀 Installation and Usage

### 1. **Clone and Install**
```
git clone <repo-url>
cd rag_car_agent
pip install -r requirements.txt


2. Configure Environment
# Create .env file
echo "GOOGLE_API_KEY=your_key_here" > .env



3. Add Documents
# Place PDFs in data/ folder
cp car_manual.pdf data/



4. Run API
# Development
python app.py

# Production
uvicorn app:app --host 0.0.0.0 --port 8000



5. Test
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "How to adjust the steering wheel?"}'



📡 API Endpoints
Endpoint	Method	Description
/	GET	API status
/health	GET	Health check
/ask	POST	Ask question
Response Example
{
  "answer": "Para regular o volante do Fiat Argo...",
  "sources": ["Page 45", "Page 67"],
  "context_used": true
}


json
⚙️ Configuration
Adjust parameters in config.py:

# Chunking
MIN_CHUNK_SIZE: int = 200
MAX_CHUNK_SIZE: int = 1000
CHUNK_OVERLAP: int = 150

# Retrieval
RETRIEVAL_K: int = 5
SIMILARITY_THRESHOLD: float = 0.5  # Reduced for better recall

# Models
LLM_MODEL: str = "gemini-2.0-flash-lite"
EMBEDDING_MODEL: str = "models/embedding-001"


python
🔍 Hybrid Search System
1. Semantic Search
Embeddings with Google Generative AI

Configurable similarity threshold

Relevance filtering

2. Term Expansion
"steering" → ["wheel", "column", "adjustment"]
"adjust" → ["configure", "position", "calibrate"]


3. Keyword Search
Reduced threshold (0.3)

Manual relevance filtering

Robust fallback

4. Web Search
DuckDuckGo Search

Expanded automotive terms

Final fallback

📊 Monitoring
Structured Logs
2025-08-09 16:18:46 - INFO - 📝 Processing question: How to adjust steering wheel?
2025-08-09 16:18:47 - WARNING - No relevant docs (threshold 0.7)
2025-08-09 16:18:48 - INFO - 🌐 Searching web...
2025-08-09 16:18:49 - INFO - ✅ Response generated with 3 sources


Health Check
curl http://localhost:8000/health
# {"status": "healthy", "message": "RAG system operational"}



🛠️ Development
Test Structure
# Run tests
pytest tests/

# Coverage
pytest --cov=. tests/



Add New Documents
Place PDF in data/

Restart application (auto rebuild)

Test with specific questions

Adjust Threshold
# For specific documents
SIMILARITY_THRESHOLD = 0.3  # More permissive

# For generic documents  
SIMILARITY_THRESHOLD = 0.7  # More restrictive


🔧 Troubleshooting
Problem: "No relevant docs retrieved"
Solution : Reduce SIMILARITY_THRESHOLD in config.py

Problem: Generic responses
Solution : Check if PDF is in data/ and vectorstore was created

Problem: API not responding
Solution : Check GOOGLE_API_KEY in .env

📈 Roadmap
 Multi-language support
 Response caching
 Web interface
 Performance metrics
 More format support (DOCX, TXT)
 Image/diagram search
📄 License
MIT License - see LICENSE for details.

🤝 Contributing
Fork the project

Create branch ( git checkout -b feature/new-feature)

Commit ( git commit -m 'Add new feature')

Push ( git push origin feature/new-feature)

Open Pull Request