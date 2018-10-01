import io
import contextlib
from pathlib import Path
from multiprocessing import Pool

import pytest
import mypy.api
import mccabe
from pylint import epylint


import synopse


ProjectPath = Path(synopse.__name__)


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


def test_complexity():
    def test_complexity_on_module(filename, complexity):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            mccabe.main(["-m", str(complexity), filename])
        output = output.getvalue()
        if output:
            print(filename)
            print(output)
            print()
            return False
        return True

    success = True
    for filepath in iter_py_files(ProjectPath):
        success &= test_complexity_on_module(str(filepath), 6)
    assert success


def test_mypy():
    out, err, result = mypy.api.run(["{}/".format(ProjectPath), "--strict"])
    print(out)
    print(err)
    assert not result
