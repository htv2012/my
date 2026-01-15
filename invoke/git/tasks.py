import pathlib

from invoke import task, Context


def banner(text: str):
    print(f"\n#\n# {text}\n#")


def show(dir: str, res):
    if res.exited == 0:
        if res.stdout:
            banner(dir)
            print(res.stdout)
    else:
        banner(dir)
        print(res.stdout)
        print("-" * 80)
        print(res.stderr)


def list_repos():
    home = pathlib.Path.home()
    yield home / "my"

    projects = pathlib.Path("~/Projects").expanduser()
    for dir_ in projects.rglob(".git"):
        yield dir_.parent


@task
def pull(c: Context, dir: str ="."):
    with c.cd(dir):
        res = c.run("git pull", hide=True)
        show(dir, res)

@task
def status(c, dir="."):
    with c.cd(dir):
        res = c.run("git status --short", hide=True)
        if res.exited == 0:
            show(dir, res)


@task
def status_all(c):
    for repo in list_repos():
        status(c, repo)


@task
def push(c):
    c.run("git push")


@task
def repos(c):
    for dir_ in list_repos():
        print(dir_)
