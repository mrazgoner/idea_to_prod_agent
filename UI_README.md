# Idea-To-Prod Web UI

A modern web-based interface for the Idea-To-Prod Agent Team platform. Transform your application ideas into production-ready code with an intuitive visual workflow and MCP configuration dashboard.

## Features

### 📝 Application Input
- **Textbox Interface**: Clean, intuitive input for describing your application idea
- **Real-time Feedback**: Immediate status messages and error handling
- **Reset Functionality**: Clear inputs and start fresh

### 🔄 Visual Pipeline Diagram
- **5-Stage Workflow Visualization**:
  1. High-Level Design
  2. Detailed Design
  3. Code Generation
  4. Test Generation
  5. Test Execution

- **Interactive Step Tracking**: Watch steps progress with visual indicators
- **Color-Coded Status**: Completed (green), Active (blue), Failed (red)
- **Connected with Arrows**: Clear flow visualization showing the progression

### 🔌 MCP Platform Configuration

Four dedicated configuration tabs for external platforms:

#### **GitHub MCP**
- Personal Access Token authentication
- Custom username and base URL
- Stub mode for testing, API mode for real operations
- Optional logging

#### **Jira MCP**
- Atlassian instance URL
- Email and API token authentication
- Stub/API mode selection
- Logging configuration

#### **Google Drive MCP**
- Credentials path configuration
- Folder ID setup
- Stub/API mode selection
- Logging options

#### **Playwright MCP**
- Headless browser mode toggle
- Timeout configuration
- Stub/API mode selection
- Logging control

### 📊 MCP Connectivity Dashboard
- **Real-time Status**: Shows connection status for each platform
- **Auto-Detection**: Tests connections on page load
- **Visual Indicators**: Green (Connected), Red (Disconnected)
- **Manual Testing**: One-click button to test all MCPs

## Getting Started

### Prerequisites
- Python 3.11+
- All core Idea-To-Prod dependencies installed

### Installation

#### Option 1: Quick Setup (Recommended)
```bash
cd /path/to/IdeaToProdAgent
python setup_ui.py
```

This script will:
1. Install FastAPI and uvicorn
2. Display getting started instructions
3. Show example commands

#### Option 2: Manual Installation
```bash
pip install fastapi uvicorn
```

### Starting the Server

#### Default (localhost:8000)
```bash
python run_ui.py
```

#### Custom Port
```bash
python run_ui.py --port 5000
```

#### Custom Host and Port
```bash
python run_ui.py --host 0.0.0.0 --port 8080
```

### Accessing the UI
Once the server is running, open your browser to:
```
http://localhost:8000
```

## Usage Guide

### Processing an Application Idea

1. **Enter Your Idea**: Type your application description in the textbox
   - Example: "A real-time collaboration tool for remote teams with chat, file sharing, and video conferencing"

2. **Configure MCPs** (Optional):
   - Click on each MCP tab (GitHub, Jira, Google Drive, Playwright)
   - Enter your credentials and settings
   - Click "Save [Platform] Config"

3. **Test Connections** (Optional):
   - Click "Test MCPs" button to verify all platform connections
   - Check the status dashboard for connectivity indicators

4. **Process the Idea**:
   - Click "Process Idea" button
   - Watch the pipeline diagram animate as each stage completes
   - Monitor status messages for updates

5. **Review Results**:
   - Wait for all 5 stages to complete
   - Check the status message for completion confirmation
   - Results are available in the backend

### MCP Configuration Workflow

Each MCP tab follows a similar wizard-style pattern:

1. **Select Mode**: Choose between "Stub" (testing) and "API" (real)
2. **Enter Credentials**: Provide platform-specific authentication details
3. **Configure Options**: Set platform-specific settings (URLs, timeouts, etc.)
4. **Optional Logging**: Enable detailed logging if needed
5. **Save**: Click "Save [Platform] Config" to apply settings

## API Endpoints

The UI server exposes the following REST API endpoints:

### Processing Ideas
```
POST /api/process-idea
Body: {
    "idea": "string",
    "enabled_steps": [bool, bool, bool, bool, bool],
    "start_step": 0
}
Response: {
    "success": bool,
    "message": "string",
    "results": {...}
}
```

### MCP Testing
```
GET /api/test-mcp-connections
Response: {
    "success": bool,
    "connected_platforms": [string],
    "failed_platforms": [string],
    "platform_results": {...}
}

GET /api/test-mcp/{platform}
Response: {
    "platform": "string",
    "result": {...}
}
```

