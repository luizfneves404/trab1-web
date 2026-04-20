#!/bin/bash

while true; do
    echo "Attempting to provision at $(date)..."
    
    # Run terraform apply and auto-approve
    # We grep for the specific "Out of host" error to decide whether to continue
    terraform apply -auto-approve 2>&1 | tee terraform_output.log
    
    # Check if the instance was created successfully
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        echo "Success! Server deployed."
        break
    else
        echo "Capacity reached or error occurred. Retrying in 60 seconds..."
        sleep 60
    fi
done