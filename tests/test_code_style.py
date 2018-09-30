from pylint import epylint
import mypy.api


def test_pylint():
    args = ["--disable=too-few-public-methods",
            "--const-naming-style=PascalCase"]
    assert not epylint.lint("pricky", args)


def test_pylint_tests():
    args = ["--disable=too-few-public-methods",
            "--disable=missing-docstring",
            "--disable=no-self-use",
            "--disable=misplaced-comparison-constant",
            "--const-naming-style=PascalCase"]
    assert not epylint.lint(".", args)


def test_mypy():
    out, err, result = mypy.api.run(["pricky/", "--strict"])
    print(out)
    print(err)
    assert not result
