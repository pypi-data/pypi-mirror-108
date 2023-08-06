import unittest.mock as mock

import pytest

from rost.generator import _has_argument, Rost


def foo():
    """Test data for ``_has_argument`` tests."""


def boo(x):
    """Test data for ``_has_argument`` tests."""


@pytest.mark.parametrize(
    "func, expected",
    [
        (foo, False),
        (boo, True)
    ]
)
def test_has_arguments(func, expected):
    assert _has_argument(func) == expected


def test_context():
    context = {"title": "Rost > Unit Tests"}
    rost = Rost(context=context)

    template = mock.Mock()
    template.name = "index.html"

    actual = rost.get_context(template)

    assert actual == context


def test_contexts():
    context = {"title": "Rost", "description": "..."}
    contexts = [
        ("index.html", {"title": "Rost > Unit Tests", "name": "Rost"}),
        (".*.html", {"keywords": "HTML, Jinja2, Click"})
    ]

    rost = Rost(context=context, contexts=contexts)

    template = mock.Mock()
    template.name = "index.html"

    actual = rost.get_context(template)

    assert actual == {
        "title": "Rost > Unit Tests",
        "name": "Rost",
        "description": "..."
    }


def test_merge_contexts():
    context = {"title": "Rost", "description": "..."}
    contexts = [
        (".*.html", {"title": "Rost > Unit Tests"}),
        ("index.html", {"name": "Rost"})
    ]

    rost = Rost(context=context, contexts=contexts, merge_contexts=True)

    template = mock.Mock()
    template.name = "index.html"

    actual = rost.get_context(template)

    assert actual == {
        "title": "Rost > Unit Tests",
        "name": "Rost",
        "description": "..."
    }


@pytest.mark.parametrize(
    "template_name, expected",
    [
        ("static/style.css", True),
        ("static/main.js", True),
        ("public/img/logo.png", True),
        ("public/img/logo.svg", True),
        ("index.html", False),
        ("components/_title.html", False)
    ]
)
def test_is_static(template_name, expected):
    rost = Rost(staticpaths=["static", "public"])

    assert rost.is_static(template_name) == expected


@pytest.mark.parametrize(
    "template_name, expected",
    [
        ("components/_title.html", True),
        ("_components/title.html", True),
        ("static/style.css", False),
        ("static/main.js", False),
        ("public/img/logo.png", False),
        ("public/img/logo.svg", False),
        ("index.html", False)
    ]
)
def test_is_partial(template_name, expected):
    rost = Rost()

    assert rost.is_partial(template_name) == expected


@pytest.mark.parametrize(
    "template_name, expected",
    [
        (".git", True),
        ("components/.title.html", True),
        (".components/title.html", True),
        ("static/style.css", False),
        ("static/main.js", False),
        ("public/img/logo.png", False),
        ("public/img/logo.svg", False),
        ("index.html", False)
    ]
)
def test_is_ignored(template_name, expected):
    rost = Rost()

    assert rost.is_ignored(template_name) == expected
