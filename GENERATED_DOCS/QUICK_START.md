# Quick Installation Guide

## System Components

### Core Layers

1. **Services Layer** (`src/idea_to_prod/services/`)
   - `MCPSetupService` - Handles MCP configuration and testing
   - `MCPConnectionService` - Initializes and manages MCP instances
   - `ConfigStore` - Persists configuration data

2. **Agent Layer** (`src/idea_to_prod/agents/`)
   - 5 specialized agents orchestrated by `IdeaToProdTeam`
   - Uses MCPs via MCPConnectionService

3. **MCP Layer** (`src/idea_to_prod/mcp_servers/`)
   - GitHub, Jira, Google Drive, Playwright MCPs
   - Each with configuration and implementation files

4. **UI Layer**
   - **Desktop App**: `desktop_app.py` (PyQt6 native)
   - **Web Server**: `ui_server.py` (FastAPI)
   - Both use services layer for all MCP operations



#### Agent Frameworks (3)
- ✅ **Agno** - Primary multi-agent framework
- ✅ **LangChain** - LLM utilities
- ✅ **LangGraph** - Workflow orchestration

#### MCP Servers (5)
- ✅ **MCP-Use** - MCP communication layer
- ✅ **Google Drive MCP** - Document storage
- ✅ **Jira MCP** - Task management
- ✅ **GitHub MCP** - Repository management
- ✅ **Playwright MCP** - Test execution

#### LLM Providers (3)
- ✅ **OpenAI** - GPT-4 / GPT-4 Turbo
- ✅ **Anthropic** - Claude
- ✅ **Google Gemini** - Document analysis

#### External APIs (4)
- ✅ **Google APIs** - Drive, Auth
- ✅ **Jira API** - Task management
- ✅ **GitHub API** - Repository management
- ✅ **Playwright** - Browser automation

#### Data & Config (4)
- ✅ **Pydantic** - Data validation
- ✅ **PyYAML** - Config parsing
- ✅ **Python Dotenv** - Environment variables
- ✅ **Requests** - HTTP client

**Total: 22 Core Tools** + dev/test tools

---

## Installation Steps

### Step 1: Install UV (if not already installed)

```bash
pip install uv
```

### Step 2: Install All Dependencies

```bash
cd d:\source\AI_Projects\IdeaToProdAgent

# Install with development dependencies
uv pip install -e ".[dev]"

# Generate lock file
uv lock
```

### Step 3: Verify Installation

```bash
# Run this to verify all major tools are installed
uv run python -c "
import agno
import langchain
import langgraph
import openai
import anthropic
import google.generativeai
import jira
import github
import playwright

print('✅ All agent frameworks installed')
print('✅ All LLM providers installed')
print('✅ All APIs installed')
print('✅ Ready to start development!')
"
```

### Step 4: (Optional) Create Traditional .venv

If you want IDE support or traditional venv activation:

```bash
uv venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux
```

---

## Optional Feature Installation

### Install with Documentation Tools

```bash
uv pip install -e ".[docs]"
```

### Install with MCP Development Tools

```bash
uv pip install -e ".[mcp]"
```

### Install Everything

```bash
uv pip install -e ".[all]"
```

---

## Running Commands with UV

```bash
# No venv activation needed - just use uv run!

# Run Python
uv run python src/main.py

# Run tests
uv run pytest

# Code formatting
uv run black src/

# Linting
uv run ruff check src/

# Type checking
uv run mypy src/

# Interactive Python
uv run python
uv run ipython
```

---

## Dependency Breakdown by Agent

### Agent 1: HL Design
- Framework: **Agno**
- Model: **Claude (Anthropic)**
- APIs: **Google Drive API**
- Data: **Pydantic, PyYAML**

### Agent 2: Detailed Design & Tasks
- Framework: **Agno**
- Model: **Claude (Anthropic)**
- APIs: **Google Drive, Jira**
- Data: **Pydantic, PyYAML**

### Agent 3: Code Generation
- Framework: **Agno + LangGraph**
- Model: **GPT-4 (OpenAI)**
- APIs: **Jira, GitHub**
- Data: **Pydantic**

### Agent 4: Unit Test Generation
- Framework: **Agno**
- Model: **GPT-4 Turbo (OpenAI)**
- APIs: **GitHub**
- Test: **Pytest**

### Agent 5: Test Execution
- Framework: **Standalone**
- APIs: **Playwright, GitHub**
- Test: **Pytest, Playwright**

### Agent 6: Deployment (Optional)
- Framework: **Agno**
- APIs: **GitHub, Cloud SDKs (not in core deps)**
- Deploy: **Docker (system dependency)**

---

## Environment Setup

1. Copy `.env.example` to `.env`
2. Fill in API keys:
   ```bash
   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=sk-ant-...
   GOOGLE_API_KEY=...
   JIRA_BASE_URL=https://...
   JIRA_API_TOKEN=...
   GITHUB_TOKEN=ghp_...
   ```

3. Download Google credentials:
   ```bash
   # Save credentials.json to project root
   # Or point GOOGLE_DRIVE_CREDENTIALS_FILE in .env
   ```

---

## Testing the Installation

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src tests/

# Run specific agent tests
uv run pytest tests/test_agent_1.py -v
```

---

## Troubleshooting

### UV command not found
```bash
pip install uv --user
# or 
pip install uv
```

### Import errors
```bash
# Regenerate lock file
uv lock --upgrade

# Reinstall
uv pip install -e ".[dev]" --upgrade
```

### Playwright browsers not installed
```bash
uv run playwright install
uv run playwright install chromium
```

### API key errors
- Verify `.env` file exists
- Check `python-dotenv` is loaded: `from dotenv import load_dotenv; load_dotenv()`
- Ensure no typos in environment variable names

---

## Documentation Files

- **ARCHITECTURE.md** - System design and workflow
- **TOOLS_DEPENDENCIES.md** - Complete tool reference
- **UV_SETUP.md** - UV environment guide
- **pyproject.toml** - Project and dependency configuration
- **.env.example** - Environment variable template

---

## Next Steps

1. ✅ Dependencies installed
2. 📝 Set up environment variables (.env)
3. 🚀 Build Agent infrastructure (src/agents/)
4. 🔗 Implement MCP server integrations
5. ✨ Test end-to-end workflow

---

**Status**: All 22+ tools configured and ready to use!
