"""
Main WaveDash application module.

This module contains the Dash app initialization, layout creation,
and main application entry point.
"""

import dash
from dash import html, dcc
from typing import List

from src.data.stores import create_data_stores
from src.components.upload import create_file_upload_component
from src.components.signal_list import create_signal_list_component
# Import callbacks to register them
import src.callbacks.upload_callbacks
import src.callbacks.signal_callbacks


def create_app() -> dash.Dash:
    """
    Create and configure the main Dash application.
    
    Returns:
        Configured Dash app instance.
    """
    app = dash.Dash(
        __name__,
        title="WaveDash - SPICE Waveform Viewer",
        suppress_callback_exceptions=True
    )
    
    # Set the layout
    app.layout = create_app_layout()
    
    return app


def create_app_layout() -> html.Div:
    """
    Create the main application layout.
    
    Returns:
        Main layout component containing all UI sections and data stores.
    """
    # Get all data stores
    data_stores = create_data_stores()
    
    layout = html.Div(
        id='main-container',
        children=[
            # Data stores (hidden components for state management)
            *data_stores,
            
            # Header section
            html.Div(
                id='header-section',
                children=[
                    html.H1("WaveDash", className='app-title'),
                    html.P("SPICE Waveform Viewer", className='app-subtitle')
                ],
                className='header'
            ),
            
            # Main app content
            html.Div(
                id='app-content',
                children=[
                    # Sidebar
                    html.Div(
                        id='sidebar',
                        children=[
                            html.H3("Controls", className='sidebar-title'),
                            create_file_upload_component(),
                            html.Hr(),
                            create_signal_list_component()
                        ],
                        className='sidebar'
                    ),
                    
                    # Main content area
                    html.Div(
                        id='main-content',
                        children=[
                            html.H3("Plot Area", className='plot-area-title'),
                            html.P("Plot tiles will go here.")
                        ],
                        className='main-content'
                    )
                ],
                className='app-content'
            )
        ],
        className='main-container'
    )
    
    return layout


def main():
    """Main entry point for the application."""
    app = create_app()
    app.run(debug=True)


if __name__ == '__main__':
    main() 