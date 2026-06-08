"""Frame and container styling functions"""

from .colors import *


def get_step_frame_style() -> str:
    """Get default step frame style"""
    return f"""
        QFrame {{
            background-color: {BACKGROUND_FRAME};
            border-left: 4px solid {PRIMARY};
            border-radius: 6px;
            padding: 12px;
        }}
    """


def get_step_frame_status_style(status: str) -> str:
    """Get step frame style based on status
    
    Args:
        status: One of 'pending', 'active', 'completed', 'failed'
    """
    if status == "completed":
        return f"""
            QFrame {{
                border-left: 4px solid {STATUS_COMPLETED};
                background-color: {SUCCESS_LIGHT};
                border-radius: 6px;
                padding: 12px;
            }}
        """
    elif status == "active":
        return f"""
            QFrame {{
                border-left: 4px solid {STATUS_ACTIVE};
                background-color: {INFO_LIGHT};
                border-radius: 6px;
                padding: 12px;
            }}
        """
    elif status == "failed":
        return f"""
            QFrame {{
                border-left: 4px solid {STATUS_FAILED};
                background-color: {ERROR_LIGHT};
                border-radius: 6px;
                padding: 12px;
            }}
        """
    else:  # pending
        return f"""
            QFrame {{
                border-left: 4px solid {BORDER_LIGHT};
                background-color: {BACKGROUND_FRAME};
                border-radius: 6px;
                padding: 12px;
            }}
        """


def get_mcp_card_style() -> str:
    """Get MCP card default style"""
    return f"""
        QFrame {{
            background-color: {BACKGROUND_LIGHT};
            border-left: 4px solid {BORDER_LIGHT};
            border-radius: 6px;
            padding: 12px;
        }}
    """


def get_mcp_card_connected_style() -> str:
    """Get MCP card connected style"""
    return f"""
        QFrame {{
            background-color: {SUCCESS_LIGHT};
            border-left: 4px solid {STATUS_COMPLETED};
            border-radius: 6px;
            padding: 12px;
        }}
    """


def get_mcp_card_disconnected_style() -> str:
    """Get MCP card disconnected style"""
    return f"""
        QFrame {{
            background-color: {ERROR_LIGHT};
            border-left: 4px solid {STATUS_FAILED};
            border-radius: 6px;
            padding: 12px;
        }}
    """
