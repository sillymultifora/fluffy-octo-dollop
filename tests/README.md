## 🧪 Testing

### Installation
Before running the tests, make sure you have installed the required dependencies by running the following command:

```bash
pip install -r requirements.txt
```

### Running the Tests

#### 1. **Start the VLLM Server**
Before executing the tests, ensure that the VLLM server is running:

```bash
vllm serve meta-llama/Meta-Llama-3.1-8B-Instruct --api-key my_token
```

This step is essential to allow the tests to communicate with the model server during execution.

#### 2. **Run Unit Tests**

You can run the unit tests using Python's `unittest` module. The command below runs the specific test file `test_flask_app.py`:

```bash
python -m unittest tests/test_flask_app.py
```

> **Note**: If you're running the tests from the `tests` directory, make sure the root directory of the repository is in your `PYTHONPATH`. You can set it with:

```bash
export PYTHONPATH=..
```
