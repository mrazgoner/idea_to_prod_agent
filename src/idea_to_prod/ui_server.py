"""
Web UI Server for Idea-To-Prod Agent Team

Provides a FastAPI-based web interface with:
- Workflow diagram with input textbox
- MCP configuration tabs (GitHub, Jira, Google Drive, Playwright)
- Real-time processing status
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import logging
from pathlib import Path
from typing import Optional
from pydantic import BaseModel

from .agents.team import IdeaToProdTeam

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Idea-To-Prod UI", description="Web UI for Idea-To-Prod Agent Team")

# Initialize team
team = IdeaToProdTeam()


# ============================================================================
# Pydantic Models
# ============================================================================

class ProcessIdeaRequest(BaseModel):
    """Request model for processing an idea"""
    idea: str
    enabled_steps: Optional[list] = None
    start_step: int = 0


class MCPConfig(BaseModel):
    """Base model for MCP configuration"""
    mode: str = "stub"
    enable_logging: bool = False


class GitHubConfig(MCPConfig):
    """GitHub MCP configuration"""
    token: Optional[str] = None
    username: Optional[str] = None
    base_url: Optional[str] = "https://api.github.com"


class JiraConfig(MCPConfig):
    """Jira MCP configuration"""
    instance_url: Optional[str] = None
    email: Optional[str] = None
    api_token: Optional[str] = None


class GoogleDriveConfig(MCPConfig):
    """Google Drive MCP configuration"""
    credentials_path: Optional[str] = None
    folder_id: Optional[str] = None


class PlaywrightConfig(MCPConfig):
    """Playwright MCP configuration"""
    headless: bool = True
    timeout: int = 30000


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def get_ui():
    """Serve the main UI page"""
    return get_html_content()


@app.post("/api/process-idea")
async def process_idea(request: ProcessIdeaRequest):
    """
    Process an application idea through the pipeline.
    
    Args:
        request: ProcessIdeaRequest with idea and optional configuration
        
    Returns:
        dict: Processing results
    """
    try:
        if not request.idea.strip():
            raise ValueError("Idea cannot be empty")
        
        logger.info(f"Processing idea: {request.idea[:100]}...")
        
        result = team.process_idea(
            application_idea=request.idea,
            steps_enabled=request.enabled_steps,
            start_of_step=request.start_step
        )
        
        return {
            "success": result["success"],
            "message": "Idea processed successfully" if result["success"] else "Error processing idea",
            "results": result
        }
        
    except Exception as e:
        logger.error(f"Error processing idea: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/test-mcp-connections")
async def test_mcp_connections():
    """
    Test connectivity of all MCP servers.
    
    Returns:
        dict: MCP connectivity test results
    """
    try:
        logger.info("Testing MCP connections...")
        result = team.test_mcp_connections()
        return result
    except Exception as e:
        logger.error(f"Error testing MCP connections: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/test-mcp/{platform}")
async def test_single_mcp(platform: str):
    """
    Test a specific MCP platform.
    
    Args:
        platform: Name of the platform (github, jira, google_drive, playwright)
        
    Returns:
        dict: Test results for the specific platform
    """
    try:
        platform_lower = platform.lower()
        
        test_methods = {
            "github": team._test_github_mcp,
            "jira": team._test_jira_mcp,
            "google_drive": team._test_google_drive_mcp,
            "playwright": team._test_playwright_mcp,
        }
        
        if platform_lower not in test_methods:
            raise ValueError(f"Unknown platform: {platform}")
        
        logger.info(f"Testing {platform} MCP...")
        result = test_methods[platform_lower]()
        
        return {
            "platform": platform,
            "result": result
        }
    except Exception as e:
        logger.error(f"Error testing {platform}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/configure-mcp/github")
async def configure_github(config: GitHubConfig):
    """Configure GitHub MCP settings"""
    try:
        logger.info(f"Configuring GitHub MCP with mode: {config.mode}")
        # TODO: Persist configuration
        return {"success": True, "message": "GitHub MCP configured"}
    except Exception as e:
        logger.error(f"Error configuring GitHub: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/configure-mcp/jira")
async def configure_jira(config: JiraConfig):
    """Configure Jira MCP settings"""
    try:
        logger.info(f"Configuring Jira MCP")
        # TODO: Persist configuration
        return {"success": True, "message": "Jira MCP configured"}
    except Exception as e:
        logger.error(f"Error configuring Jira: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/configure-mcp/google-drive")
async def configure_google_drive(config: GoogleDriveConfig):
    """Configure Google Drive MCP settings"""
    try:
        logger.info(f"Configuring Google Drive MCP")
        # TODO: Persist configuration
        return {"success": True, "message": "Google Drive MCP configured"}
    except Exception as e:
        logger.error(f"Error configuring Google Drive: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/configure-mcp/playwright")
async def configure_playwright(config: PlaywrightConfig):
    """Configure Playwright MCP settings"""
    try:
        logger.info(f"Configuring Playwright MCP")
        # TODO: Persist configuration
        return {"success": True, "message": "Playwright MCP configured"}
    except Exception as e:
        logger.error(f"Error configuring Playwright: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/status")
async def get_status():
    """Get system status"""
    try:
        status = {
            "system": "ready",
            "team": "initialized",
            "mcp_count": 4
        }
        return status
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# HTML Content
# ============================================================================

def get_html_content() -> str:
    """Generate the complete HTML UI"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Idea-To-Prod Agent Team</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 30px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                font-weight: 700;
            }
            
            .header p {
                font-size: 1.1em;
                opacity: 0.95;
            }
            
            .content {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                padding: 40px;
                max-height: calc(100vh - 200px);
                overflow-y: auto;
            }
            
            .section {
                display: flex;
                flex-direction: column;
            }
            
            .section-title {
                font-size: 1.3em;
                font-weight: 600;
                color: #333;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .section-title::before {
                content: '';
                display: inline-block;
                width: 4px;
                height: 24px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 2px;
            }
            
            /* Input Section */
            .input-section {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            
            textarea {
                padding: 15px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 1em;
                font-family: inherit;
                resize: vertical;
                min-height: 150px;
                transition: border-color 0.3s, box-shadow 0.3s;
            }
            
            textarea:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            
            .button-group {
                display: flex;
                gap: 10px;
            }
            
            button {
                flex: 1;
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-size: 1em;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            .btn-process {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            
            .btn-process:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            }
            
            .btn-test {
                background: #4CAF50;
                color: white;
            }
            
            .btn-test:hover {
                background: #45a049;
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(76, 175, 80, 0.3);
            }
            
            .btn-reset {
                background: #f44336;
                color: white;
            }
            
            .btn-reset:hover {
                background: #da190b;
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(244, 67, 54, 0.3);
            }
            
            button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            
            /* Workflow Diagram */
            .workflow-diagram {
                display: flex;
                flex-direction: column;
                gap: 20px;
                background: #f5f5f5;
                padding: 20px;
                border-radius: 8px;
            }
            
            .workflow-step {
                display: flex;
                align-items: center;
                gap: 15px;
            }
            
            .step-box {
                background: white;
                padding: 15px 20px;
                border-radius: 8px;
                border-left: 4px solid #667eea;
                flex: 1;
                font-weight: 600;
                color: #333;
                transition: all 0.3s;
            }
            
            .step-box.completed {
                border-left-color: #4CAF50;
                background: #e8f5e9;
            }
            
            .step-box.active {
                background: #e3f2fd;
                border-left-color: #2196F3;
            }
            
            .step-box.failed {
                background: #ffebee;
                border-left-color: #f44336;
            }
            
            .step-number {
                display: flex;
                align-items: center;
                justify-content: center;
                width: 40px;
                height: 40px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 50%;
                font-weight: 700;
                font-size: 1.1em;
            }
            
            .arrow {
                width: 3px;
                height: 20px;
                background: #667eea;
                margin: -10px auto;
                position: relative;
            }
            
            .arrow::after {
                content: '';
                position: absolute;
                bottom: -8px;
                left: 50%;
                transform: translateX(-50%);
                width: 0;
                height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid #667eea;
            }
            
            /* Tabs Section */
            .tabs-section {
                grid-column: 1 / -1;
            }
            
            .tabs-header {
                display: flex;
                gap: 10px;
                border-bottom: 2px solid #e0e0e0;
                margin-bottom: 20px;
                flex-wrap: wrap;
            }
            
            .tab-button {
                padding: 12px 24px;
                background: none;
                border: none;
                border-bottom: 3px solid transparent;
                cursor: pointer;
                font-weight: 600;
                color: #999;
                transition: all 0.3s;
            }
            
            .tab-button:hover {
                color: #667eea;
            }
            
            .tab-button.active {
                color: #667eea;
                border-bottom-color: #667eea;
            }
            
            .tab-content {
                display: none;
            }
            
            .tab-content.active {
                display: block;
            }
            
            .form-group {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 20px;
            }
            
            .form-field {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
            
            .form-field label {
                font-weight: 600;
                color: #333;
            }
            
            .form-field input,
            .form-field select {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 0.95em;
                transition: border-color 0.3s;
            }
            
            .form-field input:focus,
            .form-field select:focus {
                outline: none;
                border-color: #667eea;
            }
            
            .form-full-width {
                grid-column: 1 / -1;
            }
            
            /* Status Messages */
            .status-message {
                padding: 15px;
                border-radius: 6px;
                margin-bottom: 15px;
                display: none;
            }
            
            .status-message.show {
                display: block;
            }
            
            .status-message.success {
                background: #e8f5e9;
                color: #2e7d32;
                border-left: 4px solid #4CAF50;
            }
            
            .status-message.error {
                background: #ffebee;
                color: #c62828;
                border-left: 4px solid #f44336;
            }
            
            .status-message.info {
                background: #e3f2fd;
                color: #1565c0;
                border-left: 4px solid #2196F3;
            }
            
            .status-message.warning {
                background: #fff3e0;
                color: #e65100;
                border-left: 4px solid #ff9800;
            }
            
            .loading {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .mcp-status {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 15px;
                margin-bottom: 20px;
            }
            
            .mcp-card {
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                border-left: 4px solid #ccc;
                background: #f5f5f5;
            }
            
            .mcp-card.connected {
                border-left-color: #4CAF50;
                background: #e8f5e9;
            }
            
            .mcp-card.disconnected {
                border-left-color: #f44336;
                background: #ffebee;
            }
            
            .mcp-card h3 {
                font-size: 0.95em;
                margin-bottom: 8px;
            }
            
            .mcp-card .status {
                font-size: 0.85em;
                font-weight: 600;
            }
            
            .mcp-card .status.connected {
                color: #2e7d32;
            }
            
            .mcp-card .status.disconnected {
                color: #c62828;
            }
            
            @media (max-width: 1024px) {
                .content {
                    grid-template-columns: 1fr;
                }
                
                .mcp-status {
                    grid-template-columns: repeat(2, 1fr);
                }
            }
            
            @media (max-width: 768px) {
                .mcp-status {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Idea-To-Prod Agent Team</h1>
                <p>Transform your ideas into production-ready, tested code</p>
            </div>
            
            <div class="content">
                <!-- Left: Input Section -->
                <div class="section">
                    <h2 class="section-title">Application Idea</h2>
                    <div class="input-section">
                        <textarea id="ideaInput" placeholder="Describe your application idea here...
                        
Example: A real-time collaboration tool for remote teams with chat, file sharing, and video conferencing capabilities"></textarea>
                        
                        <div class="button-group">
                            <button class="btn-process" onclick="processIdea()">Process Idea</button>
                            <button class="btn-test" onclick="testMCPConnections()">Test MCPs</button>
                            <button class="btn-reset" onclick="resetForm()">Reset</button>
                        </div>
                        
                        <div id="statusMessage" class="status-message"></div>
                    </div>
                </div>
                
                <!-- Right: Workflow Diagram -->
                <div class="section">
                    <h2 class="section-title">Processing Pipeline</h2>
                    <div class="workflow-diagram" id="workflowDiagram">
                        <div class="workflow-step">
                            <div class="step-number">1</div>
                            <div class="step-box" id="step-1">High-Level Design</div>
                        </div>
                        <div class="arrow"></div>
                        
                        <div class="workflow-step">
                            <div class="step-number">2</div>
                            <div class="step-box" id="step-2">Detailed Design</div>
                        </div>
                        <div class="arrow"></div>
                        
                        <div class="workflow-step">
                            <div class="step-number">3</div>
                            <div class="step-box" id="step-3">Code Generation</div>
                        </div>
                        <div class="arrow"></div>
                        
                        <div class="workflow-step">
                            <div class="step-number">4</div>
                            <div class="step-box" id="step-4">Test Generation</div>
                        </div>
                        <div class="arrow"></div>
                        
                        <div class="workflow-step">
                            <div class="step-number">5</div>
                            <div class="step-box" id="step-5">Test Execution</div>
                        </div>
                    </div>
                </div>
                
                <!-- MCP Configuration Tabs -->
                <div class="tabs-section">
                    <h2 class="section-title">MCP Platform Configuration</h2>
                    
                    <div class="mcp-status" id="mcpStatus">
                        <div class="mcp-card" id="github-status">
                            <h3>GitHub</h3>
                            <div class="status">Checking...</div>
                        </div>
                        <div class="mcp-card" id="jira-status">
                            <h3>Jira</h3>
                            <div class="status">Checking...</div>
                        </div>
                        <div class="mcp-card" id="google-drive-status">
                            <h3>Google Drive</h3>
                            <div class="status">Checking...</div>
                        </div>
                        <div class="mcp-card" id="playwright-status">
                            <h3>Playwright</h3>
                            <div class="status">Checking...</div>
                        </div>
                    </div>
                    
                    <div class="tabs-header">
                        <button class="tab-button active" onclick="switchTab('github')">GitHub</button>
                        <button class="tab-button" onclick="switchTab('jira')">Jira</button>
                        <button class="tab-button" onclick="switchTab('google-drive')">Google Drive</button>
                        <button class="tab-button" onclick="switchTab('playwright')">Playwright</button>
                    </div>
                    
                    <!-- GitHub Tab -->
                    <div id="github" class="tab-content active">
                        <h3>GitHub Configuration</h3>
                        <form onsubmit="configureGitHub(event)">
                            <div class="form-group">
                                <div class="form-field">
                                    <label for="github-mode">Mode:</label>
                                    <select id="github-mode">
                                        <option value="stub">Stub (Testing)</option>
                                        <option value="api">API (Real)</option>
                                    </select>
                                </div>
                                <div class="form-field">
                                    <label for="github-token">Personal Access Token:</label>
                                    <input type="password" id="github-token" placeholder="ghp_xxxxxxxxxxxxxxxxxxxx">
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="form-field">
                                    <label for="github-username">Username:</label>
                                    <input type="text" id="github-username" placeholder="Your GitHub username">
                                </div>
                                <div class="form-field">
                                    <label for="github-url">Base URL:</label>
                                    <input type="text" id="github-url" placeholder="https://api.github.com" value="https://api.github.com">
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="form-field form-full-width">
                                    <label for="github-logging">
                                        <input type="checkbox" id="github-logging"> Enable Logging
                                    </label>
                                </div>
                            </div>
                            <button type="submit" class="btn-process">Save GitHub Config</button>
                        </form>
                    </div>
                    
                    <!-- Jira Tab -->
                    <div id="jira" class="tab-content">
                        <h3>Jira Configuration</h3>
                        <form onsubmit="configureJira(event)">
                            <div class="form-group">
                                <div class="form-field">
                                    <label for="jira-mode">Mode:</label>
                                    <select id="jira-mode">
                                        <option value="stub">Stub (Testing)</option>
                                        <option value="api">API (Real)</option>
                                    </select>
                                </div>
                                <div class="form-field">
                                    <label for="jira-url">Instance URL:</label>
                                    <input type="text" id="jira-url" placeholder="https://your-domain.atlassian.net">
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="form-field">
                                    <label for="jira-email">Email:</label>
                                    <input type="email" id="jira-email" placeholder="your-email@example.com">
                                </div>
                                <div class="form-field">
                                    <label for="jira-api-token">API Token:</label>
                                    <input type="password" id="jira-api-token" placeholder="Your API token">
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="form-field form-full-width">
                                    <label for="jira-logging">
                                        <input type="checkbox" id="jira-logging"> Enable Logging
                                    </label>
                                </div>
                            </div>
                            <button type="submit" class="btn-process">Save Jira Config</button>
                        </form>
                    </div>
                    
                    <!-- Google Drive Tab -->
                    <div id="google-drive" class="tab-content">
                        <h3>Google Drive Configuration</h3>
                        <form onsubmit="configureGoogleDrive(event)">
                            <div class="form-group">
                                <div class="form-field">
                                    <label for="gd-mode">Mode:</label>
                                    <select id="gd-mode">
                                        <option value="stub">Stub (Testing)</option>
                                        <option value="api">API (Real)</option>
                                    </select>
                                </div>
                                <div class="form-field">
                                    <label for="gd-creds">Credentials Path:</label>
                                    <input type="text" id="gd-creds" placeholder="/path/to/credentials.json">
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="form-field">
                                    <label for="gd-folder">Folder ID:</label>
                                    <input type="text" id="gd-folder" placeholder="Google Drive folder ID">
                                </div>
                                <div class="form-field form-full-width">
                                    <label for="gd-logging">
                                        <input type="checkbox" id="gd-logging"> Enable Logging
                                    </label>
                                </div>
                            </div>
                            <button type="submit" class="btn-process">Save Google Drive Config</button>
                        </form>
                    </div>
                    
                    <!-- Playwright Tab -->
                    <div id="playwright" class="tab-content">
                        <h3>Playwright Configuration</h3>
                        <form onsubmit="configurePlaywright(event)">
                            <div class="form-group">
                                <div class="form-field">
                                    <label for="pw-mode">Mode:</label>
                                    <select id="pw-mode">
                                        <option value="stub">Stub (Testing)</option>
                                        <option value="api">API (Real)</option>
                                    </select>
                                </div>
                                <div class="form-field">
                                    <label for="pw-headless">
                                        <input type="checkbox" id="pw-headless" checked> Headless Mode
                                    </label>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="form-field">
                                    <label for="pw-timeout">Timeout (ms):</label>
                                    <input type="number" id="pw-timeout" placeholder="30000" value="30000">
                                </div>
                                <div class="form-field form-full-width">
                                    <label for="pw-logging">
                                        <input type="checkbox" id="pw-logging"> Enable Logging
                                    </label>
                                </div>
                            </div>
                            <button type="submit" class="btn-process">Save Playwright Config</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            // ================================================================
            // Tab Switching
            // ================================================================
            
            function switchTab(tabName) {
                // Hide all tabs
                const tabs = document.querySelectorAll('.tab-content');
                tabs.forEach(tab => tab.classList.remove('active'));
                
                // Remove active from all buttons
                const buttons = document.querySelectorAll('.tab-button');
                buttons.forEach(btn => btn.classList.remove('active'));
                
                // Show selected tab
                const selectedTab = document.getElementById(tabName);
                if (selectedTab) {
                    selectedTab.classList.add('active');
                }
                
                // Mark button as active
                event.target.classList.add('active');
            }
            
            // ================================================================
            // Form Functions
            // ================================================================
            
            function configureGitHub(event) {
                event.preventDefault();
                showStatus('GitHub configuration saved!', 'success');
            }
            
            function configureJira(event) {
                event.preventDefault();
                showStatus('Jira configuration saved!', 'success');
            }
            
            function configureGoogleDrive(event) {
                event.preventDefault();
                showStatus('Google Drive configuration saved!', 'success');
            }
            
            function configurePlaywright(event) {
                event.preventDefault();
                showStatus('Playwright configuration saved!', 'success');
            }
            
            // ================================================================
            // Main Functions
            // ================================================================
            
            async function processIdea() {
                const idea = document.getElementById('ideaInput').value;
                
                if (!idea.trim()) {
                    showStatus('Please enter an application idea', 'error');
                    return;
                }
                
                try {
                    showStatus('Processing idea... <span class="loading"></span>', 'info');
                    disableButtons();
                    resetWorkflow();
                    
                    const response = await fetch('/api/process-idea', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            idea: idea,
                            enabled_steps: [true, true, true, true, true],
                            start_step: 0
                        })
                    });
                    
                    if (!response.ok) {
                        throw new Error('Failed to process idea');
                    }
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        showStatus('Idea processed successfully!', 'success');
                        animateWorkflow();
                    } else {
                        showStatus('Error: ' + data.message, 'error');
                    }
                    
                } catch (error) {
                    showStatus('Error: ' + error.message, 'error');
                } finally {
                    enableButtons();
                }
            }
            
            async function testMCPConnections() {
                try {
                    showStatus('Testing MCP connections... <span class="loading"></span>', 'info');
                    
                    const response = await fetch('/api/test-mcp-connections');
                    
                    if (!response.ok) {
                        throw new Error('Failed to test MCP connections');
                    }
                    
                    const data = await response.json();
                    updateMCPStatus(data);
                    
                    if (data.success) {
                        showStatus('All MCPs are connected!', 'success');
                    } else {
                        const failed = data.failed_platforms.join(', ');
                        showStatus('Some MCPs failed: ' + failed, 'warning');
                    }
                    
                } catch (error) {
                    showStatus('Error testing MCPs: ' + error.message, 'error');
                }
            }
            
            function resetForm() {
                document.getElementById('ideaInput').value = '';
                resetWorkflow();
                clearStatus();
            }
            
            // ================================================================
            // UI Helper Functions
            // ================================================================
            
            function showStatus(message, type) {
                const statusEl = document.getElementById('statusMessage');
                statusEl.innerHTML = message;
                statusEl.className = 'status-message show ' + type;
            }
            
            function clearStatus() {
                const statusEl = document.getElementById('statusMessage');
                statusEl.classList.remove('show');
            }
            
            function disableButtons() {
                document.querySelectorAll('.btn-process, .btn-test, .btn-reset').forEach(btn => {
                    btn.disabled = true;
                });
            }
            
            function enableButtons() {
                document.querySelectorAll('.btn-process, .btn-test, .btn-reset').forEach(btn => {
                    btn.disabled = false;
                });
            }
            
            function resetWorkflow() {
                document.querySelectorAll('.step-box').forEach(box => {
                    box.classList.remove('completed', 'active', 'failed');
                });
            }
            
            function animateWorkflow() {
                const steps = document.querySelectorAll('.step-box');
                steps.forEach((step, index) => {
                    setTimeout(() => {
                        step.classList.add('completed');
                    }, 500 * (index + 1));
                });
            }
            
            function updateMCPStatus(data) {
                const mcpPlatforms = {
                    'GitHub': 'github-status',
                    'Jira': 'jira-status',
                    'Google Drive': 'google-drive-status',
                    'Playwright': 'playwright-status'
                };
                
                for (const [platform, elementId] of Object.entries(mcpPlatforms)) {
                    const statusEl = document.getElementById(elementId);
                    const result = data.platform_results[platform];
                    
                    if (result && result.connected) {
                        statusEl.classList.add('connected');
                        statusEl.classList.remove('disconnected');
                        statusEl.querySelector('.status').textContent = '✓ Connected';
                        statusEl.querySelector('.status').className = 'status connected';
                    } else {
                        statusEl.classList.add('disconnected');
                        statusEl.classList.remove('connected');
                        statusEl.querySelector('.status').textContent = '✗ Disconnected';
                        statusEl.querySelector('.status').className = 'status disconnected';
                    }
                }
            }
            
            // ================================================================
            // Initialization
            // ================================================================
            
            document.addEventListener('DOMContentLoaded', function() {
                console.log('UI Loaded - Testing MCP connections...');
                testMCPConnections();
            });
        </script>
    </body>
    </html>
    """


# ============================================================================
# Server Entry Point
# ============================================================================

def run_ui_server(host: str = "0.0.0.0", port: int = 8000):
    """
    Run the UI server.
    
    Args:
        host: Server host (default: 0.0.0.0)
        port: Server port (default: 8000)
    """
    import uvicorn
    
    logger.info(f"Starting Idea-To-Prod UI Server on {host}:{port}")
    logger.info(f"Open your browser to http://localhost:{port}")
    
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_ui_server()
