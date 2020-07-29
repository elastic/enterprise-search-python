import nox


SOURCE_FILES = ("noxfile.py", "elastic_enterprise_search/", "utils/")


@nox.session()
def blacken(session):
    session.install("black")
    session.run("black", "--target-version=py27", *SOURCE_FILES)

    lint(session)


@nox.session
def lint(session):
    session.install("flake8", "black", "mypy")
    session.run("black", "--check", "--target-version=py27", *SOURCE_FILES)
    session.run("flake8", "--ignore=E501,W503", *SOURCE_FILES)
