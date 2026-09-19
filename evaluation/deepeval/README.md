# DeepEval: Comprehensive Overview

## Introduction

DeepEval is an open‑source evaluation framework tailored for large language models (LLMs). It brings the discipline of software engineering—such as unit testing, continuous integration/continuous deployment (CI/CD), and performance monitoring—into the AI domain. By providing structured tests, clear metrics, and automated reporting, DeepEval helps teams verify model behavior, track improvements, and ensure reliability every step of the way.

## What Is DeepEval?

DeepEval treats LLMs like software: instead of manually sampling outputs, it lets you define precise test cases and metrics. Each test evaluates a specific model behavior—for example, factual accuracy, relevance, or ethical compliance—and returns a numerical score. Over time, these scores form a clear record of your model’s strengths and areas for improvement.

## Core Principles

* **Unit-Test Style**: Write isolated checks for discrete behaviors (e.g., “Does the model answer fact-based questions correctly?”).
* **CI/CD Integration**: Incorporate evaluations into your development pipeline to catch regressions before they reach production.
* **Automated Monitoring**: Continuously track model performance using preconfigured dashboards and alerts.
* **Reproducibility**: Ensure every test run is identical, enabling consistent comparisons across model versions.

## Key Features

1. **Extensive Metrics Library**
   Over 30 built‑in, research‑backed measures covering accuracy, relevance, coherence, toxicity, and more. Metrics are customizable to domain‑specific requirements.

2. **Flexible Evaluation Scopes**

    * **End-to-End**: Validate complete workflows, such as retrieval-augmented generation (RAG) pipelines or multi-turn dialogues.
    * **Component-Level**: Isolate and test individual modules—retrievers, generators, summarizers, or tool-invoking agents.

3. **Synthetic Data Generation**
   Automatically create and evolve edge‑case test examples, ensuring comprehensive coverage without manual data curation.

4. **Scalability & Performance**
   Support for parallel test execution and seamless integration into CI/CD pipelines, delivering fast feedback on large test suites.

5. **Centralized Reporting**
   Visual dashboards via the Confident AI platform enable regression tracking, collaborative review, and alerting on performance deviations.

6. **Safety & Red‑Teaming**
   With the companion DeepTeam package, perform adversarial “red‑team” exercises to expose biases, toxicity, prompt injections, and security vulnerabilities.



## Goldens & Datasets

Before diving into evaluation runs, it’s crucial to understand how DeepEval modularizes your tests. By treating each scenario as a **Golden** and grouping them into **Datasets**, you gain fine-grained control over test definitions, versioning, and experiment scope. For example, you might maintain separate Datasets for “factual QA,” “customer support flows,” and “API-driven data lookup,” all while reusing common Goldens across them.

DeepEval’s evaluation workflow pivots on two key concepts:

- **Goldens**: Lightweight “pending test cases” that define only the **input** (or high-level **scenario**) and the **expected outcome**—no dynamic artifacts.  
- **Datasets**: Ordered collections of Goldens that you group together for a full evaluation run, ensuring consistent execution order, manifest versioning, and easy regression comparisons.

By separating **definition** (Goldens) from **execution** (Test Cases), you:

1. **Maintain Clean Specs**  
   Only the essential inputs/outcomes live in your repository, decoupled from runtime logs or outputs.  
2. **Guarantee Reproducibility**  
   Each Golden’s static manifest can be checksum-verified, so identical inputs always produce identical Test Case structures.  
3. **Enable Full Traceability**  
   DeepEval’s runtime harness fills in actual outputs, retrieval contexts, and tool calls automatically, producing audit-ready records without manual logging.

---

### 📑 Understanding the Golden Structure

A **Golden** is the atomic unit of your evaluation suite. It’s a Pydantic model capturing exactly what you need to test—nothing more, nothing less. Think of it as the blueprint for a Test Case, with runtime details deferred until execution.

Each Golden includes:

**Core fields:**  
- **input** (or **scenario** for multi-turn flows) — the prompt, query, or high-level user goal.  
- **expected_output** (or **expected_outcome**) — the reference answer or final dialogue goal.

**Optional metadata:**  
- **context** paragraphs or document snippets to ground complex prompts.  
- **expected_tools** specifying which external APIs or functions the LLM should invoke.  
- **tags**, **comments**, and **additional_metadata** for slicing results, advanced reporting, and integration with dashboards.

**Dynamic fields (populated at runtime):**  
- **actual_output**: the text the LLM generated.  
- **retrieval_context**: any documents, embeddings, or tool outputs the model consulted.  
- **tools_called**: the sequence of external calls or plugin invocations.

> **Advanced Note:**  
> - You can extend the Pydantic schema to include custom validation rules (e.g., enforce that `expected_tools` matches your API spec).  
> - Leverage JSON Schema exports to integrate Golden validation into pre-commit hooks or CI pipelines, preventing malformed test definitions from slipping through.

#### Example Golden Data

Here’s an example of a single-turn Golden in JSON/YAML format:

