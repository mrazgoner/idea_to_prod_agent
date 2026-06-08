"""Status label styling functions"""

from .colors import *


def get_status_label_style() -> str:
    """Get default status label style"""
    return f"""
        background-color: {INFO_LIGHT};
        color: {INFO_TEXT};
        padding: 10px;
        border-radius: 6px;
        border-left: 4px solid {INFO};
    """


def get_success_status_style() -> str:
    """Get success status label style"""
    return f"""
        background-color: {SUCCESS_LIGHT};
        color: {SUCCESS_TEXT};
        padding: 10px;
        border-radius: 6px;
        border-left: 4px solid {SUCCESS};
    """


def get_error_status_style() -> str:
    """Get error status label style"""
    return f"""
        background-color: {ERROR_LIGHT};
        color: {ERROR_TEXT};
        padding: 10px;
        border-radius: 6px;
        border-left: 4px solid {ERROR};
    """


def get_warning_status_style() -> str:
    """Get warning status label style"""
    return f"""
        background-color: {WARNING_LIGHT};
        color: {WARNING_TEXT};
        padding: 10px;
        border-radius: 6px;
        border-left: 4px solid {WARNING};
    """


def get_info_status_style() -> str:
    """Get info status label style"""
    return f"""
        background-color: {INFO_LIGHT};
        color: {INFO_TEXT};
        padding: 10px;
        border-radius: 6px;
        border-left: 4px solid {INFO};
    """
