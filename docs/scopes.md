# Scopes

The idea of _scopes_ is to make the actual generation code simpler. In
particular, we want to decouple the feature (product) from the context it is
used for. A common problem for applications is to let users decide which
provider and/or model they want to use for a certain request.

## Example

This is the simplest example. It creates a lazy initialized OpenAI client.

```python
from unimodel import scoped_for

with scoped_for(api_key="…") as scoped_client:
    response = scoped_client.chat.completions.create(model="openai/gpt-4")
```

Let's look at a more complex version, where we want to support multiple vendors.
Every scope variable can be vendor prefixed (`openai_`, `anthropic_`, …), this
way it is easy to support multiple vendors in a single scope.

```python
from unimodel import scoped_for

with scoped_for(
        openai_api_key="…",
        anthropic_api_key="…"
) as scoped_client:
    response = scoped_client.chat.completions.create(
        models=[
            "openai/gpt-4",
            "anthropic/claude-3-5-sonnet"
        ]
    )
```

This is equivalent to this version. The primary model is automatically looking
for both arguments, `api_key` and `openai_api_key`.

```python
from unimodel import scoped_for

with scoped_for(
        api_key="…",
        anthropic_api_key="…"
) as scoped_client:
    response = scoped_client.chat.completions.create(
        models=[
            "openai/gpt-4",
            "anthropic/claude-3-5-sonnet"
        ]
    )
```

It is also fine to not provide any arguments at all. The scope initialization
code will look for any environment variables that are present. The name of the
variables must match the names form the respective vendor documentation
(OPENAI_API_KEY, …).
