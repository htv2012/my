import pathlib

from fabric import Connection, task

from tools import banner


def iter_repos(c: Connection):
    repos = []
    for d in ["~", "~/Projects"]:
        res = c.run(
            f"find {d} -mindepth 2 -maxdepth 2 -type d -name .git", hide=True, warn=True
        )
        for p in res.stdout.strip().splitlines():
            repos.append(pathlib.Path(p).parent)
    return repos


def execute(c: Connection, cmd: str, repo: str, predicate):
    with c.cd(repo):
        res = c.run(cmd, hide=True, warn=True)
    if predicate(res):
        banner(c, repo)
        if res.stderr:
            print(res.stderr.strip())
            print("---")
        print(res.stdout)


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
            res = c.run("git branch --show-current", hide=True)
            branch[str(repo)] = res.stdout.strip()
    max_width = max(map(len, branch))
    print("Repo".ljust(max_width), "Branch")
    print("-" * max_width, "------")
    for repo, branch_name in branch.items():
        print(f"{repo:<{max_width}} {branch_name}")


@task
def pull(c: Connection):
    for repo in iter_repos(c):
        execute(c, "git pull", repo, lambda res: "up to date" not in res.stdout)


@task
def push(c: Connection):
    for repo in iter_repos(c):
        execute(c, "git push", repo, lambda res: "up-to-date" not in res.stderr)


@task
def status(c: Connection):
    for repo in iter_repos(c):
        execute(c, "git status --porcelain", repo, lambda res: res.stdout)
