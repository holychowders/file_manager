# Readme

## Development

This project uses a variety of code quality tools to automatically check and enforce certain standards.

The purpose of this approach is to ensure that all code across the codebase remains consistent and maintains some baseline of quality and safety. This also ensures that the developer can be more confident in the changes they make and focus more on the important details.

`pre-commit` is the tool that will manage all of the other code quality tools. It's the only tool that will be needed to be run by the developer. Its typical use is noted below.

### Setup

- Ensure that `python` is version 3.10+
  - `python --version` -> `Python 3.1x.x`
- Create, activate and verify a virtual environment in the project's directory
  - `python -m virtualenv venv`
  - `source venv/Scripts/activate`
  - `which python` -> `project_dir/venv/Scripts/python`
- Install the development requirements
  - `python -m pip install -r requirements-dev.txt`
  - `pre-commit install`
  - `pre-commit`

### Developing

Periodically check changes for issues. Do this more frequently for larger or more complicated changes.

- Run `pre-commit` to check staged changes.
- Run `pre-commit run --all-files` to check both staged and unstaged changes.
- `git commit` will automatically cause `pre-commit` to run and will fail if all checks do not pass. Correct the issues (if not corrected automatically), re-stage, and re-attempt commit.
