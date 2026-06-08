"""
Idea-To-Prod Desktop Application Entry Point

A native PyQt6-based desktop application for the Idea-To-Prod Agent Team.
Provides all features of the web UI but as a standalone desktop app.

The application is now organized in a modular structure under the desktop_app package.
See the desktop_app/ folder for the modular implementation.
"""

from idea_to_prod.desktop_app import main


if __name__ == "__main__":
    main()
