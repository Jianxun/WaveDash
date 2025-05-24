"""
Tests for file upload and parsing functionality.
"""

import pytest
import base64
import os
from src.utils.spice_parser import parse_uploaded_raw_file, extract_signals_to_dataframe
from src.components.upload import create_file_upload_component, get_upload_feedback, get_error_feedback
from spicelib import RawRead


class TestSpiceParser:
    """Test SPICE file parsing functionality."""
    
    def test_upload_feedback_generation(self):
        """Test upload feedback message generation."""
        # Test success feedback
        feedback = get_upload_feedback("test.raw", 1024)
        assert "✓ Uploaded" in feedback['message']
        assert "test.raw" in feedback['message']
        assert "1.0 KB" in feedback['message']
        assert feedback['style']['color'] == '#28a745'
        
        # Test error feedback
        error_feedback = get_error_feedback("Invalid file format")
        assert "✗ Error" in error_feedback['message']
        assert "Invalid file format" in error_feedback['message']
        assert error_feedback['style']['color'] == '#dc3545'
    
    def test_file_size_formatting(self):
        """Test file size formatting in feedback."""
        # Test bytes
        feedback = get_upload_feedback("test.raw", 512)
        assert "512 B" in feedback['message']
        
        # Test KB
        feedback = get_upload_feedback("test.raw", 2048)
        assert "2.0 KB" in feedback['message']
        
        # Test MB
        feedback = get_upload_feedback("test.raw", 2048 * 1024)
        assert "2.0 MB" in feedback['message']


class TestUploadComponent:
    """Test upload component creation."""
    
    def test_create_upload_component(self):
        """Test that upload component is created correctly."""
        component = create_file_upload_component()
        
        assert component.id == 'upload-section'
        assert len(component.children) == 3  # Title, Upload, Status
        
        # Check that dcc.Upload is present
        upload_children = component.children
        upload_component = None
        for child in upload_children:
            if hasattr(child, 'id') and child.id == 'upload-data':
                upload_component = child
                break
        
        assert upload_component is not None
        assert upload_component.accept == '.raw'
        assert upload_component.multiple == False


@pytest.mark.integration
class TestFileParsingIntegration:
    """Integration tests for file parsing with real files."""
    
    def test_parse_sample_file_exists(self):
        """Test that sample file exists and can be loaded."""
        sample_file = "raw_data/Ring_Oscillator_7stage.raw"
        assert os.path.exists(sample_file), f"Sample file {sample_file} not found"
        
        # Test that spicelib can read it
        raw_data = RawRead(sample_file)
        traces = list(raw_data.get_trace_names())
        assert len(traces) > 0, "No traces found in sample file"
    
    def test_extract_signals_from_sample(self):
        """Test extracting signals from the sample file."""
        sample_file = "raw_data/Ring_Oscillator_7stage.raw"
        if not os.path.exists(sample_file):
            pytest.skip(f"Sample file {sample_file} not available")
        
        raw_data = RawRead(sample_file)
        result = extract_signals_to_dataframe(raw_data)
        
        assert result['data'] is not None
        assert len(result['signals']) > 0
        assert len(result['index']) > 0
        assert 'metadata' in result
        assert result['metadata']['num_signals'] == len(result['signals'])
        
        # Check DataFrame structure
        df = result['data']
        assert df.shape[0] == len(result['index'])  # Rows match index length
        assert df.shape[1] == len(result['signals'])  # Columns match signals
    
    def test_parse_uploaded_file_format(self):
        """Test parsing a file in the upload format (base64)."""
        sample_file = "raw_data/Ring_Oscillator_7stage.op.raw"  # Use smaller file for testing
        if not os.path.exists(sample_file):
            pytest.skip(f"Sample file {sample_file} not available")
        
        # Read and encode file as if uploaded
        with open(sample_file, 'rb') as f:
            file_content = f.read()
        
        # Encode as base64 (simulating dcc.Upload format)
        encoded = base64.b64encode(file_content).decode('utf-8')
        contents = f"data:application/octet-stream;base64,{encoded}"
        
        # Parse the uploaded format
        result = parse_uploaded_raw_file(contents, "test.raw")
        
        assert result['success'] == True
        assert result['error'] is None
        assert len(result['signals']) > 0
        assert result['data'] is not None
        assert result['index'] is not None
        assert 'metadata' in result


if __name__ == '__main__':
    pytest.main([__file__]) 