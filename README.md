# Idea-To-Prod

A multi-agent platform that transforms application ideas into fully implemented, tested, and deployable code.

## Quick Start

### Installation

```bash
# Install dependencies
uv pip install -e ".[dev,desktop]"

# Run desktop app
uv run python run_desktop_app.py

# Or run web server
uv run python run_ui.py
```

## Documentation

Complete documentation is available in the `GENERATED_DOCS/` folder:

- **[ARCHITECTURE.md](GENERATED_DOCS/ARCHITECTURE.md)** - System architecture and design
- **[QUICK_START.md](GENERATED_DOCS/QUICK_START.md)** - Installation and setup guide
- **[DESKTOP_VS_WEB.md](GENERATED_DOCS/DESKTOP_VS_WEB.md)** - Choosing between desktop and web UI
- **[README.md](GENERATED_DOCS/README.md)** - Full project overview

## What is Idea-To-Prod?

Idea-To-Prod is an AI-powered system that takes a high-level application idea and automatically:

1. **Creates high-level architectural design** (Agent 1)
2. **Generates detailed design specifications** (Agent 2)
3. **Produces production-ready code** (Agent 3)
4. **Creates comprehensive unit tests** (Agent 4)
5. **Executes and validates tests** (Agent 5)

All through a coordinated team of AI agents working together.

## Features

- ✅ **Multi-Agent Orchestration** - 5 specialized agents working in harmony
- ✅ **Dual UI** - Native desktop app (PyQt6) or web interface (FastAPI)
- ✅ **MCP Integration** - GitHub, Jira, Google Drive, Playwright
- ✅ **Configuration Management** - Persistent MCP setup and testing
- ✅ **Real-Time Progress** - Visual pipeline showing workflow progress

## Project Structure

```
idea-to-prod/
├── src/idea_to_prod/
│   ├── services/              # Configuration & MCP management
│   ├── agents/                # Agent implementations
│   ├── mcp_servers/           # MCP implementations
│   ├── desktop_app.py         # PyQt6 desktop UI
│   └── ui_server.py           # FastAPI web server
├── GENERATED_DOCS/            # Complete documentation
└── pyproject.toml             # Project configuration
```

## Technology Stack

- **Agents**: Agno, LangChain, LangGraph
- **LLMs**: OpenAI (GPT-4), Anthropic (Claude), Google (Gemini)
- **UI**: PyQt6 (Desktop) + FastAPI (Web)
- **MCPs**: GitHub, Jira, Google Drive, Playwright
- **Package Management**: UV (fast Python environment)

## License

MIT
