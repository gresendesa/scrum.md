"""Placeholder CLI entrypoint for future sprint scope."""

import typer

app = typer.Typer(
    name="smd",
    help="Scrum memory orchestration for AI-assisted development.",
    add_completion=False,
)


@app.callback()
def main() -> None:
    """Run smd commands."""
