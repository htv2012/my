# File Structure

```
├── features
│   ├── steps
│   │   └── tutorial.py
│   └── tutorial.feature
```

# Sample feature: features/tutorial.feature

```
Feature: showing off behave
    Scenario: run a simple test
        Given we have behave installed
         When we implement a test
         Then behave will test it for us!
```

# Sample test: features/steps/tutorial.py

```python
from behave import given, then, when


@given("we have behave installed")
def step_impl(context):  # noqa: F811
    pass


@when("we implement a test")
def step_impl(context):  # noqa: F811
    assert True


@then("behave will test it for us!")
def step_impl(context):  # noqa: F811
    assert context.failed is False
```

# How to Run

```bash
$ behave

Feature: showing off behave # features/tutorial.feature:1

  Scenario: run a simple test        # features/tutorial.feature:2
    Given we have behave installed   # features/steps/tutorial.py:4 0.000s
    When we implement a test         # features/steps/tutorial.py:9 0.000s
    Then behave will test it for us! # features/steps/tutorial.py:14 0.000s

1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 0 skipped
3 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m0.000s
```
