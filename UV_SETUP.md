# UV Environment Setup Guide

## UV Philosophy: No Manual .venv Management!

**UV is designed to eliminate the `.venv` activation workflow:**

- ❌ No need to run `source .venv/bin/activate` or `.venv\Scripts\activate`
- ❌ No need to remember "am I in the venv?"
- ✅ Just use `uv run` and UV handles the environment automatically
- ✅ Dependencies are locked and reproducible
- ✅ UV creates `.venv` internally if needed (optional, hidden in `.uv/`)

### UV's Approach:
1. **Install dependencies** → `uv pip install`
2. **Run code** → `uv run python script.py`
3. **That's it!** UV manages the environment transparently

Optional: If you prefer traditional venv activation (for IDE integration), you can still create one.

## Installation

### Install UV

**On Windows (PowerShell):**
```powershell
# Using pip (requires Python already installed)
pip install uv

# Or using Scoop
scoop install uv

# Or using Chocolatey
choco install uv
```

**On macOS/Linux:**
```bash
# Using Homebrew (macOS)
brew install uv

# Or using pip
pip install uv

# Or using the installer script
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Verify installation:**
```bash
uv --version
```

## Project Setup (UV Way - No .venv Activation Needed!)

### 1. Install Dependencies

```bash
# Navigate to project directory
cd d:\source\AI_Projects\IdeaToProdAgent

# Install all dependencies from pyproject.toml
# UV handles environment management automatically
uv pip install -e .

# Or install with development dependencies
uv pip install -e ".[dev]"

# Or install with documentation dependencies
uv pip install -e ".[docs]"

# Install all optional dependencies
uv pip install -e ".[dev,docs]"
```

### 2. Lock Dependencies

```bash
# Generate uv.lock file (for reproducible installs)
uv lock

# This creates uv.lock which should be committed to git
```

### 3. Create .venv (Optional)

If you prefer traditional venv activation for IDE integration:

```bash
# Create virtual environment (optional)
uv venv

# Activate (only if you created one above)
# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

## Common UV Commands

### Managing Dependencies

```bash
# Add a new package
uv pip install <package-name>

# Add multiple packages
uv pip install package1 package2 package3

# Uninstall a package
uv pip uninstall <package-name>

# List installed packages
uv pip list

# Show package details
uv pip show <package-name>

# Upgrade a package
uv pip install --upgrade <package-name>
```

### Virtual Environment Management

```bash
# Create a new venv
uv venv

# Create venv with specific Python version
uv venv --python 3.12

# List available Python versions
uv python list

# Download Python version
uv python install 3.11

# Remove virtual environment
uv venv --remove
```

### Compilation & Building

```bash
# Build package
uv build

# Build only wheel
uv build --wheel

# Build only source distribution
uv build --sdist
```

### Dependency Analysis

```bash
# Show dependency tree
uv pip tree

# Check for outdated packages
uv pip list --outdated

# Audit for security vulnerabilities
uv pip audit
```

## Development Workflow (UV Way)

The beauty of UV is **no venv activation needed**. Just use `uv` commands:

### Run Python Code

```bash
# Run Python script directly (UV handles env automatically)
uv run python src/main.py

# Or run Python modules
uv run python -m idea_to_prod.agents

# Or as a shortcut
uv run idea_to_prod
```

### Run Tests

```bash
# Run tests without activating venv
uv run pytest

# With coverage
uv run pytest --cov=src tests/

# Specific test file
uv run pytest tests/test_agent1.py

# Verbose output
uv run pytest -v
```

### Code Quality

```bash
# Format code with Black (automatically uses UV environment)
uv run black src/ tests/

# Lint with Ruff
uv run ruff check src/ tests/

# Type check with mypy
uv run mypy src/
```

### Interactive Shell

```bash
# Start interactive Python shell (with all dependencies available)
uv run python

# Or IPython if installed
uv run ipython
```

## Project Structure with UV

```
idea-to-prod/
├── pyproject.toml           # Project metadata & dependencies
├── uv.lock                  # Locked dependency versions
├── .venv/                   # Virtual environment (created by uv)
├── src/
│   └── idea_to_prod/
│       ├── __init__.py
│       ├── agents/
│       ├── mcp_servers/
│       ├── utils/
│       └── main.py
├── tests/
│   ├── __init__.py
│   ├── test_agent1.py
│   ├── test_agent2.py
│   └── ...
├── docs/
├── README.md
├── ARCHITECTURE.md
└── .gitignore
```

## Configuration Files

### .gitignore

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
*.egg
*.egg-info/
dist/
build/

# Virtual environments
.venv/
venv/
ENV/
env/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Environment variables
.env
.env.local
.env.*.local

# Testing
.pytest_cache/
.coverage
htmlcov/

# UV
.python-version
```

### .env.example

```
# AI Models
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key

# Google Drive
GOOGLE_DRIVE_FOLDER_ID=your_folder_id
GOOGLE_DRIVE_CREDENTIALS_FILE=credentials.json

# Jira
JIRA_BASE_URL=https://your-jira-instance.atlassian.net
JIRA_API_TOKEN=your_jira_token
JIRA_PROJECT_KEY=PROJ

# GitHub
GITHUB_TOKEN=your_github_token
GITHUB_ORG=your_org_name

# MCP Servers
MCP_GOOGLE_DRIVE_URL=http://localhost:3001
MCP_JIRA_URL=http://localhost:3002
MCP_GITHUB_URL=http://localhost:3003
MCP_PLAYWRIGHT_URL=http://localhost:3004
```

## Troubleshooting

### UV not found after installation

```powershell
# Verify Python path
python -m pip show uv

# Or reinstall with flag to create command
pip install --user uv
```

### Slow performance on first run

- UV downloads and caches wheels, first run is slower
- Subsequent runs are much faster
- This is normal behavior

### Lock file conflicts

```bash
# Regenerate lock file
uv lock --upgrade

# Clean and reinstall
uv venv --remove
uv venv
uv pip install -e ".[dev]"
uv lock
```

### Python version mismatch

```bash
# Check which Python UV is using
uv python show

# Use specific Python version
uv venv --python /path/to/python3.11
```

## Resources

- **UV Documentation**: https://docs.astral.sh/uv/
- **Astral Blog**: https://astral.sh/blog/
- **GitHub Repository**: https://github.com/astral-sh/uv

## Advantages of UV over Pip

| Feature | UV | Pip |
|---------|----|----|
| **Speed** | ⚡ Very fast (~10-100x) | Slow |
| **Dependency Resolution** | Advanced, accurate | Basic |
| **Lock Files** | Native support | Third-party tools needed |
| **Python Management** | Built-in | External tool needed |
| **Installation** | Single binary | Requires Python |
| **Memory Usage** | Low | Higher |

---

**Version**: 1.0  
**Last Updated**: March 2026
