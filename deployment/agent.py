import time

from eth_typing import HexAddress, HexStr
from prediction_market_agent_tooling.markets.data_models import Currency
from prediction_market_agent_tooling.markets.omen.omen_subgraph_handler import OmenSubgraphHandler


def run():
    # This class entails the agent logic for placing bets.
    # It could call for example the main() function from the trader folder.
    market_id = HexAddress(HexStr("0x57c6bab1ba758d911f11e67ef323acebcfca04b7"))
    print("Started heavy computation")
    print(Currency.xDai)
    time.sleep(2)
    market = OmenSubgraphHandler().get_omen_market_by_market_id(market_id)
    print(f"market {market}")
    print("Finished heavy computation")