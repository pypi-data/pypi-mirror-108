import re
import os.path

from rost.generator import Rost, build


def test_happy_flow(tmpdir):
    searchpath = "{}/example/templates".format(os.path.abspath("."))
    outputpath = "{}/dist".format(tmpdir)
    staticpaths = ["static"]

    rost = Rost(searchpath=searchpath, outputpath=outputpath, staticpaths=staticpaths)
    rost.build()

    assert os.path.isdir(searchpath)
    assert os.path.isdir(outputpath)
    assert os.path.isfile("{}/index.html".format(outputpath))

    for static in staticpaths:
        assert os.path.exists("{}/{}".format(outputpath, static))


def test_build(tmpdir):
    searchpath = "{}/example/templates".format(os.path.abspath("."))
    outputpath = "{}/dist".format(tmpdir)
    staticpaths = ["static"]

    build(searchpath=searchpath, outputpath=outputpath, staticpaths=staticpaths)

    assert os.path.isdir(searchpath)
    assert os.path.isdir(outputpath)
    assert os.path.isfile("{}/index.html".format(outputpath))

    for static in staticpaths:
        assert os.path.exists("{}/{}".format(outputpath, static))


def test_context(tmpdir):
    searchpath = "{}/example/templates".format(os.path.abspath("."))
    outputpath = "{}/dist".format(tmpdir)
    staticpaths = ["static"]

    context = {
        "title": "Rost - Integration Tests"
    }

    rost = Rost(searchpath=searchpath, outputpath=outputpath, staticpaths=staticpaths,
                context=context)
    rost.build()

    assert os.path.isfile("{}/index.html".format(outputpath))
    with open("{}/index.html".format(outputpath)) as fp:
        data = fp.read()

    match = re.search(r'<h1 id="title">Rost - Integration Tests</h1>', data)
    assert match is not None


def test_contexts(tmpdir):
    searchpath = "{}/example/templates".format(os.path.abspath("."))
    outputpath = "{}/dist".format(tmpdir)
    staticpaths = ["static"]

    context = {
        "title": "Rost - Integration Tests"
    }
    contexts = [
        ("index.html", context)
    ]

    rost = Rost(searchpath=searchpath, outputpath=outputpath, staticpaths=staticpaths,
                contexts=contexts)
    rost.build()

    assert os.path.isfile("{}/index.html".format(outputpath))
    with open("{}/index.html".format(outputpath)) as fp:
        data = fp.read()

    match = re.search(r'<h1 id="title">Rost - Integration Tests</h1>', data)
    assert match is not None


def test_filters(tmpdir):
    searchpath = "{}/tests/data/templates".format(os.path.abspath("."))
    outputpath = "{}/dist".format(tmpdir)
    staticpaths = ["static"]

    context = {
        "title": "Rost - Integration Tests"
    }
    filters = {
        "hello": lambda x: "Hello, {}!".format(x)
    }

    rost = Rost(searchpath=searchpath, outputpath=outputpath, staticpaths=staticpaths,
                context=context, filters=filters)
    rost.build()

    assert os.path.isfile("{}/index.html".format(outputpath))
    with open("{}/index.html".format(outputpath)) as fp:
        data = fp.read()

    print(data)
    match = re.search(r'<h1 id="title">Hello, Rost - Integration Tests!</h1>', data)
    assert match is not None
