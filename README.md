🚀 Local AI Agent Core
A lightweight, local-first multi-agent architecture powered by Ollama. Designed for privacy, modularity, and offline execution.

🌟 Vision & Architecture
local-ai-agent-core is a modular framework built to run autonomous AI agents entirely on local hardware. No cloud dependency, no data leaks, and zero API costs. It bridges the gap between general-purpose LLMs and domain-specific operations by implementing a clean Router-Agent-Tool architecture.

Core Features
🔒 100% Local & Private: Powered by Ollama (Llama 3, Mistral, etc.). Your data never leaves your machine.

🛠️ Modular Tool Registry: Easily plug in custom tools (file readers, system monitors, custom business logic).

🤝 Multi-Agent Collaboration: Specialized roles (e.g., Architect, Coder) working in tandem.

🧠 Context-Aware: Local RAG integration for analyzing documents, logs, and local databases.

🛠️ Tech Stack
Language: Python 3.10+

LLM Engine: Ollama

Architecture: Modular Agentic Core & Tool Wrapper

⚙️ Getting Started
Prerequisites
Make sure you have Ollama installed and running on your local machine.

Clone the repository:

Bash
git clone https://github.com/erhnnr/local-ai-agent-core.git
cd local-ai-agent-core
Install dependencies:

Bash
pip install -r requirements.txt
Run the core system:

Bash
python main.py
🗺️ Roadmap
[x] Core agent loop and prompt management

[x] Modular tool registry system

[ ] Advanced multi-agent conversation state machine

[ ] Optimized local RAG pipeline for enterprise documents

🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check out the issues page.

📜 License
This project is open-source and available under the MIT License.
