# research-lab

GenAI engineer moving into alignment research — this is where my research, experiments, and notes live.

## Sections

| Section | Status | What's there |
|---|---|---|
| [evaluation/](evaluation/) | ✅ | LLM evaluation with DeepEval — custom model wrappers, synthetic golden generation, notebooks |
| [paper-notes/](paper-notes/) | ✅ | LLM-as-a-Judge deep dive and mindmap, plus the papers behind them |
| [roadmap/](roadmap/) | 🟡 | Long-form notes: memory systems in AI, AI red-teaming & pentesting roadmap |
| [Datasets/](Datasets/) | ✅ | Sample documents and generated goldens used by the evaluation work |
| [utils/](utils/) | ✅ | Shared helpers — currently the OpenAI-compatible chat model connector |
| Agents | ⏳ | Multi-agent systems with LangGraph |
| Graph RAG | ⏳ | LLM-driven knowledge-graph extraction with Neo4j |
| RL | ⏳ | Reinforcement learning for language models |
| Alignment | ⏳ | Alignment research notes and experiments |

Planned sections have no folder yet — they appear here first and get a directory once there's real content.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # then fill in your model, API key, and base URL
```

Notebooks import shared helpers as `from utils.llm_con import get_chat_openai`, so run them with the repository root on your Python path.

## License

MIT
