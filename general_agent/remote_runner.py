import os
import pathlib

from modal import Image, App, Period
from modal.secret import Secret

from general_agent.main import main

# Loading env and poetry files
dir_path = os.path.dirname(os.path.realpath(__file__))
path_to_pyproject_toml = pathlib.Path(dir_path).parent.joinpath("pyproject.toml")
path_to_env = pathlib.Path(dir_path).parent.joinpath(".env")

image = Image.debian_slim().poetry_install_from_file(
    poetry_pyproject_toml=path_to_pyproject_toml.as_posix()
)

app = App(image=image)


@app.function(
    schedule=Period(minutes=5), secrets=[Secret.from_dotenv(path_to_env.as_posix())]
)
def execute_remote() -> None:
    main()