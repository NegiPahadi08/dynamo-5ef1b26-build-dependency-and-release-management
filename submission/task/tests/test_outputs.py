"""
Use this file to define pytest tests that verify the outputs of the task.

This file will be copied to /tests/test_outputs.py and run by the /tests/test.sh file
from the working directory.
"""


def test_outputs():
    """Test that the outputs are correct."""
    import os
import subprocess
import time
import signal

def test_sigterm_stops_without_a_forced_kill():
    # Start the solution script
    process = subprocess.Popen(['bash', 'solution/solve.sh'])

    # Give the script a moment to start and register the trap
    time.sleep(1) 

    # Send SIGTERM signal to the process
    process.send_signal(signal.SIGTERM)

    # Wait for the process to exit gracefully
    try:
        process.wait(timeout=3)
    except subprocess.TimeoutExpired:
        process.kill()
        assert False, "Script did not exit after receiving SIGTERM"

    # Check if it exited with code 0 (success)
    assert process.returncode == 0, "Script failed to exit gracefully with code 0"

def test_output_file_generated():
    # Verify that the expected output file was created
    assert os.path.exists('/app/output.json'), "Output file /app/output.json was not found"
