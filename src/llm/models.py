import os
import json
from langchain_anthropic import ChatAnthropic
from langchain_deepseek import ChatDeepSeek
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_xai import ChatXAI
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_gigachat import GigaChat
from langchain_ollama import ChatOllama
from enum import Enum
from pydantic import BaseModel
from typing import Tuple, List
from pathlib import Path

from src.llm.compatible import AnthropicCompatibleChatModel, OpenAICompatibleChatModel


class ModelProvider(str, Enum):
    """Enum for supported LLM providers"""

    ALIBABA = "Alibaba"
    ANTHROPIC = "Anthropic"
    ANTHROPIC_COMPATIBLE = "Anthropic Compatible"
    DEEPSEEK = "DeepSeek"
    GOOGLE = "Google"
    GROQ = "Groq"
    META = "Meta"
    MISTRAL = "Mistral"
    LM_STUDIO = "LM Studio"
    OPENAI = "OpenAI"
    OPENAI_COMPATIBLE = "OpenAI Compatible"
    OLLAMA = "Ollama"
    OPENROUTER = "OpenRouter"
    GIGACHAT = "GigaChat"
    AZURE_OPENAI = "Azure OpenAI"
    XAI = "xAI"


class LLMModel(BaseModel):
    """Represents an LLM model configuration"""

    display_name: str
    model_name: str
    provider: ModelProvider
    supports_json_mode: bool = True
    custom: bool = False

    def to_choice_tuple(self) -> Tuple[str, str, str]:
        """Convert to format needed for questionary choices"""
        return (self.display_name, self.model_name, self.provider.value)

    def is_custom(self) -> bool:
        """Check if the model is a custom entry."""
        return self.custom

    def has_json_mode(self) -> bool:
        """Check if the model supports JSON mode"""
        if not self.supports_json_mode:
            return False
        if self.is_deepseek() or self.is_gemini():
            return False
        # Only certain Ollama models support JSON mode
        if self.is_ollama():
            return "llama3" in self.model_name or "neural-chat" in self.model_name
        # OpenRouter models generally support JSON mode
        if self.provider == ModelProvider.OPENROUTER:
            return True
        return True

    def is_deepseek(self) -> bool:
        """Check if the model is a DeepSeek model"""
        return self.model_name.startswith("deepseek")

    def is_gemini(self) -> bool:
        """Check if the model is a Gemini model"""
        return self.model_name.startswith("gemini")

    def is_ollama(self) -> bool:
        """Check if the model is an Ollama model"""
        return self.provider == ModelProvider.OLLAMA


# Load models from JSON file
def load_models_from_json(json_path: str) -> List[LLMModel]:
    """Load models from a JSON file"""
    with open(json_path, 'r') as f:
        models_data = json.load(f)
    
    models = []
    for model_data in models_data:
        # Convert string provider to ModelProvider enum
        provider_enum = ModelProvider(model_data["provider"])
        models.append(
            LLMModel(
                display_name=model_data["display_name"],
                model_name=model_data["model_name"],
                provider=provider_enum,
                supports_json_mode=model_data.get("supports_json_mode", True),
                custom=model_data.get("custom", False),
            )
        )
    return models


# Get the path to the JSON files
current_dir = Path(__file__).parent
models_json_path = current_dir / "api_models.json"
ollama_models_json_path = current_dir / "ollama_models.json"

# Load available models from JSON
AVAILABLE_MODELS = load_models_from_json(str(models_json_path))

# Load Ollama models from JSON
OLLAMA_MODELS = load_models_from_json(str(ollama_models_json_path))

# Create LLM_ORDER in the format expected by the UI
LLM_ORDER = [model.to_choice_tuple() for model in AVAILABLE_MODELS]

# Create Ollama LLM_ORDER separately
OLLAMA_LLM_ORDER = [model.to_choice_tuple() for model in OLLAMA_MODELS]


def _normalize_provider(model_provider: ModelProvider | str) -> ModelProvider:
    if isinstance(model_provider, ModelProvider):
        return model_provider
    return ModelProvider(model_provider)


def _get_api_setting(api_keys: dict | None, *keys: str, default: str | None = None) -> str | None:
    for key in keys:
        if not key:
            continue
        value = (api_keys or {}).get(key) or os.getenv(key)
        if value:
            return value
    return default


def _resolve_model_name(model_name: str, provider: ModelProvider, api_keys: dict | None) -> str:
    if model_name and not model_name.startswith("__"):
        return model_name

    env_key_by_provider = {
        ModelProvider.ANTHROPIC: "ANTHROPIC_MODEL",
        ModelProvider.OPENAI_COMPATIBLE: "OPENAI_COMPATIBLE_MODEL",
        ModelProvider.ANTHROPIC_COMPATIBLE: "ANTHROPIC_COMPATIBLE_MODEL",
        ModelProvider.LM_STUDIO: "LM_STUDIO_MODEL",
    }
    env_key = env_key_by_provider.get(provider)
    resolved_model_name = _get_api_setting(api_keys, env_key) if env_key else None
    if resolved_model_name:
        return resolved_model_name

    raise ValueError(f"Custom model name not found for provider {provider.value}. Please configure a model name in the UI or set {env_key}.")


