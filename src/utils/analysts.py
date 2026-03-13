"""Constants and utilities related to analysts configuration."""

from src.agents import portfolio_manager
from src.agents.aswath_damodaran import aswath_damodaran_agent
from src.agents.ben_graham import ben_graham_agent
from src.agents.bill_ackman import bill_ackman_agent
from src.agents.cathie_wood import cathie_wood_agent
from src.agents.charlie_munger import charlie_munger_agent
from src.agents.fundamentals import fundamentals_analyst_agent
from src.agents.michael_burry import michael_burry_agent
from src.agents.phil_fisher import phil_fisher_agent
from src.agents.peter_lynch import peter_lynch_agent
from src.agents.sentiment import sentiment_analyst_agent
from src.agents.stanley_druckenmiller import stanley_druckenmiller_agent
from src.agents.technicals import technical_analyst_agent
from src.agents.valuation import valuation_analyst_agent
from src.agents.warren_buffett import warren_buffett_agent
from src.agents.rakesh_jhunjhunwala import rakesh_jhunjhunwala_agent
from src.agents.mohnish_pabrai import mohnish_pabrai_agent
from src.agents.news_sentiment import news_sentiment_agent
from src.agents.growth_agent import growth_analyst_agent


def _build_analyst_config(
    *,
    display_name: str,
    description: str,
    investing_style: str,
    agent_func,
    order: int,
    strategy_family: str,
    primary_capabilities: list[str],
    data_requirements: list[str],
    best_for: str,
    a_share_readiness: str,
):
    return {
        "display_name": display_name,
        "description": description,
        "investing_style": investing_style,
        "agent_func": agent_func,
        "type": "analyst",
        "order": order,
        "strategy_family": strategy_family,
        "primary_capabilities": primary_capabilities,
        "data_requirements": data_requirements,
        "best_for": best_for,
        "a_share_readiness": a_share_readiness,
    }


SYSTEM_AGENT_CONFIG = {
    "risk_manager": {
        "display_name": "Risk Manager",
        "description": "Portfolio risk control and position sizing",
        "role": "system",
        "primary_capabilities": [
            "volatility-aware position caps",
            "correlation-aware concentration control",
            "portfolio-level risk budgeting",
        ],
        "data_requirements": ["prices", "portfolio"],
        "best_for": "Constraining exposures after analyst signals are generated.",
        "a_share_readiness": "high",
        "order": 0,
    },
    "portfolio_manager": {
        "display_name": "Portfolio Manager",
        "description": "Aggregates signals into final buy/sell/hold decisions",
        "role": "system",
        "primary_capabilities": [
            "cross-agent signal synthesis",
            "final action selection",
            "trade sizing coordination",
        ],
        "data_requirements": ["analyst_signals", "risk_management"],
        "best_for": "Producing the final trade decision after analysts and risk controls finish.",
        "a_share_readiness": "high",
        "order": 1,
    },
}

