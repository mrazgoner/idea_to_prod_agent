#!/usr/bin/env python
"""
Quick setup script for Idea-To-Prod UI

This script installs all required dependencies and provides instructions
for running the UI server.
"""

import subprocess
import sys
from pathlib import Path


def install_dependencies():
    """Install required Python packages"""
    packages = [
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.0.0",
    ]
    
    print("Installing required dependencies...")
    print("=" * 60)
    
    for package in packages:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    print("=" * 60)
    print("✓ All dependencies installed successfully!")


def main():
    """Main setup function"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  Idea-To-Prod UI - Setup Script".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")
    
    try:
        # Install dependencies
        install_dependencies()
        
        # Print instructions
        print("\n")
        print("╔" + "=" * 58 + "╗")
        print("║" + "  Getting Started".center(58) + "║")
        print("╚" + "=" * 58 + "╝")
        print("\n")
        
        print("To start the UI server, run one of the following commands:\n")
        print("  1. Default (localhost:8000):")
        print("     python run_ui.py\n")
        print("  2. Custom port:")
        print("     python run_ui.py --port 5000\n")
        print("  3. Custom host and port:")
        print("     python run_ui.py --host 0.0.0.0 --port 8080\n")
        
        print("After starting the server, open your browser to:")
        print("  http://localhost:8000 (default)")
        print("\n")
        
        print("Features:")
        print("  • Input textbox for application ideas")
        print("  • Visual pipeline diagram with step progression")
        print("  • MCP connectivity status dashboard")
        print("  • Configuration tabs for GitHub, Jira, Google Drive, Playwright")
        print("  • Real-time processing status")
        print("\n")
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error installing dependencies: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
