#!/usr/bin/env python
# encoding: utf-8
"""
Git IO utilities.
"""

import git


def absolute_git_root_dir(path):
    """Get the absolute path of the git repository root."""
    try:
        repo = git.Repo(path, search_parent_directories=True)
        return repo.git.rev_parse("--show-toplevel")
    except git.InvalidGitRepositoryError:
        return None


def read_git_blob(commit_ref, path, repo_dir='.'):
    """Read a file from a git blob."""
    repo = git.Repo(repo_dir)
    commit = repo.commit(commit_ref)
    blob = commit.tree / path
    return blob.data_stream.read().decode('utf-8')
