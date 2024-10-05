# 🦙 LLama-based Question Answering Service

This project leverages the LLama model to generate answers based on user requests. It is composed of two primary components: a **Processing Server** and a **Model Server**, working together to provide seamless and safe interactions.

---

## 📜 Architecture Overview

### **1. Processing Server**  
Handles user input and response processing, with two core tasks:
- **Preprocessing**: Validates input for prohibited or offensive words.
- **Postprocessing**: Detects the toxicity level of the model's response and rechecks for any prohibited or offensive words.

### **2. Model Server**  
Hosts the LLama model and generates responses to user inputs.

---

## ✨ Features

- **Language Support**: English only.
- **Toxicity Detection**: Ensures safe responses by checking for offensive content both before and after processing.
- **Dockerized Setup**: Simplified deployment using a pre-built Docker image.

---

## 🚀 Installation Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sillymultifora/fluffy-octo-dollop.git
   cd fluffy-octo-dollop
   ```

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
The repo was tested on python3.8 and cuda 12.1
> **Note**:  
> This service utilizes the `meta-llama/Meta-Llama-3.1-8B-Instruct` model. To work with this model, access must be obtained via [Hugging Face](https://huggingface.co/meta-llama/Meta-Llama-3.1-8B-Instruct).  
> If you'd prefer a different model, simply update the model name in the configuration.

---

## 🛠️ Running the Servers

### **Start the servers with a single command**:
```bash
bash start_servers.sh
```

### **Manually start the servers**:

1. **Start the Model Server** (VLLM server) in the background:
   ```bash
   vllm serve meta-llama/Meta-Llama-3.1-8B-Instruct --api-key my_token
   ```

2. **Start the Processing Server** in the background:
   ```bash
   python processing_server.py --api-key my_token --api-base http://localhost:8000/v1/ --model-name meta-llama/Meta-Llama-3.1-8B-Instruct
   ```

---

## 📡 Sending Requests

You can send a request to the processing server using `curl`:

```bash
curl -X POST http://localhost:5000/process \
  -H "Content-Type: application/json" \
  -d '{"input": "Who are you?"}'
```

This command sends an input prompt to the server, processes it, and returns a response from the LLama model after both preprocessing and postprocessing.

---
