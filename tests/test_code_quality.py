import io
import contextlib
from pathlib import Path
from multiprocessing import Pool
from collections import namedtuple

import pytest
import mypy.api
import mccabe
from pylint import epylint

import synopse


ProjectPath = Path(synopse.__name__)
Complexity = namedtuple("Complexity", "position, function, value")


def iter_py_files(folder):
    for pyfile in Path(folder).glob('**/*.py'):
        yield pyfile


@pytest.mark.last
def test_pylint():
    folders = {
        ProjectPath: ["--disable=too-few-public-methods",
                      "--const-naming-style=PascalCase"],
        "tests": ["--disable=too-few-public-methods",
                  "--disable=missing-docstring",
                  "--disable=no-self-use",
                  "--disable=misplaced-comparison-constant",
                  "--const-naming-style=PascalCase"]
    }

    success = True
    pool = Pool()
    for folder, args in folders.items():
        files_and_args = ((str(filename), args)
                          for filename in iter_py_files(folder))
        success &= all(
            result == 0
            for result in pool.starmap(epylint.lint, files_and_args)
        )
    assert success


def get_complexities_of_module(filename):
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        mccabe.main(["-m0", filename])
    return (Complexity(line.split()[0], line.split()[1], int(line.split()[2]))
            for line in output.getvalue().split("\n") if line)


def test_complexity():
    complexities = []
    for filepath in iter_py_files(ProjectPath):
        complexities.extend(get_complexities_of_module(str(filepath)))

    print()
    for complexity in sorted(complexities,
                             key=lambda c: c.value,
                             reverse=True):
        print(complexity)
    assert 5 >= max(complexity.value for complexity in complexities)


def test_mypy():
    out, err, result = mypy.api.run(["{}/".format(ProjectPath), "--strict"])
    print(out)
    print(err)
    assert not result
