"""
Tests for the main application layout and structure.
"""

import pytest
from dash import html, dcc


def test_app_creation():
    """Test that the Dash app can be created."""
    from src.app import create_app
    
    app = create_app()
    
    # Check that app is created with correct properties
    assert app.title == "WaveDash - SPICE Waveform Viewer"
    assert hasattr(app, 'layout')


def test_app_layout_structure():
    """Test that the app layout has the correct structure."""
    from src.app import create_app_layout
    
    layout = create_app_layout()
    
    # Layout should be a Div containing main sections
    assert isinstance(layout, html.Div)
    assert layout.id == 'main-container'
    
    # Check that layout contains expected components
    children_ids = []
    for child in layout.children:
        if hasattr(child, 'id') and child.id:
            children_ids.append(child.id)
    
    expected_sections = [
        'header-section',
        'app-content'
    ]
    
    for section_id in expected_sections:
        assert section_id in children_ids


def test_app_content_structure():
    """Test that the app content area has correct structure."""
    from src.app import create_app_layout
    
    layout = create_app_layout()
    
    # Find the app-content div
    app_content = None
    for child in layout.children:
        if hasattr(child, 'id') and child.id == 'app-content':
            app_content = child
            break
    
    assert app_content is not None
    assert isinstance(app_content, html.Div)
    
    # App content should have sidebar and main content
    content_children_ids = []
    for child in app_content.children:
        if hasattr(child, 'id') and child.id:
            content_children_ids.append(child.id)
    
    expected_content_sections = [
        'sidebar',
        'main-content'
    ]
    
    for section_id in expected_content_sections:
        assert section_id in content_children_ids


def test_data_stores_in_layout():
    """Test that all data stores are included in the layout."""
    from src.app import create_app_layout
    
    layout = create_app_layout()
    
    # Collect all dcc.Store components from layout
    stores_in_layout = []
    
    def collect_stores(component):
        if isinstance(component, dcc.Store):
            stores_in_layout.append(component.id)
        if hasattr(component, 'children'):
            if isinstance(component.children, list):
                for child in component.children:
                    collect_stores(child)
            else:
                collect_stores(component.children)
    
    collect_stores(layout)
    
    # Check that all required stores are present
    expected_stores = [
        'parsed-data-store',
        'signal-list-store',
        'selected-signal-store', 
        'active-tile-store',
        'tile-config-store'
    ]
    
    for store_id in expected_stores:
        assert store_id in stores_in_layout 