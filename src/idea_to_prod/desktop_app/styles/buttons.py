"""Button styling functions"""

from .colors import *


def get_primary_button_style() -> str:
    """Get primary button style"""
    return f"""
        QPushButton {{
            background-color: {PRIMARY};
            color: white;
            padding: 10px;
            border-radius: 6px;
            border: none;
        }}
        QPushButton:hover {{
            background-color: {PRIMARY_DARK};
        }}
        QPushButton:pressed {{
            background-color: {PRIMARY_DARKER};
        }}
    """


def get_success_button_style() -> str:
    """Get success button style"""
    return f"""
        QPushButton {{
            background-color: {SUCCESS};
            color: white;
            padding: 10px;
            border-radius: 6px;
            border: none;
        }}
        QPushButton:hover {{
            background-color: {SUCCESS_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {SUCCESS_PRESSED};
        }}
    """


def get_error_button_style() -> str:
    """Get error button style"""
    return f"""
        QPushButton {{
            background-color: {ERROR};
            color: white;
            padding: 10px;
            border-radius: 6px;
            border: none;
        }}
        QPushButton:hover {{
            background-color: {ERROR_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {ERROR_PRESSED};
        }}
    """


def get_generic_button_style(bg_color: str, hover_color: str, pressed_color: str) -> str:
    """Get generic button style with custom colors"""
    return f"""
        QPushButton {{
            background-color: {bg_color};
            color: white;
            padding: 8px;
            border-radius: 4px;
            border: none;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
        QPushButton:pressed {{
            background-color: {pressed_color};
        }}
    """
