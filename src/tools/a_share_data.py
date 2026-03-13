import datetime as dt
import os
from typing import Callable

import requests

from src.data.models import Price


DEFAULT_PRICE_DATA_SOURCES = [
    "financial_datasets",
    "akshare",
    "baostock",
    "tushare",
    "tencent",
    "xueqiu",
    "baidu",
]


def is_a_share_ticker(ticker: str) -> bool:
    try:
        normalize_a_share_code(ticker)
        return True
    except ValueError:
        return False


def normalize_a_share_code(ticker: str) -> tuple[str, str]:
    raw = ticker.strip().upper()
    if raw.startswith(("SH", "SZ")) and len(raw) >= 8:
        exchange = raw[:2]
        code = raw[2:]
    elif "." in raw:
        code, suffix = raw.split(".", 1)
        suffix = suffix.upper()
        exchange = "SH" if suffix in {"SH", "SS"} else "SZ" if suffix in {"SZ"} else ""
    else:
        code = raw
        exchange = ""

    if not code.isdigit() or len(code) != 6:
        raise ValueError(f"Unsupported A-share ticker format: {ticker}")

    if not exchange:
        exchange = "SH" if code.startswith(("5", "6", "8", "9")) else "SZ"

    return code, exchange


def get_configured_price_data_sources(api_keys: dict | None = None) -> list[str]:
    raw = (
        (api_keys or {}).get("PRICE_DATA_SOURCES")
        or os.getenv("PRICE_DATA_SOURCES")
        or os.getenv("MARKET_DATA_SOURCES")
        or ",".join(DEFAULT_PRICE_DATA_SOURCES)
    )
    return [item.strip().lower() for item in raw.split(",") if item.strip()]


def fetch_a_share_prices(
    source: str,
    ticker: str,
    start_date: str,
    end_date: str,
    api_keys: dict | None = None,
) -> list[Price]:
    handlers: dict[str, Callable[[str, str, str, dict | None], list[Price]]] = {
        "akshare": _fetch_akshare_prices,
        "baostock": _fetch_baostock_prices,
        "tushare": _fetch_tushare_prices,
        "tencent": _fetch_tencent_prices,
        "xueqiu": _fetch_xueqiu_prices,
        "baidu": _fetch_baidu_prices,
    }
    handler = handlers.get(source)
    if not handler:
        return []
    try:
        return handler(ticker, start_date, end_date, api_keys)
    except Exception:
        return []


def _build_price(time_str: str, open_price: float, high_price: float, low_price: float, close_price: float, volume: float) -> Price:
    return Price(
        open=float(open_price),
        high=float(high_price),
        low=float(low_price),
        close=float(close_price),
        volume=int(float(volume)),
        time=f"{time_str}T00:00:00",
    )


def _can_use_realtime_snapshot(start_date: str, end_date: str) -> bool:
    try:
        start = dt.datetime.strptime(start_date, "%Y-%m-%d").date()
        end = dt.datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return False

    today = dt.date.today()
    return end >= today and (end - start).days <= 3


def _quote_to_price(quote: dict, end_date: str) -> list[Price]:
    price = quote.get("现价")
    if not price:
        return []

    price_value = float(str(price).replace(",", ""))
    open_price = float(str(quote.get("今开", price_value)).replace(",", "")) if quote.get("今开") not in {None, "N/A"} else price_value
    high_price = float(str(quote.get("最高", price_value)).replace(",", "")) if quote.get("最高") not in {None, "N/A"} else price_value
    low_price = float(str(quote.get("最低", price_value)).replace(",", "")) if quote.get("最低") not in {None, "N/A"} else price_value
    volume_text = str(quote.get("成交量", "0")).replace("手", "").replace(",", "")
    volume = float(volume_text) * 100 if volume_text not in {"", "N/A"} else 0
    return [_build_price(end_date, open_price, high_price, low_price, price_value, volume)]


def _fetch_tencent_prices(ticker: str, start_date: str, end_date: str, api_keys: dict | None = None) -> list[Price]:
    if not _can_use_realtime_snapshot(start_date, end_date):
        return []
    monitor = AShareRealtimeMonitor()
    return _quote_to_price(monitor.fetch_tencent_quote(ticker), end_date)


def _fetch_xueqiu_prices(ticker: str, start_date: str, end_date: str, api_keys: dict | None = None) -> list[Price]:
    if not _can_use_realtime_snapshot(start_date, end_date):
        return []
    monitor = AShareRealtimeMonitor()
    return _quote_to_price(monitor.fetch_xueqiu_quote(ticker), end_date)


def _fetch_baidu_prices(ticker: str, start_date: str, end_date: str, api_keys: dict | None = None) -> list[Price]:
    if not _can_use_realtime_snapshot(start_date, end_date):
        return []
    monitor = AShareRealtimeMonitor()
    return _quote_to_price(monitor.fetch_baidu_quote(ticker), end_date)


def _fetch_akshare_prices(ticker: str, start_date: str, end_date: str, api_keys: dict | None = None) -> list[Price]:
    ak = __import__("akshare")
    code, _ = normalize_a_share_code(ticker)
    compact_start = start_date.replace("-", "")
    compact_end = end_date.replace("-", "")

    data_frame = None
    if hasattr(ak, "stock_zh_a_hist"):
        data_frame = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=compact_start, end_date=compact_end, adjust="qfq")
    elif hasattr(ak, "stock_zh_kline"):
        data_frame = ak.stock_zh_kline(symbol=code, period="daily", start_date=compact_start, end_date=compact_end, adjust="qfq")

    if data_frame is None or data_frame.empty:
        return []

    rows: list[Price] = []
    for _, row in data_frame.iterrows():
        time_value = row.get("日期") or row.get("date")
        open_value = row.get("开盘") if "开盘" in row else row.get("open")
        high_value = row.get("最高") if "最高" in row else row.get("high")
        low_value = row.get("最低") if "最低" in row else row.get("low")
        close_value = row.get("收盘") if "收盘" in row else row.get("close")
        volume_value = row.get("成交量") if "成交量" in row else row.get("volume", 0)

        if time_value is None or close_value is None:
            continue

        rows.append(
            _build_price(
                str(time_value)[:10],
                open_value,
                high_value,
                low_value,
                close_value,
                volume_value,
            )
        )

    return rows


