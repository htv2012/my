
from fabric import Connection, task
from invoke.runners import Result

from tools import banner

HOME_DIR = None


def get_home_dir(c: Connection) -> str:
    global HOME_DIR
    if HOME_DIR is None:
        res = c.run("echo $HOME", hide=True)
        HOME_DIR = res.stdout.strip()
    return HOME_DIR


def is_repo(c: Connection, name: str) -> bool:
    res = c.run(f"test -d '{name}/.git'", hide=True, warn=True)
    return res.ok


def list_dir(c: Connection, path: str):
    with c.cd(path):
        res = c.run("/bin/ls", hide=True, warn=True)

    if res.failed:
        return []
    return res.stdout.splitlines()


def iter_repos(c: Connection):
    home_dir = get_home_dir(c)
    my_dir = f"{home_dir}/my"
    repos = [my_dir]

    projects_dir = f"{home_dir}/Projects"
    repos.extend(f"{projects_dir}/{d}" for d in list_dir(c, projects_dir))

    repos = [repo for repo in repos if is_repo(c, repo)]
    return repos


def print_result(result: Result):
    if result.stderr:
        print(result.stderr)
    if result.stdout:
        print(result.stdout)


@task
def ls(c: Connection):
    banner(c, "Repositories")
    home_dir = get_home_dir(c)
    for repo in iter_repos(c):
        print(repo.replace(home_dir, "~"))


@task
def branch(c: Connection):
    banner(c, "Branch")
    home_dir = get_home_dir(c)
    branch = {}
    for repo in iter_repos(c):
        with c.cd(repo):
            result = c.run("git branch --show-current", hide=True)
            branch[repo.replace(home_dir, "~")] = result.stdout.strip()
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
