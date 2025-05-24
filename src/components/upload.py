"""
File upload component for WaveDash application.

This module provides components for uploading and handling SPICE .raw files.
"""

from dash import html, dcc
from typing import Dict, Any


def create_file_upload_component() -> html.Div:
    """
    Create the file upload component for .raw SPICE files.
    
    Returns:
        HTML div containing the upload component and status display.
    """
    upload_component = html.Div(
        id='upload-section',
        children=[
            html.H4("File Upload", className='upload-title'),
            
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select a .raw file')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px 0',
                    'cursor': 'pointer'
                },
                # Allow only single file
                multiple=False,
                # Accept .raw files specifically
                accept='.raw'
            ),
            
            # Status/feedback display
            html.Div(
                id='upload-status',
                children="No file uploaded",
                style={
                    'margin': '10px 0',
                    'padding': '5px',
                    'fontSize': '14px',
                    'color': '#666'
                }
            )
        ],
        className='upload-section'
    )
    
    return upload_component


def get_upload_feedback(filename: str, filesize: int) -> Dict[str, Any]:
    """
    Generate feedback information for uploaded file.
    
    Args:
        filename: Name of the uploaded file
        filesize: Size of the uploaded file in bytes
    
    Returns:
        Dictionary with feedback information including status and styling.
    """
    # Convert filesize to human readable format
    if filesize < 1024:
        size_str = f"{filesize} B"
    elif filesize < 1024 * 1024:
        size_str = f"{filesize / 1024:.1f} KB"
    else:
        size_str = f"{filesize / (1024 * 1024):.1f} MB"
    
    return {
        'message': f"✓ Uploaded: {filename} ({size_str})",
        'style': {
            'margin': '10px 0',
            'padding': '5px',
            'fontSize': '14px',
            'color': '#28a745',  # Green for success
            'backgroundColor': '#d4edda',
            'border': '1px solid #c3e6cb',
            'borderRadius': '3px'
        }
    }


def get_error_feedback(error_message: str) -> Dict[str, Any]:
    """
    Generate error feedback for upload issues.
    
    Args:
        error_message: Description of the error
    
    Returns:
        Dictionary with error information including status and styling.
    """
    return {
        'message': f"✗ Error: {error_message}",
        'style': {
            'margin': '10px 0',
            'padding': '5px',
            'fontSize': '14px',
            'color': '#dc3545',  # Red for error
            'backgroundColor': '#f8d7da',
            'border': '1px solid #f5c6cb',
            'borderRadius': '3px'
        }
    } 