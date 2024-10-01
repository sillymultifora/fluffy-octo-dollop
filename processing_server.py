from flask import Flask, request, jsonify
import requests
from better_profanity import profanity
from openai import OpenAI


app = Flask(__name__)
openai_api_key = "token-abc123"
openai_api_base = "http://localhost:8000/v1/"
model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct"


def get_llm_client():
    return OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )


llm_client = get_llm_client()


def is_bad_content(text):
    # TODO: add detection language?
    return profanity.contains_profanity(text)


def preprocess_input(input_text):
    return input_text


def postprocess_output(output_text):
    return output_text


def generate_bad_response():
    return jsonify({"response": "Your message contains bad words. Please, repharise it"})


# Route to handle preprocessing, sending to model server, and postprocessing
@app.route("/process", methods=["POST"])
def process_request():
    data = request.json
    user_input = data.get("input", "")

    if is_bad_content(user_input):
        return generate_bad_response()
    preprocessed_input = preprocess_input(user_input)

    response = llm_client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": preprocessed_input}],
        # prompt="What's Your Name",
        # temperature=0.5,
        # max_tokens=50,
        # top_p=0.9,
        # stop=["\n"],
    )

    return jsonify({"response": response.choices[0].message.content})

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
