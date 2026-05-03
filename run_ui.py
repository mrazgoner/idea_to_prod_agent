#!/usr/bin/env python
"""
Startup script for Idea-To-Prod UI Server

Usage:
    python run_ui.py [--host HOST] [--port PORT]
    
Examples:
    python run_ui.py                          # Default: localhost:8000
    python run_ui.py --port 5000             # Custom port
    python run_ui.py --host 0.0.0.0 --port 8080
"""

import argparse
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from idea_to_prod.ui_server import run_ui_server


def main():
    """Parse arguments and start the UI server"""
    parser = argparse.ArgumentParser(
        description="Start the Idea-To-Prod UI Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_ui.py                          # Default: localhost:8000
  python run_ui.py --port 5000             # Custom port
  python run_ui.py --host 0.0.0.0 --port 8080
        """
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Server host (default: 127.0.0.1)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Server port (default: 8000)"
    )
    
    args = parser.parse_args()
    
    try:
        run_ui_server(host=args.host, port=args.port)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
