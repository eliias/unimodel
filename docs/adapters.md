# Adapters

_unimodel_ does not expect you to initialize a specific client (e.g., OpenAI), 
but instead provides an OpenAI like interface that allows you to use various
LLM API backends. This is done through lazy initializing vendor clients.

## Lean footprint

We do not initialize or import packages that aren't used. For example, if the
user does solely rely on OpenAI as an LLM API backend, we do not import or load
any Anthropic dependencies.

Vendor specific clients are also not created more than once per [scope](.scope).
Clients are also automatically memoized.
