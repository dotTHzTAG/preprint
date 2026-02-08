#!/usr/bin/env python
# encoding: utf-8
"""
LaTeX utilities.
"""

import os
import re
import logging
from TexSoup import TexSoup

from .gitio import read_git_blob


class RootNotFound(Exception):
    pass


def remove_comments(tex):
    """Remove comments from LaTeX."""
    return re.sub(r'(?<!\\)%.*', '', tex)


def inline(tex, base_dir='.', replacer=None, ifexists_replacer=None):
    """Inline LaTeX files."""

    def sub_if_exists(match):
        file_path = os.path.join(base_dir, match.group(1) + '.tex')
        if not os.path.exists(file_path):
            file_path = os.path.join('.', match.group(1) + '.tex')

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
            return inline(content,
                          base_dir=os.path.dirname(file_path),
                          replacer=replacer,
                          ifexists_replacer=ifexists_replacer)
        return ''

    if replacer is None:
        replacer = sub_if_exists

    if ifexists_replacer is None:
        ifexists_replacer = sub_if_exists

    tex = re.sub(r'\\input{(.*?)}', replacer, tex)
    tex = re.sub(r'\\InputIfFileExists{(.*?)}{.*?}{.*?}', ifexists_replacer, tex)
    return tex


def inline_bbl(tex, bbl_text):
    """Inline a .bbl file."""
    soup = TexSoup(tex)
    
    # Find the \bibliography command and replace it with the bbl content
    bib_node = soup.bibliography
    if bib_node:
        bib_node.replace_with(bbl_text)
    else:
        # If no \bibliography command is found, try to find a \begin{document}
        # and insert the bbl_text before it, as a fallback.
        # This is a less ideal, but might work for some cases.
        begin_document = soup.find('document')
        if begin_document:
            begin_document.insert_before(bbl_text)

    return str(soup)


def inline_blob(commit_ref, tex, base_dir='.', repo_dir='.'):
    """Inline LaTeX files from a git blob."""
    soup = TexSoup(tex)
    for node in soup.find_all(('input', 'InputIfFileExists')):
        if not node.args:
            continue

        file_path = os.path.join(base_dir, node.args[0] + '.tex')
        try:
            content = read_git_blob(commit_ref, file_path, repo_dir=repo_dir)
            # Recursively inline content
            content = inline_blob(commit_ref, content,
                                  base_dir=os.path.dirname(file_path),
                                  repo_dir=repo_dir)
            node.replace_with(content)
        except Exception:
            # If the file does not exist in the blob, replace with empty string
            node.replace_with('')
    return str(soup)


def find_root_tex_document(base_dir='.'):
    """Find the root .tex document in a directory."""
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.tex') and 'main' in file.lower(): # Simple heuristic
                return os.path.join(root, file)
    raise RootNotFound("No root .tex document found.")


def _find_exts(fig_path, ext_priority):
    """Return a tuple of all formats for which a figure exists."""
    basepath = os.path.splitext(fig_path)[0]
    has_exts = []
    for ext in ext_priority:
        p = ".".join((basepath, ext))
        if os.path.exists(p):
            has_exts.append(ext)
    return tuple(has_exts)