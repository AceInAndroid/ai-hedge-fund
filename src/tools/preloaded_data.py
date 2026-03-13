import json
from pathlib import Path
from typing import Any

from src.data.models import CompanyNews, FinancialMetrics, InsiderTrade, LineItem, Price


_preloaded_payload: dict[str, Any] = {}
_data_only_mode = False


def clear_preloaded_data() -> None:
    global _preloaded_payload, _data_only_mode
    _preloaded_payload = {}
    _data_only_mode = False


def load_preloaded_data_file(path: str, *, data_only: bool = False) -> None:
    payload = json.loads(Path(path).read_text())
    set_preloaded_data(payload, data_only=data_only)


def set_preloaded_data(payload: dict[str, Any], *, data_only: bool = False) -> None:
    global _preloaded_payload, _data_only_mode
    if "tickers" in payload and isinstance(payload["tickers"], dict):
        _preloaded_payload = payload
    else:
        _preloaded_payload = {"tickers": payload}
    _data_only_mode = data_only


def is_data_only_mode() -> bool:
    return _data_only_mode


def _get_ticker_payload(ticker: str) -> dict[str, Any] | None:
    tickers = _preloaded_payload.get("tickers", {})
    if not isinstance(tickers, dict):
        return None

    candidates = [ticker, ticker.upper(), ticker.lower()]
    for candidate in candidates:
        payload = tickers.get(candidate)
        if isinstance(payload, dict):
            return payload
    return None


def _normalize_date(value: str | None) -> str | None:
    if value is None:
        return None
    return str(value)[:10]


def _limit(items: list[Any], limit: int | None) -> list[Any]:
    if limit is None or limit <= 0:
        return items
    return items[:limit]


def get_preloaded_prices(ticker: str, start_date: str, end_date: str) -> tuple[bool, list[Price]]:
    payload = _get_ticker_payload(ticker)
    if not payload or "prices" not in payload:
        return False, []

    start = _normalize_date(start_date)
    end = _normalize_date(end_date)
    prices = [
        Price(**item)
        for item in payload.get("prices", [])
        if start <= _normalize_date(item.get("time")) <= end
    ]
    prices.sort(key=lambda item: item.time)
    return True, prices


def get_preloaded_financial_metrics(ticker: str, end_date: str, period: str, limit: int) -> tuple[bool, list[FinancialMetrics]]:
    payload = _get_ticker_payload(ticker)
    if not payload or "financial_metrics" not in payload:
        return False, []

    end = _normalize_date(end_date)
    metrics = [
        FinancialMetrics(**item)
        for item in payload.get("financial_metrics", [])
        if (not item.get("period") or item.get("period") == period)
        and _normalize_date(item.get("report_period")) <= end
    ]
    metrics.sort(key=lambda item: item.report_period, reverse=True)
    return True, _limit(metrics, limit)


def get_preloaded_line_items(
    ticker: str,
    end_date: str,
    period: str,
    limit: int,
) -> tuple[bool, list[LineItem]]:
    payload = _get_ticker_payload(ticker)
    if not payload or "line_items" not in payload:
        return False, []

    end = _normalize_date(end_date)
    line_items = [
        LineItem(**item)
        for item in payload.get("line_items", [])
        if (not item.get("period") or item.get("period") == period)
        and _normalize_date(item.get("report_period")) <= end
    ]
    line_items.sort(key=lambda item: item.report_period, reverse=True)
    return True, _limit(line_items, limit)


def get_preloaded_insider_trades(
    ticker: str,
    start_date: str | None,
    end_date: str,
    limit: int,
) -> tuple[bool, list[InsiderTrade]]:
    payload = _get_ticker_payload(ticker)
    if not payload or "insider_trades" not in payload:
        return False, []

    start = _normalize_date(start_date) if start_date else None
    end = _normalize_date(end_date)
    trades = []
    for item in payload.get("insider_trades", []):
        filing_date = _normalize_date(item.get("filing_date"))
        if filing_date is None or filing_date > end:
            continue
        if start and filing_date < start:
            continue
        trades.append(InsiderTrade(**item))

    trades.sort(key=lambda item: item.filing_date, reverse=True)
    return True, _limit(trades, limit)


def get_preloaded_company_news(
    ticker: str,
    start_date: str | None,
    end_date: str,
    limit: int,
) -> tuple[bool, list[CompanyNews]]:
    payload = _get_ticker_payload(ticker)
    if not payload or "company_news" not in payload:
        return False, []

    start = _normalize_date(start_date) if start_date else None
    end = _normalize_date(end_date)
    news = []
    for item in payload.get("company_news", []):
        news_date = _normalize_date(item.get("date"))
        if news_date is None or news_date > end:
            continue
        if start and news_date < start:
            continue
        news.append(CompanyNews(**item))

    news.sort(key=lambda item: item.date, reverse=True)
    return True, _limit(news, limit)


def get_preloaded_market_cap(ticker: str) -> tuple[bool, float | None]:
    payload = _get_ticker_payload(ticker)
    if not payload:
        return False, None

    if "market_cap" in payload:
        market_cap = payload.get("market_cap")
        return True, float(market_cap) if market_cap is not None else None

    company_facts = payload.get("company_facts")
    if isinstance(company_facts, dict) and company_facts.get("market_cap") is not None:
        return True, float(company_facts["market_cap"])

    metrics = payload.get("financial_metrics", [])
    if metrics:
        market_cap = metrics[0].get("market_cap")
        return True, float(market_cap) if market_cap is not None else None

    return False, None
