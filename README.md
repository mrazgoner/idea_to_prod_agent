# Idea-To-Prod

A multi-agent platform that transforms application ideas into fully implemented, tested, and deployable code.

## Overview

Idea-To-Prod is an AI-powered code generation system that orchestrates multiple specialized agents to handle different stages of the software development lifecycle, from architecture design to testing and deployment.

### Core Features

- **Automatic Design**: Generates high-level and detailed architectural designs from ideas
- **Code Generation**: Produces production-ready code based on specifications
- **Test Generation**: Creates comprehensive unit tests with high coverage
- **CI/CD Ready**: Includes deployment and test automation
- **Multi-Agent Orchestration**: Seamless workflow between specialized agents

## System Architecture

```
Idea Input
    ↓
Agent 1: High-Level Design → Google Drive
    ↓
Agent 2: Detailed Design & Tasks → Jira
    ↓
Agent 3: Code Generation → GitHub
    ↓
Agent 4: Unit Test Generation → GitHub
    ↓
Agent 5: Test Execution → Validation
    ↓
[Tests Pass?] → Yes → Return Code
    ↓ No
    └─→ Regenerate (Agent 4)
    ↓
Agent 6: Deployment (Optional)
    ↓
Back to User
```

## Quick Start

### Prerequisites

- Python 3.11+
- UV package manager
- API Keys: OpenAI, Anthropic, Google, GitHub, Jira

### Installation

```bash
# Install UV
pip install uv

# Clone/navigate to project
cd idea-to-prod

# Install dependencies
uv pip install -e ".[dev]"
uv lock

# Set up environment
cp .env.example .env
# Edit .env with your API keys
```

### Running

```bash
# Run without venv activation (UV handles it!)
uv run python src/main.py

# Run tests
uv run pytest

# Format code
uv run black src/
```

## Project Structure

```
idea-to-prod/
├── src/
│   └── idea_to_prod/
│       ├── agents/          # Agent implementations
│       ├── mcp_servers/     # MCP server integrations
│       ├── utils/           # Shared utilities
│       └── main.py          # Entry point
├── tests/                   # Test suite
├── docs/                    # Documentation
├── pyproject.toml           # Project configuration
├── uv.lock                  # Locked dependencies
├── .env.example             # Environment template
└── README.md                # This file
```

## Technology Stack

### Agent Frameworks
- **Agno** - Primary multi-agent framework
- **LangChain** - LLM utilities
- **LangGraph** - Workflow orchestration

### LLM Providers
- **OpenAI** - GPT-4 (code generation)
- **Anthropic** - Claude (design & docs)
- **Google Gemini** - Document analysis

### External Services
- **Google Drive API** - Design documents
- **Jira API** - Task management
- **GitHub API** - Repository management
- **Playwright** - Test automation

## Agents

### Agent 1: High-Level Design
Generates architectural design documents from application ideas.
- Model: Claude
- Output: Stored in Google Drive

### Agent 2: Detailed Design & Tasks
Expands design into implementation specifications and creates Jira tasks.
- Model: Claude
- Output: Jira tasks, detailed specs in Google Drive

### Agent 3: Code Generation
Generates complete application code from Jira tasks.
- Model: GPT-4
- Output: GitHub repository

### Agent 4: Unit Test Generation
Creates comprehensive unit tests for generated code.
- Model: GPT-4 Turbo
- Output: Test files in GitHub

### Agent 5: Test Execution
Runs tests and validates code quality.
- Engine: Playwright
- Output: Test report, pass/fail status

### Agent 6: Deployment (Optional)
Deploys validated application to production.
- Targets: Docker, AWS, GCP, Azure
- Output: Deployed application

## Configuration

See `.env.example` for all configuration options:

```bash
# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Services
JIRA_BASE_URL=https://...
GITHUB_TOKEN=ghp_...

# Deployment
DEPLOY_TARGET=docker
```

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - Complete system design
- [TOOLS_DEPENDENCIES.md](TOOLS_DEPENDENCIES.md) - Tool reference
- [UV_SETUP.md](UV_SETUP.md) - Environment setup guide
- [QUICK_START.md](QUICK_START.md) - Quick reference

## Development

### Run Tests
```bash
uv run pytest
uv run pytest --cov=src
```

### Code Quality
```bash
uv run black src/
uv run ruff check src/
uv run mypy src/
```

### Pre-commit Hooks
```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

## Contributing

Contributions welcome! Please:
1. Create a feature branch
2. Add tests for new functionality
3. Run `uv run pytest` to verify
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Authors

AI For Dev Team

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review ARCHITECTURE.md for design details

---

**Status**: Architecture Ready for Implementation  
**Version**: 0.1.0  
**Last Updated**: March 2026
