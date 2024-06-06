import random

import pandas as pd
import typer
from dotenv import load_dotenv
from prediction_market_agent_tooling.gtypes import HexAddress, HexStr
from prediction_market_agent_tooling.loggers import logger
from prediction_market_agent_tooling.markets.omen.omen import OmenAgentMarket
from prediction_market_agent_tooling.markets.omen.omen_subgraph_handler import (
    OmenSubgraphHandler,
)
from prediction_market_agent_tooling.tools.utils import utcnow

from trader.prediction import predict

MARKET_CREATOR_USED_FOR_EVALUATION = HexAddress(
    HexStr("0xa7E93F5A0e718bDDC654e525ea668c64Fd572882")
)


def main(final: bool = False) -> None:
    # Load the environment variables.
    load_dotenv()

    # Get all markets created by the specified creator.
    markets = OmenSubgraphHandler().get_omen_binary_markets(
        limit=None,
        opened_after=utcnow(),
        # If `final` is True, get all markets created by the specified creator that will be used for the evaluation of the winner.
        creator=MARKET_CREATOR_USED_FOR_EVALUATION if final else None,
    )

    if not markets:
        logger.error("No markets found, please try again later.")
        return

    # If this isn't for the final evaluation, just bet on random 10 markets.
    if not final:
        markets = random.sample(markets, k=min(10, len(markets)))

    results: dict[str, list[str | bool | None]] = {
        "market_id": [],
        "question": [],
        "prediction": [],
    }

    for market_idx, market in enumerate(markets):
        # AgentMarket class contains the logic to interact with the market.
        agent_market = OmenAgentMarket.from_data_model(market)

        # Get the prediction.
        prediction = predict(agent_market.question)

        # Place a bet.
        if prediction is not None:
            agent_market.place_bet(
                prediction,
                amount=agent_market.get_tiny_bet_amount(),  # Just 0.00001 xDai.
            )

        results["market_id"].append(market.id)
        results["question"].append(agent_market.question)
        results["prediction"].append(prediction)

        logger.info(
            f"[{market_idx + 1} / {len(markets)}] Placed {prediction} bet on market {market.url}."
        )

    pd.DataFrame.from_dict(results).to_csv("results.csv", index=False)


if __name__ == "__main__":
    typer.run(main)
