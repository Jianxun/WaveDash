"""
Tests for signal selection functionality.
"""

import pytest
from dash import html
from src.components.signal_list import (
    create_signal_list_component, 
    create_signal_item, 
    create_signal_list_from_data,
    get_plot_button_style,
    _classify_signal_type
)


class TestSignalListComponent:
    """Test signal list component creation."""
    
    def test_create_signal_list_component(self):
        """Test that signal list component is created correctly."""
        component = create_signal_list_component()
        
        assert component.id == 'signal-selection-section'
        assert len(component.children) == 4  # Title, List Display, Selected Display, Button
        
        # Check for signal list display
        signal_list_display = None
        selected_signal_display = None
        plot_button = None
        
        for child in component.children:
            if hasattr(child, 'id'):
                if child.id == 'signal-list-display':
                    signal_list_display = child
                elif child.id == 'selected-signal-display':
                    selected_signal_display = child
                elif child.id == 'plot-button':
                    plot_button = child
        
        assert signal_list_display is not None
        assert selected_signal_display is not None
        assert plot_button is not None
        assert plot_button.disabled == True
    
    def test_create_signal_item(self):
        """Test signal item creation."""
        # Test unselected voltage signal
        signal_item = create_signal_item("V(out)", "voltage", False)
        assert signal_item.id == {'type': 'signal-item', 'index': 'V(out)'}
        assert len(signal_item.children) == 2  # Name span and type span
        
        # Test selected current signal
        selected_item = create_signal_item("I(R1)", "current", True)
        assert selected_item.style['backgroundColor'] == '#e3f2fd'
        assert selected_item.style['border'] == '1px solid #2196f3'
    
    def test_signal_type_classification(self):
        """Test signal type classification."""
        assert _classify_signal_type("V(out)") == "voltage"
        assert _classify_signal_type("v(in)") == "voltage"  # Case insensitive
        assert _classify_signal_type("I(R1)") == "current"
        assert _classify_signal_type("i(vdd)") == "current"
        assert _classify_signal_type("P(load)") == "power"
        assert _classify_signal_type("unknown_signal") == "unknown"
    
    def test_create_signal_list_from_data_empty(self):
        """Test creating signal list with empty data."""
        result = create_signal_list_from_data([])
        assert len(result) == 1
        assert "No signals available" in result[0].children
    
    def test_create_signal_list_from_data_with_signals(self):
        """Test creating signal list with signal data."""
        signals = ["V(out)", "I(R1)", "V(in)"]
        result = create_signal_list_from_data(signals)
        
        assert len(result) == 3
        
        # Check that all signals are represented
        signal_names = []
        for item in result:
            if hasattr(item, 'id') and isinstance(item.id, dict):
                signal_names.append(item.id['index'])
        
        assert set(signal_names) == set(signals)
    
    def test_create_signal_list_with_selection(self):
        """Test creating signal list with a selected signal."""
        signals = ["V(out)", "I(R1)", "V(in)"]
        selected = "V(out)"
        result = create_signal_list_from_data(signals, selected)
        
        # Find the selected item
        selected_item = None
        unselected_items = []
        
        for item in result:
            if hasattr(item, 'id') and isinstance(item.id, dict):
                if item.id['index'] == selected:
                    selected_item = item
                else:
                    unselected_items.append(item)
        
        assert selected_item is not None
        assert selected_item.style['backgroundColor'] == '#e3f2fd'
        
        # Check unselected items
        for item in unselected_items:
            assert item.style['backgroundColor'] == '#f8f9fa'


class TestPlotButtonStyling:
    """Test plot button styling functionality."""
    
    def test_plot_button_enabled_style(self):
        """Test enabled plot button styling."""
        style = get_plot_button_style(True)
        
        assert style['backgroundColor'] == '#28a745'
        assert style['cursor'] == 'pointer'
        assert 'opacity' not in style
    
    def test_plot_button_disabled_style(self):
        """Test disabled plot button styling."""
        style = get_plot_button_style(False)
        
        assert style['backgroundColor'] == '#6c757d'
        assert style['cursor'] == 'not-allowed'
        assert style['opacity'] == '0.6'


class TestSignalTypeClassification:
    """Test signal type classification edge cases."""
    
    def test_voltage_signals(self):
        """Test various voltage signal formats."""
        voltage_signals = [
            "V(out)",
            "v(input)",
            "V(vdd)",
            "v(gnd)",
            "V(net123)"
        ]
        
        for signal in voltage_signals:
            assert _classify_signal_type(signal) == "voltage"
    
    def test_current_signals(self):
        """Test various current signal formats."""
        current_signals = [
            "I(R1)",
            "i(c1)",
            "I(VDD)",
            "i(load)"
        ]
        
        for signal in current_signals:
            assert _classify_signal_type(signal) == "current"
    
    def test_power_signals(self):
        """Test various power signal formats."""
        power_signals = [
            "P(load)",
            "p(resistor)",
            "P(MAIN)"
        ]
        
        for signal in power_signals:
            assert _classify_signal_type(signal) == "power"
    
    def test_unknown_signals(self):
        """Test signals that don't match known patterns."""
        unknown_signals = [
            "time",
            "frequency",
            "phase(out)",
            "temperature",
            "X(something)"
        ]
        
        for signal in unknown_signals:
            assert _classify_signal_type(signal) == "unknown"


if __name__ == '__main__':
    pytest.main([__file__]) 