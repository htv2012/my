from fabric import Connection, task


@task
def hi(c: Connection):
    print("hi")
