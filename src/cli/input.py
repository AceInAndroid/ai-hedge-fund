import sys
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import argparse
import questionary
from colorama import Fore, Style

from src.utils.analysts import ANALYST_ORDER
from src.llm.models import OLLAMA_LLM_ORDER, ModelProvider
from src.utils.ollama import ensure_ollama_and_model

from dataclasses import dataclass
from typing import Optional


CLI_PROVIDER_ORDER = [
    ModelProvider.ANTHROPIC,
    ModelProvider.OPENAI,
    ModelProvider.OPENAI_COMPATIBLE,
    ModelProvider.ANTHROPIC_COMPATIBLE,
    ModelProvider.LM_STUDIO,
    ModelProvider.DEEPSEEK,
    ModelProvider.GOOGLE,
    ModelProvider.GROQ,
    ModelProvider.OPENROUTER,
    ModelProvider.XAI,
    ModelProvider.GIGACHAT,
    ModelProvider.AZURE_OPENAI,
]

MODEL_ENV_KEYS: dict[ModelProvider, str] = {
    ModelProvider.ANTHROPIC: "ANTHROPIC_MODEL",
    ModelProvider.OPENAI: "OPENAI_MODEL",
    ModelProvider.OPENAI_COMPATIBLE: "OPENAI_COMPATIBLE_MODEL",
    ModelProvider.ANTHROPIC_COMPATIBLE: "ANTHROPIC_COMPATIBLE_MODEL",
    ModelProvider.LM_STUDIO: "LM_STUDIO_MODEL",
    ModelProvider.DEEPSEEK: "DEEPSEEK_MODEL",
    ModelProvider.GOOGLE: "GOOGLE_MODEL",
    ModelProvider.GROQ: "GROQ_MODEL",
    ModelProvider.OPENROUTER: "OPENROUTER_MODEL",
    ModelProvider.XAI: "XAI_MODEL",
    ModelProvider.GIGACHAT: "GIGACHAT_MODEL",
    ModelProvider.AZURE_OPENAI: "AZURE_OPENAI_DEPLOYMENT_NAME",
}

PROVIDER_ALIASES = {
    "anthropic": ModelProvider.ANTHROPIC,
    "openai": ModelProvider.OPENAI,
    "openai-compatible": ModelProvider.OPENAI_COMPATIBLE,
    "openai_compatible": ModelProvider.OPENAI_COMPATIBLE,
    "openaicompatible": ModelProvider.OPENAI_COMPATIBLE,
    "anthropic-compatible": ModelProvider.ANTHROPIC_COMPATIBLE,
    "anthropic_compatible": ModelProvider.ANTHROPIC_COMPATIBLE,
    "anthropiccompatible": ModelProvider.ANTHROPIC_COMPATIBLE,
    "lm-studio": ModelProvider.LM_STUDIO,
    "lm_studio": ModelProvider.LM_STUDIO,
    "lmstudio": ModelProvider.LM_STUDIO,
    "deepseek": ModelProvider.DEEPSEEK,
    "google": ModelProvider.GOOGLE,
    "groq": ModelProvider.GROQ,
    "openrouter": ModelProvider.OPENROUTER,
    "xai": ModelProvider.XAI,
    "gigachat": ModelProvider.GIGACHAT,
    "azure-openai": ModelProvider.AZURE_OPENAI,
    "azure_openai": ModelProvider.AZURE_OPENAI,
    "azureopenai": ModelProvider.AZURE_OPENAI,
}


def add_common_args(
    parser: argparse.ArgumentParser,
    *,
    require_tickers: bool = False,
    include_analyst_flags: bool = True,
    include_ollama: bool = True,
) -> argparse.ArgumentParser:
    parser.add_argument(
        "--tickers",
        type=str,
        required=require_tickers,
        help="Comma-separated list of stock ticker symbols (e.g., AAPL,MSFT,GOOGL)",
    )
    if include_analyst_flags:
        parser.add_argument(
            "--analysts",
            type=str,
            required=False,
            help="Comma-separated list of analysts to use (e.g., michael_burry,other_analyst)",
        )
        parser.add_argument(
            "--analysts-all",
            action="store_true",
            help="Use all available analysts (overrides --analysts)",
        )
    if include_ollama:
        parser.add_argument("--ollama", action="store_true", help="Use Ollama for local LLM inference")
    parser.add_argument(
        "--model-provider",
        type=str,
        required=False,
        help="LLM provider to use (e.g., anthropic, openai-compatible, lm-studio). If omitted, CLI will use the configured provider from .env.",
    )
    parser.add_argument(
        "--model",
        type=str,
        required=False,
        help="Model name to use. If omitted, CLI will use the configured *_MODEL value from .env or prompt for a custom model name.",
    )
    parser.add_argument(
        "--data-file",
        type=str,
        required=False,
        help="Path to a JSON file containing preloaded market/fundamental data. When provided, the app will read from this file before making external data requests.",
    )
    parser.add_argument(
        "--data-only",
        action="store_true",
        help="Use only the preloaded data supplied by --data-file and skip all external data fetching.",
    )
    return parser


