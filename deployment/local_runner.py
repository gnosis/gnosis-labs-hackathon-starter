import modal

from deployment.agent import run

app = modal.App("example-get-started")


@app.function()
def execute():
    run()


@app.local_entrypoint()
def main():
    execute.local()