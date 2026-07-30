from src.agents.tools import ToolRegistry
from src.rag.vector_kb import VectorKnowledgeBase

class BaseSpecializedAgent:
    def __init__(self, name, role_prompt):
        self.name = name
        self.role_prompt = role_prompt
        self.kb = VectorKnowledgeBase()

class CoderAgent(BaseSpecializedAgent):
    def __init__(self):
        super(CoderAgent, self).__init__("CoderAgent", "Sen uzman bir yazılım geliştiricisin. Kod analizi ve dosya okuma konularında uzmansın.")

    def process(self, prompt: str) -> str:
        if "oku" in prompt.lower() or "dosya" in prompt.lower():
            # Dosya adını ayıkla
            target_file = "app.py"
            for word in prompt.split():
                if "." in word:
                    target_file = word.strip(".,'\"")
                    break
            content = ToolRegistry.execute_tool("read_local_file", target_file)
            return f"[{self.name} - Kod Analizi]:\n```python\n{content}\n```"
        return f"[{self.name}]: Kod göreviniz alındı, işleniyor."

class ArchitectAgent(BaseSpecializedAgent):
    def __init__(self):
        super(ArchitectAgent, self).__init__("ArchitectAgent", "Sen kıdemli bir sistem mimarısın. ADR ve mimari kararlarda uzmansın.")

    def process(self, prompt: str) -> str:
        rag_result = self.kb.search(prompt)
        return f"[{self.name} - Mimari / ADR Analizi]:\n{rag_result}"