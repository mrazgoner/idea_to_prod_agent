#!/usr/bin/env python
"""
QUICK START GUIDE - Idea-To-Prod Web UI

This file documents how to get the UI running in under 5 minutes.
"""

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║              ✨ Idea-To-Prod Web UI - Quick Start Guide ✨                     ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝

📋 TABLE OF CONTENTS
  1. Prerequisites
  2. Installation
  3. Starting the Server
  4. Accessing the UI
  5. Using the UI
  6. Common Commands

═══════════════════════════════════════════════════════════════════════════════

1️⃣  PREREQUISITES
  ✓ Python 3.11 or higher
  ✓ pip package manager
  ✓ All core Idea-To-Prod dependencies installed

2️⃣  INSTALLATION (Choose one method)

METHOD A: Automatic Setup (RECOMMENDED)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  cd path/to/IdeaToProdAgent
  python setup_ui.py

  This will:
    • Install FastAPI and uvicorn
    • Display setup instructions
    • Show command examples

METHOD B: Manual Installation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  pip install fastapi uvicorn

3️⃣  STARTING THE SERVER

  Command: python run_ui.py

  With options:
    python run_ui.py --host 127.0.0.1 --port 8000    # Default
    python run_ui.py --port 5000                      # Custom port
    python run_ui.py --host 0.0.0.0 --port 8080      # Public server

4️⃣  ACCESSING THE UI

  Open your browser to:
    👉 http://localhost:8000

  Expected output in terminal:
    INFO:     Started server process [1234]
    INFO:     Uvicorn running on http://0.0.0.0:8000
    INFO:     Application startup complete

5️⃣  USING THE UI

STEP 1: Enter Your Idea
  • Type your application description in the textbox
  • Example: "A real-time chat application with file sharing"

STEP 2: (Optional) Configure MCPs
  • Click on GitHub tab
    - Select Mode (Stub or API)
    - Enter your Personal Access Token (if API mode)
    - Click "Save GitHub Config"
  
  • Repeat for Jira, Google Drive, and Playwright tabs

STEP 3: Test MCP Connections
  • Click "Test MCPs" button
  • Wait for status dashboard to update
  • Green = Connected, Red = Disconnected

STEP 4: Process Your Idea
  • Click "Process Idea" button
  • Watch the pipeline diagram progress through 5 stages:
    1. High-Level Design
    2. Detailed Design
    3. Code Generation
    4. Test Generation
    5. Test Execution
  • Wait for completion notification

STEP 5: Review Results
  • Check status message for confirmation
  • Results are available in the backend

6️⃣  COMMON COMMANDS

Start with default settings:
  python run_ui.py

Start on different port:
  python run_ui.py --port 5000

Start for public access:
  python run_ui.py --host 0.0.0.0 --port 8000

Development mode with auto-reload:
  uvicorn src.idea_to_prod.ui_server:app --reload --port 8000

Stop the server:
  Press Ctrl+C in the terminal

═══════════════════════════════════════════════════════════════════════════════

🎯 UI FEATURES AT A GLANCE

INPUT SECTION
  • Large textbox for describing your idea
  • Example placeholder text
  • Status messages (Success/Error/Info/Warning)

WORKFLOW DIAGRAM
  • 5-stage pipeline visualization
  • Step numbers and names
  • Connected with animated arrows
  • Color-coded progress (pending/active/completed/failed)

MCP STATUS DASHBOARD
  • Shows connection status for:
    - GitHub
    - Jira
    - Google Drive
    - Playwright
  • Auto-tests on page load
  • Manual refresh via button

CONFIGURATION TABS
  • GitHub: API token, username, base URL
  • Jira: Instance URL, email, API token
  • Google Drive: Credentials path, folder ID
  • Playwright: Headless mode, timeout settings

ACTION BUTTONS
  • Process Idea (Blue): Start the pipeline
  • Test MCPs (Green): Verify all connections
  • Reset (Red): Clear all inputs

═══════════════════════════════════════════════════════════════════════════════

🔧 TROUBLESHOOTING

Q: Port 8000 is already in use
A: Use a different port: python run_ui.py --port 8001

Q: "FastAPI not found" error
A: Install dependencies: pip install fastapi uvicorn

Q: UI won't load in browser
A: 1. Check server is running (look for "Uvicorn running on...")
   2. Try clearing browser cache (Ctrl+Shift+Delete)
   3. Try http://127.0.0.1:8000 instead of localhost

Q: MCPs showing as disconnected
A: 1. Check your internet connection
   2. Verify credentials in configuration tabs
   3. Click "Test MCPs" again
   4. Check server console for error messages

Q: Processing seems stuck
A: 1. Check if status shows "Processing..." or if it's hung
   2. Try closing browser tab and reopening
   3. Check server logs for errors
   4. Try restarting the server

═══════════════════════════════════════════════════════════════════════════════

📚 ADDITIONAL RESOURCES

For more detailed information, see:
  • UI_README.md - Complete UI documentation
  • UI_IMPLEMENTATION_SUMMARY.md - Technical implementation details
  • pyproject.toml - Project dependencies

═══════════════════════════════════════════════════════════════════════════════

🚀 YOU'RE ALL SET!

Start the server now:
  python run_ui.py

Then open your browser:
  http://localhost:8000

Happy coding! 🎉

═══════════════════════════════════════════════════════════════════════════════
""")
