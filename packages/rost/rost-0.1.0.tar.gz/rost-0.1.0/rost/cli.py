import click
from click_help_colors import HelpColorsGroup

from .generator import Rost


ASCI_ART = """\

  RRRRRRRRRRRRRRRRR                                              tttt
  R::::::::::::::::R                                          ttt:::t
  R::::::RRRRRR:::::R                                         t:::::t
  RR:::::R     R:::::R                                        t:::::t
    R::::R     R:::::R   ooooooooooo       ssssssssss   ttttttt:::::ttttttt
    R::::R     R:::::R oo:::::::::::oo   ss::::::::::s  t:::::::::::::::::t
    R::::RRRRRR:::::R o:::::::::::::::oss:::::::::::::s t:::::::::::::::::t
    R:::::::::::::RR  o:::::ooooo:::::os::::::ssss:::::stttttt:::::::tttttt
    R::::RRRRRR:::::R o::::o     o::::o s:::::s  ssssss       t:::::t
    R::::R     R:::::Ro::::o     o::::o   s::::::s            t:::::t
    R::::R     R:::::Ro::::o     o::::o      s::::::s         t:::::t
    R::::R     R:::::Ro::::o     o::::ossssss   s:::::s       t:::::t    tttttt
  RR:::::R     R:::::Ro:::::ooooo:::::os:::::ssss::::::s      t::::::tttt:::::t
  R::::::R     R:::::Ro:::::::::::::::os::::::::::::::s       tt::::::::::::::t
  R::::::R     R:::::R oo:::::::::::oo  s:::::::::::ss          tt:::::::::::tt
  RRRRRRRR     RRRRRRR   ooooooooooo     sssssssssss              ttttttttttt

"""

CONTEXT_SETTINGS = dict(help_option_names=["--help", "-h"])


searchpath = click.option(
    "--searchpath", type=click.Path(exists=True, file_okay=False),
    default="templates/", show_default=True,
    help="The directory to look in for templates.")

outputpath = click.option(
    "--outputpath", type=click.Path(exists=False, file_okay=False),
    default="dist/", show_default=True,
    help="The directory to place rendered files in.")

staticpath = click.option(
    "--staticpath", "staticpaths", type=click.Path(exists=False),
    default=("static/", ), show_default=True, multiple=True,
    help="The directory (or directories) within searchpath where static files (such as CSS and JavaScript) are stored.")


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options


@click.group(
    context_settings=CONTEXT_SETTINGS,
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="green"
)
@click.version_option(None, "--version", "-v")
def cli():
    """A simple static site generator based on Jinja2 with a CLI build using Click."""

    click.secho(ASCI_ART, fg="bright_black", bold=True)


@cli.command()
@add_options([
    searchpath,
    outputpath,
    staticpath
])
def build(searchpath, outputpath, staticpaths):
    """Build the project."""

    click.echo("  Searchpath:  {}".format(click.style(searchpath, fg="blue", bold=True)))
    click.echo("  Outputpath:  {}".format(click.style(outputpath, fg="blue", bold=True)))
    click.echo("  Staticpaths: {}".format(", ".join([click.style(path, fg="blue", bold=True) for path in staticpaths])))
    click.echo("")

    click.secho("  Build project...", bold=True, fg="bright_black")

    rost = Rost(searchpath=searchpath, outputpath=outputpath, staticpaths=staticpaths)
    rost.build()

    click.secho("  Project successfully build.\n", bold=True, fg="green")


@cli.command()
@add_options([
    searchpath,
    outputpath,
    staticpath
])
def watch(searchpath, outputpath, staticpaths):
    """Start an development server and re-build the project if the source directory for change."""

    def before_callback(*args, **kwargs):
        click.echo()
        click.secho("  Build project...", bold=True, fg="bright_black")

    def after_callback(*args, **kwargs):
        click.secho("  Successfully build.\n", bold=True, fg="green")

    monitorpaths = [searchpath]

    click.secho("  Start monitoring:", bold=True, fg="bright_black")
    for path in monitorpaths:
        click.secho("   * {}".format(path), bold=True, fg="cyan")
    click.echo()

    bind = "localhost"
    port = 8080
    url = "http://{}:{}/".format(bind, port)

    click.secho("  Serving on {}".format(click.style(url, fg="cyan")), bold=True, fg="bright_black")
    click.secho("  Press Ctrl + C to stop...", bold=True, fg="bright_black")

    rost = Rost(searchpath=searchpath, outputpath=outputpath, staticpaths=staticpaths,
                before_callback=before_callback, after_callback=after_callback)
    rost.watch(monitorpaths=monitorpaths, bind=bind, port=port)

    click.secho()
    click.secho("  Server closed.", bold=True, fg="bright_black")
    click.secho("  File monitor closed.", bold=True, fg="bright_black")
    click.secho()


if __name__ == "__main__":
    cli()
