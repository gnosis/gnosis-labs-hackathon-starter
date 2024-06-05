import time
from pathlib import Path

from eth_typing import HexAddress, HexStr
from modal import Image, App, Period
from prediction_market_agent_tooling.markets.data_models import Currency
from prediction_market_agent_tooling.markets.omen.omen_subgraph_handler import OmenSubgraphHandler

current_path = Path(__file__)
pyproject_toml_path = current_path.parent.parent.joinpath("pyproject.toml")
lockfile_path = current_path.parent.parent.joinpath("poetry.lock")

image = Image.from_registry("ghcr.io/gnosis/prediction-market-agent:main").pip_install("pydantic==2.6.1")

app = App(image=image)  # Note: prior to April 2024, "app" was called "stub"

@app.function(schedule=Period(minutes=5))
def perform_heavy_computation():
    market_id = HexAddress(HexStr("0x57c6bab1ba758d911f11e67ef323acebcfca04b7"))
    print ("Started heavy computation")
    print(Currency.xDai)
    time.sleep(2)
    market = OmenSubgraphHandler().get_omen_market_by_market_id(market_id)
    print (f"market {market}")
    print("Finished heavy computation")