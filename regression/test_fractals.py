import os
from pathlib import Path

from pyfractals import fractals


expected_directory = os.path.join(os.path.dirname(__file__), 'expected')


def generate(output_directory: str) -> None:
    for fractal_name, fractal_function in fractals.FRACTALS.items():
        fractal_function(output_file=os.path.join(output_directory, f"{fractal_name}.gif"))


def test_regression(tmpdir: Path) -> None:
    tmpdir = str(tmpdir)
    generate(tmpdir)
    for file in os.listdir(tmpdir):
        with open(os.path.join(tmpdir, file), 'rb') as f:
            actual = f.read()
        with open(os.path.join(expected_directory, file), 'rb') as f:
            expected = f.read()
        assert actual == expected, file


if __name__ == '__main__':
    generate(expected_directory)
