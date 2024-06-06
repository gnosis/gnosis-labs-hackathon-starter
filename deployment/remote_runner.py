from modal import Image, App, Period

from deployment.agent import run

image = Image.from_registry("ghcr.io/gnosis/prediction-market-agent:main").pip_install("pydantic==2.6.1")

app = App(image=image)

@app.function(schedule=Period(minutes=5))
def execute_remote():
    run()