"""
Plot tiles component for WaveDash application.

This module provides the main plotting area with 4 clickable plot tiles.
"""

from dash import html, dcc
import plotly.graph_objects as go
from typing import List, Dict, Any, Optional


def create_plot_tiles_component() -> html.Div:
    """
    Create the main plot tiles component with 4 clickable plot areas.
    
    Returns:
        HTML div containing 4 plot tiles arranged vertically.
    """
    plot_tiles = []
    
    # Create 4 plot tiles
    for i in range(1, 5):
        tile_id = f'plot-tile-{i}'
        
        # Create a wrapper div that makes the tile clickable
        tile_wrapper = html.Div(
            id=f'{tile_id}-wrapper',
            children=[
                # Tile header with number and status
                html.Div(
                    id=f'{tile_id}-header',
                    children=[
                        html.Span(f"Tile {i}", className='tile-number'),
                        html.Span("Empty", id=f'{tile_id}-status', className='tile-status')
                    ],
                    className='tile-header'
                ),
                
                # The actual plot component
                dcc.Graph(
                    id=tile_id,
                    figure=create_empty_plot_figure(f"Plot Tile {i}"),
                    config={
                        'displayModeBar': True,
                        'displaylogo': False,
                        'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d']
                    },
                    style={'height': '300px'}
                )
            ],
            className='plot-tile-wrapper',
            style=get_tile_wrapper_style(False)  # Not active by default
        )
        
        plot_tiles.append(tile_wrapper)
    
    plot_tiles_component = html.Div(
        id='plot-tiles-container',
        children=[
            html.H3("Plot Tiles", className='plot-tiles-title'),
            html.P("Click on a tile to make it active, then use 'Plot to Active Tile' to display signals.", 
                   className='plot-tiles-subtitle'),
            html.Div(plot_tiles, className='plot-tiles-grid')
        ],
        className='plot-tiles-container'
    )
    
    return plot_tiles_component


def create_empty_plot_figure(title: str) -> go.Figure:
    """
    Create an empty plot figure as placeholder.
    
    Args:
        title: Title for the plot
    
    Returns:
        Empty Plotly figure with styling.
    """
    fig = go.Figure()
    
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        xaxis={
            'title': 'Time / Frequency',
            'showgrid': True,
            'gridcolor': '#e0e0e0'
        },
        yaxis={
            'title': 'Amplitude',
            'showgrid': True,
            'gridcolor': '#e0e0e0'
        },
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin={'l': 60, 'r': 20, 't': 60, 'b': 60},
        annotations=[
            {
                'text': 'No signal plotted<br>Select a signal and click "Plot to Active Tile"',
                'x': 0.5,
                'y': 0.5,
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 14, 'color': '#666666'},
                'align': 'center'
            }
        ]
    )
    
    return fig


def create_signal_plot_figure(signal_name: str, time_data: List[float], 
                            signal_data: List[float], metadata: Dict) -> go.Figure:
    """
    Create a plot figure for a specific signal.
    
    Args:
        signal_name: Name of the signal to plot
        time_data: Time/frequency data for x-axis
        signal_data: Signal amplitude data for y-axis
        metadata: Metadata about the simulation
    
    Returns:
        Plotly figure with the signal data.
    """
    fig = go.Figure()
    
    # Add the signal trace
    fig.add_trace(
        go.Scattergl(
            x=time_data,
            y=signal_data,
            mode='lines',
            name=signal_name,
            line={'width': 2, 'color': '#1f77b4'},
            hovertemplate=f'<b>{signal_name}</b><br>' +
                         'Time: %{x:.3e}<br>' +
                         'Value: %{y:.3e}<br>' +
                         '<extra></extra>'
        )
    )
    
    # Determine axis labels based on metadata
    x_label = metadata.get('independent_var', 'Time')
    y_label = _get_signal_y_label(signal_name)
    
    fig.update_layout(
        title={
            'text': signal_name,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': '#1976d2'}
        },
        xaxis={
            'title': x_label,
            'showgrid': True,
            'gridcolor': '#e0e0e0'
        },
        yaxis={
            'title': y_label,
            'showgrid': True,
            'gridcolor': '#e0e0e0'
        },
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin={'l': 60, 'r': 20, 't': 60, 'b': 60},
        showlegend=False
    )
    
    return fig


def get_tile_wrapper_style(is_active: bool) -> Dict[str, Any]:
    """
    Get styling for tile wrapper based on active state.
    
    Args:
        is_active: Whether this tile is currently active
    
    Returns:
        Dictionary with wrapper styling.
    """
    base_style = {
        'margin': '10px 0',
        'borderRadius': '8px',
        'padding': '10px',
        'cursor': 'pointer',
        'transition': 'all 0.2s ease'
    }
    
    if is_active:
        base_style.update({
            'border': '3px solid #2196f3',
            'backgroundColor': '#f3f8ff',
            'boxShadow': '0 4px 8px rgba(33, 150, 243, 0.3)'
        })
    else:
        base_style.update({
            'border': '2px solid #dee2e6',
            'backgroundColor': '#ffffff',
            'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)'
        })
    
    return base_style


def get_tile_header_style(is_active: bool) -> Dict[str, Any]:
    """
    Get styling for tile header based on active state.
    
    Args:
        is_active: Whether this tile is currently active
    
    Returns:
        Dictionary with header styling.
    """
    return {
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center',
        'padding': '5px 10px',
        'marginBottom': '5px',
        'borderRadius': '4px',
        'backgroundColor': '#2196f3' if is_active else '#f8f9fa',
        'color': 'white' if is_active else '#495057',
        'fontSize': '14px',
        'fontWeight': 'bold' if is_active else 'normal'
    }


def _get_signal_y_label(signal_name: str) -> str:
    """
    Get appropriate Y-axis label based on signal type.
    
    Args:
        signal_name: Name of the signal
    
    Returns:
        Appropriate Y-axis label.
    """
    signal_lower = signal_name.lower()
    
    if signal_lower.startswith('v('):
        return 'Voltage (V)'
    elif signal_lower.startswith('i('):
        return 'Current (A)'
    elif signal_lower.startswith('p('):
        return 'Power (W)'
    else:
        return 'Amplitude'


def get_tile_status_text(signal_name: Optional[str], is_active: bool) -> str:
    """
    Get status text for tile header.
    
    Args:
        signal_name: Name of signal plotted in this tile
        is_active: Whether this tile is currently active
    
    Returns:
        Status text for the tile.
    """
    if signal_name:
        status = f"Plotting: {signal_name}"
        if is_active:
            status += " (Active)"
        return status
    else:
        return "Active" if is_active else "Empty" 