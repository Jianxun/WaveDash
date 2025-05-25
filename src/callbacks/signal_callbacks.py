"""
Signal selection callback handlers for WaveDash application.

This module contains callbacks for handling signal selection and plot actions.
"""

from dash import callback, Output, Input, State, ALL, ctx, no_update, html
from typing import List, Dict, Any, Optional, Tuple
import json

from src.components.signal_list import create_signal_list_from_data, get_plot_button_style, get_clear_button_style


@callback(
    Output('signal-list-display', 'children'),
    [
        Input('signal-list-store', 'data')
    ],
    [
        State('selected-signal-store', 'data')
    ]
)
def update_signal_list_display(signals: List[str], selected_signal: Optional[str]) -> List:
    """
    Update the signal list display when signals are loaded or selection changes.
    
    Args:
        signals: List of available signal names
        selected_signal: Currently selected signal name
    
    Returns:
        List of signal item components.
    """
    if not signals:
        return create_signal_list_from_data([])
    
    return create_signal_list_from_data(signals, selected_signal)


@callback(
    Output('selected-signal-store', 'data'),
    [
        Input({'type': 'signal-item', 'index': ALL}, 'n_clicks')
    ],
    [
        State({'type': 'signal-item', 'index': ALL}, 'id'),
        State('selected-signal-store', 'data')
    ]
)
def handle_signal_selection(n_clicks_list: List[Optional[int]], 
                          signal_ids: List[Dict], 
                          current_selection: Optional[str]) -> str:
    """
    Handle signal item clicks to update the selected signal.
    
    Args:
        n_clicks_list: List of n_clicks values for all signal items
        signal_ids: List of signal item IDs
        current_selection: Currently selected signal name
    
    Returns:
        Updated selected signal name.
    """
    # Check if any signal was clicked
    if not ctx.triggered or not any(n_clicks_list):
        return current_selection or no_update
    
    # Find which signal was clicked
    triggered_prop_id = ctx.triggered[0]['prop_id']
    
    # Extract the signal name from the triggered component
    for idx, signal_id in enumerate(signal_ids):
        signal_name = signal_id['index']
        if f'{{"index":"{signal_name}","type":"signal-item"}}.n_clicks' in triggered_prop_id:
            return signal_name
    
    return current_selection or no_update


@callback(
    Output('selected-signal-display', 'children'),
    [
        Input('selected-signal-store', 'data')
    ]
)
def update_selected_signal_display(selected_signal: Optional[str]) -> html.P:
    """
    Update the selected signal display.
    
    Args:
        selected_signal: Currently selected signal name
    
    Returns:
        Updated display component.
    """
    display_text = f"Selected Signal: {selected_signal}" if selected_signal else "Selected Signal: None"
    
    return html.P(
        display_text,
        style={
            'margin': '10px 0',
            'padding': '8px',
            'backgroundColor': '#e3f2fd' if selected_signal else '#f8f9fa',
            'border': f'1px solid {"#2196f3" if selected_signal else "#dee2e6"}',
            'borderRadius': '4px',
            'fontSize': '14px',
            'fontWeight': 'bold' if selected_signal else 'normal',
            'color': '#1976d2' if selected_signal else '#495057'
        }
    )


