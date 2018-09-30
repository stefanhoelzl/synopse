import io
import contextlib
from pathlib import Path

from pylint import epylint
import mypy.api
import mccabe


ProjectName = "pricky"


def test_pylint():
    args = ["--disable=too-few-public-methods",
            "--const-naming-style=PascalCase"]
    assert not epylint.lint(ProjectName, args)


def test_pylint_tests():
    args = ["--disable=too-few-public-methods",
            "--disable=missing-docstring",
            "--disable=no-self-use",
            "--disable=misplaced-comparison-constant",
            "--const-naming-style=PascalCase"]
    assert not epylint.lint(".", args)


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
    for filename in Path(ProjectName).glob('**/*.py'):
        success &= test_complexity_on_module(str(filename), 6)
    assert success


def test_mypy():
    out, err, result = mypy.api.run(["{}/".format(ProjectName), "--strict"])
    print(out)
    print(err)
    assert not result
