# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Structure

This repository has **two parallel main branches** that will never merge into each other:

- `master` - the original PyTorch Sphinx theme
- `pytorch_sphinx_theme2` - a separate, independent version of the theme

Both branches accept PRs independently. GitHub Actions workflows are configured to trigger on pushes and PRs to both branches.

## Build Commands

Build the theme assets:
```bash
npx grunt default
```

Build the documentation:
```bash
cd docs
sphinx-build -b html . _build/html
```

Install dependencies:
```bash
pip install -r docs/requirements.txt
pip install -e .
```
