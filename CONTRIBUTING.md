# Contributing to Preprint3

Thanks for helping out with preprint3. The prerequisite for working on preprint3 is a [GitHub](http://github.com) account. This document provides tips on submitting bug reports, building the source code to test changes, and what to do when submitting a pull request.

## Contents

* [Submitting a Bug Report (Issues)](#submitting-a-bug-report-issues)
* [Building & Editing Preprint (Development)](#building-editing-preprint-development)
  - [Code Overview & Philosophy](#code-overview-philosophy)
  - [Building Preprint](#building-preprint)
  - [Making & Submitting Changes (Pull Request)](#making-submitting-changes-pull-request)

## Submitting a Bug Report

If preprint3 doesn't work right, *submit an [Issue](https://github.com/dotTHzTAG/preprint/issues)*.

To help us out, you'll want to rerun your preprint3 command with the `--debug` flag enabled.

When submitting an [Issue](https://github.com/dotTHzTAG/preprint/issues), mention the command or paper you're running, and copy the debugging output of the log file or terminal.

*Thank you!*




## Building & Editing Preprint

### Code Overview & Philosophy

Preprint3 is a command-line tool built around the [cliff](https://cliff.readthedocs.io/en/latest/) framework. This means each subcommand must be registered as a setuptools entry point. See [`setup.py`](https://github.com/dotTHzTAG/preprint/blob/main/setup.py) and [`preprint/make.py`](https://github.com/dotTHzTAG/preprint/blob/main/preprint/make.py) for an example of a simple command. Before building a new command, please create an Issue to discuss it.

### Building Preprint

First, clone the source code from GitHub:

```bash
git clone https://github.com/dotTHzTAG/preprint.git
cd preprint
```

(If you're making changes to the source, you'll want to work from your own fork, see below.)

**Setup your development environment:**

1.  **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
2.  **Install in editable mode:**
 
    ```bash
    pip install -e .
    ```
    This installs `preprint3` and its dependencies in your virtual environment, and any changes you make to the source code will be immediately reflected.

**To check your installation and run tests:**

1.  **Run commands:**

    ```bash
    which preprint3
    preprint3 --version
    preprint3 --help
    ```
2.  **Run tests:**

    ```bash
    pytest
    ```

### Making & Submitting Changes (Pull Request)

Here are some guidelines for developing Preprint3 to fix a bug or implement a new feature.

1.  Submit an [Issue](https://github.com/dotTHzTAG/preprint/issues) so we know what you're up to. This Issue will get closed by the pull request, and also make sure that effort isn't duplicated.
2.  Fork Preprint3; [this guide](https://docs.github.com/en/get-started/quickstart/fork-a-repo) will tell you how.
3.  Work from a branch, e.g., `git checkout -b dev/my_fix`.
4.  Make sure your changes conform to [PEP8](https://www.python.org/dev/peps/pep-0008/). The `flake8` package helps with this: `pip install flake8`. Also, all variables should be named `like_this` and not `likeThis` (i.e., use underscore separators, not camel case).
5.  Submit the Pull Request as mentioned in the GitHub guide. In the comment for your pull request, mention the Issue number (e.g., 'fixes #33.').

*Thank you*