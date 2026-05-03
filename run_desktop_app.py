#!/usr/bin/env python
"""
Launcher script for Idea-To-Prod Desktop Application

Usage:
    python run_desktop_app.py
    
Note: Ensure you're using the virtual environment:
    .venv/Scripts/python.exe run_desktop_app.py  (Windows)
    .venv/bin/python run_desktop_app.py          (macOS/Linux)
"""

import sys
from pathlib import Path

# Verify we're in a virtual environment
venv_indicator = Path(sys.prefix) / "pyvenv.cfg"
if not venv_indicator.exists():
    print("⚠️  WARNING: Not running in virtual environment!")
    print("\nTo activate the virtual environment, run:")
    print("  .venv\\Scripts\\activate  (Windows)")
    print("  source .venv/bin/activate  (macOS/Linux)")
    print("\nThen run this script again:")
    print("  python run_desktop_app.py\n")

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

print("Starting Idea-To-Prod Desktop Application...")

try:
    from idea_to_prod.desktop_app import main
    print("✓ Successfully loaded application")
    print("Launching UI...\n")
    main()
except ImportError as e:
    print(f"\n✗ Error: Missing required package")
    print(f"Details: {e}")
    print("\nTo install required packages, run:")
    print("  pip install PyQt6 anthropic")
    print("\nOr use the setup script:")
    print("  python setup_desktop_app.py")
    sys.exit(1)
except Exception as e:
    print(f"\n✗ Error starting desktop app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