# Define analyst configuration - single source of truth
ANALYST_CONFIG = {
    "aswath_damodaran": _build_analyst_config(
        display_name="Aswath Damodaran",
        description="The Dean of Valuation",
        investing_style="Focuses on intrinsic value and financial metrics to assess investment opportunities through rigorous valuation analysis.",
        agent_func=aswath_damodaran_agent,
        order=0,
        strategy_family="valuation",
        primary_capabilities=["dcf-style valuation", "growth/reinvestment analysis", "relative valuation cross-check"],
        data_requirements=["financial_metrics", "line_items", "market_cap"],
        best_for="Valuation-led stock selection when you already have usable fundamentals.",
        a_share_readiness="medium",
    ),
    "ben_graham": _build_analyst_config(
        display_name="Ben Graham",
        description="The Father of Value Investing",
        investing_style="Emphasizes a margin of safety and invests in undervalued companies with strong fundamentals through systematic value analysis.",
        agent_func=ben_graham_agent,
        order=1,
        strategy_family="deep_value",
        primary_capabilities=["margin-of-safety screening", "balance-sheet strength checks", "earnings stability review"],
        data_requirements=["financial_metrics", "line_items", "market_cap"],
        best_for="Classic value screens on mature businesses with long reporting history.",
        a_share_readiness="medium",
    ),
    "bill_ackman": _build_analyst_config(
        display_name="Bill Ackman",
        description="The Activist Investor",
        investing_style="Seeks to influence management and unlock value through strategic activism and contrarian investment positions.",
        agent_func=bill_ackman_agent,
        order=2,
        strategy_family="activist_value",
        primary_capabilities=["business quality review", "capital structure review", "upside from strategic change"],
        data_requirements=["financial_metrics", "line_items", "market_cap"],
        best_for="Concentrated long ideas where execution change or rerating matters.",
        a_share_readiness="medium",
    ),
    "cathie_wood": _build_analyst_config(
        display_name="Cathie Wood",
        description="The Queen of Growth Investing",
        investing_style="Focuses on disruptive innovation and growth, investing in companies that are leading technological advancements and market disruption.",
        agent_func=cathie_wood_agent,
        order=3,
        strategy_family="innovation_growth",
        primary_capabilities=["innovation narrative analysis", "high-growth scenario valuation", "disruption-led upside framing"],
        data_requirements=["financial_metrics", "line_items", "market_cap"],
        best_for="Innovation-heavy growth names where the upside case matters more than near-term stability.",
        a_share_readiness="medium",
    ),
    "charlie_munger": _build_analyst_config(
        display_name="Charlie Munger",
        description="The Rational Thinker",
        investing_style="Advocates for value investing with a focus on quality businesses and long-term growth through rational decision-making.",
        agent_func=charlie_munger_agent,
        order=4,
        strategy_family="quality_compounder",
        primary_capabilities=["moat analysis", "management quality review", "predictability and durability checks"],
        data_requirements=["financial_metrics", "line_items", "market_cap", "insider_trades", "company_news"],
        best_for="Long-duration compounders where moat and management quality dominate the thesis.",
        a_share_readiness="low",
    ),
    "michael_burry": _build_analyst_config(
        display_name="Michael Burry",
        description="The Big Short Contrarian",
        investing_style="Makes contrarian bets, often shorting overvalued markets and investing in undervalued assets through deep fundamental analysis.",
        agent_func=michael_burry_agent,
        order=5,
        strategy_family="contrarian_value",
        primary_capabilities=["deep value review", "balance sheet stress review", "contrarian sentiment framing"],
        data_requirements=["financial_metrics", "line_items", "market_cap", "insider_trades", "company_news"],
        best_for="Dislocated names where consensus is too negative or the balance sheet is misunderstood.",
        a_share_readiness="low",
    ),
    "mohnish_pabrai": _build_analyst_config(
        display_name="Mohnish Pabrai",
        description="The Dhandho Investor",
        investing_style="Focuses on value investing and long-term growth through fundamental analysis and a margin of safety.",
        agent_func=mohnish_pabrai_agent,
        order=6,
        strategy_family="concentrated_value",
        primary_capabilities=["downside protection review", "cash yield and valuation review", "double-or-nothing setup framing"],
        data_requirements=["financial_metrics", "line_items", "market_cap"],
        best_for="Simple, asymmetric value ideas with clear downside protection.",
        a_share_readiness="medium",
    ),
    "peter_lynch": _build_analyst_config(
        display_name="Peter Lynch",
        description="The 10-Bagger Investor",
        investing_style="Invests in companies with understandable business models and strong growth potential using the 'buy what you know' strategy.",
        agent_func=peter_lynch_agent,
        order=7,
        strategy_family="growth_at_reasonable_price",
        primary_capabilities=["growth quality review", "peg-style valuation check", "growth plus sentiment cross-check"],
        data_requirements=["line_items", "market_cap", "insider_trades", "company_news"],
        best_for="Everyday businesses with visible expansion and reasonable valuation.",
        a_share_readiness="low",
    ),
    "phil_fisher": _build_analyst_config(
        display_name="Phil Fisher",
        description="The Scuttlebutt Investor",
        investing_style="Emphasizes investing in companies with strong management and innovative products, focusing on long-term growth through scuttlebutt research.",
        agent_func=phil_fisher_agent,
        order=8,
        strategy_family="quality_growth",
        primary_capabilities=["growth and quality analysis", "management efficiency review", "scuttlebutt-style sentiment framing"],
        data_requirements=["line_items", "market_cap", "insider_trades", "company_news"],
        best_for="High-quality growth names where management and execution matter heavily.",
        a_share_readiness="low",
    ),
    "rakesh_jhunjhunwala": _build_analyst_config(
        display_name="Rakesh Jhunjhunwala",
        description="The Big Bull Of India",
        investing_style="Leverages macroeconomic insights to invest in high-growth sectors, particularly within emerging markets and domestic opportunities.",
        agent_func=rakesh_jhunjhunwala_agent,
        order=9,
        strategy_family="emerging_market_growth",
        primary_capabilities=["growth and profitability review", "cash flow analysis", "management action review"],
        data_requirements=["financial_metrics", "line_items", "market_cap"],
        best_for="Domestic growth stories and emerging-market style compounding opportunities.",
        a_share_readiness="medium",
    ),
    "stanley_druckenmiller": _build_analyst_config(
        display_name="Stanley Druckenmiller",
        description="The Macro Investor",
        investing_style="Focuses on macroeconomic trends, making large bets on currencies, commodities, and interest rates through top-down analysis.",
        agent_func=stanley_druckenmiller_agent,
        order=10,
        strategy_family="macro_momentum",
        primary_capabilities=["growth plus momentum analysis", "risk-reward framing", "top-down macro-style synthesis"],
        data_requirements=["financial_metrics", "line_items", "market_cap", "insider_trades", "company_news", "prices"],
        best_for="Names where momentum, narrative, and asymmetric payoff matter together.",
        a_share_readiness="medium",
    ),
    "warren_buffett": _build_analyst_config(
        display_name="Warren Buffett",
        description="The Oracle of Omaha",
        investing_style="Seeks companies with strong fundamentals and competitive advantages through value investing and long-term ownership.",
        agent_func=warren_buffett_agent,
        order=11,
        strategy_family="quality_value",
        primary_capabilities=["moat analysis", "pricing power review", "quality-at-a-fair-price valuation"],
        data_requirements=["financial_metrics", "line_items", "market_cap"],
        best_for="Wide-moat businesses with durable returns and disciplined valuation.",
        a_share_readiness="medium",
    ),
    "technical_analyst": _build_analyst_config(
        display_name="Technical Analyst",
        description="Chart Pattern Specialist",
        investing_style="Focuses on chart patterns and market trends to make investment decisions, often using technical indicators and price action analysis.",
        agent_func=technical_analyst_agent,
        order=12,
        strategy_family="technical",
        primary_capabilities=["trend analysis", "momentum analysis", "mean-reversion analysis"],
        data_requirements=["prices"],
        best_for="Price-led screening, fast market checks, and A-share runs with only historical bars.",
        a_share_readiness="high",
    ),
    "fundamentals_analyst": _build_analyst_config(
        display_name="Fundamentals Analyst",
        description="Financial Statement Specialist",
        investing_style="Delves into financial statements and economic indicators to assess the intrinsic value of companies through fundamental analysis.",
        agent_func=fundamentals_analyst_agent,
        order=13,
        strategy_family="fundamental",
        primary_capabilities=["profitability analysis", "growth analysis", "balance-sheet health review"],
        data_requirements=["financial_metrics"],
        best_for="Structured financial quality checks without requiring price action or news.",
        a_share_readiness="medium",
    ),
    "growth_analyst": _build_analyst_config(
        display_name="Growth Analyst",
        description="Growth Specialist",
        investing_style="Analyzes growth trends and valuation to identify growth opportunities through growth analysis.",
        agent_func=growth_analyst_agent,
        order=14,
        strategy_family="growth",
        primary_capabilities=["revenue and earnings acceleration review", "growth durability checks", "insider-trend support"],
        data_requirements=["financial_metrics", "insider_trades"],
        best_for="Companies where the main question is whether growth is persistent and investable.",
        a_share_readiness="medium",
    ),
    "news_sentiment_analyst": _build_analyst_config(
        display_name="News Sentiment Analyst",
        description="News Sentiment Specialist",
        investing_style="Analyzes news sentiment to predict market movements and identify opportunities through news analysis.",
        agent_func=news_sentiment_agent,
        order=15,
        strategy_family="news_sentiment",
        primary_capabilities=["article-level sentiment analysis", "headline aggregation", "news-driven signal generation"],
        data_requirements=["company_news"],
        best_for="Event-driven monitoring and fast changes in narrative tone.",
        a_share_readiness="low",
    ),
    "sentiment_analyst": _build_analyst_config(
        display_name="Sentiment Analyst",
        description="Market Sentiment Specialist",
        investing_style="Gauges market sentiment and investor behavior to predict market movements and identify opportunities through behavioral analysis.",
        agent_func=sentiment_analyst_agent,
        order=16,
        strategy_family="behavioral_sentiment",
        primary_capabilities=["insider activity review", "news plus behavior synthesis", "sentiment-led signal generation"],
        data_requirements=["insider_trades", "company_news"],
        best_for="Behavioral overlays where insider activity and narrative tone matter.",
        a_share_readiness="low",
    ),
    "valuation_analyst": _build_analyst_config(
        display_name="Valuation Analyst",
        description="Company Valuation Specialist",
        investing_style="Specializes in determining the fair value of companies, using various valuation models and financial metrics for investment decisions.",
        agent_func=valuation_analyst_agent,
        order=17,
        strategy_family="valuation",
        primary_capabilities=["multi-method valuation", "wacc and dcf modelling", "market-cap gap analysis"],
        data_requirements=["financial_metrics", "line_items", "market_cap"],
        best_for="A disciplined valuation signal when you want deterministic metrics before narrative overlays.",
        a_share_readiness="medium",
    ),
}