def add_date_args(parser: argparse.ArgumentParser, *, default_months_back: int | None = None) -> argparse.ArgumentParser:
    if default_months_back is None:
        parser.add_argument("--start-date", type=str, help="Start date (YYYY-MM-DD)")
        parser.add_argument("--end-date", type=str, help="End date (YYYY-MM-DD)")
    else:
        parser.add_argument(
            "--end-date",
            type=str,
            default=datetime.now().strftime("%Y-%m-%d"),
            help="End date in YYYY-MM-DD format",
        )
        parser.add_argument(
            "--start-date",
            type=str,
            default=(datetime.now() - relativedelta(months=default_months_back)).strftime("%Y-%m-%d"),
            help="Start date in YYYY-MM-DD format",
        )
    return parser


def parse_tickers(tickers_arg: str | None) -> list[str]:
    if not tickers_arg:
        return []
    return [ticker.strip() for ticker in tickers_arg.split(",") if ticker.strip()]


def select_analysts(flags: dict | None = None) -> list[str]:
    if flags and flags.get("analysts_all"):
        return [a[1] for a in ANALYST_ORDER]

    if flags and flags.get("analysts"):
        return [a.strip() for a in flags["analysts"].split(",") if a.strip()]

    choices = questionary.checkbox(
        "Select your AI analysts.",
        choices=[questionary.Choice(display, value=value) for display, value in ANALYST_ORDER],
        instruction="\n\nInstructions: \n1. Press Space to select/unselect analysts.\n2. Press 'a' to select/unselect all.\n3. Press Enter when done.",
        validate=lambda x: len(x) > 0 or "You must select at least one analyst.",
        style=questionary.Style(
            [
                ("checkbox-selected", "fg:green"),
                ("selected", "fg:green noinherit"),
                ("highlighted", "noinherit"),
                ("pointer", "noinherit"),
            ]
        ),
    ).ask()

    if not choices:
        print("\n\nInterrupt received. Exiting...")
        sys.exit(0)

    print(
        f"\nSelected analysts: {', '.join(Fore.GREEN + c.title().replace('_', ' ') + Style.RESET_ALL for c in choices)}\n"
    )
    return choices


def _env_has_any(*keys: str) -> bool:
    return any(os.getenv(key) for key in keys)


def _env_has_all(*keys: str) -> bool:
    return all(os.getenv(key) for key in keys)


def _is_provider_configured(provider: ModelProvider) -> bool:
    if provider == ModelProvider.ANTHROPIC:
        return _env_has_any("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")
    if provider == ModelProvider.OPENAI:
        return _env_has_any("OPENAI_API_KEY")
    if provider == ModelProvider.OPENAI_COMPATIBLE:
        return _env_has_any("OPENAI_COMPATIBLE_BASE_URL")
    if provider == ModelProvider.ANTHROPIC_COMPATIBLE:
        return _env_has_all("ANTHROPIC_COMPATIBLE_BASE_URL", "ANTHROPIC_COMPATIBLE_API_KEY") or (
            _env_has_any("ANTHROPIC_COMPATIBLE_BASE_URL") and _env_has_any("ANTHROPIC_AUTH_TOKEN")
        )
    if provider == ModelProvider.LM_STUDIO:
        return _env_has_any("LM_STUDIO_MODEL", "LM_STUDIO_BASE_URL", "LM_STUDIO_API_KEY")
    if provider == ModelProvider.DEEPSEEK:
        return _env_has_any("DEEPSEEK_API_KEY")
    if provider == ModelProvider.GOOGLE:
        return _env_has_any("GOOGLE_API_KEY")
    if provider == ModelProvider.GROQ:
        return _env_has_any("GROQ_API_KEY")
    if provider == ModelProvider.OPENROUTER:
        return _env_has_any("OPENROUTER_API_KEY")
    if provider == ModelProvider.XAI:
        return _env_has_any("XAI_API_KEY")
    if provider == ModelProvider.GIGACHAT:
        return _env_has_any("GIGACHAT_API_KEY", "GIGACHAT_CREDENTIALS") or _env_has_all("GIGACHAT_USER", "GIGACHAT_PASSWORD")
    if provider == ModelProvider.AZURE_OPENAI:
        return _env_has_all("AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_DEPLOYMENT_NAME")
    return False


