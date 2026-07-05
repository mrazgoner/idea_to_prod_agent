"""Styles package for desktop application"""

from .colors import *
from .buttons import *
from .frames import *
from .status_labels import *

__all__ = [
    # Colors
    'PRIMARY', 'PRIMARY_DARK', 'PRIMARY_DARKER',
    'SUCCESS', 'SUCCESS_LIGHT', 'SUCCESS_TEXT', 'SUCCESS_HOVER', 'SUCCESS_PRESSED',
    'ERROR', 'ERROR_LIGHT', 'ERROR_TEXT', 'ERROR_HOVER', 'ERROR_PRESSED',
    'WARNING', 'WARNING_LIGHT', 'WARNING_TEXT',
    'INFO', 'INFO_LIGHT', 'INFO_TEXT',
    'BORDER_LIGHT', 'BACKGROUND_LIGHT', 'BACKGROUND_FRAME',
    'TEXT_PRIMARY', 'TEXT_SECONDARY',
    'STATUS_PENDING', 'STATUS_ACTIVE', 'STATUS_COMPLETED', 'STATUS_FAILED',
    # Buttons
    'get_primary_button_style', 'get_success_button_style', 'get_error_button_style',
    'get_generic_button_style',
    # Frames
    'get_step_frame_style', 'get_step_frame_status_style',
    # Status labels
    'get_status_label_style', 'get_success_status_style', 'get_error_status_style',
    'get_warning_status_style', 'get_info_status_style',
]
