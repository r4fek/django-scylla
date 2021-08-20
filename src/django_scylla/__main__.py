"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Django Scylla."""


if __name__ == "__main__":
    main(prog_name="django-scylla")  # pragma: no cover