def _get_configured_providers() -> list[ModelProvider]:
    return [provider for provider in CLI_PROVIDER_ORDER if _is_provider_configured(provider)]


def _get_env_model_name(provider: ModelProvider) -> str | None:
    env_key = MODEL_ENV_KEYS.get(provider)
    return os.getenv(env_key) if env_key else None


def _parse_provider(provider_name: str) -> ModelProvider:
    if not provider_name:
        raise ValueError("Model provider cannot be empty.")

    try:
        return ModelProvider(provider_name)
    except ValueError:
        alias = PROVIDER_ALIASES.get(provider_name.strip().lower())
        if alias:
            return alias

    supported = ", ".join(provider.value for provider in CLI_PROVIDER_ORDER)
    raise ValueError(f"Unknown model provider '{provider_name}'. Supported values: {supported}")


def _select_provider_interactively(configured_providers: list[ModelProvider]) -> ModelProvider:
    if len(configured_providers) == 1:
        provider = configured_providers[0]
        print(f"\nUsing configured provider from .env: {Fore.CYAN}{provider.value}{Style.RESET_ALL}\n")
        return provider

    provider_choice = questionary.select(
        "Select your configured LLM provider:",
        choices=[
            questionary.Choice(
                f"{provider.value}{f' ({_get_env_model_name(provider)})' if _get_env_model_name(provider) else ''}",
                value=provider,
            )
            for provider in configured_providers
        ],
        style=questionary.Style(
            [
                ("selected", "fg:green bold"),
                ("pointer", "fg:green bold"),
                ("highlighted", "fg:green"),
                ("answer", "fg:green bold"),
            ]
        ),
    ).ask()

    if not provider_choice:
        print("\n\nInterrupt received. Exiting...")
        sys.exit(0)

    return provider_choice


def select_model(
    use_ollama: bool,
    model_flag: str | None = None,
    model_provider_flag: str | None = None,
) -> tuple[str, str]:
    model_name: str = ""
    model_provider: str | None = None

    if use_ollama:
        print(f"{Fore.CYAN}Using Ollama for local LLM inference.{Style.RESET_ALL}")
        model_name = questionary.select(
            "Select your Ollama model:",
            choices=[questionary.Choice(display, value=value) for display, value, _ in OLLAMA_LLM_ORDER],
            style=questionary.Style(
                [
                    ("selected", "fg:green bold"),
                    ("pointer", "fg:green bold"),
                    ("highlighted", "fg:green"),
                    ("answer", "fg:green bold"),
                ]
            ),
        ).ask()

        if not model_name:
            print("\n\nInterrupt received. Exiting...")
            sys.exit(0)

        if model_name == "-":
            model_name = questionary.text("Enter the custom model name:").ask()
            if not model_name:
                print("\n\nInterrupt received. Exiting...")
                sys.exit(0)

        if not ensure_ollama_and_model(model_name):
            print(f"{Fore.RED}Cannot proceed without Ollama and the selected model.{Style.RESET_ALL}")
            sys.exit(1)

        model_provider = ModelProvider.OLLAMA.value
        print(
            f"\nSelected {Fore.CYAN}Ollama{Style.RESET_ALL} model: {Fore.GREEN + Style.BRIGHT}{model_name}{Style.RESET_ALL}\n"
        )
    else:
        configured_providers = _get_configured_providers()

        if model_provider_flag:
            provider = _parse_provider(model_provider_flag)
            if not _is_provider_configured(provider):
                raise ValueError(
                    f"Provider {provider.value} is not configured in your environment. "
                    f"Please update .env first, then rerun the command."
                )
        else:
            if not configured_providers:
                raise ValueError(
                    "No configured LLM providers found in .env. "
                    "Please configure one provider such as ANTHROPIC_AUTH_TOKEN/ANTHROPIC_MODEL or OPENAI_API_KEY/OPENAI_MODEL."
                )
            provider = _select_provider_interactively(configured_providers)

        model_provider = provider.value

        if model_flag:
            model_name = model_flag
        else:
            model_name = _get_env_model_name(provider) or ""
            if model_name:
                print(
                    f"\nUsing configured model from .env: {Fore.CYAN}{model_provider}{Style.RESET_ALL} - "
                    f"{Fore.GREEN + Style.BRIGHT}{model_name}{Style.RESET_ALL}\n"
                )
            else:
                model_name = questionary.text(f"Enter the model name for {provider.value}:").ask()
                if not model_name:
                    print("\n\nInterrupt received. Exiting...")
                    sys.exit(0)

        print(
            f"\nSelected {Fore.CYAN}{model_provider}{Style.RESET_ALL} model: "
            f"{Fore.GREEN + Style.BRIGHT}{model_name}{Style.RESET_ALL}\n"
        )

    return model_name, model_provider or ""


