# Preloaded Data Reference

Use `--data-file <path>` to inject external data directly into the CLI.

Use `--data-only` when you want to disable all network fetching and rely only on the supplied file.

## Supported commands

```bash
bash scripts/run-analysis.sh 600519.SH,000001.SZ --data-file ./sample-data.json --data-only
bash scripts/run-backtest.sh 600519.SH,000001.SZ --data-file ./sample-data.json --data-only
```

## JSON shape

The file must be JSON. Recommended shape:

```json
{
  "tickers": {
    "600519.SH": {
      "market_cap": 1700000000000,
      "prices": [
        {
          "open": 1720.0,
          "close": 1735.5,
          "high": 1740.0,
          "low": 1718.0,
          "volume": 320000,
          "time": "2026-03-10T00:00:00"
        }
      ],
      "financial_metrics": [
        {
          "ticker": "600519.SH",
          "report_period": "2025-12-31",
          "period": "ttm",
          "currency": "CNY",
          "market_cap": 1700000000000,
          "price_to_earnings_ratio": 28.5,
          "price_to_book_ratio": 9.2,
          "price_to_sales_ratio": 12.4,
          "enterprise_value": 1690000000000,
          "enterprise_value_to_ebitda_ratio": 21.0,
          "enterprise_value_to_revenue_ratio": 11.8,
          "free_cash_flow_yield": 0.03,
          "peg_ratio": 1.8,
          "gross_margin": 0.91,
          "operating_margin": 0.52,
          "net_margin": 0.48,
          "return_on_equity": 0.33,
          "return_on_assets": 0.22,
          "return_on_invested_capital": 0.29,
          "asset_turnover": 0.46,
          "inventory_turnover": 0.0,
          "receivables_turnover": 0.0,
          "days_sales_outstanding": 0.0,
          "operating_cycle": 0.0,
          "working_capital_turnover": 0.0,
          "current_ratio": 4.1,
          "quick_ratio": 3.9,
          "cash_ratio": 2.8,
          "operating_cash_flow_ratio": 0.0,
          "debt_to_equity": 0.12,
          "debt_to_assets": 0.07,
          "interest_coverage": 100.0,
          "revenue_growth": 0.15,
          "earnings_growth": 0.14,
          "book_value_growth": 0.12,
          "earnings_per_share_growth": 0.14,
          "free_cash_flow_growth": 0.13,
          "operating_income_growth": 0.14,
          "ebitda_growth": 0.14,
          "payout_ratio": 0.55,
          "earnings_per_share": 62.4,
          "book_value_per_share": 188.2,
          "free_cash_flow_per_share": 49.1
        }
      ],
      "line_items": [
        {
          "ticker": "600519.SH",
          "report_period": "2025-12-31",
          "period": "ttm",
          "currency": "CNY",
          "revenue": 174500000000,
          "net_income": 84000000000,
          "free_cash_flow": 62000000000,
          "operating_income": 91000000000,
          "cash_and_equivalents": 180000000000,
          "total_debt": 22000000000,
          "shareholders_equity": 320000000000,
          "outstanding_shares": 1256197800,
          "ebit": 90500000000,
          "ebitda": 92000000000
        }
      ],
      "company_news": [
        {
          "ticker": "600519.SH",
          "title": "Sample headline",
          "author": "External Feed",
          "source": "Custom Source",
          "date": "2026-03-10T08:00:00",
          "url": "https://example.com/news/1",
          "sentiment": "positive"
        }
      ],
      "insider_trades": [
        {
          "ticker": "600519.SH",
          "issuer": "Kweichow Moutai",
          "name": "Sample Person",
          "title": "Director",
          "is_board_director": true,
          "transaction_date": "2026-03-08",
          "transaction_shares": 1000,
          "transaction_price_per_share": 1700.0,
          "transaction_value": 1700000.0,
          "shares_owned_before_transaction": 5000,
          "shares_owned_after_transaction": 6000,
          "security_title": "A Share",
          "filing_date": "2026-03-09"
        }
      ]
    }
  }
}
```

## Supported keys per ticker

- `prices`
- `financial_metrics`
- `line_items`
- `company_news`
- `insider_trades`
- `market_cap`
- `company_facts`

## Behavior

- Date filtering is still applied based on the CLI arguments.
- `prices` are filtered by `time`.
- `financial_metrics` and `line_items` are filtered by `report_period`.
- `company_news` is filtered by `date`.
- `insider_trades` is filtered by `filing_date`.
- If `market_cap` is missing, the runtime tries `company_facts.market_cap`, then `financial_metrics[0].market_cap`.