```json
{
  "input": "Translate the following sentence into French: 'The quick brown fox jumps over the lazy dog.'",
  "expected_output": "Le renard brun rapide saute par-dessus le chien paresseux.",
  "context": [
    "User requests a translation service.",
    "Source language: English; Target language: French."
  ],
  "expected_tools": []
}
````

Or in YAML:

```yaml
input: "Translate the following sentence into French: 'The quick brown fox jumps over the lazy dog.'"
expected_output: "Le renard brun rapide saute par-dessus le chien paresseux."
context:
  - "User requests a translation service."
  - "Source language: English; Target language: French."
expected_tools: []
```

---

### 📂 Generating a Dataset from Your DOCX (or PDF/TXT)

When you lack a hand-curated evaluation set, DeepEval’s **Synthesizer** automates dataset creation, transforming your existing documentation into a structured test suite in minutes:

1. **Document Preprocessing**

   * Native support for Word, PDF (including OCR-scanned pages), and plain text.
   * Configure **chunk\_size** (e.g., 512 tokens) and **chunk\_overlap** to balance context completeness against prompt length limits.

2. **Context Extraction & Clustering**

   * Use semantic embeddings (OpenAI, Hugging Face, or local models) to cluster related passages.
   * Employ TF-IDF and custom filters to prune boilerplate, ensuring high information density per chunk.

3. **Golden Generation**

   * For each chunk or cluster, an LLM drafts single-turn Q\&A pairs.
   * Applies **data evolution** strategies:

      * **Paraphrase augmentation** for lexical variety.
      * **Adversarial rewrites** to surface edge-case phrasings.
      * **Difficulty scaling** (fact retrieval → inference → multi-hop reasoning).

4. **Quality Filtering & Sampling**

   * Deduplicate semantically similar pairs using clustering or cosine similarity thresholds.
   * Filter by answer length, question complexity, or model confidence scores to meet your coverage vs. speed tradeoff.

5. **Dataset Assembly**

   * Batches validated Goldens into a Dataset object with manifest, metadata, and checksums.
   * Exports to JSON/YAML or pushes directly into your CI/CD pipeline.

*No manual tagging or spreadsheets—your DOCX/PDF files become a high-coverage, versionable test suite.*

---

## Synthesizer: Rapid Single-Turn Generation

The **Synthesizer** isn’t just a simple Q\&A generator—it’s a full data pipeline with pluggable stages and advanced controls:

1. **From Documents**

   * Full end-to-end: raw files → chunking → clustering → Q\&A pairs.

2. **From Prepared Contexts**

   * Inject your own context list (e.g., search-retrieved snippets) to focus tests on mission-critical content.

3. **From Scratch**

   * Define prompt templates or scenarios; the LLM invents both questions and answers, useful for zero-data bootstrapping.

4. **By Augmenting Existing Goldens**

   * Seed with small, human-curated Goldens and exponentially expand via paraphrasing, adversarial noise injection, and difficulty layering.

> **Pro Tips:**
>
> * Tune generation hyperparameters (temperature, top-p, max tokens) per stage to balance creativity vs. factuality.
> * Leverage batch processing and parallel API calls to scale to thousands of Goldens.
> * Integrate custom filters (bias, profanity, domain-specific validation) as post-processing hooks.

---

## ConversationSimulator: Scalable Multi-Turn Testing

For real-world dialogue scenarios, ConversationSimulator orchestrates dynamic, multi-turn exchanges:

* **Define High-Level Scenarios**
  E.g., “User wants to open a bank account,” plus profile attributes (KYC fields, tone preferences).

* **Turn-By-Turn Simulation**
  Alternating **user\_message** and **expected\_assistant\_message** entries, generated via model callbacks, until a stopping criterion (e.g., “Account opened”) is met.

* **Edge-Case Injection**
  Randomly introduce typos, intent pivots, or context resets to stress-test fallback logic and error handling.

* **Export ConversationalTestCases**
  Ready for evaluation with metrics like dialogue success rate, turn efficiency, context retention, and user satisfaction proxies.

---

## Results & Benefits

By combining Goldens, Datasets, Synthesizer, and ConversationSimulator, you achieve:

* **Speed:** Zero to 300+ Goldens in <10 minutes, including end-to-end dataset build.
* **Coverage:** Mix of fact checks, adversarial edge cases, and multi-turn flows ensures comprehensive testing.
* **Insights:** Automated metrics (Accuracy, BLEU, F1, coherence), metadata-driven slicing (by domain, complexity), and performance telemetry (latency, resource usage).

---

## Golden Data Model & Best Practices

* **Core fields:** `input/scenario` + `expected_output/outcome`
* **Metadata:** `context`, `expected_tools`, `tags`, `comments`, `additional_metadata`
* **Dynamic fields:** `actual_output`, `retrieval_context`, `tools_called` (runtime-populated)
* **Dataset sizing:** 100–500 Goldens per run for optimal CI latency vs. statistical power
* **Ordering & Versioning:** Immutable order and manifest checksums for accurate regression tracking and drift detection
* **Schema Validation:** Enforce via Pydantic or JSON Schema in pre-commit hooks and CI pipelines

---



*Next time, we will make a dataset for evaluation from DOCX files.*

