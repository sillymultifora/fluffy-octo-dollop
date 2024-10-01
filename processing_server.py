from argparse import ArgumentParser

from better_profanity import profanity
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--api-key", type=str, default="token-abc123")
    parser.add_argument("--api-base", type=str, default="http://localhost:8000/v1/")
    parser.add_argument("--model-name", type=str, default="meta-llama/Meta-Llama-3.1-8B-Instruct")
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()
    app.run(host=args.host, port=args.port)
