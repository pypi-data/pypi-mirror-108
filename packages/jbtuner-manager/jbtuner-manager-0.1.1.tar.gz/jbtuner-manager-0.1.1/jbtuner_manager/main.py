import json
from enum import Enum
from json import JSONDecodeError
from typing import Optional

import typer
from ampy import pyboard
from ampy import files

from jbtuner_manager import __version__

app = typer.Typer()


class JbtDevices(str, Enum):
    lab = "lab"
    hptest = "hptest"
    preprod = "preprod"


def version_callback(value: bool):
    if value:
        typer.secho(f"CLI Version: {__version__}", fg=typer.colors.MAGENTA)
        raise typer.Exit()


# Main command
@app.callback()
def main(
        _version: Optional[bool] = typer.Option(
            None, "--version", "-v", callback=version_callback, is_eager=True
        ),
):
    """
    ====================================================================\t
    JB Tuner manager - An integrated tool for managing Chord X JB Tuners\t
    ====================================================================\t
    """
    typer.echo(f"Welcome to use JB Tuner manager {__version__}\n")


@app.command()
def read(
        name: JbtDevices = typer.Argument(..., help="the name of JB Tuner"),
        out: Optional[str] = typer.Option(None, "--out", "-o", help="A local filename to save config"),
):
    try:
        port = f"/dev/ttyJBT_{name}"
        _board = pyboard.Pyboard(port, baudrate=115200, rawdelay=0.5)
        board_files = files.Files(_board)
        typer.echo(f"Connected to JB Tuner [{name}]")
    except Exception:
        typer.echo(f"Please check if JB Tuner [{name}] is connected?")
        raise typer.Exit(1)
    typer.echo("Reading config file")
    typer.echo("------(start of config)")
    try:
        f = board_files.get("config.json")
        typer.echo(f)
    except Exception:
        typer.echo("Cannot read config file")
        raise typer.Exit(1)
    typer.echo("------(end of config)")
    if f and out:
        with open(out, "wb") as outfile:
            outfile.write(f)
        typer.echo(f"Saved to {out}")


@app.command()
def write(
        name: JbtDevices = typer.Argument(..., help="the name of JB Tuner"),
        config: str = typer.Option("config.json", "--config", "-f", help="the name of config file"),
        rpm: Optional[int] = typer.Option(None, "--rpm", help="Set RPM value"),
):
    try:
        port = f"/dev/ttyJBT_{name}"
        _board = pyboard.Pyboard(port, baudrate=115200, rawdelay=0.5)
        board_files = files.Files(_board)
        typer.echo(f"Connected to JB Tuner [{name}]")
    except Exception:
        typer.echo(f"Please check if JB Tuner [{name}] is connected?")
        raise typer.Exit(1)

    if rpm:
        try:
            typer.echo(f"Change RPM to {rpm}")
            with open(config, "r") as f:
                j = json.load(f)
                j["rpm"] = rpm
            with open(config, "w") as f:
                json.dump(j, f, indent=4)
        except (FileNotFoundError, JSONDecodeError) as ex:
            typer.echo(f"Fail to change RPM in local file: {config}")
            raise typer.Exit(1)

    try:
        typer.echo("Upload config file")
        with open(config, "rb") as infile:
            remote_filename = "config.json"
            board_files.put(remote_filename, infile.read())
    except Exception:
        typer.echo("Fail to upload config file.")
        raise typer.Exit(1)
    try:
        typer.echo("Reboot device...")
        _board.enter_raw_repl()
        _board.exec_raw_no_follow("import machine; machine.reset()")
        _board.exit_raw_repl()
        typer.echo("Done.")
    except Exception:
        typer.echo("Fail to reboot device.")
        raise typer.Exit(1)


@app.command()
def reboot(
        name: JbtDevices = typer.Argument(..., help="the name of JB Tuner"),
):
    try:
        port = f"/dev/ttyJBT_{name}"
        _board = pyboard.Pyboard(port, baudrate=115200, rawdelay=0.5)
        # board_files = files.Files(_board)
        typer.echo(f"Connected to JB Tuner [{name}]")
    except Exception:
        typer.echo(f"Please check if JB Tuner [{name}] is connected?")
        raise typer.Exit(1)
    try:
        typer.echo("Reboot device...")
        _board.enter_raw_repl()
        _board.exec_raw_no_follow("import machine; machine.reset()")
        _board.exit_raw_repl()
        typer.echo("Done.")
    except Exception:
        typer.echo("Fail to reboot device.")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
