"""
Upload callback handlers for WaveDash application.

This module contains callbacks for handling file uploads and parsing.
"""

from dash import callback, Output, Input, State, no_update
from typing import Tuple, Dict, Any, Optional
import json

from src.utils.spice_parser import parse_uploaded_raw_file
from src.components.upload import get_upload_feedback, get_error_feedback


@callback(
    [
        Output('upload-status', 'children'),
        Output('upload-status', 'style'),
        Output('parsed-data-store', 'data'),
        Output('signal-list-store', 'data')
    ],
    [
        Input('upload-data', 'contents')
    ],
    [
        State('upload-data', 'filename')
    ]
)
def handle_file_upload(contents: Optional[str], filename: Optional[str]) -> Tuple[str, Dict[str, Any], Optional[Dict], list]:
    """
    Handle file upload and parse SPICE data.
    
    Args:
        contents: Base64 encoded file contents from dcc.Upload
        filename: Original filename of the uploaded file
    
    Returns:
        Tuple of:
        - Upload status message
        - Status styling
        - Parsed data for storage
        - List of signal names
    """
    if contents is None:
        return "No file uploaded", {'margin': '10px 0', 'padding': '5px', 'fontSize': '14px', 'color': '#666'}, None, []
    
    if filename is None:
        error_feedback = get_error_feedback("No filename provided")
        return error_feedback['message'], error_feedback['style'], None, []
    
    # Check file extension
    if not filename.lower().endswith('.raw'):
        error_feedback = get_error_feedback("Please upload a .raw file")
        return error_feedback['message'], error_feedback['style'], None, []
    
    try:
        # Parse the uploaded file
        parsing_result = parse_uploaded_raw_file(contents, filename)
        
        if not parsing_result['success']:
            error_feedback = get_error_feedback(f"Failed to parse file: {parsing_result['error']}")
            return error_feedback['message'], error_feedback['style'], None, []
        
        # Calculate file size from base64 content for feedback
        content_type, content_string = contents.split(',')
        file_size = len(content_string) * 3 / 4  # Approximate original size
        
        # Prepare success feedback
        success_feedback = get_upload_feedback(filename, int(file_size))
        
        # Prepare data for storage
        # Store both the DataFrame records and metadata
        stored_data = {
            'data': parsing_result['data'],
            'index': parsing_result['index'],
            'metadata': parsing_result['metadata'],
            'filename': filename
        }
        
        return (
            success_feedback['message'],
            success_feedback['style'],
            stored_data,
            parsing_result['signals']
        )
        
    except Exception as e:
        error_feedback = get_error_feedback(f"Unexpected error: {str(e)}")
        return error_feedback['message'], error_feedback['style'], None, []


def register_upload_callbacks(app):
    """
    Register all upload-related callbacks with the app.
    
    Args:
        app: Dash application instance
    """
    # The callback decorator automatically registers with the app
    # when this module is imported, so this function is mainly for
    # explicit registration if needed in the future
    pass 