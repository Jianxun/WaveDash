"""
SPICE file parsing utilities for WaveDash application.

This module provides functions for parsing SPICE .raw files and converting
them to structured data formats suitable for plotting.
"""

import base64
import io
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from spicelib import RawRead
import tempfile
import os


def parse_uploaded_raw_file(contents: str, filename: str) -> Dict[str, Any]:
    """
    Parse an uploaded .raw file and extract signal data.
    
    Args:
        contents: Base64 encoded file contents from dcc.Upload
        filename: Original filename of the uploaded file
    
    Returns:
        Dictionary containing:
        - 'success': Boolean indicating if parsing was successful
        - 'data': Pandas DataFrame with signals as columns, time/sweep as index
        - 'signals': List of signal names
        - 'error': Error message if parsing failed
    """
    try:
        # Decode the base64 content
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        # Create a temporary file to work with spicelib
        with tempfile.NamedTemporaryFile(delete=False, suffix='.raw') as tmp_file:
            tmp_file.write(decoded)
            tmp_file_path = tmp_file.name
        
        try:
            # Parse with spicelib
            raw_data = RawRead(tmp_file_path)
            
            # Extract data and convert to DataFrame
            result = extract_signals_to_dataframe(raw_data)
            
            return {
                'success': True,
                'data': result['data'].to_dict('records') if result['data'] is not None else None,
                'index': result['index'],
                'signals': result['signals'],
                'metadata': result['metadata'],
                'error': None
            }
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
    except Exception as e:
        return {
            'success': False,
            'data': None,
            'index': None,
            'signals': [],
            'metadata': {},
            'error': str(e)
        }


def extract_signals_to_dataframe(raw_data: RawRead) -> Dict[str, Any]:
    """
    Extract signal data from RawRead object and convert to DataFrame.
    
    Args:
        raw_data: Parsed RawRead object from spicelib
    
    Returns:
        Dictionary containing:
        - 'data': Pandas DataFrame with signals as columns
        - 'index': Index values (time or frequency)
        - 'signals': List of signal names
        - 'metadata': Additional metadata about the simulation
    """
    # Get all traces (signals)
    signal_names = []
    signal_data = {}
    
    # Extract the independent variable (usually time or frequency)
    # This is typically the first trace
    traces = list(raw_data.get_trace_names())
    
    if not traces:
        raise ValueError("No traces found in the raw file")
    
    # The first trace is usually the independent variable (time/frequency)
    independent_var = traces[0]
    index_data = raw_data.get_trace(independent_var).data
    
    # Extract all other traces as dependent variables
    for trace_name in traces[1:]:  # Skip the first trace (independent variable)
        try:
            trace = raw_data.get_trace(trace_name)
            # Handle complex data by taking magnitude for now
            if np.iscomplexobj(trace.data):
                signal_data[trace_name] = np.abs(trace.data)
            else:
                signal_data[trace_name] = trace.data
            signal_names.append(trace_name)
        except Exception as e:
            print(f"Warning: Could not extract trace {trace_name}: {e}")
            continue
    
    # Create DataFrame
    df = pd.DataFrame(signal_data, index=index_data)
    
    # Get metadata
    metadata = {
        'title': getattr(raw_data, 'title', 'Unknown'),
        'date': getattr(raw_data, 'date', 'Unknown'),
        'plot_name': getattr(raw_data, 'plot_name', 'Unknown'),
        'num_points': len(index_data),
        'num_signals': len(signal_names),
        'independent_var': independent_var
    }
    
    return {
        'data': df,
        'index': index_data.tolist(),  # Convert to list for JSON serialization
        'signals': signal_names,
        'metadata': metadata
    }


def get_signal_info(signals: List[str]) -> List[Dict[str, Any]]:
    """
    Generate signal information for display purposes.
    
    Args:
        signals: List of signal names
    
    Returns:
        List of dictionaries with signal information.
    """
    signal_info = []
    
    for signal in signals:
        # Extract basic information about the signal
        info = {
            'name': signal,
            'display_name': signal,
            'type': _classify_signal_type(signal),
            'node': _extract_node_name(signal)
        }
        signal_info.append(info)
    
    return signal_info


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


def _extract_node_name(signal_name: str) -> str:
    """
    Extract node name from signal name.
    
    Args:
        signal_name: Full signal name (e.g., "V(out)")
    
    Returns:
        Node name (e.g., "out").
    """
    # Handle common SPICE naming patterns
    if '(' in signal_name and ')' in signal_name:
        start = signal_name.find('(') + 1
        end = signal_name.find(')')
        return signal_name[start:end]
    
    return signal_name 