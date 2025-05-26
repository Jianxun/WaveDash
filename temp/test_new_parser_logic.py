import sys
import os
import numpy as np
from spicelib import RawRead

# Add the project root to the Python path if this script needs to import from src
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.insert(0, project_root)

def extract_data_with_new_logic(raw_file_path: str):
    print(f"Parsing {raw_file_path} with new logic...")
    raw_data = RawRead(raw_file_path)

    steps = raw_data.get_steps()
    print(f"Detected steps: {steps}")

    if not steps:
        print("No steps found.")
        return None, None, []

    # For this test, let's focus on the first step reported
    step_to_process = steps[0]
    print(f"Processing data for step: {step_to_process}")

    time_vector = raw_data.get_axis(step_to_process)
    
    all_trace_names = raw_data.get_trace_names()
    if not all_trace_names:
        print("No trace names found.")
        return time_vector, None, []

    # The first trace name is usually the independent variable (time/frequency)
    # We already got time_vector via get_axis(), but let's keep its name for metadata.
    independent_var_name = all_trace_names[0]
    print(f"Independent variable name (from get_trace_names): {independent_var_name}")

    extracted_signals = {}
    signal_names_processed = []

    # Try to get a couple of other signals, skipping the independent variable name
    signals_to_extract = [name for name in all_trace_names[1:4] if name != independent_var_name] 

    for signal_name in signals_to_extract:
        try:
            trace_obj = raw_data.get_trace(signal_name)
            wave_data = trace_obj.get_wave(step_to_process)
            
            if np.iscomplexobj(wave_data):
                extracted_signals[signal_name] = np.abs(wave_data)
            else:
                extracted_signals[signal_name] = wave_data
            signal_names_processed.append(signal_name)
            print(f"Successfully extracted signal: {signal_name}")
        except Exception as e:
            print(f"Could not extract signal {signal_name} for step {step_to_process}: {e}")
            
    return time_vector, extracted_signals, signal_names_processed

def is_monotonic(arr):
    if arr is None or len(arr) < 2:
        return True # Or False, depending on definition for empty/single element arrays
    return np.all(np.diff(arr) >= 0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_new_parser_logic.py <raw_file_path>")
        sys.exit(1)

    target_raw_file = sys.argv[1]

    if not os.path.exists(target_raw_file):
        print(f"Error: File not found at {target_raw_file}")
        sys.exit(1)

    time_data, signals_data, processed_signal_names = extract_data_with_new_logic(target_raw_file)

    if time_data is not None:
        print(f"\n--- Time Vector (Step {RawRead(target_raw_file).get_steps()[0] if RawRead(target_raw_file).get_steps() else 'N/A'}) ---")
        print(f"First 10 points: {time_data[:10].tolist() if isinstance(time_data, np.ndarray) else time_data[:10]}")
        monotonic_check = is_monotonic(time_data)
        print(f"Is time vector monotonically increasing? {monotonic_check}")
        if not monotonic_check and len(time_data) > 1:
            diffs = np.diff(time_data)
            violation_indices = np.where(diffs < 0)[0]
            if len(violation_indices) > 0:
                first_violation_idx = violation_indices[0]
                print(f"First non-monotonic point at index {first_violation_idx}:")
                print(f"  time[{first_violation_idx}] = {time_data[first_violation_idx]}, time[{first_violation_idx+1}] = {time_data[first_violation_idx+1]}")

    if signals_data and processed_signal_names:
        for sig_name in processed_signal_names:
            if sig_name in signals_data:
                print(f"\n--- Signal: {sig_name} (Step {RawRead(target_raw_file).get_steps()[0] if RawRead(target_raw_file).get_steps() else 'N/A'}) ---")
                print(f"First 10 points: {signals_data[sig_name][:10].tolist() if isinstance(signals_data[sig_name], np.ndarray) else signals_data[sig_name][:10]}")
    elif not processed_signal_names:
        print("\nNo other signals were processed or extracted.") 