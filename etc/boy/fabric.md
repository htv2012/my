# Getting Started

```python
import fabric

with fabric.Connection(host="primary") as connection:
    # Run and suppress (hide) the output
    result = connection.run("whoami", hide=True)
    user = result.stdout.strip()
    print(f"{user=}")
```

---

# Connection Object

## Common keywords for `__init__`:

- host (required)
- user
- port
- config
- gateway
- ssh_config
- connect_timeout
- connect_kwargs

## Common Attributes

- host
- user
- port
- is_connected
- ssh_config


## Common Methods

| Method                                          | Description                    |
|-------------------------------------------------|--------------------------------|
| `get(remote, local=None, preserve_mode=True)`   | Download                       |
| `local(local, remote=None, preserve_mode=True)` | Run a command locally          |
| `put(*args, **kwargs)`                          | Upload                         |
| `run(command, **kargs)`                         | Run a command, return a result |
| `sftp()`                                        | Opens a SFTP connection        |
| `sudo(command, **kargs)`                        | Run a command as root          |

## Common run() args

| Argument | Description                                                       |
|----------|-------------------------------------------------------------------|
| `command`  | str                                                               |
| `hide`     | True (or 'both'), 'stdout', or 'stderr'. Hide output from console |
| `env`      | dict. Environment                                                 |
| `timeout`  | int                                                               |
| `warn`     | bool. Default: False. If True, do not raise on non-zero exit code |

---

# Result Object

Returned by the `Connection.run()` method

## Common Attributes

- failed: bool
- ok: bool
- return_code: int
- stdout: str
- stderr: str

This object implements the `__bool__` method, which returns the same as `.ok`:

```python
result = connection.run(..., warn=True)
if result:
    print("OK")
else:
    print("Bad command")
```
