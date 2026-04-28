# Tools & Dependencies Reference

## Overview of Tools Mentioned in Idea-To-Prod

### 1. Agent Frameworks

| Tool | Purpose | PyPI | Status |
|------|---------|------|--------|
| **LangChain** | General-purpose LLM framework | `langchain` | ✅ Recommended |
| **LangGraph** | Workflow orchestration & state management | `langgraph` | ✅ Recommended |
| **Agno** | Modern multi-agent framework | `agno` | ✅ Primary Choice |
| **CrewAI** | Multi-agent coordination | `crewai` | ⚠️ Optional |

### 2. MCP (Model Context Protocol) Servers & Integration

| Tool | Purpose | PyPI | Used By |
|------|---------|------|---------|
| **MCP-Use** | Programmatic MCP server communication | `mcp-use` | All Agents |
| **Google Drive MCP** | Document storage integration | Custom MCP | Agent 1, 2 |
| **Jira MCP** | Task management integration | Custom MCP | Agent 2, 3 |
| **GitHub MCP** | Repository management | Custom MCP | Agent 3, 4 |
| **Playwright MCP** | Test execution automation | Custom MCP | Agent 5 |

### 3. External APIs & SDKs

| Tool | Purpose | PyPI | Auth |
|------|---------|------|------|
| **OpenAI** | GPT-4 API for code gen/testing | `openai>=1.0.0` | API Key |
| **Anthropic** | Claude API for design/docs | `anthropic>=0.7.0` | API Key |
| **Google AI** | Gemini API | `google-generativeai>=0.3.0` | API Key |
| **Google Auth** | Google Drive auth | `google-auth-oauthlib>=1.0.0` | OAuth2 |
| **Google API Client** | Google Drive SDK | `google-api-python-client>=2.100.0` | OAuth2 |
| **Jira Python** | Jira API client | `jira>=3.13.0` | Token |
| **PyGithub** | GitHub API client | `pygithub>=2.1.0` | Token |

### 4. Testing & Automation

| Tool | Purpose | PyPI |
|------|---------|------|
| **Playwright** | Browser-based testing | `playwright>=1.40.0` |
| **Pytest** | Testing framework | Built into dev deps |
| **Coverage** | Code coverage analysis | Built into dev deps |

### 5. Data & Configuration

| Tool | Purpose | PyPI |
|------|---------|------|
| **Pydantic** | Data validation & settings | `pydantic>=2.0.0` |
| **PyYAML** | YAML configuration parsing | `pyyaml>=6.0.0` |
| **Python Dotenv** | Environment variable management | `python-dotenv>=1.0.0` |

### 6. HTTP & Networking

| Tool | Purpose | PyPI |
|------|---------|------|
| **Requests** | HTTP client library | `requests>=2.31.0` |

### 7. Development Tools

| Tool | Purpose | PyPI | Category |
|------|---------|------|----------|
| **Black** | Code formatter | Included | dev |
| **Ruff** | Fast Python linter | Included | dev |
| **Mypy** | Static type checker | Included | dev |
| **Pre-commit** | Git hooks framework | Included | dev |
| **Pytest-asyncio** | Async test support | Included | dev |
| **Pytest-cov** | Coverage reporting | Included | dev |

---

## Agno Detailed Information

### What is Agno?

**Agno** is a modern Python framework for building multi-agent AI systems with:

- **Lightweight & Fast**: Minimal dependencies, quick startup
- **Flexible Agent Definition**: Simple decorator-based agent creation
- **Built-in Tools**: Common tool integrations included
- **Async Support**: First-class async/await support
- **State Management**: Automatic state tracking across agents
- **Type-Safe**: Full type hints throughout
- **Easy Integration**: Works well with LangChain, OpenAI, etc.

### Core Agno Concepts

```python
from agno.agent import Agent
from agno.tools import Tool

# Define an agent
@Agent(name="Designer", model="gpt-4")
def design_agent(idea: str) -> str:
    """Creates high-level design from an idea"""
    return design_response

# Use as decorator or class
agent = Agent(
    name="CodeGen",
    model="gpt-4",
    tools=[github_tool, jira_tool],
    instructions="Generate production-ready code"
)
```

### Agno vs CrewAI vs LangChain vs LangGraph

