from flask import Flask, request, jsonify
import requests

from openai import OpenAI

app = Flask(__name__)


# Preprocessing function
def preprocess_input(input_text):
    # Example: Remove or replace inappropriate words
    prohibited_words = ["badword1", "badword2"]
    replacement = "****"

    for word in prohibited_words:
        input_text = input_text.replace(word, replacement)

    return input_text


# Postprocessing function
def postprocess_output(output_text):
    # Example: Modify output if needed (e.g., formatting, censoring, etc.)
    return output_text


# Route to handle preprocessing, sending to model server, and postprocessing
@app.route("/process", methods=["POST"])
def process_request():
    data = request.json
    user_input = data.get("input", "")
    print(user_input)

    # Step 1: Preprocess the input
    preprocessed_input = preprocess_input(user_input)

    openai_api_key = "token-abc123"
    openai_api_base = "http://localhost:8000/v1/"

    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )

    chat_response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
        messages=[{"role": "user", "content": preprocessed_input}],
        # prompt="What's Your Name",
        # temperature=0.5,
        # max_tokens=50,
        # top_p=0.9,
        # stop=["\n"],
    )

    return jsonify({"response": chat_response.choices[0].message.content})

    # Step 2: Forward preprocessed input to the model-serving server
    model_server_url = "http://localhost:8000/generate"  # Replace with the actual URL of the model server
    headers = {"User-Agent": "Test Client"}
    data = {
        # "model": "neuralmagic/Meta-Llama-3.1-8B-quantized.w8a8",
        "prompt": preprocessed_input,
        # "max_tokens": 1000,
        "temperature": 0,
    }

    response = requests.post(model_server_url, headers=headers, json=data)
    data = response.content
    print(data)
    if response.status_code == 200:
        # Step 3: Postprocess the output
        model_output = response.json().get("response", "")
        postprocessed_output = postprocess_output(model_output)

        return jsonify({"response": postprocessed_output})
    else:
        return jsonify({"error": "Model server error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
