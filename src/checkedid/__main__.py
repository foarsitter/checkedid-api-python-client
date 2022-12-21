"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """CheckedID Python API client."""


if __name__ == "__main__":
    main(prog_name="checkedid-python-client")  # pragma: no cover