def resolve_dates(start_date: str | None, end_date: str | None, *, default_months_back: int | None = None) -> tuple[str, str]:
    if start_date:
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Start date must be in YYYY-MM-DD format")
    if end_date:
        try:
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("End date must be in YYYY-MM-DD format")

    final_end = end_date or datetime.now().strftime("%Y-%m-%d")
    if start_date:
        final_start = start_date
    else:
        months = default_months_back if default_months_back is not None else 3
        end_date_obj = datetime.strptime(final_end, "%Y-%m-%d")
        final_start = (end_date_obj - relativedelta(months=months)).strftime("%Y-%m-%d")
    return final_start, final_end


@dataclass
class CLIInputs:
    tickers: list[str]
    selected_analysts: list[str]
    model_name: str
    model_provider: str
    start_date: str
    end_date: str
    initial_cash: float
    margin_requirement: float
    data_file: str | None = None
    data_only: bool = False
    show_reasoning: bool = False
    show_agent_graph: bool = False
    raw_args: Optional[argparse.Namespace] = None


def parse_cli_inputs(
    *,
    description: str,
    require_tickers: bool,
    default_months_back: int | None,
    include_graph_flag: bool = False,
    include_reasoning_flag: bool = False,
) -> CLIInputs:
    parser = argparse.ArgumentParser(description=description)

    # Common/interactive flags
    add_common_args(parser, require_tickers=require_tickers, include_analyst_flags=True, include_ollama=True)
    add_date_args(parser, default_months_back=default_months_back)

    # Funding flags (standardized, with alias)
    parser.add_argument(
        "--initial-cash",
        "--initial-capital",
        dest="initial_cash",
        type=float,
        default=100000.0,
        help="Initial cash position (alias: --initial-capital). Defaults to 100000.0",
    )
    parser.add_argument(
        "--margin-requirement",
        dest="margin_requirement",
        type=float,
        default=0.0,
        help="Initial margin requirement ratio for shorts (e.g., 0.5 for 50%%). Defaults to 0.0",
    )

    if include_reasoning_flag:
        parser.add_argument("--show-reasoning", action="store_true", help="Show reasoning from each agent")
    if include_graph_flag:
        parser.add_argument("--show-agent-graph", action="store_true", help="Show the agent graph")

    args = parser.parse_args()

    # Normalize parsed values
    tickers = parse_tickers(getattr(args, "tickers", None))
    selected_analysts = select_analysts({
        "analysts_all": getattr(args, "analysts_all", False),
        "analysts": getattr(args, "analysts", None),
    })
    model_name, model_provider = select_model(
        getattr(args, "ollama", False),
        getattr(args, "model", None),
        getattr(args, "model_provider", None),
    )
    start_date, end_date = resolve_dates(getattr(args, "start_date", None), getattr(args, "end_date", None), default_months_back=default_months_back)

    return CLIInputs(
        tickers=tickers,
        selected_analysts=selected_analysts,
        model_name=model_name,
        model_provider=model_provider,
        start_date=start_date,
        end_date=end_date,
        initial_cash=getattr(args, "initial_cash", 100000.0),
        margin_requirement=getattr(args, "margin_requirement", 0.0),
        data_file=getattr(args, "data_file", None),
        data_only=getattr(args, "data_only", False),
        show_reasoning=getattr(args, "show_reasoning", False),
        show_agent_graph=getattr(args, "show_agent_graph", False),
        raw_args=args,
    )
