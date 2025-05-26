import sys
import os

# Add the project root to the Python path to allow importing src.utils.spice_parser
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from spicelib import RawRead
# We will use RawRead.get_axis() directly, so extract_signals_to_dataframe might not be needed here
# from src.utils.spice_parser import extract_signals_to_dataframe 
import numpy as np

def check_monotonicity_for_vector(time_vector_np, step_id):
    if time_vector_np is None or len(time_vector_np) == 0:
        print(f"Step {step_id}: Error - Time vector is empty or None.")
        return False

    diff = np.diff(time_vector_np)
    is_monotonic_overall = np.all(diff >= 0)

    print(f"--- Analysis for Step {step_id} ---")
    print(f"Time vector (first 10 points): {time_vector_np[:10].tolist()}")
    print(f"Is time vector monotonically increasing? {is_monotonic_overall}")

    if not is_monotonic_overall:
        violation_index = -1
        for i in range(len(diff)):
            if diff[i] < 0:
                violation_index = i + 1  # diff[i] corresponds to time_array[i+1] - time_array[i]
                break
        
        if violation_index != -1:
            print(f"Monotonicity violated at index {violation_index} within this step.")
            start_idx = max(0, violation_index - 5)
            end_idx = min(len(time_vector_np), violation_index + 6) # Print one more point after violation
            print(f"Time values around violation (indices {start_idx} to {end_idx-1}):")
            for i in range(start_idx, end_idx):
                current_diff_val = 'N/A'
                if i < len(diff): # diff is one element shorter
                    current_diff_val = diff[i]
                
                print(f"  Index {i}: {time_vector_np[i]} (Diff to next: {current_diff_val})")
                if i < len(diff) and diff[i] < 0:
                     print(f"    -> VIOLATION HERE: time_step[{i}] = {time_vector_np[i]}, time_step[{i+1}] = {time_vector_np[i+1]}")
    print(f"--- End Analysis for Step {step_id} ---")
    return is_monotonic_overall

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_monotonic_time.py <raw_file_path>")
        sys.exit(1)

    raw_file_path = sys.argv[1]

    if not os.path.exists(raw_file_path):
        print(f"Error: File not found at {raw_file_path}")
        sys.exit(1)

    print(f"Analyzing raw file: {raw_file_path}")
    try:
        raw_data_obj = RawRead(raw_file_path)
        
        simulation_steps = raw_data_obj.get_steps()
        print(f"Detected simulation steps: {simulation_steps}")

        if not simulation_steps:
            print("Error: No simulation steps found by spicelib.")
            sys.exit(1)

        overall_monotonic = True
        for step_index in simulation_steps:
            print(f"\nProcessing step index: {step_index}")
            try:
                # Get the time axis for the current step
                # .get_axis() returns a numpy array directly if data exists, or list
                time_axis_data = raw_data_obj.get_axis(step_index) 
                
                if isinstance(time_axis_data, list):
                    time_vector_np = np.array(time_axis_data)
                elif isinstance(time_axis_data, np.ndarray):
                    time_vector_np = time_axis_data
                else:
                    print(f"Step {step_index}: Warning - get_axis returned an unexpected type: {type(time_axis_data)}")
                    time_vector_np = np.array([])


                if not check_monotonicity_for_vector(time_vector_np, step_index):
                    overall_monotonic = False
            except Exception as e_step:
                print(f"Error processing step {step_index}: {e_step}")
                overall_monotonic = False
        
        print("\nSummary:")
        if overall_monotonic:
            print("All analyzed steps have monotonically increasing time vectors.")
        else:
            print("At least one step has a non-monotonically increasing time vector.")

    except Exception as e:
        print(f"An error occurred during parsing or step analysis: {e}")
        sys.exit(1) 