### MCP Configuration
```
POST /api/configure-mcp/github
POST /api/configure-mcp/jira
POST /api/configure-mcp/google-drive
POST /api/configure-mcp/playwright
```

### System Status
```
GET /api/status
Response: {
    "system": "ready|busy",
    "team": "initialized",
    "mcp_count": 4
}
```

## Supported Modes

### Stub Mode
- **Purpose**: Testing and development without external API calls
- **Use Case**: Quick testing, CI/CD pipelines, offline development
- **Data**: Uses mock/sample data

### API Mode
- **Purpose**: Real integration with external platforms
- **Use Case**: Production use, real GitHub/Jira operations
- **Requirements**: Valid credentials for each platform

## UI Components

### Textbox
- Accepts multi-line input
- Placeholder with example text
- Character limit: None (but practical limits apply)
- Auto-focus on page load

### Workflow Diagram
- 5 steps connected with arrows
- Color-coded status indicators
- Step numbers in circles
- Smooth animation on processing

### Configuration Forms
- Organized by platform in tabs
- Form validation
- Password fields for sensitive data
- Checkbox toggles for boolean settings
- Save buttons per form

### Status Dashboard
- 4 MCP cards (GitHub, Jira, Google Drive, Playwright)
- Real-time status updates
- Manual refresh capability
- Connected/Disconnected visual indicators

### Action Buttons
- **Process Idea** (Primary - Blue): Start the pipeline
- **Test MCPs** (Success - Green): Test platform connections
- **Reset** (Danger - Red): Clear all inputs

## Troubleshooting

### Server Won't Start
```bash
# Check port availability
netstat -ano | findstr :8000  # Windows
lsof -i :8000                # Mac/Linux

# Try different port
python run_ui.py --port 8001
```

### UI Not Loading
- Clear browser cache (Ctrl+Shift+Delete)
- Try incognito/private mode
- Check browser console for errors (F12)

### MCPs Showing Disconnected
1. Check credentials in configuration tabs
2. Verify internet connectivity
3. Test each platform individually with "Test MCPs" button
4. Check server logs for detailed error messages

### Processing Hangs
- Check if server is responsive: `http://localhost:8000/api/status`
- Look at server logs for errors
- Try with smaller/simpler idea first
- Increase browser timeout if needed

## Development

### Project Structure
```
src/idea_to_prod/
├── ui_server.py          # Main FastAPI application
├── agents/
│   ├── team.py           # Agent team orchestration
│   └── agent_*.py        # Individual agents
└── mcp_servers/          # MCP implementations
```

### Running in Development Mode
```bash
# With auto-reload
uvicorn src.idea_to_prod.ui_server:app --reload --host 0.0.0.0 --port 8000
```

### Extending the UI
1. Edit HTML/CSS/JavaScript in `get_html_content()` function
2. Add new API endpoints to `ui_server.py`
3. Update frontend JavaScript to call new endpoints
4. Test with browser dev tools (F12)

## Browser Compatibility

- **Chrome/Chromium**: ✓ Fully supported
- **Firefox**: ✓ Fully supported
- **Safari**: ✓ Fully supported (macOS 12+)
- **Edge**: ✓ Fully supported
- **Internet Explorer**: ✗ Not supported

## Performance

- **Light UI Load**: ~50KB HTML
- **Response Time**: <1s for API calls
- **Pipeline Processing**: 30s - 5min (depends on idea complexity)
- **MCP Testing**: 1-5s per connection

## Security Considerations

- ⚠️ **Not HTTPS by default**: Add SSL certificate for production
- ⚠️ **No Authentication**: Add auth layer before exposing publicly
- ⚠️ **Credentials in Forms**: Use environment variables or secure vaults
- ✓ **CORS**: Enabled for same-origin requests

## Contributing

Improvements and feature suggestions welcome! Areas for enhancement:
- Add WebSocket support for real-time updates
- Create mobile-responsive design
- Add dark mode theme
- Implement persistent configuration storage
- Add more detailed analytics dashboard
- Create result visualization and download

## License

MIT License - See project root LICENSE file

## Support

For issues, questions, or suggestions:
1. Check the Troubleshooting section above
2. Review server logs for detailed error messages
3. Test MCP connections individually
4. Check the GitHub MCP/UI repository for known issues
