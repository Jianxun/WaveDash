"""
Tests for data store definitions and initialization.
"""

import pytest
from dash import dcc


def test_data_store_definitions():
    """Test that data stores are defined correctly."""
    from src.data.stores import create_data_stores
    
    stores = create_data_stores()
    
    # Check that all required stores are created
    expected_store_ids = [
        'parsed-data-store',
        'signal-list-store', 
        'selected-signal-store',
        'active-tile-store',
        'tile-config-store'
    ]
    
    assert len(stores) == len(expected_store_ids)
    
    for store in stores:
        assert isinstance(store, dcc.Store)
        assert store.id in expected_store_ids
        
    # Check specific store properties
    store_dict = {store.id: store for store in stores}
    
    # Parsed data store should allow large data
    assert store_dict['parsed-data-store'].storage_type == 'memory'
    
    # UI state stores can be session-based
    assert store_dict['selected-signal-store'].storage_type == 'session'
    assert store_dict['active-tile-store'].storage_type == 'session'


def test_store_initialization_data():
    """Test initial data structure for stores."""
    from src.data.stores import get_initial_store_data
    
    initial_data = get_initial_store_data()
    
    # Check structure of initial data
    assert 'parsed-data-store' in initial_data
    assert 'signal-list-store' in initial_data
    assert 'selected-signal-store' in initial_data
    assert 'active-tile-store' in initial_data
    assert 'tile-config-store' in initial_data
    
    # Check initial values
    assert initial_data['parsed-data-store'] is None  # No data loaded initially
    assert initial_data['signal-list-store'] == []   # Empty signal list
    assert initial_data['selected-signal-store'] is None  # No signal selected
    assert initial_data['active-tile-store'] is None      # No active tile
    assert initial_data['tile-config-store'] == {}        # Empty tile config 