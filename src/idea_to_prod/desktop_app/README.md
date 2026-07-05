# Desktop Application - Modular Structure

The desktop application has been refactored from a monolithic single file into a well-organized modular folder structure.

## Folder Structure

```
desktop_app/
├── __init__.py           # Package entry point
├── main.py              # Main application window (IdeaToProdApp class)
├── workers/             # Background worker threads
│   ├── __init__.py
│   ├── process_idea_worker.py    # Thread for processing ideas
│   └── test_mcp_worker.py        # Thread for testing MCP connections
├── widgets/             # Custom PyQt6 widgets
│   ├── __init__.py
│   ├── workflow_diagram.py       # Workflow visualization widget
│   └── mcp_status_panel.py       # MCP connection status panel
├── tabs/                # Configuration tab panels
│   ├── __init__.py
│   ├── github_tab.py             # GitHub configuration
│   ├── jira_tab.py               # Jira configuration
│   ├── google_drive_tab.py       # Google Drive configuration
│   └── playwright_tab.py         # Playwright configuration
├── styles/              # Styling and theme
│   ├── __init__.py
│   ├── colors.py                 # Color constants
│   ├── buttons.py                # Button styling functions
│   ├── frames.py                 # Frame/container styling
│   └── status_labels.py          # Status label styling
└── templates/           # UI templates and base classes
    ├── __init__.py
    ├── tab_template.py           # Base class for configuration tabs
    └── widget_template.py        # Base class for custom widgets
```

## Key Components

### Main Application (`main.py`)
- **IdeaToProdApp**: Main application window with all UI logic
  - Manages left panel (idea input, buttons, workflow diagram)
  - Manages right panel (MCP configuration tabs)
  - Handles process workflows and status updates

### Workers (`workers/`)
- **ProcessIdeaWorker**: Processes ideas asynchronously using the agent team
- **TestMCPWorker**: Tests MCP connections in background thread

### Widgets (`widgets/`)
- **WorkflowDiagram**: Displays 5-step processing pipeline with status indicators
- **Status in Tab Names**: MCP connection status shown as ✓/✗ prefix in tab button text

### Configuration Tabs (`tabs/`)
Each tab inherits from `TabTemplate` and provides platform-specific configuration:
- **GitHubTab**: Token, username, base URL configuration
- **JiraTab**: Instance URL, email, API token configuration  
- **GoogleDriveTab**: Credentials path and folder ID configuration
- **PlaywrightTab**: Headless mode, timeout, logging settings

### Styles (`styles/`)
Centralized styling with no hardcoded strings:
- **colors.py**: All color constants (primary, success, error, warning, info, etc.)
- **buttons.py**: Button style functions (primary, success, error, generic)
- **frames.py**: Frame styling for step boxes
- **status_labels.py**: Status message styling

### Templates (`templates/`)
Base classes for consistent UI development:
- **TabTemplate**: Provides form building methods (`add_mode_selector()`, `add_text_input()`, etc.)
- **WidgetTemplate**: Base for custom widgets with layout helpers

## Entry Point

### `desktop_app.py` (in parent directory)
Simple entry point that imports and runs the refactored application:
```python
from idea_to_prod.desktop_app import main

if __name__ == "__main__":
    main()
```

Run with: `uv run ./desktop_app.py`

## Benefits of This Structure

1. **Separation of Concerns**: Each component has a single responsibility
2. **Reusability**: Templates and styles can be extended for new features
3. **Maintainability**: Changes to styling don't require searching the entire file
4. **Testability**: Individual components can be tested independently
5. **Scalability**: Easy to add new tabs, widgets, or styling
6. **Code Quality**: ~200 lines per file vs 850 in monolithic version

## Adding New Features

### Add a New MCP Tab
1. Create `new_platform_tab.py` in `tabs/`
2. Inherit from `TabTemplate`
3. Override `setup_layout()` with platform-specific fields
4. Add callback in `main.py`

### Add a New Widget
1. Create `new_widget.py` in `widgets/`
2. Inherit from `WidgetTemplate`
3. Use styles from `styles/` package
4. Import in `widgets/__init__.py`

### Add New Styling
1. Add colors to `styles/colors.py`
2. Create styling function in appropriate file (`buttons.py`, `frames.py`, etc.)
3. Export from `styles/__init__.py`