def _fetch_baostock_prices(ticker: str, start_date: str, end_date: str, api_keys: dict | None = None) -> list[Price]:
    bs = __import__("baostock")
    code, exchange = normalize_a_share_code(ticker)
    login_result = bs.login()
    if getattr(login_result, "error_code", "1") != "0":
        return []

    try:
        query = bs.query_history_k_data_plus(
            f"{exchange.lower()}.{code}",
            "date,open,high,low,close,volume",
            start_date=start_date,
            end_date=end_date,
            frequency="d",
            adjustflag="2",
        )

        rows: list[Price] = []
        while query.error_code == "0" and query.next():
            record = query.get_row_data()
            if len(record) < 6:
                continue
            rows.append(
                _build_price(
                    record[0],
                    record[1],
                    record[2],
                    record[3],
                    record[4],
                    record[5],
                )
            )

        return rows
    finally:
        bs.logout()


def _fetch_tushare_prices(ticker: str, start_date: str, end_date: str, api_keys: dict | None = None) -> list[Price]:
    token = (api_keys or {}).get("TUSHARE_TOKEN") or os.getenv("TUSHARE_TOKEN")
    if not token:
        return []

    ts = __import__("tushare")
    if hasattr(ts, "set_token"):
        ts.set_token(token)
    pro = ts.pro_api(token)

    code, exchange = normalize_a_share_code(ticker)
    data_frame = pro.daily(
        ts_code=f"{code}.{exchange}",
        start_date=start_date.replace("-", ""),
        end_date=end_date.replace("-", ""),
    )
    if data_frame is None or data_frame.empty:
        return []

    data_frame = data_frame.sort_values("trade_date")
    return [
        _build_price(
            f"{str(row['trade_date'])[:4]}-{str(row['trade_date'])[4:6]}-{str(row['trade_date'])[6:8]}",
            row["open"],
            row["high"],
            row["low"],
            row["close"],
            float(row.get("vol", 0)) * 100,
        )
        for _, row in data_frame.iterrows()
    ]


class AShareRealtimeMonitor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-CN,zh;q=0.9",
            }
        )

    def _format_code(self, ticker: str, source: str) -> str:
        code, exchange = normalize_a_share_code(ticker)
        if source == "tencent":
            return f"{exchange.lower()}{code}"
        if source == "xueqiu":
            return f"{exchange}{code}"
        return code

    def fetch_tencent_quote(self, ticker: str) -> dict:
        code = self._format_code(ticker, "tencent")
        response = self.session.get(f"http://qt.gtimg.cn/q={code}", timeout=10)
        response.encoding = "gbk"
        if "=" not in response.text:
            return {}
        fields = response.text.split("=")[1].strip().strip('"').split("~")
        if len(fields) < 10 or not fields[3] or not fields[4]:
            return {}
        current = float(fields[3])
        previous_close = float(fields[4])
        return {
            "现价": current,
            "今开": fields[5] or current,
            "最高": fields[6] or current,
            "最低": fields[7] or current,
            "成交量": f"{float(fields[8]) / 100:.0f}手" if fields[8] else "0手",
            "涨跌额": current - previous_close,
            "涨跌幅": ((current / previous_close) - 1) * 100 if previous_close else 0,
        }

    def fetch_xueqiu_quote(self, ticker: str) -> dict:
        code = self._format_code(ticker, "xueqiu")
        headers = dict(self.session.headers)
        headers["Referer"] = f"https://xueqiu.com/S/{code}"
        headers["X-Requested-With"] = "XMLHttpRequest"

        self.session.get("https://www.xueqiu.com/", timeout=3, headers=headers)
        response = self.session.get(
            "https://stock.xueqiu.com/v5/stock/realtime/quotec.json",
            params={"symbol": code},
            timeout=10,
            headers=headers,
        )
        data = response.json()
        quote = data.get("data")
        if isinstance(quote, list):
            quote = quote[0] if quote else {}
        if not isinstance(quote, dict) or not quote.get("current"):
            return {}
        return {
            "现价": quote.get("current"),
            "今开": quote.get("open"),
            "最高": quote.get("high"),
            "最低": quote.get("low"),
            "成交量": f"{float(quote.get('volume', 0)) / 100:.0f}手",
        }

    def fetch_baidu_quote(self, ticker: str) -> dict:
        code = self._format_code(ticker, "baidu")
        response = self.session.get(
            "https://finance.pae.baidu.com/selfselect/getstockinfo",
            params={"code": code, "market": "ab", "type": "stock"},
            timeout=10,
        )
        data = response.json()
        market_data = data.get("data", {}).get("marketData", {})
        if not market_data or market_data.get("price") in {None, ""}:
            return {}
        return {
            "现价": market_data.get("price"),
            "今开": market_data.get("open"),
            "最高": market_data.get("high"),
            "最低": market_data.get("low"),
            "成交量": f"{float(market_data.get('volume', 0)) / 100:.0f}手",
        }
