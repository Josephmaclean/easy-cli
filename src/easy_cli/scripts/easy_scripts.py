import importlib
import importlib.util
import os
import pathlib
import typing

import click
from cookiecutter.main import cookiecutter

from ..resources import create_model, create_repository


@click.group()
def cli():
    pass


@cli.group()
def generate():
    pass


@cli.command("scaffold")
@click.argument("output_dir", required=False)
def scaffold(output_dir: str):

    if output_dir is None:
        val = click.prompt("Project name")
        cookiecutter("https://github.com/Josephmaclean/easy-scaffold.git",
                     extra_context={
                         "_project_name": val
                     })
    else:
        cookiecutter("https://github.com/Josephmaclean/easy-scaffold.git",
                     output_dir=output_dir,
                     extra_context={
                         "_project_name": "My Awesome App",
                         "_remove_parent": True
                     })


@generate.command("model")
@click.argument("name")
def generate_model(name: str):
    config = get_config()
    if config:
        try:
            db_engine = config.DB_ENGINE
            if db_engine == "mongodb":
                create_model(os.path.join(os.getcwd(), 'app'), name, is_sql=False)
                create_repository(os.path.join(os.getcwd(), 'app'), f"{name}_repository", is_sql=False)
            else:
                create_model(os.path.join(os.getcwd(), 'app'), name)
                create_repository(os.path.join(os.getcwd(), 'app'), f"{name}_repository")

            click.echo(click.style(f"{name} model and repository created successfully", fg="bright_green"))
        except AttributeError:
            click.echo(click.style("DB_ENGINE not set", fg="red"))


def get_config():
    config_path = os.path.join(os.getcwd(), "config.py")
    path = pathlib.Path(config_path)
    if not path.is_file():
        click.echo("cannot generate resource here")
        return None

    try:
        spec = importlib.util.spec_from_file_location("config", config_path)
        config_file: typing.Any = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_file)
        config = config_file.Config()
        return config
    except AttributeError:
        click.echo(
            click.style(
                "Could not import <class Config> from config.py. "
                "Please make sure the class 'Config' exists in config.py",
                fg="red"
            )
        )
        return None


if __name__ == "__main__":
    cli()
