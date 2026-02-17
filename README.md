# mini-RAG

This repository is a follow-up implementation of the practical course [mini-RAG | From notebooks to PRODUCTION](https://www.youtube.com/playlist?list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj). It implements a minimal RAG (Retrieval-Augmented Generation) model for question answering.

**Key difference**: This project uses [`uv`](https://docs.astral.sh/uv/) as the package manager and Python runtime manager, instead of conda or traditional pip.

## Requirements

- **Python 3.11 or later** (managed by `uv`)
- **`uv` package manager** - [Installation guide](https://docs.astral.sh/uv/getting-started/installation/)

## Quick Start

### 1. Install `uv`

Follow the official [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) for your operating system.

### 2. Clone and Navigate to the Project

```bash
git clone <repository-url>
cd mini-rag
```

### 3. Set Up the Project with `uv`

`uv` will automatically manage Python versions and dependencies:

```bash
# Install Python and project dependencies
uv sync
```

This command will:
- Download and install Python 3.11+ (if not already installed)
- Create a virtual environment
- Install all dependencies from `pyproject.toml`

### 4. Run the Project

```bash
# Activate the uv environment and run your script
uv run python main.py
```

Or, if you have specific scripts defined in `pyproject.toml`:
```bash
uv run <script-name>
```

## Managing Dependencies with `uv`

### Add a New Dependency

```bash
uv add package-name
```

### Add a Development-Only Dependency

```bash
uv add --dev package-name
```

### Update Dependencies

```bash
uv sync --upgrade
```

### View Project Dependencies

```bash
uv pip freeze
```

## Project Structure

```
mini-rag/
├── main.py           # Main entry point
├── pyproject.toml    # Project configuration and dependencies
└── README.md         # This file
```

## Benefits of Using `uv`

- **Fast installation**: Written in Rust, significantly faster than pip
- **Python version management**: No need for separate version managers
- **Virtual environment**: Automatically created and managed
- **Reproducible builds**: Lock file support for deterministic installations
- **Cross-platform**: Works seamlessly on Windows, macOS, and Linux

## Additional Resources

- [uv Documentation](https://docs.astral.sh/uv/)
- [Original Course](https://www.youtube.com/playlist?list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj)