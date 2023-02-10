# What to test

At the very least, major new features or changes should ideally be covered by appropriate tests.

It is probably less useful to test functionality that can be taken "for granted" by the underlying AWS Service, as this can usually be assumed to work. However, complex functionality should be tested to ensure there is a repeatable working implementation and to illustrate how it works.

# Why test?

There are several benefits to having test coverage of any module. These include:

- Ensure the module behaves as we expect, by verifying it against actual AWS resources, before rolling out changes to customers.
- Provide confidence in the code review process that changes have an intended effect. Also, provide the code reviewer with a way to easily verify a change by pulling the branch and running tests themselves.
- Ensure that changes to the module do not break existing functionality that is covered by tests, and which customers might be using now.
- Ensure that bug fixes are permanent, by covering them with tests.
- Help illustrate how to use the module via tests, and also how not to use the module.
- Provide a single, simple place to assess if all important functionality is still working. External changes eg upgrades can be tested for impact by running these tests.

# How to test

## Setup test environment
To run the tests, first create a test environment.

1. Create a Python virtual environment

```sh
python3 -m venv .venv
```

2. Activate your Python virtual environment

Activate / enter your virtual environment whenever you wish to test.

```sh
##  Examples to activate Python virtual environment
# Linux / Mac
source .venv/bin/activate
# Windows
.venv\Scripts\Activate.ps1
```

> VSCode can automatically activate the Python virtual environment for terminals it creates. Just set `Select Python Interpreter` as .venv/Scripts\python.exe or similar.

3. Install test environment dependencies

```sh
pip install -r requirements.txt
```

## Execute tests

To execute the tests you will need valid AWS credentials, and sufficient access to execute the actions needed by the tests.

The example below uses the profile `<your_profile>`.

```sh
aws sso login --profile <your_profile>
```

To run tests using this profile:

```sh
pytest --profile <your_profile>
```

## Maintain tests

Periodically review the template framework in the [terraform-aws-template](https://github.com/cloudandthings/terraform-aws-template) and ensure this project is kept up to date.
