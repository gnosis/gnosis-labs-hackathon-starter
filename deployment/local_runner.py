import modal

from deployment.agent import run

app = modal.App(
    "example-get-started"
)  # Note: prior to April 2024, "app" was called "stub"


@app.function()
def execute():
    run()


@app.local_entrypoint()
def main():
    execute.local()