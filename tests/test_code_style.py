import pylint.lint
import mypy.api


def test_pylint():
    args = ["--disable=R0903",  # too-few-public-methods
            "dui"]
    assert 0 == pylint.lint.Run(args, exit=False).linter.msg_status


def test_mypy():
    out, err, result = mypy.api.run(["dui", "--strict"])
    print(out)
    print(err)
    assert 0 == result
