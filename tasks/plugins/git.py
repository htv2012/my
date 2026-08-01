import pathlib

from fabric import Connection, task
from invoke.runners import Result

from tools import banner


def iter_repos(c: Connection):
    my_dir = pathlib.Path("~/my").expanduser()
    repos = [my_dir]

    for d in ["~/Projects"]:
        result = c.run(
            f"find {d} -mindepth 2 -maxdepth 2 -type d -name .git", hide=True, warn=True
        )
        for p in result.stdout.strip().splitlines():
            repos.append(pathlib.Path(p).parent)
    return repos


def print_result(result: Result):
    if result.stderr:
        print(result.stderr)
    if result.stdout:
        print(result.stdout)


@task
def ls(c: Connection):
    banner(c, "Repositories")
    for repo in iter_repos(c):
        print(repo)


@task
def branch(c: Connection):
    banner(c, "Branch")
    branch = {}
    for repo in iter_repos(c):
        with c.cd(repo):
            result = c.run("git branch --show-current", hide=True)
            branch[str(repo)] = result.stdout.strip()
    max_width = max(map(len, branch))
    print("Repo".ljust(max_width), "Branch")
    print("-" * max_width, "------")
    for repo, branch_name in branch.items():
        print(f"{repo:<{max_width}} {branch_name}")


@task
def pull(c: Connection):
    for repo in iter_repos(c):
        with c.cd(repo):
            result = c.run("git pull", hide=True, warn=True)
            if "Already up to date" in result.stdout:
                continue

            banner(c, repo)
            print_result(result)


@task
def push(c: Connection):
    for repo in iter_repos(c):
        with c.cd(repo):
            result = c.run("git push", hide=True, warn=True)
        if "Everything up-to-date" in result.stderr:
            continue

        banner(c, repo)
        print_result(result)


@task
def status(c: Connection):
    for repo in iter_repos(c):
        with c.cd(repo):
            result = c.run("git status --porcelain", hide=True, warn=True)

        if result.stderr or result.stdout:
            banner(c, repo)
        print_result(result)
