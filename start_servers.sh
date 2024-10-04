#!/bin/bash

# Start VLLM server in the background
vllm serve NousResearch/Hermes-3-Llama-3.1-8B --tensor-parallel-size 2  --api-key my_token --dtype auto  &
SERVER_VLMM_PID=$!

# Start processing server in the background
python processing_server.py --api-key my_token --api-base http://localhost:8000/v1/ --model-name NousResearch/Hermes-3-Llama-3.1-8B &
SERVER_PROCESSING_PID=$!

function terminate_servers {
    echo "Terminating servers..."
    kill $SERVER_VLMM_PID
    kill $SERVER_PROCESSING_PID
    wait $SERVER_VLMM_PID
    wait $SERVER_PROCESSING_PID
    exit 0
}

trap terminate_servers SIGINT SIGTERM

# Wait for both process to finish
wait $SERVER_VLMM_PID
wait $SERVER_PROCESSING_PID