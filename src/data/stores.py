"""
Data store definitions for WaveDash application.

This module defines all the dcc.Store components used for managing
application state and data flow between components.
"""

from typing import List, Dict, Any, Optional
from dash import dcc


def create_data_stores() -> List[dcc.Store]:
    """
    Create all data stores required for the WaveDash application.
    
    Returns:
        List of dcc.Store components with appropriate configuration.
    """
    stores = [
        # Main data storage for parsed SPICE file content
        dcc.Store(
            id='parsed-data-store',
            storage_type='memory',  # Large data, session-only
            data=None
        ),
        
        # List of available signal names from loaded file
        dcc.Store(
            id='signal-list-store',
            storage_type='session',
            data=[]
        ),
        
        # Currently selected signal name
        dcc.Store(
            id='selected-signal-store',
            storage_type='session',
            data=None
        ),
        
        # ID of currently active plot tile
        dcc.Store(
            id='active-tile-store',
            storage_type='session',
            data=None
        ),
        
        # Mapping of tile IDs to signal names
        dcc.Store(
            id='tile-config-store',
            storage_type='session',
            data={}
        )
    ]
    
    return stores


def get_initial_store_data() -> Dict[str, Any]:
    """
    Get initial data values for all stores.
    
    Returns:
        Dictionary mapping store IDs to their initial data values.
    """
    return {
        'parsed-data-store': None,
        'signal-list-store': [],
        'selected-signal-store': None,
        'active-tile-store': None,
        'tile-config-store': {}
    } 