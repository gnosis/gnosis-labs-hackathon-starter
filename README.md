# gnosis-labs-zuberlin2024

Repository for the hackathon run by Gnosis Labs at ZuBerlin 2024.

## Support

Contact us at https://t.me/+Fb0trLKZdMw2MTQ8.

## Setup

Install the project dependencies with `poetry`, using Python 3.10 (you can use [pyenv](https://github.com/pyenv/pyenv) to manage multiple Python versions):

```bash
python3.10 -m pip install poetry
python3.10 -m poetry install
python3.10 -m poetry shell
```

Copy `.env.example` to `.env` and fill in the values:

### OpenAI API key

We will provide you with OpenAI key that's allowed to use gpt-3.5-turbo and embedding models, contact us on the TG group above.

However, everyone is welcome to use arbitrary LLM if wanted.

### Tavily API key

Create a free acount on https://tavily.com and get the key there.

Again, everyone is welcome to use arbitrary search engines, combine them, or even do a totally different approaches!

### Private key on Gnosis Chain

Use your existing or create a new wallet on Gnosis Chain. 

By default the script will do only very tiny bets (0.00001 xDai per market), but of course, you can contact us on the TG group above with your public key to get some free xDai.

## Task

Your task is to modify `predict` function in `trader/prediction.py` by any means necessary.

Goal of the `predict` function is, given an `question` about the future, answer it with either `True` (the answer is `yes`), `False` (if the answer is `no`) or `None` (if the prediction failed).

All the questions are guaranteed to be about the future and to be in a binary yes/no format.

You can play with the prompts, different approaches, different LLMs, search engines, or anything you can think of.

### Experimenting

Run 

```bash
PYTHONPATH=. streamlit run trader/app.py
```

to start a Streamlit application where you can give your prediction method either question [from the Omen market](https://aiomen.eth.limo/), or write your own.

Run 

```bash
python trader/benchmark.py --n N
```

where `N` is number of markets to do a prediction on. The benchmark script will run

1. Random agent (coin flip between yes and no answers)
2. Question-only agent (only LLM call, without any information from internet)
3. `prediction.py/predict`-based agent

on `N` open markets from https://manifold.markets. 

The idea is that markets on Manifold are mostly answered by real people, so the closer your agent is to their predictions, the better. However, it isn't always the case.

Bear in mind your LLM credits, Tavily credits or any other paid 3rd provider credits when running the benchmark, as it answers many markets in a single run, which can be very costly.

### Submission

1. Run `python trader/main.py`, it will place bets on all markets that will be used for the evaluation. You can run the script multiple times, but we will always look only at the latest bet on the market from your public key.
2. Open a PR against this repository with your implementation and public key used for placing bets.
3. Make sure the CI pipeline is all green.

### Evaluation

1. Quantitative 
    1. We will create N markets from the address `0xa7E93F5A0e718bDDC654e525ea668c64Fd572882` by the end of the June, and they will be resolved in roughly two weeks after the creation.
    2. We will measure the accuracy of your agent's answers (by the last bet on each market).

2. Qualitative
    1. We will look into implementation and judge the creativity of the improvements.

3. Cheating
    1. For example, sometimes, the exactly same markets can be found on other prediction market platforms. If we see in the code that the prediction isn’t doing anything practical, we will disqualify it. That being said, it's okay to look at other markets if they are not about the same question, for example, given the evaluation question `Will GNO hit $1000 by the end of 2025?` it's okay to use markets such as `Will GNO hit $500 by the mid of 2025?` as a guidance, but it's not okay to look at the market `Will GNO hit $1000 by the end of 2025?` and copy-paste current probabilities.
