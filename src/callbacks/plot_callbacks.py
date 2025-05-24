"""
Plot callback handlers for WaveDash application.

This module contains callbacks for handling plot tile selection and signal plotting.
"""

from dash import callback, Output, Input, State, ALL, ctx, no_update
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
import plotly.graph_objects as go

from src.components.plot_tiles import (
    create_empty_plot_figure, 
    create_signal_plot_figure,
    get_tile_wrapper_style,
    get_tile_header_style,
    get_tile_status_text
)


@callback(
    Output('active-tile-store', 'data'),
    [
        Input('plot-tile-1-wrapper', 'n_clicks'),
        Input('plot-tile-2-wrapper', 'n_clicks'),
        Input('plot-tile-3-wrapper', 'n_clicks'),
        Input('plot-tile-4-wrapper', 'n_clicks')
    ]
)
def handle_tile_selection(tile1_clicks: Optional[int], tile2_clicks: Optional[int],
                         tile3_clicks: Optional[int], tile4_clicks: Optional[int]) -> Optional[str]:
    """
    Handle tile wrapper clicks to update the active tile.
    
    Args:
        tile1_clicks: Number of clicks on tile 1 wrapper
        tile2_clicks: Number of clicks on tile 2 wrapper
        tile3_clicks: Number of clicks on tile 3 wrapper
        tile4_clicks: Number of clicks on tile 4 wrapper
    
    Returns:
        ID of the active tile.
    """
    if not ctx.triggered:
        return no_update
    
    # Find which tile was clicked
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Map wrapper IDs to tile IDs
    tile_mapping = {
        'plot-tile-1-wrapper': 'plot-tile-1',
        'plot-tile-2-wrapper': 'plot-tile-2', 
        'plot-tile-3-wrapper': 'plot-tile-3',
        'plot-tile-4-wrapper': 'plot-tile-4'
    }
    
    return tile_mapping.get(triggered_id, no_update)


@callback(
    [
        Output('plot-tile-1-wrapper', 'style'),
        Output('plot-tile-2-wrapper', 'style'),
        Output('plot-tile-3-wrapper', 'style'),
        Output('plot-tile-4-wrapper', 'style')
    ],
    [
        Input('active-tile-store', 'data')
    ]
)
def update_tile_wrapper_styles(active_tile: Optional[str]) -> Tuple[Dict, Dict, Dict, Dict]:
    """
    Update tile wrapper styles based on active tile.
    
    Args:
        active_tile: ID of the currently active tile
    
    Returns:
        Tuple of style dictionaries for all 4 tile wrappers.
    """
    styles = []
    
    for i in range(1, 5):
        tile_id = f'plot-tile-{i}'
        is_active = (tile_id == active_tile)
        styles.append(get_tile_wrapper_style(is_active))
    
    return tuple(styles)


@callback(
    [
        Output('plot-tile-1-header', 'style'),
        Output('plot-tile-2-header', 'style'),
        Output('plot-tile-3-header', 'style'),
        Output('plot-tile-4-header', 'style')
    ],
    [
        Input('active-tile-store', 'data')
    ]
)
def update_tile_header_styles(active_tile: Optional[str]) -> Tuple[Dict, Dict, Dict, Dict]:
    """
    Update tile header styles based on active tile.
    
    Args:
        active_tile: ID of the currently active tile
    
    Returns:
        Tuple of style dictionaries for all 4 tile headers.
    """
    styles = []
    
    for i in range(1, 5):
        tile_id = f'plot-tile-{i}'
        is_active = (tile_id == active_tile)
        styles.append(get_tile_header_style(is_active))
    
    return tuple(styles)


@callback(
    [
        Output('plot-tile-1-status', 'children'),
        Output('plot-tile-2-status', 'children'),
        Output('plot-tile-3-status', 'children'),
        Output('plot-tile-4-status', 'children')
    ],
    [
        Input('active-tile-store', 'data'),
        Input('tile-config-store', 'data')
    ]
)
def update_tile_status_text(active_tile: Optional[str], 
                           tile_config: Dict) -> Tuple[str, str, str, str]:
    """
    Update tile status text based on active tile and tile configuration.
    
    Args:
        active_tile: ID of the currently active tile
        tile_config: Configuration mapping tile IDs to signal names
    
    Returns:
        Tuple of status text for all 4 tiles.
    """
    status_texts = []
    
    for i in range(1, 5):
        tile_id = f'plot-tile-{i}'
        is_active = (tile_id == active_tile)
        signal_name = tile_config.get(tile_id) if tile_config else None
        status_text = get_tile_status_text(signal_name, is_active)
        status_texts.append(status_text)
    
    return tuple(status_texts)


