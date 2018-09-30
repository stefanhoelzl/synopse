from pylint import epylint
import mypy.api


def test_pylint():
    args = ["--disable=R0903",  # too-few-public-methods
            "--const-naming-style=PascalCase"]
    assert 0 == epylint.lint("pricky", args)


def test_mypy():
    out, err, result = mypy.api.run(["pricky/", "--strict"])
    print(out)
    print(err)
    assert 0 == result
