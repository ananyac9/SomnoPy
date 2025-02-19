"""Console script for psg_analyser."""
import psg_analyser

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for psg_analyser."""
    console.print("Replace this message by putting your code into "
               "psg_analyser.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    


if __name__ == "__main__":
    app()
