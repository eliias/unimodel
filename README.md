<p align="center">
  <img alt="unimodel" src="./docs/assets/logo.png" width="300" />
</p>

---

> A unified, resilient, and lightweight client for seamless multi-LLM API integration.

*unimodel* is a lightweight HTTP client for LLM APIs. It adds a couple of
useful, but unobtrusive abstractions to handle common scenarios.

The primary use  case is to allow application developers to easily switch 
between the various vendors and models in their applications.

## Usage

```bash
pip install unimodel

touch .env && "OPENAI_API_KEY=${OPENAI_API_KEY}" >> ".env"
```

## Example

```python
from unimodel import Client

client = Client()
# Use the Chat API, prefer OpenAI/GPT-4o, if it fails,
# fallback to Anthropic/Claude-3.5-Sonnet
response = client.chat.completions.create(
    models=[
        "openai/gpt-4o",
        "anthropic/claude-3-5-sonnet"
    ],
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who is the best Formula 1 driver?"},
    ]
)
```

### Features

* Supports many vendors (OpenAI compatible APIs like OpenAI and Azure, Anthrophic API, …)
* Fallback to different vendor/model when first one fails
* Auto-retry w/ exponential backoff
* Use Jinja2 for prompt templates
* Multi-step prompt grammar
* Helps you write better tests

#### Design decisions

* The API roughly follows the OpenAI Python SDK (most popular)

#### What is it not?

* Not an agent, guidance framework, etc. (e.g. DSPy, Guidance, LangChain, lmql, etc.)

### Status

* [ ] Vendors
  * [ ] OpenAI
  * [ ] Anthropic
  * [ ] Replicate
  * [ ] Azure
* [ ] Chat completion
  * [ ] Support all params 
  * [ ] JSON mode
  * [ ] Tools (Functions)
  * [ ] Streaming
  * [ ] Access original response
* [ ] Text completion
* [ ] Embeddings
* [ ] Images
* [ ] Audio
* [ ] Cost estimation (and limits)
