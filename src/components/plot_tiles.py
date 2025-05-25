"""
Plot tiles component for WaveDash application.

This module provides the main plotting area with 4 clickable plot tiles.
"""

from dash import html, dcc
import plotly.graph_objects as go
from typing import List, Dict, Any, Optional
import pandas as pd


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


def create_multi_signal_plot_figure(signal_names: List[str], time_data: List[float], 
                                   df: 'pd.DataFrame', metadata: Dict, tile_id: str) -> go.Figure:
    """
    Create a plot figure for multiple overlaid signals for comparison.
    
    Args:
        signal_names: List of signal names to plot
        time_data: Time/frequency data for x-axis
        df: DataFrame containing the signal data
        metadata: Metadata about the simulation
        tile_id: ID of the tile for error handling
    
    Returns:
        Plotly figure with multiple signal traces overlaid.
    """
    fig = go.Figure()
    
    # Color palette for multiple signals
    colors = [
        '#1f77b4',  # Blue
        '#ff7f0e',  # Orange  
        '#2ca02c',  # Green
        '#d62728',  # Red
        '#9467bd',  # Purple
        '#8c564b',  # Brown
        '#e377c2',  # Pink
        '#7f7f7f',  # Gray
        '#bcbd22',  # Olive
        '#17becf'   # Cyan
    ]
    
    # Track valid signals and missing signals
    valid_signals = []
    missing_signals = []
    
    # Add traces for each signal
    for i, signal_name in enumerate(signal_names):
        if signal_name not in df.columns:
            missing_signals.append(signal_name)
            continue
            
        # Extract signal data
        signal_data = df[signal_name].tolist()
        color = colors[i % len(colors)]
        
        # Add the signal trace
        fig.add_trace(
            go.Scattergl(
                x=time_data,
                y=signal_data,
                mode='lines',
                name=signal_name,
                line={'width': 2, 'color': color},
                hovertemplate=f'<b>{signal_name}</b><br>' +
                             'Time: %{x:.3e}<br>' +
                             'Value: %{y:.3e}<br>' +
                             '<extra></extra>'
            )
        )
        valid_signals.append(signal_name)
    
    # Handle case where no valid signals were found
    if not valid_signals:
        tile_number = tile_id.split('-')[-1]
        fig = create_empty_plot_figure(f"Plot Tile {tile_number}")
        
        if missing_signals:
            missing_text = ', '.join(missing_signals)
            fig.add_annotation(
                text=f"Signal(s) not found in data:<br>{missing_text}",
                x=0.5, y=0.5,
                xref='paper', yref='paper',
                showarrow=False,
                font={'size': 14, 'color': '#ff0000'}
            )
        return fig
    
    # Determine axis labels based on metadata and signal types
    x_label = metadata.get('independent_var', 'Time')
    
    # Use mixed units if signals have different types
    signal_types = set()
    for signal in valid_signals:
        signal_types.add(_get_signal_type_from_name(signal))
    
    if len(signal_types) == 1:
        # All signals are same type
        signal_type = list(signal_types)[0]
        y_label = _get_y_label_for_type(signal_type)
    else:
        # Mixed signal types
        y_label = 'Amplitude (Mixed Units)'
    
    # Create title showing all signals
    if len(valid_signals) == 1:
        title_text = valid_signals[0]
    elif len(valid_signals) <= 3:
        title_text = ', '.join(valid_signals)
    else:
        title_text = f"{valid_signals[0]}, {valid_signals[1]} + {len(valid_signals)-2} more"
    
    fig.update_layout(
        title={
            'text': title_text,
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
        showlegend=len(valid_signals) > 1,  # Show legend only for multiple signals
        legend={
            'x': 1.02,
            'y': 1,
            'xanchor': 'left',
            'yanchor': 'top',
            'bgcolor': 'rgba(255,255,255,0.8)',
            'bordercolor': '#dee2e6',
            'borderwidth': 1
        }
    )
    
    # Add warning annotation for missing signals
    if missing_signals:
        missing_text = ', '.join(missing_signals)
        fig.add_annotation(
            text=f"⚠️ Missing: {missing_text}",
            x=1, y=1,
            xref='paper', yref='paper',
            xanchor='right', yanchor='top',
            showarrow=False,
            font={'size': 10, 'color': '#ff6b35'},
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#ff6b35',
            borderwidth=1
        )
    
    return fig


def _get_signal_type_from_name(signal_name: str) -> str:
    """Get signal type from signal name."""
    signal_lower = signal_name.lower()
    if signal_lower.startswith('v('):
        return 'voltage'
    elif signal_lower.startswith('i('):
        return 'current'
    elif signal_lower.startswith('p('):
        return 'power'
    else:
        return 'other'


def _get_y_label_for_type(signal_type: str) -> str:
    """Get Y-axis label for signal type."""
    type_labels = {
        'voltage': 'Voltage (V)',
        'current': 'Current (A)', 
        'power': 'Power (W)',
        'other': 'Amplitude'
    }
    return type_labels.get(signal_type, 'Amplitude')


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


def get_tile_status_text(signal_names: Optional[any], is_active: bool) -> str:
    """
    Get status text for tile header.
    
    Args:
        signal_names: Signal name(s) plotted in this tile (string or list)
        is_active: Whether this tile is currently active
    
    Returns:
        Status text for the tile.
    """
    # Handle both old format (single signal) and new format (signal list)
    if signal_names:
        # Convert to list format for consistent handling
        if isinstance(signal_names, str):
            signals = [signal_names]
        elif isinstance(signal_names, list):
            signals = signal_names
        else:
            signals = []
        
        if signals:
            if len(signals) == 1:
                status = f"Plotting: {signals[0]}"
            else:
                # Show count and first signal for multiple signals
                status = f"Plotting {len(signals)} signals: {signals[0]}..."
            
            if is_active:
                status += " (Active)"
            return status
    
    return "Active" if is_active else "Empty" 