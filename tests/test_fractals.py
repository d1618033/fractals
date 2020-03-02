import pytest

from pyfractals.fractals import Generator


@pytest.fixture
def generator() -> Generator:
    return Generator("F", {"F": "+F−−F+"})


def test_generator_update(generator: Generator) -> None:
    assert generator.current == "F"
    generator.update()
    assert generator.current == "+F−−F+"