@callback(
    Output('plot-tile-1', 'figure'),
    [
        Input('tile-config-store', 'data')
    ],
    [
        State('parsed-data-store', 'data')
    ]
)
def update_plot_tile_1(tile_config: Dict, parsed_data: Optional[Dict]) -> go.Figure:
    """Update plot tile 1 figure."""
    return _update_tile_figure('plot-tile-1', tile_config, parsed_data)


@callback(
    Output('plot-tile-2', 'figure'),
    [
        Input('tile-config-store', 'data')
    ],
    [
        State('parsed-data-store', 'data')
    ]
)
def update_plot_tile_2(tile_config: Dict, parsed_data: Optional[Dict]) -> go.Figure:
    """Update plot tile 2 figure."""
    return _update_tile_figure('plot-tile-2', tile_config, parsed_data)


@callback(
    Output('plot-tile-3', 'figure'),
    [
        Input('tile-config-store', 'data')
    ],
    [
        State('parsed-data-store', 'data')
    ]
)
def update_plot_tile_3(tile_config: Dict, parsed_data: Optional[Dict]) -> go.Figure:
    """Update plot tile 3 figure."""
    return _update_tile_figure('plot-tile-3', tile_config, parsed_data)


@callback(
    Output('plot-tile-4', 'figure'),
    [
        Input('tile-config-store', 'data')
    ],
    [
        State('parsed-data-store', 'data')
    ]
)
def update_plot_tile_4(tile_config: Dict, parsed_data: Optional[Dict]) -> go.Figure:
    """Update plot tile 4 figure."""
    return _update_tile_figure('plot-tile-4', tile_config, parsed_data)


def _update_tile_figure(tile_id: str, tile_config: Dict, 
                       parsed_data: Optional[Dict]) -> go.Figure:
    """
    Update a single tile figure based on configuration and data.
    
    Args:
        tile_id: ID of the tile to update
        tile_config: Configuration mapping tile IDs to signal names
        parsed_data: Parsed SPICE data
    
    Returns:
        Updated Plotly figure.
    """
    # Check if this tile has a signal assigned
    if not tile_config or tile_id not in tile_config:
        tile_number = tile_id.split('-')[-1]
        return create_empty_plot_figure(f"Plot Tile {tile_number}")
    
    signal_name = tile_config[tile_id]
    
    # Check if we have parsed data
    if not parsed_data or not parsed_data.get('data'):
        tile_number = tile_id.split('-')[-1]
        return create_empty_plot_figure(f"Plot Tile {tile_number}")
    
    try:
        # Reconstruct DataFrame from stored data
        df_data = parsed_data['data']
        index_data = parsed_data['index']
        metadata = parsed_data.get('metadata', {})
        
        # Convert back to DataFrame
        df = pd.DataFrame(df_data, index=index_data)
        
        # Check if signal exists in the data
        if signal_name not in df.columns:
            tile_number = tile_id.split('-')[-1]
            fig = create_empty_plot_figure(f"Plot Tile {tile_number}")
            fig.add_annotation(
                text=f"Signal '{signal_name}' not found in data",
                x=0.5, y=0.5,
                xref='paper', yref='paper',
                showarrow=False,
                font={'size': 14, 'color': '#ff0000'}
            )
            return fig
        
        # Extract signal data
        time_data = index_data
        signal_data = df[signal_name].tolist()
        
        # Create the plot
        return create_signal_plot_figure(signal_name, time_data, signal_data, metadata)
        
    except Exception as e:
        # Create error plot
        tile_number = tile_id.split('-')[-1]
        fig = create_empty_plot_figure(f"Plot Tile {tile_number}")
        fig.add_annotation(
            text=f"Error plotting signal: {str(e)}",
            x=0.5, y=0.5,
            xref='paper', yref='paper',
            showarrow=False,
            font={'size': 14, 'color': '#ff0000'}
        )
        return fig


def register_plot_callbacks(app):
    """
    Register all plot-related callbacks with the app.
    
    Args:
        app: Dash application instance
    """
    # The callback decorators automatically register with the app
    # when this module is imported, so this function is mainly for
    # explicit registration if needed in the future
    pass 