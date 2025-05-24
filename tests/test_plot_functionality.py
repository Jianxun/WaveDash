"""
Tests for plot tiles functionality.
"""

import pytest
import plotly.graph_objects as go
from dash import html, dcc
from src.components.plot_tiles import (
    create_plot_tiles_component,
    create_empty_plot_figure,
    create_signal_plot_figure,
    get_tile_wrapper_style,
    get_tile_header_style,
    get_tile_status_text,
    _get_signal_y_label
)


class TestPlotTilesComponent:
    """Test plot tiles component creation."""
    
    def test_create_plot_tiles_component(self):
        """Test that plot tiles component is created correctly."""
        component = create_plot_tiles_component()
        
        assert component.id == 'plot-tiles-container'
        assert len(component.children) == 3  # Title, subtitle, grid
        
        # Find the grid containing the tiles
        plot_grid = None
        for child in component.children:
            if hasattr(child, 'className') and child.className == 'plot-tiles-grid':
                plot_grid = child
                break
        
        assert plot_grid is not None
        assert len(plot_grid.children) == 4  # 4 plot tiles
        
        # Check that each tile has the right structure
        for i, tile_wrapper in enumerate(plot_grid.children, 1):
            assert tile_wrapper.id == f'plot-tile-{i}-wrapper'
            assert len(tile_wrapper.children) == 2  # Header and Graph
            
            # Check header
            header = tile_wrapper.children[0]
            assert header.id == f'plot-tile-{i}-header'
            assert len(header.children) == 2  # Tile number and status
            
            # Check graph
            graph = tile_wrapper.children[1]
            assert isinstance(graph, dcc.Graph)
            assert graph.id == f'plot-tile-{i}'
    
    def test_create_empty_plot_figure(self):
        """Test empty plot figure creation."""
        fig = create_empty_plot_figure("Test Plot")
        
        assert isinstance(fig, go.Figure)
        assert fig.layout.title.text == "Test Plot"
        assert fig.layout.title.x == 0.5  # Centered
        assert fig.layout.xaxis.title.text == "Time / Frequency"
        assert fig.layout.yaxis.title.text == "Amplitude"
        assert len(fig.layout.annotations) == 1  # No signal plotted message
    
    def test_create_signal_plot_figure(self):
        """Test signal plot figure creation."""
        signal_name = "V(out)"
        time_data = [0, 1e-9, 2e-9, 3e-9, 4e-9]
        signal_data = [0, 1.5, 3.0, 1.5, 0]
        metadata = {'independent_var': 'time'}
        
        fig = create_signal_plot_figure(signal_name, time_data, signal_data, metadata)
        
        assert isinstance(fig, go.Figure)
        assert fig.layout.title.text == signal_name
        assert fig.layout.xaxis.title.text == "time"
        assert fig.layout.yaxis.title.text == "Voltage (V)"
        assert len(fig.data) == 1  # One trace
        
        trace = fig.data[0]
        assert trace.name == signal_name
        assert trace.mode == "lines"
        assert len(trace.x) == len(time_data)
        assert len(trace.y) == len(signal_data)


class TestPlotStyling:
    """Test plot styling functionality."""
    
    def test_tile_wrapper_style_inactive(self):
        """Test inactive tile wrapper styling."""
        style = get_tile_wrapper_style(False)
        
        assert style['border'] == '2px solid #dee2e6'
        assert style['backgroundColor'] == '#ffffff'
        assert 'cursor' in style
    
    def test_tile_wrapper_style_active(self):
        """Test active tile wrapper styling."""
        style = get_tile_wrapper_style(True)
        
        assert style['border'] == '3px solid #2196f3'
        assert style['backgroundColor'] == '#f3f8ff'
        assert 'boxShadow' in style
    
    def test_tile_header_style_inactive(self):
        """Test inactive tile header styling."""
        style = get_tile_header_style(False)
        
        assert style['backgroundColor'] == '#f8f9fa'
        assert style['color'] == '#495057'
        assert style['fontWeight'] == 'normal'
    
    def test_tile_header_style_active(self):
        """Test active tile header styling."""
        style = get_tile_header_style(True)
        
        assert style['backgroundColor'] == '#2196f3'
        assert style['color'] == 'white'
        assert style['fontWeight'] == 'bold'


class TestSignalLabeling:
    """Test signal Y-axis labeling functionality."""
    
    def test_voltage_signal_label(self):
        """Test voltage signal Y-axis labeling."""
        assert _get_signal_y_label("V(out)") == "Voltage (V)"
        assert _get_signal_y_label("v(input)") == "Voltage (V)"
        assert _get_signal_y_label("V(vdd)") == "Voltage (V)"
    
    def test_current_signal_label(self):
        """Test current signal Y-axis labeling."""
        assert _get_signal_y_label("I(R1)") == "Current (A)"
        assert _get_signal_y_label("i(load)") == "Current (A)"
        assert _get_signal_y_label("I(VDD)") == "Current (A)"
    
    def test_power_signal_label(self):
        """Test power signal Y-axis labeling."""
        assert _get_signal_y_label("P(load)") == "Power (W)"
        assert _get_signal_y_label("p(resistor)") == "Power (W)"
    
    def test_unknown_signal_label(self):
        """Test unknown signal Y-axis labeling."""
        assert _get_signal_y_label("time") == "Amplitude"
        assert _get_signal_y_label("frequency") == "Amplitude"
        assert _get_signal_y_label("phase(out)") == "Amplitude"


class TestTileStatusText:
    """Test tile status text generation."""
    
    def test_empty_inactive_tile(self):
        """Test status text for empty inactive tile."""
        status = get_tile_status_text(None, False)
        assert status == "Empty"
    
    def test_empty_active_tile(self):
        """Test status text for empty active tile."""
        status = get_tile_status_text(None, True)
        assert status == "Active"
    
    def test_plotting_inactive_tile(self):
        """Test status text for tile plotting a signal (inactive)."""
        status = get_tile_status_text("V(out)", False)
        assert status == "Plotting: V(out)"
    
    def test_plotting_active_tile(self):
        """Test status text for tile plotting a signal (active)."""
        status = get_tile_status_text("V(out)", True)
        assert status == "Plotting: V(out) (Active)"


class TestPlotFigureEdgeCases:
    """Test plot figure creation edge cases."""
    
    def test_signal_plot_with_minimal_metadata(self):
        """Test signal plot creation with minimal metadata."""
        signal_name = "test_signal"
        time_data = [0, 1, 2]
        signal_data = [0, 1, 0]
        metadata = {}  # Empty metadata
        
        fig = create_signal_plot_figure(signal_name, time_data, signal_data, metadata)
        
        assert isinstance(fig, go.Figure)
        assert fig.layout.title.text == signal_name
        # Should default to 'Time' when no independent_var in metadata
        assert fig.layout.xaxis.title.text == "Time"
    
    def test_empty_plot_customization(self):
        """Test empty plot with custom title."""
        custom_title = "Custom Empty Plot"
        fig = create_empty_plot_figure(custom_title)
        
        assert fig.layout.title.text == custom_title
        assert len(fig.layout.annotations) > 0
        assert "No signal plotted" in fig.layout.annotations[0].text


if __name__ == '__main__':
    pytest.main([__file__]) 