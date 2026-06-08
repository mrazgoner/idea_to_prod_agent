"""Desktop application package initialization"""

import sys
from PyQt6.QtWidgets import QApplication
from idea_to_prod.desktop_app.main import IdeaToProdApp


def main():
    """Main entry point for desktop application"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = IdeaToProdApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
