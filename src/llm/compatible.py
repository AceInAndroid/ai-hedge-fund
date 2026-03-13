from dataclasses import dataclass
from typing import Any

import httpx


@dataclass
class CompatibleChatResponse:
    content: str


def _coerce_content(content: Any) -> str:
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text") or item.get("content")
                if text:
                    parts.append(str(text))
            else:
                parts.append(str(item))
        return "\n".join(part for part in parts if part)

    if content is None:
        return ""

    return str(content)


def prompt_to_messages(prompt: Any) -> list[dict[str, str]]:
    if isinstance(prompt, str):
        return [{"role": "user", "content": prompt}]

    if hasattr(prompt, "to_messages"):
        raw_messages = prompt.to_messages()
    elif isinstance(prompt, list):
        raw_messages = prompt
    else:
        return [{"role": "user", "content": str(prompt)}]

    role_map = {
        "human": "user",
        "user": "user",
        "ai": "assistant",
        "assistant": "assistant",
        "system": "system",
        "tool": "tool",
    }

    messages: list[dict[str, str]] = []
    for raw_message in raw_messages:
        role = getattr(raw_message, "type", None) or getattr(raw_message, "role", None) or "user"
        content = _coerce_content(getattr(raw_message, "content", raw_message))
        messages.append(
            {
                "role": role_map.get(str(role).lower(), "user"),
                "content": content,
            }
        )

    return messages or [{"role": "user", "content": str(prompt)}]


def build_endpoint_url(base_url: str, path: str) -> str:
    normalized_base = base_url.rstrip("/")
    normalized_path = path if path.startswith("/") else f"/{path}"
    if normalized_base.endswith(normalized_path):
        return normalized_base
    return f"{normalized_base}{normalized_path}"


class OpenAICompatibleChatModel:
    def __init__(self, model: str, base_url: str, api_key: str | None = None, timeout: float = 120.0):
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout

    def invoke(self, prompt: Any) -> CompatibleChatResponse:
        messages = prompt_to_messages(prompt)
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "model": self.model,
            "messages": messages,
        }

        response = httpx.post(
            build_endpoint_url(self.base_url, "/chat/completions"),
            headers=headers,
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()

        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError(f"Invalid OpenAI-compatible response payload: {data}") from exc

        return CompatibleChatResponse(content=_coerce_content(content))


class AnthropicCompatibleChatModel:
    def __init__(self, model: str, base_url: str, api_key: str | None = None, timeout: float = 120.0):
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout

    def invoke(self, prompt: Any) -> CompatibleChatResponse:
        input_messages = prompt_to_messages(prompt)
        system_chunks = [message["content"] for message in input_messages if message["role"] == "system" and message["content"]]
        messages = [
            {
                "role": message["role"],
                "content": [
                    {
                        "type": "text",
                        "text": message["content"],
                    }
                ],
            }
            for message in input_messages
            if message["role"] != "system"
        ]

        if not messages:
            messages = [{"role": "user", "content": ""}]

        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["x-api-key"] = self.api_key

        payload: dict[str, Any] = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": messages,
        }
        if system_chunks:
            payload["system"] = "\n\n".join(system_chunks)

        endpoint_path = "/messages" if self.base_url.rstrip("/").endswith("/v1") else "/v1/messages"

        response = httpx.post(
            build_endpoint_url(self.base_url, endpoint_path),
            headers=headers,
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()

        try:
            content_blocks = data["content"]
        except KeyError as exc:
            raise ValueError(f"Invalid Anthropic-compatible response payload: {data}") from exc

        text_parts = [
            _coerce_content(block.get("text"))
            for block in content_blocks
            if isinstance(block, dict) and block.get("type") == "text"
        ]
        content = "\n".join(part for part in text_parts if part).strip()
        if not content:
            raise ValueError(f"Anthropic-compatible response did not contain text content: {data}")

        return CompatibleChatResponse(content=content)
