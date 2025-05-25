"""
Signal list component for WaveDash application.

This module provides components for displaying and selecting signals from parsed SPICE files.
"""

from dash import html, dcc
from typing import List, Dict, Any, Optional


def create_signal_list_component() -> html.Div:
    """
    Create the signal list display component.
    
    Returns:
        HTML div containing the signal list and plot action button.
    """
    signal_list_component = html.Div(
        id='signal-selection-section',
        children=[
            html.H4("Signal Selection", className='signal-selection-title'),
            
            # Signal list display area
            html.Div(
                id='signal-list-display',
                children=[
                    html.P(
                        "Upload a .raw file to see available signals",
                        style={
                            'color': '#666',
                            'fontStyle': 'italic',
                            'textAlign': 'center',
                            'margin': '20px 0'
                        }
                    )
                ],
                style={
                    'maxHeight': '300px',
                    'overflowY': 'auto',
                    'border': '1px solid #ddd',
                    'borderRadius': '4px',
                    'padding': '10px',
                    'margin': '10px 0'
                }
            ),
            
            # Selected signal display
            html.Div(
                id='selected-signal-display',
                children=[
                    html.P(
                        "Selected Signal: None",
                        style={
                            'margin': '10px 0',
                            'padding': '8px',
                            'backgroundColor': '#f8f9fa',
                            'border': '1px solid #dee2e6',
                            'borderRadius': '4px',
                            'fontSize': '14px'
                        }
                    )
                ]
            ),
            
            # Plot action button
            html.Button(
                "Plot to Active Tile",
                id='plot-button',
                disabled=True,
                style={
                    'width': '100%',
                    'padding': '10px',
                    'margin': '10px 0',
                    'backgroundColor': '#007bff',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '4px',
                    'fontSize': '16px',
                    'cursor': 'not-allowed'
                }
            ),
            
            # Clear tile button
            html.Button(
                "Clear Active Tile",
                id='clear-tile-button',
                disabled=True,
                style={
                    'width': '100%',
                    'padding': '8px',
                    'margin': '5px 0',
                    'backgroundColor': '#dc3545',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '4px',
                    'fontSize': '14px',
                    'cursor': 'not-allowed'
                }
            )
        ],
        className='signal-selection-section'
    )
    
    return signal_list_component


def create_signal_item(signal_name: str, signal_type: str = 'unknown', is_selected: bool = False) -> html.Div:
    """
    Create a clickable signal item for the signal list.
    
    Args:
        signal_name: Name of the signal
        signal_type: Type of signal (voltage, current, power, unknown)
        is_selected: Whether this signal is currently selected
    
    Returns:
        HTML div representing a clickable signal item.
    """
    # Define signal type styling
    type_colors = {
        'voltage': '#28a745',  # Green
        'current': '#dc3545',  # Red
        'power': '#ffc107',    # Yellow
        'unknown': '#6c757d'   # Gray
    }
    
    # Define base style
    base_style = {
        'padding': '8px 12px',
        'margin': '2px 0',
        'borderRadius': '4px',
        'cursor': 'pointer',
        'fontSize': '14px',
        'border': '1px solid transparent',
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center'
    }
    
    # Apply selection styling
    if is_selected:
        base_style.update({
            'backgroundColor': '#e3f2fd',
            'border': '1px solid #2196f3',
            'color': '#1976d2'
        })
    else:
        base_style.update({
            'backgroundColor': '#f8f9fa',
            'border': '1px solid #dee2e6',
            'color': '#495057'
        })
        # Add hover effect class
        base_style['className'] = 'signal-item-hover'
    
    signal_item = html.Div(
        id={'type': 'signal-item', 'index': signal_name},
        children=[
            html.Span(signal_name, style={'flex': '1', 'textAlign': 'left'}),
            html.Span(
                signal_type.upper(),
                style={
                    'fontSize': '10px',
                    'padding': '2px 6px',
                    'borderRadius': '10px',
                    'backgroundColor': type_colors.get(signal_type, type_colors['unknown']),
                    'color': 'white',
                    'fontWeight': 'bold'
                }
            )
        ],
        style=base_style
    )
    
    return signal_item


def create_signal_list_from_data(signals: List[str], selected_signal: Optional[str] = None) -> List[html.Div]:
    """
    Create a list of signal items from signal data.
    
    Args:
        signals: List of signal names
        selected_signal: Currently selected signal name
    
    Returns:
        List of signal item components.
    """
    if not signals:
        return [
            html.P(
                "No signals available",
                style={
                    'color': '#666',
                    'fontStyle': 'italic',
                    'textAlign': 'center',
                    'margin': '20px 0'
                }
            )
        ]
    
    signal_items = []
    for signal in signals:
        # Classify signal type
        signal_type = _classify_signal_type(signal)
        is_selected = signal == selected_signal
        
        signal_item = create_signal_item(signal, signal_type, is_selected)
        signal_items.append(signal_item)
    
    return signal_items


def _classify_signal_type(signal_name: str) -> str:
    """
    Classify signal type based on naming conventions.
    
    Args:
        signal_name: Name of the signal
    
    Returns:
        Signal type classification.
    """
    signal_lower = signal_name.lower()
    
    if signal_lower.startswith('v('):
        return 'voltage'
    elif signal_lower.startswith('i('):
        return 'current'
    elif signal_lower.startswith('p('):
        return 'power'
    else:
        return 'unknown'


def get_plot_button_style(enabled: bool) -> Dict[str, Any]:
    """
    Get styling for the plot button based on enabled state.
    
    Args:
        enabled: Whether the button should be enabled
    
    Returns:
        Dictionary with button styling.
    """
    if enabled:
        return {
            'width': '100%',
            'padding': '10px',
            'margin': '10px 0',
            'backgroundColor': '#28a745',
            'color': 'white',
            'border': 'none',
            'borderRadius': '4px',
            'fontSize': '16px',
            'cursor': 'pointer',
            'transition': 'background-color 0.2s'
        }
    else:
        return {
            'width': '100%',
            'padding': '10px',
            'margin': '10px 0',
            'backgroundColor': '#6c757d',
            'color': 'white',
            'border': 'none',
            'borderRadius': '4px',
            'fontSize': '16px',
            'cursor': 'not-allowed',
            'opacity': '0.6'
        }


def get_clear_button_style(enabled: bool) -> Dict[str, Any]:
    """
    Get styling for the clear button based on enabled state.
    
    Args:
        enabled: Whether the button should be enabled
    
    Returns:
        Dictionary with button styling.
    """
    if enabled:
        return {
            'width': '100%',
            'padding': '8px',
            'margin': '5px 0',
            'backgroundColor': '#dc3545',
            'color': 'white',
            'border': 'none',
            'borderRadius': '4px',
            'fontSize': '14px',
            'cursor': 'pointer',
            'transition': 'background-color 0.2s'
        }
    else:
        return {
            'width': '100%',
            'padding': '8px',
            'margin': '5px 0',
            'backgroundColor': '#6c757d',
            'color': 'white',
            'border': 'none',
            'borderRadius': '4px',
            'fontSize': '14px',
            'cursor': 'not-allowed',
            'opacity': '0.6'
        } 