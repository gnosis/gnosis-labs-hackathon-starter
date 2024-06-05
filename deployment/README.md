# Deployment of agents (Work in progress)

This folder contains scripts for quickly deploying your agent to a cloud provider (Modal) and have it executed on a cron schedule. Additionally, a local setup is also provided.

## Pre-requisites

We suggest using Modal (modal.com) for deploying the agents for its simplicity. We don't use Modal in production.

For deploying on Modal, follow the steps below:
- Create account (https://modal.com/)
- Install modal, setup auth key
- Run 
```bash
pip install modal
python3 -m modal setup
```

## Run locally

```shell
modal run deployment/local_runner.py
```

## Run on the cloud

- Run
```shell
modal deploy --name execute_agent deployment/remote_runner.py
```

# Todo
- Improve README
- Define agent function
- make cron_runner and local_runner call same function (from agent)
