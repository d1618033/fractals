"""Generate fractal gifs"""

import math
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from typing import Callable, Dict, List

import matplotlib.pyplot as plt


def _get_limits(elements: List[float]) -> List[float]:
    min_, max_ = min(elements), max(elements)
    distance = (abs(max_ - min_)) ** 0.5
    eps = 1e-7
    return [min_ - distance - eps, max_ + distance + eps]


@dataclass
class Point:
    x: float
    y: float


class Turtle:
    """Implements turtle graphics"""

    _DEFAULT_STARTING_POINT = Point(0, 0)
    _DEFAULT_STARTING_DIRECTION = Point(-1, 0)

    def __init__(self) -> None:
        self.current = self._DEFAULT_STARTING_POINT
        self.all_points: List[Point] = []
        self.direction = self._DEFAULT_STARTING_DIRECTION

    def draw(self, steps: int) -> None:
        """draws from current to new by direction and number of steps"""
        self.current = Point(
            self.current.x + steps * self.direction.x,
            self.current.y + steps * self.direction.y,
        )
        self.all_points.append(self.current)

    def turn(self, degrees: float) -> None:
        """rotates the drawer object clockwise a given number of degrees"""
        rad = degrees / 180 * math.pi
        # rotation tranformation
        x, y = self.direction.x, self.direction.y
        self.direction = Point(
            x * math.cos(rad) - y * math.sin(rad),
            x * math.sin(rad) + y * math.cos(rad),
        )

    @property
    def all_x(self) -> List[float]:
        return [point.x for point in self.all_points]

    @property
    def all_y(self) -> List[float]:
        return [point.y for point in self.all_points]

    def clear(self) -> None:
        self.current = self._DEFAULT_STARTING_POINT
        self.all_points = []
        self.direction = self._DEFAULT_STARTING_DIRECTION


class Drawer:
    def plot(self, turtle: Turtle) -> None:
        plt.xlim(_get_limits(turtle.all_x))
        plt.ylim(_get_limits(turtle.all_y))
        plt.axis("off")
        plt.plot(turtle.all_x, turtle.all_y, "b-")

    def save(self, file_name: str) -> None:
        plt.savefig(file_name)

    def clear(self) -> None:
        plt.clf()


# pylint: disable=too-few-public-methods
class Generator:
    """class for generating L system style fractals"""

    def __init__(self, start: str, rules: Dict[str, str]):
        """initializes a generator object
        start- the first string
        rules- update rules. a dictionary mapping variables to their update"""
        self.rules = rules
        self.current = start

    def update(self) -> None:
        """updates the string once"""
        self.current = "".join(
            [
                self.rules[character] if character in self.rules else character
                for character in self.current
            ]
        )


@dataclass
class Fractal:
    start: str
    rules: Dict[str, str]
    methods: Dict[str, Callable[[], None]]
    name: str


def parse(string: str, fractal: Fractal) -> None:
    """
    Parses a L system string
    string- the string to parse
    methods- a dictionary mapping each character in
    string to a function"""
    for character in string:
        fractal.methods[character]()


def fractal_gif(fractal: Fractal, num_iterations: int, turtle: Turtle) -> None:
    """creates a fractal picture for every stage"""
    generator = Generator(fractal.start, fractal.rules)
    all_files = []
    drawer = Drawer()
    with tempfile.TemporaryDirectory() as tempdir:
        for i in range(num_iterations):
            generator.update()
            string = generator.current
            parse(string, fractal)
            drawer.plot(turtle)
            for j in range(5 if i == num_iterations - 1 else 1):
                file_name = os.path.join(tempdir, f"{fractal.name}{i + j}.png")
                all_files.append(file_name)
                drawer.save(file_name)
            drawer.clear()
            turtle.clear()
        subprocess.check_call(
            ["convert", "-delay100", "-loop0 ", *all_files, f"{fractal.name}.gif"]
        )


def ccurve() -> None:
    start = "F"
    rules = {"F": "+F--F+"}
    num_iterations = 12
    drawer = Turtle()
    methods = {
        "F": lambda: drawer.draw(1),
        "+": lambda: drawer.turn(45),
        "-": lambda: drawer.turn(315),
    }
    fractal = Fractal(start=start, rules=rules, methods=methods, name="ccurve")
    fractal_gif(fractal, num_iterations, drawer)


def sierpinski() -> None:
    start = "A"
    rules = {"A": "B-A-B", "B": "A+B+A"}
    num_iterations = 9
    drawer = Turtle()
    methods = {
        "A": lambda: drawer.draw(1),
        "B": lambda: drawer.draw(1),
        "+": lambda: drawer.turn(60),
        "-": lambda: drawer.turn(300),
    }
    fractal = Fractal(start=start, rules=rules, methods=methods, name="sierpinski")
    fractal_gif(fractal, num_iterations, drawer)


def dragon_curve() -> None:
    start = "FX"
    rules = {"X": "X+YF+", "Y": "-FX-Y"}
    num_iterations = 15
    drawer = Turtle()
    methods = {
        "F": lambda: drawer.draw(1),
        "-": lambda: drawer.turn(360 - 90),
        "+": lambda: drawer.turn(90),
        "X": lambda: None,
        "Y": lambda: None,
    }
    fractal = Fractal(start=start, rules=rules, methods=methods, name="dragon_curve")
    fractal_gif(fractal, num_iterations, drawer)


if __name__ == "__main__":
    if sys.argv[1] == "dragon_curve":
        dragon_curve()
    elif sys.argv[1] == "sierpinski":
        sierpinski()
    elif sys.argv[1] == "ccurve":
        ccurve()
