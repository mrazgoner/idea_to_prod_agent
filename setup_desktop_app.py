#!/usr/bin/env python
"""
Setup script for Idea-To-Prod Desktop Application

Installs all required dependencies for running the desktop app.
"""

import subprocess
import sys
from pathlib import Path


def install_dependencies():
    """Install required Python packages"""
    packages = [
        "PyQt6>=6.5.0",
        "PyQt6-Charts>=6.5.0",
    ]
    
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  Idea-To-Prod Desktop App - Setup".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")
    
    print("Installing required dependencies...")
    print("=" * 60)
    
    for package in packages:
        print(f"\nInstalling {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}")
            return False
    
    print("\n" + "=" * 60)
    print("✓ All dependencies installed successfully!")
    print("=" * 60)
    
    return True


def main():
    """Main setup function"""
    try:
        if not install_dependencies():
            sys.exit(1)
        
        print("\n")
        print("╔" + "=" * 58 + "╗")
        print("║" + "  Getting Started".center(58) + "║")
        print("╚" + "=" * 58 + "╝")
        print("\n")
        
        print("To start the desktop application, run:\n")
        print("  python run_desktop_app.py\n")
        
        print("Features:")
        print("  • Native desktop application with PyQt6")
        print("  • Application idea input textbox")
        print("  • Visual 5-stage pipeline diagram")
        print("  • Real-time MCP connectivity dashboard")
        print("  • Configuration wizard tabs")
        print("  • Multi-threaded processing (responsive UI)")
        print("\n")
        
    except Exception as e:
        print(f"\n✗ Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