def get_model_info(model_name: str, model_provider: ModelProvider | str) -> LLMModel | None:
    """Get model information by model_name"""
    all_models = AVAILABLE_MODELS + OLLAMA_MODELS
    provider = _normalize_provider(model_provider)
    exact_match = next((model for model in all_models if model.model_name == model_name and model.provider == provider), None)
    if exact_match:
        return exact_match

    provider_custom_model = next((model for model in all_models if model.provider == provider and model.custom), None)
    if provider_custom_model:
        return provider_custom_model

    if model_name:
        return LLMModel(
            display_name=model_name,
            model_name=model_name,
            provider=provider,
            supports_json_mode=False,
            custom=True,
        )

    return None


def find_model_by_name(model_name: str) -> LLMModel | None:
    """Find a model by its name across all available models."""
    all_models = AVAILABLE_MODELS + OLLAMA_MODELS
    return next((model for model in all_models if model.model_name == model_name), None)


def get_models_list():
    """Get the list of models for API responses."""
    return [
        {
            "display_name": model.display_name,
            "model_name": model.model_name,
            "provider": model.provider.value
        }
        for model in AVAILABLE_MODELS
    ]


def get_model(model_name: str, model_provider: ModelProvider | str, api_keys: dict = None) -> ChatOpenAI | ChatGroq | ChatOllama | GigaChat | OpenAICompatibleChatModel | AnthropicCompatibleChatModel | None:
    provider = _normalize_provider(model_provider)
    resolved_model_name = _resolve_model_name(model_name, provider, api_keys) if provider in {
        ModelProvider.ANTHROPIC,
        ModelProvider.OPENAI_COMPATIBLE,
        ModelProvider.ANTHROPIC_COMPATIBLE,
        ModelProvider.LM_STUDIO,
    } else model_name

    if provider == ModelProvider.GROQ:
        api_key = (api_keys or {}).get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
        if not api_key:
            # Print error to console
            print(f"API Key Error: Please make sure GROQ_API_KEY is set in your .env file or provided via API keys.")
            raise ValueError("Groq API key not found.  Please make sure GROQ_API_KEY is set in your .env file or provided via API keys.")
        return ChatGroq(model=resolved_model_name, api_key=api_key)
    elif provider == ModelProvider.OPENAI:
        # Get and validate API key
        api_key = _get_api_setting(api_keys, "OPENAI_API_KEY")
        base_url = _get_api_setting(api_keys, "OPENAI_API_BASE")
        if not api_key:
            # Print error to console
            print(f"API Key Error: Please make sure OPENAI_API_KEY is set in your .env file or provided via API keys.")
            raise ValueError("OpenAI API key not found.  Please make sure OPENAI_API_KEY is set in your .env file or provided via API keys.")
        return ChatOpenAI(model=resolved_model_name, api_key=api_key, base_url=base_url)
    elif provider == ModelProvider.OPENAI_COMPATIBLE:
        api_key = _get_api_setting(api_keys, "OPENAI_COMPATIBLE_API_KEY")
        base_url = _get_api_setting(api_keys, "OPENAI_COMPATIBLE_BASE_URL")
        if not base_url:
            raise ValueError("OpenAI-compatible base URL not found. Please set OPENAI_COMPATIBLE_BASE_URL in settings or environment.")
        return OpenAICompatibleChatModel(model=resolved_model_name, base_url=base_url, api_key=api_key)
    elif provider == ModelProvider.LM_STUDIO:
        api_key = _get_api_setting(api_keys, "LM_STUDIO_API_KEY", default="lm-studio")
        base_url = _get_api_setting(api_keys, "LM_STUDIO_BASE_URL", default="http://127.0.0.1:1234/v1")
        return OpenAICompatibleChatModel(model=resolved_model_name, base_url=base_url, api_key=api_key)
    elif provider == ModelProvider.ANTHROPIC:
        api_key = _get_api_setting(api_keys, "ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")
        base_url = _get_api_setting(api_keys, "ANTHROPIC_BASE_URL")
        anthropic_model_override = _get_api_setting(api_keys, "ANTHROPIC_MODEL")
        if not api_key:
            print(f"API Key Error: Please make sure ANTHROPIC_API_KEY is set in your .env file or provided via API keys.")
            raise ValueError("Anthropic API key not found.  Please make sure ANTHROPIC_API_KEY is set in your .env file or provided via API keys.")
        if base_url and anthropic_model_override:
            resolved_model_name = anthropic_model_override
        if base_url:
            return AnthropicCompatibleChatModel(model=resolved_model_name, base_url=base_url, api_key=api_key)
        return ChatAnthropic(model=resolved_model_name, api_key=api_key)
    elif provider == ModelProvider.ANTHROPIC_COMPATIBLE:
        api_key = _get_api_setting(api_keys, "ANTHROPIC_COMPATIBLE_API_KEY", "ANTHROPIC_AUTH_TOKEN")
        base_url = _get_api_setting(api_keys, "ANTHROPIC_COMPATIBLE_BASE_URL")
        if not base_url:
            raise ValueError("Anthropic-compatible base URL not found. Please set ANTHROPIC_COMPATIBLE_BASE_URL in settings or environment.")
        if not api_key:
            raise ValueError("Anthropic-compatible API key not found. Please set ANTHROPIC_COMPATIBLE_API_KEY in settings or environment.")
        return AnthropicCompatibleChatModel(model=resolved_model_name, base_url=base_url, api_key=api_key)
    elif provider == ModelProvider.DEEPSEEK:
        api_key = (api_keys or {}).get("DEEPSEEK_API_KEY") or os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            print(f"API Key Error: Please make sure DEEPSEEK_API_KEY is set in your .env file or provided via API keys.")
            raise ValueError("DeepSeek API key not found.  Please make sure DEEPSEEK_API_KEY is set in your .env file or provided via API keys.")
        return ChatDeepSeek(model=resolved_model_name, api_key=api_key)
    elif provider == ModelProvider.GOOGLE:
        api_key = (api_keys or {}).get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print(f"API Key Error: Please make sure GOOGLE_API_KEY is set in your .env file or provided via API keys.")
            raise ValueError("Google API key not found.  Please make sure GOOGLE_API_KEY is set in your .env file or provided via API keys.")
        return ChatGoogleGenerativeAI(model=resolved_model_name, api_key=api_key)
    elif provider == ModelProvider.OLLAMA:
        # For Ollama, we use a base URL instead of an API key
        # Check if OLLAMA_HOST is set (for Docker on macOS)
        ollama_host = os.getenv("OLLAMA_HOST", "localhost")
        base_url = os.getenv("OLLAMA_BASE_URL", f"http://{ollama_host}:11434")
        return ChatOllama(
            model=model_name,
            base_url=base_url,
        )
    elif provider == ModelProvider.OPENROUTER:
        api_key = (api_keys or {}).get("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print(f"API Key Error: Please make sure OPENROUTER_API_KEY is set in your .env file or provided via API keys.")
            raise ValueError("OpenRouter API key not found. Please make sure OPENROUTER_API_KEY is set in your .env file or provided via API keys.")
        
        # Get optional site URL and name for headers
        site_url = os.getenv("YOUR_SITE_URL", "https://github.com/virattt/ai-hedge-fund")
        site_name = os.getenv("YOUR_SITE_NAME", "AI Hedge Fund")
        
        return ChatOpenAI(
            model=resolved_model_name,
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            model_kwargs={
                "extra_headers": {
                    "HTTP-Referer": site_url,
                    "X-Title": site_name,
                }
            }
        )
    elif provider == ModelProvider.XAI:
        api_key = (api_keys or {}).get("XAI_API_KEY") or os.getenv("XAI_API_KEY")
        if not api_key:
            print(f"API Key Error: Please make sure XAI_API_KEY is set in your .env file or provided via API keys.")
            raise ValueError("xAI API key not found. Please make sure XAI_API_KEY is set in your .env file or provided via API keys.")
        return ChatXAI(model=resolved_model_name, api_key=api_key)
    elif provider == ModelProvider.GIGACHAT:
        if os.getenv("GIGACHAT_USER") or os.getenv("GIGACHAT_PASSWORD"):
            return GigaChat(model=resolved_model_name)
        else: 
            api_key = (api_keys or {}).get("GIGACHAT_API_KEY") or os.getenv("GIGACHAT_API_KEY") or os.getenv("GIGACHAT_CREDENTIALS")
            if not api_key:
                print("API Key Error: Please make sure api_keys is set in your .env file or provided via API keys.")
                raise ValueError("GigaChat API key not found. Please make sure GIGACHAT_API_KEY is set in your .env file or provided via API keys.")

            return GigaChat(credentials=api_key, model=resolved_model_name)
    elif provider == ModelProvider.AZURE_OPENAI:
        # Get and validate API key
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        if not api_key:
            # Print error to console
            print(f"API Key Error: Please make sure AZURE_OPENAI_API_KEY is set in your .env file.")
            raise ValueError("Azure OpenAI API key not found.  Please make sure AZURE_OPENAI_API_KEY is set in your .env file.")
        # Get and validate Azure Endpoint
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        if not azure_endpoint:
            # Print error to console
            print(f"Azure Endpoint Error: Please make sure AZURE_OPENAI_ENDPOINT is set in your .env file.")
            raise ValueError("Azure OpenAI endpoint not found.  Please make sure AZURE_OPENAI_ENDPOINT is set in your .env file.")
        # get and validate deployment name
        azure_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        if not azure_deployment_name:
            # Print error to console
            print(f"Azure Deployment Name Error: Please make sure AZURE_OPENAI_DEPLOYMENT_NAME is set in your .env file.")
            raise ValueError("Azure OpenAI deployment name not found.  Please make sure AZURE_OPENAI_DEPLOYMENT_NAME is set in your .env file.")
        return AzureChatOpenAI(azure_endpoint=azure_endpoint, azure_deployment=azure_deployment_name, api_key=api_key, api_version="2024-10-21")
