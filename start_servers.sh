#!/bin/bash

# Start VLLM server in the background
vllm serve NousResearch/Hermes-3-Llama-3.1-8B tensor-parallel-size 3 --api-key my_token --dtype auto  &

# Start processing server in the background
python processing_server.py --api-key my_token --api-base http://localhost:8000/v1/ --model-name NousResearch/Hermes-3-Llama-3.1-8B &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?