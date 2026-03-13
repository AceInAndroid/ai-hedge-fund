import argparse
import json

from src.utils.analysts import get_agent_capability_catalog


def _format_agent(agent: dict) -> str:
    capabilities = ", ".join(agent.get("primary_capabilities", []))
    data_requirements = ", ".join(agent.get("data_requirements", []))
    lines = [
        f"- {agent['display_name']} (`{agent['key']}`)",
        f"  Type: {agent.get('role', 'analyst')}",
    ]
    if agent.get("strategy_family"):
        lines.append(f"  Strategy family: {agent['strategy_family']}")
    lines.extend(
        [
            f"  Execution mode: {agent['execution_mode']}",
            f"  Description: {agent['description']}",
            f"  Analysis method: {agent['analysis_method']}",
            f"  Best for: {agent['best_for']}",
            f"  A-share readiness: {agent['a_share_readiness']}",
            f"  Data requirements: {data_requirements}",
            f"  Primary capabilities: {capabilities}",
        ]
    )
    return "\n".join(lines)


def render_text(catalog: dict) -> str:
    lines = ["Analyst Agents"]
    for agent in catalog["analysts"]:
        lines.append(_format_agent(agent))

    lines.append("")
    lines.append("System Agents")
    for agent in catalog["system_agents"]:
        lines.append(_format_agent(agent))

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="List AI hedge fund agent capabilities")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format. Defaults to text.",
    )
    args = parser.parse_args()

    catalog = get_agent_capability_catalog()
    if args.format == "json":
        print(json.dumps(catalog, indent=2))
        return

    print(render_text(catalog))


if __name__ == "__main__":
    main()