@callback(
    [
        Output('plot-button', 'disabled'),
        Output('plot-button', 'style'),
        Output('plot-button', 'children'),
        Output('clear-tile-button', 'disabled'),
        Output('clear-tile-button', 'style')
    ],
    [
        Input('selected-signal-store', 'data'),
        Input('active-tile-store', 'data'),
        Input('tile-config-store', 'data')
    ]
)
def update_button_states(selected_signal: Optional[str], 
                        active_tile: Optional[str],
                        tile_config: Dict) -> Tuple[bool, Dict[str, Any], str, bool, Dict[str, Any]]:
    """
    Update the plot and clear button states based on signal selection and active tile.
    
    Args:
        selected_signal: Currently selected signal name
        active_tile: Currently active tile ID
        tile_config: Current tile configuration
    
    Returns:
        Tuple of (plot_disabled, plot_style, plot_text, clear_disabled, clear_style).
    """
    # Plot button logic
    plot_enabled = bool(selected_signal and active_tile)
    
    if plot_enabled:
        plot_text = f"Add '{selected_signal}' to Tile {active_tile[-1] if active_tile else ''}"
        plot_style = get_plot_button_style(True)
    elif selected_signal and not active_tile:
        plot_text = "Select a tile to plot to"
        plot_style = get_plot_button_style(False)
    elif not selected_signal and active_tile:
        plot_text = "Select a signal to plot"
        plot_style = get_plot_button_style(False)
    else:
        plot_text = "Plot to Active Tile"
        plot_style = get_plot_button_style(False)
    
    # Clear button logic
    clear_enabled = bool(active_tile and tile_config and active_tile in tile_config)
    
    if clear_enabled:
        clear_style = get_clear_button_style(True)
    else:
        clear_style = get_clear_button_style(False)
    
    return not plot_enabled, plot_style, plot_text, not clear_enabled, clear_style


@callback(
    Output('tile-config-store', 'data', allow_duplicate=True),
    [
        Input('clear-tile-button', 'n_clicks')
    ],
    [
        State('active-tile-store', 'data'),
        State('tile-config-store', 'data')
    ],
    prevent_initial_call=True
)
def handle_clear_tile_action(n_clicks: Optional[int],
                           active_tile: Optional[str],
                           current_config: Dict) -> Dict:
    """
    Handle the clear tile button click to remove all signals from active tile.
    
    Args:
        n_clicks: Number of times clear button was clicked
        active_tile: Currently active tile ID
        current_config: Current tile configuration
    
    Returns:
        Updated tile configuration with active tile cleared.
    """
    if not n_clicks or not active_tile:
        return current_config or {}
    
    # Remove the active tile from configuration
    updated_config = current_config.copy() if current_config else {}
    if active_tile in updated_config:
        del updated_config[active_tile]
    
    return updated_config


@callback(
    Output('tile-config-store', 'data'),
    [
        Input('plot-button', 'n_clicks')
    ],
    [
        State('selected-signal-store', 'data'),
        State('active-tile-store', 'data'),
        State('tile-config-store', 'data')
    ]
)
def handle_plot_action(n_clicks: Optional[int],
                      selected_signal: Optional[str],
                      active_tile: Optional[str],
                      current_config: Dict) -> Dict:
    """
    Handle the plot button click to append signal to active tile for comparison.
    
    Args:
        n_clicks: Number of times plot button was clicked
        selected_signal: Currently selected signal name
        active_tile: Currently active tile ID
        current_config: Current tile configuration
    
    Returns:
        Updated tile configuration mapping tile IDs to signal lists.
    """
    if not n_clicks or not selected_signal or not active_tile:
        return current_config or {}
    
    # Update the configuration to support multiple signals per tile
    updated_config = current_config.copy() if current_config else {}
    
    # Get current signals for this tile (convert from old format if needed)
    if active_tile in updated_config:
        current_signals = updated_config[active_tile]
        
        # Handle migration from old single-signal format
        if isinstance(current_signals, str):
            # Convert old single signal to list format
            current_signals = [current_signals]
        elif not isinstance(current_signals, list):
            current_signals = []
    else:
        current_signals = []
    
    # Add new signal if not already present (avoid duplicates)
    if selected_signal not in current_signals:
        current_signals.append(selected_signal)
    
    # Update configuration with signal list
    updated_config[active_tile] = current_signals
    
    return updated_config


def register_signal_callbacks(app):
    """
    Register all signal-related callbacks with the app.
    
    Args:
        app: Dash application instance
    """
    # The callback decorators automatically register with the app
    # when this module is imported, so this function is mainly for
    # explicit registration if needed in the future
    pass 