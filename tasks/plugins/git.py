import pathlib

from fabric import Connection, task

from tools import banner


def iter_repos(c: Connection):
    roots = ["~", "~/Projects", "~/code"]
    roots = (p for d in roots if (p := pathlib.Path(d).expanduser()).is_dir())
    all_dirs = (p for root in roots for p in root.glob("*"))
    repos = (path for path in all_dirs if (path / ".git").is_dir())
    yield from repos


@task
def ls(c: Connection):
    banner("Repositories")
    for repo in iter_repos(c):
        print(repo)


@task
def branch(c: Connection):
    banner("Branch")
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
        banner(repo)
        c.run("git pull")


@task
def status(c: Connection):
    for repo in iter_repos(c):
        with c.cd(repo):
            res = c.run("git status --porcelain", hide=True)
        if res.stdout:
            banner(repo)
            print(res.stdout)
