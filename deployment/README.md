# Deployment of agents (Work in progress)

This folder contains scripts for quickly deploying your agent to a cloud provider (Modal) and have it executed on a cron schedule. Additionally, a local setup is also provided.

## Run locally

```shell
python deployment/local_runner.py
```

## Run on the cloud

We suggest using Modal (modal.com) for deploying the agents for its simplicity. We don't use Modal in production.

For deploying on Modal, follow the steps below:
- Create account (https://modal.com/)
- Install modal, setup auth key
```bash
pip install modal
python3 -m modal setup
```
- Run
```shell
modal deploy --name execute_agent cron_runner.py
```

# Todo
- Improve README
- Define agent function
- make cron_runner and local_runner call same function (from agent)
