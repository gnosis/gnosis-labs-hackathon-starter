import typer
from dotenv import load_dotenv
from microchain import OpenAIChatGenerator, LLM, Agent, Engine
from microchain.functions import Reasoning, Stop
from prediction_market_agent_tooling.config import APIKeys

from general_agent.functions import Sum, Product, GreaterThan
from general_agent.web3_functions import GetBalance, GetOwnWallet


def main() -> None:
    # Load the environment variables.
    load_dotenv()
    keys = APIKeys()
    generator = OpenAIChatGenerator(
        model="gpt-3.5-turbo",
        api_key=keys.openai_api_key.get_secret_value(),
        api_base="https://api.openai.com/v1",
        temperature=0.7,
    )

    engine = Engine()
    engine.register(Reasoning())
    engine.register(Stop())
    engine.register(Sum())
    engine.register(Product())
    engine.register(GreaterThan())
    engine.register(GetBalance())
    engine.register(GetOwnWallet())

    agent = Agent(llm=LLM(generator=generator), engine=engine)

    agent.max_tries = 3
    # How much is (2*4 + 3)*5?
    agent.prompt = (
        agent.prompt
    ) = f"""Act as a trader on-chain. You can use the following functions:

    {engine.help}

    Only output valid Python function calls.
    Output the balance of the Gnosis treasury, whose address is 0x458cD345B4C05e8DF39d0A07220feb4Ec19F5e6f.    
    Assert which balance is greater.
    """
    agent.bootstrap = [
        'Reasoning("I need to reason step-by-step")',
    ]
    agent.run(iterations=5)


if __name__ == "__main__":
    typer.run(main)