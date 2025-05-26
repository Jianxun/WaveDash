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
    signal_names = []
    signal_data = {}
    
    traces = list(raw_data.get_trace_names())
    
    if not traces:
        raise ValueError("No traces found in the raw file")

    # Determine the step to process
    # spicelib.RawRead.get_steps() returns a list of step numbers, e.g., [0] or [0, 1, 2]
    # For now, we'll process the first step reported.
    # A more robust handling for multiple/selectable steps can be added if needed.
    simulation_steps = raw_data.get_steps()
    if not simulation_steps:
        # Fallback or error if no steps are explicitly found, though get_steps() usually returns [0] for single runs.
        print("Warning: spicelib.get_steps() returned an empty list. Defaulting to step 0.")
        step_to_process = 0
    else:
        step_to_process = simulation_steps[0] # Use the first step

    # The first trace name is usually the independent variable (time/frequency)
    independent_var_name = traces[0]
    
    # Use get_axis(step) for the independent variable, as recommended by spicelib docs
    # This often includes workarounds for LTSpice issues.
    index_data = raw_data.get_axis(step_to_process)
    if index_data is None:
        raise ValueError(f"Could not retrieve axis data for step {step_to_process} using get_axis().")

    # Extract all other traces as dependent variables for the chosen step
    for trace_name in traces[1:]:  # Skip the first trace (independent variable name)
        try:
            trace_obj = raw_data.get_trace(trace_name)
            # Use get_wave(step) to get data for the specific step
            wave_data = trace_obj.get_wave(step_to_process)
            
            if wave_data is None:
                print(f"Warning: Could not retrieve wave data for trace {trace_name} at step {step_to_process}. Skipping.")
                continue

            if np.iscomplexobj(wave_data):
                signal_data[trace_name] = np.abs(wave_data)
            else:
                signal_data[trace_name] = wave_data
            signal_names.append(trace_name)
        except Exception as e:
            print(f"Warning: Could not extract trace {trace_name} for step {step_to_process}: {e}")
            continue
    
    # Create DataFrame
    # Ensure index_data and all signal_data arrays have compatible lengths.
    # This might require more careful handling if lengths can vary per signal even within a step.
    try:
        df = pd.DataFrame(signal_data, index=index_data)
    except ValueError as ve:
        print(f"Error creating DataFrame: {ve}")
        print("Lengths of data arrays:")
        print(f"  Index ({independent_var_name}): {len(index_data) if index_data is not None else 'None'}")
        for name, s_data in signal_data.items():
            print(f"  Signal ({name}): {len(s_data) if s_data is not None else 'None'}")
        # Attempt to create DataFrame with only signals that match index length
        # This is a temporary workaround; underlying data issues should be investigated
        print("Attempting to create DataFrame with conformant signals only...")
        conformant_signal_data = {}
        for name, s_data in signal_data.items():
            if s_data is not None and len(s_data) == len(index_data):
                conformant_signal_data[name] = s_data
            else:
                print(f"Excluding signal {name} due to length mismatch (len: {len(s_data) if s_data is not None else 'None'}) vs index len: {len(index_data)}")
        
        if not conformant_signal_data and signal_names: # if all signals were mismatched
             df = pd.DataFrame(index=index_data) # Create an empty DataFrame with just the index
             print("Warning: No signals had matching length with the index. DataFrame will be empty.")
        elif not conformant_signal_data and not signal_names: # No signals to begin with
             df = pd.DataFrame(index=index_data)
             print("Warning: No signals found or extracted. DataFrame will be empty.")
        else:
             df = pd.DataFrame(conformant_signal_data, index=index_data)


    # Get metadata
    metadata = {
        'title': getattr(raw_data, 'title', 'Unknown'),
        'date': getattr(raw_data, 'date', 'Unknown'),
        'plot_name': getattr(raw_data, 'plot_name', 'Unknown'),
        'num_points': len(index_data) if index_data is not None else 0,
        'num_signals': len(signal_names), # This counts successfully processed signals
        'independent_var': independent_var_name,
        'processed_step': step_to_process
    }
    
    return {
        'data': df,
        'index': index_data.tolist() if index_data is not None else [],
        'signals': signal_names, # Successfully processed signal names
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