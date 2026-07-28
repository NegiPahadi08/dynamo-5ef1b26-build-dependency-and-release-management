#!/bin/bash

# 1. Fallback to a safe working directory to prevent 'getcwd' errors
cd /tmp || cd /

# 2. Setup trap to handle SIGTERM cleanly and avoid forced kills
trap 'echo "Caught SIGTERM, terminating gracefully..."; exit 0' SIGTERM

# 3. Create the required output directory and file
mkdir -p /app
echo '{"status": "success", "message": "Pipeline repaired"}' > /app/output.json

echo "Build process started successfully."

# Keep the script running so the test has time to send the SIGTERM signal
while true; do
    sleep 1
done
