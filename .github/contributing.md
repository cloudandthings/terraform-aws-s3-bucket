# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change.

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Development environment

### Dev containers
We suggest using [Visual Studio Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) to build a local, isolated development environment.

Simply open this project in a remote container to get started.

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