| Feature | Agno | CrewAI | LangChain | LangGraph |
|---------|------|--------|-----------|-----------|
| **Learning Curve** | Easy | Medium | Hard | Medium |
| **Agent Definition** | Decorators | Classes | Functions | Graph-based |
| **Multi-Agent** | ✅ Native | ✅ Native | ⚠️ Manual | ✅ Native |
| **State Management** | ✅ Auto | ⚠️ Manual | ⚠️ Manual | ✅ Auto |
| **Async Support** | ✅ Full | ⚠️ Limited | ✅ Full | ✅ Full |
| **Code Generation** | ✅ Great | ✅ Good | ✅ Good | ✅ Good |
| **Community Size** | Small | Medium | Large | Growing |
| **Documentation** | Good | Good | Excellent | Good |

### Recommended Agno Setup

```bash
# Install Agno with all extras
pip install agno[all]

# Or install core + specific integrations
pip install agno openai anthropic google-generativeai
```

### Agno Dependencies

```toml
# Core
agno = ">=0.1.0"

# LLM Providers
openai = ">=1.0.0"
anthropic = ">=0.7.0"
google-generativeai = ">=0.3.0"

# Tools
requests = ">=2.31.0"
pydantic = ">=2.0.0"
```

---

## Complete Installation

### All Dependencies Together

```bash
# Install everything
uv pip install -e ".[dev]"

# Verify installations
uv run python -c "import agno; print(agno.__version__)"
uv run python -c "import langchain; print(langchain.__version__)"
uv run python -c "import langgraph; print(langgraph.__version__)"
```

### By Category

```bash
# Core frameworks
uv pip install agno langchain langgraph

# LLM providers
uv pip install openai anthropic google-generativeai

# MCP & APIs
uv pip install mcp-use google-auth-oauthlib google-api-python-client jira pygithub

# Testing
uv pip install playwright pytest pytest-asyncio pytest-cov

# Development
uv pip install black ruff mypy pre-commit
```

---

## Architecture: Which Tool for Which Agent

```
Agent 1: HL Design
├─ Framework: Agno
├─ Model: Claude (Anthropic)
├─ Tools: Google Drive API, Pydantic
└─ Output: Design Document

Agent 2: Detailed Design & Tasks
├─ Framework: Agno
├─ Model: Claude (Anthropic)
├─ Tools: Google Drive API, Jira API
└─ Output: Detailed specs + Jira tasks

Agent 3: Code Generation
├─ Framework: Agno + LangGraph
├─ Model: GPT-4 (OpenAI)
├─ Tools: Jira API, GitHub API
└─ Output: Repository with code

Agent 4: Unit Test Generation
├─ Framework: Agno
├─ Model: GPT-4 Turbo (OpenAI)
├─ Tools: GitHub API, Pydantic
└─ Output: Test files in GitHub

Agent 5: Test Execution
├─ Framework: Standalone + Playwright
├─ Model: Lightweight (GPT-3.5)
├─ Tools: Playwright MCP, GitHub API
└─ Output: Test report

Agent 6: Deployment (Optional)
├─ Framework: Agno
├─ Model: Any
├─ Tools: Docker SDK, Cloud SDKs
└─ Output: Deployed application
```

---

## Version Compatibility

```
Python: >=3.10
Agno: >=0.1.0
LangChain: >=0.1.0
LangGraph: >=0.0.1
OpenAI: >=1.0.0
Anthropic: >=0.7.0
```

---

## Quick Reference: Installation Commands

```bash
# Complete setup
uv pip install -e ".[dev]"
uv lock

# Run with full dependencies
uv run pytest
uv run python src/main.py
uv run black src/

# Check all tools installed
uv run python -c "
import agno
import langchain
import langgraph
import openai
import anthropic
import google.generativeai
print('✅ All major dependencies installed!')
"
```

---

## Environment Variables by Tool

```bash
# LLM APIs
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Google APIs
GOOGLE_DRIVE_CREDENTIALS_FILE=credentials.json
GOOGLE_DRIVE_FOLDER_ID=...

# Jira
JIRA_BASE_URL=https://...
JIRA_API_TOKEN=...

# GitHub
GITHUB_TOKEN=ghp_...

# Playwright
PLAYWRIGHT_BROWSER=chromium
```

---

**Last Updated**: March 2026  
**Agno Version**: 0.1.0+  
**Status**: Complete dependency map created
