from typing import List
from unittest import mock
from unittest.mock import call

import pytest

from pyfractals.fractals import Generator, _get_limits, Turtle, Point, Fractal, parse


@pytest.fixture
def generator() -> Generator:
    return Generator("F", {"F": "+F−−F+"})


def test_generator_update(generator: Generator) -> None:
    assert generator.current == "F"
    generator.update()
    assert generator.current == "+F−−F+"


def test_get_limits() -> None:
    assert _get_limits([0, 100]) == [pytest.approx(-10, 1e-5), pytest.approx(110, 1e-5)]


@pytest.fixture
def turtle() -> Turtle:
    return Turtle()


def test_turtle_draw(turtle: Turtle) -> None:
    turtle.draw(2)
    assert turtle.all_points == [Point(0, 0), Point(-2, 0)]


def make_approx_point(point: Point, tol: float = 1e-10) -> Point:
    return Point(pytest.approx(point.x, tol), pytest.approx(point.y, tol))


def make_approx_points(points: List[Point], tol: float = 1e-10) -> List[Point]:
    return [make_approx_point(point, tol) for point in points]


def test_turtle_turn(turtle: Turtle) -> None:
    turtle.turn(90)
    assert turtle.direction, make_approx_point(Point(0, -1))


def test_turtle_turn_and_draw(turtle: Turtle) -> None:
    turtle.turn(90)
    turtle.draw(10)
    assert turtle.all_points == make_approx_points([Point(0, 0), Point(0, -10)])


def test_turtle_clear(turtle: Turtle) -> None:
    turtle.turn(90)
    turtle.draw(10)
    turtle.clear()
    assert turtle.all_points == [Point(0, 0)]
    assert turtle.direction == Point(-1, 0)
    assert turtle.current == Point(0, 0)


@pytest.fixture
def drawer() -> mock.MagicMock:
    return mock.MagicMock()


@pytest.fixture
def fractal(drawer: mock.MagicMock) -> Fractal:
    start = "F"
    rules = {"F": "+F--F+"}
    methods = {
        "F": lambda: drawer.draw(1),
        "+": lambda: drawer.turn(45),
        "-": lambda: drawer.turn(315),
    }
    return Fractal(start=start, rules=rules, methods=methods, name="ccurve")


def test_parse(fractal: Fractal, drawer: mock.MagicMock) -> None:
    parse("+F--F+", fractal)
    assert drawer.method_calls == [
        call.turn(45),
        call.draw(1),
        call.turn(315),
        call.turn(315),
        call.draw(1),
        call.turn(45),
    ]
