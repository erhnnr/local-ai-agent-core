from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agents.agent_core import DecisionAgent
from src.adapters.huggingface_client import HuggingFaceClient
from src.database.db_manager import DatabaseManager
from src.logger import setup_logger

# Servis Loglayıcısı ve Veritabanı
logger = setup_logger("FastAPI_Server")
db = DatabaseManager()

# LLM İstemcisi ve Ajanı Başlatma
try:
    llm_client = HuggingFaceClient()
except Exception:
    from src.adapters.mock_client import MockClient
    llm_client = MockClient()

agent = DecisionAgent(llm_client=llm_client)


# FastAPI Uygulaması
app = FastAPI(
    title="Local AI Agent Core API",
    description="Otonom ajan çekirdeği için RESTful servis katmanı.",
    version="1.0.0"
)

# İstek ve Yanıt Veri Modelleri (Pydantic Validation)
class PromptRequest(BaseModel):
    prompt: str

class PromptResponse(BaseModel):
    response: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "Otonom Ajan API servisi çalışıyor."}

@app.post("/chat", response_model=PromptResponse)
def chat_with_agent(request: PromptRequest):
    try:
        logger.info(f"API üzerinden istek alındı: {request.prompt}")
        response_text = agent.run(request.prompt)
        return {"response": response_text}
    except Exception as e:
        logger.error(f"API hata oluştu: {e}")
        raise HTTPException(status_code=500, detail=str(e))