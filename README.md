# Gnosis Labs Hackathon starter

Welcome to the Gnosis AI Hackathon repo! Here you will find all you need to build a tool for AI Agents that can make predictions on outcomes of future events.

Follow the instructions below to get started.

## Support

Contact us at https://t.me/+Fb0trLKZdMw2MTQ8 or via the Gnosis Discord (channel gnosis-ai).

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

## Task - General agent

[Description](https://ethglobal.com/events/brussels/prizes/circles)
[Documentation](https://gnosis-labs.gitbook.io/gnosis-labs)

There are multiple avenues to explore with such a general agent. Ultimately we want it to thrive in the blockchain and be an autonomous agent ([some even claim it can be an alternate form of life](https://www.youtube.com/watch?v=Y4QKEJehYBg&t=6103s&ab_channel=DappConBerlin)).

Feel free to follow your inspiration and present us with your ideas. We list some of our ideas below:

- Add new functions to the general agent: currently it can only fetch balances and do simple math functions. Integrations we would love to see would be with DeFi protocols that are live on Gnosis, such as Aave, Spark, CowSwap, Omen, and many others.
  - Feel free to get inspiration from the tools we already built (https://github.com/gnosis/prediction-market-agent/blob/main/prediction_market_agent/agents/microchain_agent/microchain_agent.py#L30)

- Swap the framework we use for the autonomous agent. We currently use [microchain](https://github.com/galatolofederico/microchain), but many others would also make sense here.
- Use different LLMs, for example, open-source ones from Ollama.

### Getting started

- Install using Poetry

```commandline
poetry install
```

- Fill in ENV variables
```commandline
mv .env.example .env
# fill in variables
```

- Run the general agent for a few iterations to see what it does.

```commandline
poetry run python general_agent/main.py
```

### Deployment

We suggest using [Modal](https://modal.com) for the deployment of agents.
If you installed the dependencies using Poetry, Modal should already be available in your environment.
You need to create an account and generate api keys. Then, add the keys MODAL_TOKEN_ID and MODAL_TOKEN_SECRET to your .env file.

For creating a cron job that triggers the general agent, deploy it with
```
poetry run modal deploy --name <YOUR_APP_NAME> general_agent/remote_runner.py  
