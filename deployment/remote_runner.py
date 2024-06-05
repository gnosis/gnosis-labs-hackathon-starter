from pathlib import Path

from modal import Image, App, Period

from deployment.agent import run

#current_path = Path(__file__)
#pyproject_toml_path = current_path.parent.parent.joinpath("pyproject.toml")
#lockfile_path = current_path.parent.parent.joinpath("poetry.lock")

image = Image.from_registry("ghcr.io/gnosis/prediction-market-agent:main").pip_install("pydantic==2.6.1")

app = App(image=image)  # Note: prior to April 2024, "app" was called "stub"

@app.function(schedule=Period(minutes=5))
def execute_remote():
    run()