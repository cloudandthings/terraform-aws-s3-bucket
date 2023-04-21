# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change.

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Development environment

### With Dev Containers
We suggest using [VSCode](https://code.visualstudio.com/) and [Visual Studio Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) to build a local, isolated development environment.

You will need to have [Docker](https://www.docker.com/) installed.

Simply open this project in a remote container to get started.

### Without Dev Containers
If not using a containerised development environment, you will need to ensure that your local environment is correctly configured. A rough guide is shown below.

#### System-wide configuration
1. Install general binaries required, such as Terraform and Python 3. Review `terraform.tf` and the `.github` workflows for an idea of which versions to use. You may want to use [tfenv](https://github.com/tfutils/tfenv) and (pyenv)[https://github.com/pyenv/pyenv] for switching between different versions if working on several projects.
1. Install [pre-commit](https://pre-commit.com/).
1. Install binaries needed by pre-commit hooks. Review `.pre-commit-config.yaml` for a complete list.

Examples of required binaries include:
   - [terraform-docs](https://terraform-docs.io/)
   - [TFLint](https://github.com/terraform-linters/tflint)
   - [tfsec](https://github.com/aquasecurity/tfsec)

#### Repository / workspace configuration
1. Create and develop in a Python virtual environment, with `python3 -m venv .venv && source .venv/bin/activate`
1. Install `requirements.txt` into the virtual environment, with `pip install -r requirements.txt`
1. Install pre-commit hooks specific to this repository, with `pre-commit install`.

### Reducing clutter
To improve focus while developing, you may want to configure VSCode to hide all files beginning with `.` from the Explorer view. These files are typically related to low-level environment configuration. To do so, you could add `"**/.*"` to the `files.exclude` setting.

## Pull Request Process

1. Update the code, examples and/or documentation where appropriate.
1. Ideally, follow [conventional commits](https://www.conventionalcommits.org/) for your commit messages.
1. Locally run pre-commit hooks `pre-commit run -a`
1. Locally run tests via `pytest`
1. Create pull request
1. Once all checks pass, notify a reviewer.

Once all outstanding comments and checklist items have been addressed, your contribution will be merged! Merged PRs will be included in the next release. The terraform-aws-vpc maintainers take care of updating the CHANGELOG as they merge.

## Checklists for contributions

- [ ] Add [semantics prefix](#semantic-pull-requests) to your PR or Commits (at least one of your commit groups)
- [ ] CI tests are passing
- [ ] README.md has been updated after any changes to variables and outputs. See https://github.com/cloudandthings/terraform-aws-clickops-notifer/#doc-generation
- [ ] Run pre-commit hooks `pre-commit run -a`

## Semantic Pull Requests

To generate changelog, Pull Requests or Commits must have semantic and must follow conventional specs below:

- `feat:` for new features
- `fix:` for bug fixes
- `improvement:` for enhancements
- `docs:` for documentation and examples
- `refactor:` for code refactoring
- `test:` for tests
- `ci:` for CI purpose
- `chore:` for chores stuff

The `chore` prefix skipped during changelog generation. It can be used for `chore: update changelog` commit message by example.
