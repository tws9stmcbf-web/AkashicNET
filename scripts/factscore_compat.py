"""Review-only FActScore 0.2.0 helpers; no inference or downloads on import."""

import hashlib
import json
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ModelConfig:
    model: str
    endpoint: str

    @classmethod
    def from_role(cls, role):
        if role not in ("ChatGPT", "InstructGPT"):
            raise ValueError("Unsupported FActScore role")
        prefix = "FACTSCORE_VERIFY" if role == "ChatGPT" else "FACTSCORE_ATOMIC"
        model = os.environ.get(prefix + "_MODEL", "").strip()
        endpoint = "chat" if role == "ChatGPT" else os.environ.get(prefix + "_ENDPOINT", "")
        if not model or endpoint not in ("chat", "completion"):
            raise ValueError(f"Set {prefix}_MODEL and, for atomic facts, FACTSCORE_ATOMIC_ENDPOINT=chat|completion")
        return cls(model, endpoint)

    def cache_path(self, path):
        if path is None:
            raise ValueError("An explicit research cache path is required")
        identity = json.dumps(["akashicnet-compat-v1", self.model, self.endpoint])
        digest = hashlib.sha256(identity.encode()).hexdigest()
        return os.fspath(path) + "." + digest


def generate(config, prompt, max_tokens, temperature):
    """One request only. API/auth/parameter errors propagate; no model fallback."""
    import openai

    kwargs = dict(model=config.model, max_tokens=max_tokens, temperature=temperature)
    if config.endpoint == "chat":
        response = openai.ChatCompletion.create(
            messages=[{"role": "user", "content": prompt}], **kwargs)
        output = response["choices"][0]["message"]["content"]
    elif config.endpoint == "completion":
        response = openai.Completion.create(prompt=prompt, **kwargs)
        output = response["choices"][0]["text"]
    else:
        raise ValueError("Unsupported endpoint")
    if not isinstance(output, str) or not output.strip():
        raise ValueError("Model returned no usable text")
    return output, response


def require_tokenizer():
    """Use NLTK's installed tokenizer and NLTK_DATA lookup; never download."""
    from nltk.tokenize import sent_tokenize

    try:
        sent_tokenize("Tokenizer readiness probe.")
    except LookupError as exc:
        raise RuntimeError(
            "Pre-provision trusted English NLTK tokenizer data matching the installed "
            "NLTK version (punkt or punkt_tab), set NLTK_DATA before Python starts, "
            "and retry. No download was attempted by the compatibility layer."
        ) from exc