# Derive ANALYST_ORDER from ANALYST_CONFIG for backwards compatibility
ANALYST_ORDER = [(config["display_name"], key) for key, config in sorted(ANALYST_CONFIG.items(), key=lambda x: x[1]["order"])]


def get_analyst_nodes():
    """Get the mapping of analyst keys to their (node_name, agent_func) tuples."""
    return {key: (f"{key}_agent", config["agent_func"]) for key, config in ANALYST_CONFIG.items()}


def get_agents_list():
    """Get the list of agents for API responses."""
    return [
        {
            "key": key,
            "display_name": config["display_name"],
            "description": config["description"],
            "investing_style": config["investing_style"],
            "strategy_family": config["strategy_family"],
            "primary_capabilities": config["primary_capabilities"],
            "data_requirements": config["data_requirements"],
            "best_for": config["best_for"],
            "a_share_readiness": config["a_share_readiness"],
            "order": config["order"],
        }
        for key, config in sorted(ANALYST_CONFIG.items(), key=lambda x: x[1]["order"])
    ]


def get_system_agents_list():
    """Get non-selectable system agents that participate in the workflow."""
    return [
        {
            "key": key,
            **config,
        }
        for key, config in sorted(SYSTEM_AGENT_CONFIG.items(), key=lambda x: x[1]["order"])
    ]


def get_agent_capability_catalog():
    """Get the full agent capability catalog for skills, docs, and CLI helpers."""
    return {
        "analysts": get_agents_list(),
        "system_agents": get_system_agents_list(),
    }
