from agent_loop.agent import Agent
from agent_loop.llm.providers.openai.client import OpenAIClient
from agent_loop.tools.btc_price_tool import BTCPriceTool
from agent_loop.tools.tool_registry import ToolRegistry


def main() -> None:
    registry = ToolRegistry()
    registry.register(BTCPriceTool())

    agent = Agent(registry, OpenAIClient())
    response = agent.run("Quel est le prix actuel du BTC ?")
    print(response.model_dump())


if __name__ == "__main__":
    main()
