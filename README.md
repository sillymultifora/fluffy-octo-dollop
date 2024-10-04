This project enables the LLama model to generate answers based on user requests. It consists of two main components: a processing server and a model server.

### Architecture Overview

Processing Server: Handles the preprocessing of user input and the postprocessing of the LLM's responses.
Preprocessing: Includes checking for prohibited/offensive words.
Postprocessing: Includes detecting the toxic level of the response and checking for prohibited/offensive words.
Model Server: Serves the LLama model and generates responses.

### Features

Language Support: English only
Toxicity Detection: Ensures the generated responses are safe for users by checking for offensive content both before and after the model response.
Dockerized Setup: A Docker image is provided, allowing easy deployment and usage of the project.

### Installation Instructions
Clone the repository:
```
git clone https://github.com/sillymultifora/fluffy-octo-dollop.git
cd fluffy-octo-dollop
```
Install the required dependencies:
```
pip install -r requirements.txt
```
### Running the Servers

Start the Model Server (VLLM server) in the background:
```
vllm serve NousResearch/Hermes-3-Llama-3.1-8B --api-key my_token
```
Start the Processing Server in the background:
```
python processing_server.py --api-key my_token --api-base http://localhost:8000/v1/ --model-name NousResearch/Hermes-3-Llama-3.1-8B
```
### Sending Requests

You can send a request to the processing server with the following curl command:
```
curl -X POST http://localhost:5000/process -H "Content-Type: application/json" -d '{"input": "Who are you?"}'
```
This command sends an input prompt to the server and returns a response from the LLama model after preprocessing and postprocessing.