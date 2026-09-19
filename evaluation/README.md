# Evaluation

Work on evaluating LLM systems.

## [deepeval/](deepeval/)

DeepEval — an open-source framework for testing LLMs with unit-test-style metrics, end-to-end and component-level evaluation, and built-in safety/red-teaming tools.

- [README.md](deepeval/README.md) — overview of DeepEval: metrics, goldens, datasets, synthesizer.
- `custom_models.py` — wrappers for using a self-hosted OpenAI-compatible model and a local embedding model as DeepEval's judge and embedder.
- `synthetic_dataset_generate.py` — a thin `Synthesizer` wrapper for generating goldens from documents.
- `deepeval_test.ipynb` — end-to-end run: generate goldens from a document, save them.
- `how_synthetic_works.ipynb` — walkthrough of the synthesis pipeline step by step.
- `synthetic_dataset_notebook.ipynb` — fuller annotated run with logging and dataframe inspection.

Notebooks read source documents from [`../../Datasets/`](../Datasets/) and import the shared model connector via `from utils.llm_con import get_chat_openai`, so run them with the repository root on your Python path.
