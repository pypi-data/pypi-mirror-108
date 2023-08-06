# rost

A simple static site generator based on [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) with a command line interface build using [Click](https://click.palletsprojects.com/en/7.x/).

## Installation

Use the following command to install `rost`:

```console
$ python3 -m pip install rost
```

### Living on the edge

If you want to work with the latest code before it’s released, install or update the code from the `main` branch:

```console
$ python3 -m pip install -U git+https://github.com/Robert-96/rost.git
```

## Quickstart

If you’re just looking to render simple data-less templates, you can get up and running with the command line:

```
$ rost build
```

This will recursively search `./templates` for templates (any file whose name does not start with `.` or `_`) and build them to `./dist`.

To monitor your source directory for changes, recompile files if they change, and start a webserver use watch:

```
$ rost watch
```

The `build` and `watch` each take these common options:

* `--searchpath`: Sets the directory to look in for templates.
* `--outputpath`: Sets the directory to place rendered files in.
* `--staticpath` (is accepted multiple times): The directory (or directories) within searchpath where static files (such  as CSS and JavaScript) are stored.

Getting help on version, available commands, arguments or option names:

```
$ rost --version
$ rost --help
$ rost build --help
$ rost watch --help
```

## Advanced Usage

This part of the documentation covers some of `rost`’s more advanced features.

### Using Custom Build Scripts

The command line shortcut is convenient, but sometimes your project needs something different than the defaults. To change them, you can use a build script.

A minimal build script looks something like this:

```py
# build.py

from rost import build


if __name__ == "__main__":
    build(
        searchpath="templates",
        outputpath="dist",
        staticpaths=["static"]
    )

```

Finally, just save the script as build.py (or something similar) and run it with your Python3 interpreter.

```
$ python3 build.py
```

### Loading Data

The simplest way to supply data to the template is to pass a mapping from variable names to their values (a *“context”*) as the `context` keyword argument to the `build` or `watch` functions.

```py
# build.py

from rost import build


# A context that should be available all the time to all templates.
context = {
    "title": "Rost Example"
}


if __name__ == "__main__":
    build(
        searchpath="templates",
        outputpath="dist",
        staticpaths=["static"],
        context=context
    )

```

If you want to pass data to a specific template you can use the `contexts` keyword argument off the `build` and `watch` functions.

```py
# build.py

from rost import build


# A context that should be available all the time to all templates.
context = {
    "title": "Rost Example"
}

# A list of "regex, context" pairs. Each context is either a dictionary or a
# function that takes either no argument or or the current template as its sole
# argument and returns a dictionary. The regex, if matched against a filename,
# will cause the context to be used.
contexts = [
    ("*.html", {}),
]


if __name__ == "__main__":
    build(
        searchpath="templates",
        outputpath="dist",
        staticpaths=["static"],
        context=context,
        contexts=contexts
    )

```

### Custom Filters

Inside the templates variables can be modified by [filters](https://jinja.palletsprojects.com/en/2.11.x/templates/#filters). All the standard Jinja2 filters are supported (you can found the full list [here](https://jinja.palletsprojects.com/en/2.11.x/templates/#builtin-filters)). To add your own filters, simply pass your as the `filters` keyword argument to the `build` and `watch` functions.

```py
# build.py

from rost import build


filters = {
    "hello": lambda x: "Hello, {}!".format(x)
}


if __name__ == "__main__":
    build(
        searchpath="templates",
        outputpath="dist",
        staticpaths=["static"],
        filters=filters
    )

```

Then you can use them in your template as you would expect:

```
{{ 'World'|hello }}
```

## License

This project is licensed under the [MIT License](LICENSE).