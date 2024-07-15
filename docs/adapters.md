# Adapters

_unimodel_ does not expect you to initialize a specific client (e.g., OpenAI), 
but instead provides an OpenAI like interface that allows you to use various
LLM API backends. This is done by providing a lazy initialized client, that
dynamically accesses a memoized client based on the arguments of a specific
method invocation.

## Lean footprint

We do not initialize or import packages that aren't used. For example, if the
user does solely rely on OpenAI as an LLM API backend, we do not import or load
any Anthropic dependencies. 
