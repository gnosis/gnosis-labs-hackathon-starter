import typer
from prediction_market_agent_tooling.benchmark.agents import (
    AbstractBenchmarkedAgent,
    RandomAgent,
)
from prediction_market_agent_tooling.benchmark.benchmark import Benchmarker
from prediction_market_agent_tooling.benchmark.utils import (
    OutcomePrediction,
    Prediction,
)
from prediction_market_agent_tooling.gtypes import Probability
from prediction_market_agent_tooling.loggers import logger
from prediction_market_agent_tooling.markets.markets import (
    FilterBy,
    MarketType,
    SortBy,
    get_binary_markets,
)
from prediction_prophet.benchmark.agents import _make_prediction
from dotenv import load_dotenv
from trader.prediction import DEFAULT_MODEL, predict


def main(
    n: int = 10,
    output: str = "./benchmark_report.md",
) -> None:
    # Load environment variables
    load_dotenv()

    # Get n markets from https://manifold.markets, where real humans are trading.
    markets = get_binary_markets(
        n, MarketType.MANIFOLD, filter_by=FilterBy.OPEN, sort_by=SortBy.CLOSING_SOONEST
    )
    markets_deduplicated = list(({m.question: m for m in markets}.values()))
    if len(markets) != len(markets_deduplicated):
        logger.info(
            f"Warning: Deduplicated markets from {len(markets)} to {len(markets_deduplicated)}."
        )

    logger.info(f"Found {len(markets_deduplicated)} markets.")

    benchmarker = Benchmarker(
        markets=markets_deduplicated,
        agents=[
            RandomAgent(agent_name="random"),
            QuestionOnlyAgent(),
            ParticipantPredictionAgent(),
        ],
    )

    benchmarker.run_agents()
    md = benchmarker.generate_markdown_report()

    with open(output, "w") as f:
        logger.info(f"Writing benchmark report to: {output}")
        f.write(md)


class QuestionOnlyAgent(AbstractBenchmarkedAgent):
    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        agent_name: str = "question-only",
        max_workers: int = 1,
    ):
        super().__init__(agent_name=agent_name, max_workers=max_workers)
        self.model: str = model

    def predict(self, market_question: str) -> Prediction:
        try:
            return _make_prediction(
                market_question=market_question,
                additional_information="",
                engine=self.model,
                temperature=0.0,
            )
        except Exception as e:
            logger.info(f"Error in QuestionOnlyAgent's predict: {e}")
            return Prediction()


class ParticipantPredictionAgent(AbstractBenchmarkedAgent):
    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        agent_name: str = "your-agent",
        max_workers: int = 1,
    ):
        super().__init__(agent_name=agent_name, max_workers=max_workers)
        self.model: str = model

    def predict(self, market_question: str) -> Prediction:
        try:
            prediction = predict(market_question)
            return (
                Prediction(
                    outcome_prediction=OutcomePrediction(
                        decision=prediction,
                        p_yes=Probability(
                            1.0 if prediction else 0.0
                        ),  # Hardcoded to 1.0 or 0.0 based on the bool value, because the aim of this hackathon is to predict the outcome of the market, not the probability of the outcome.
                        confidence=1.0,
                        info_utility=1.0,
                    )
                )
                if prediction is not None
                else Prediction()
            )
        except Exception as e:
            logger.info(f"Error in prediction's predict: {e}")
            return Prediction()


if __name__ == "__main__":
    typer.run(main)
