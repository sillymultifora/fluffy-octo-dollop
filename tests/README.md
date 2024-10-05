# Testing

### Installation
Install the required dependencies by running:

```
pip install -r requirements.txt
```

### Running the Tests
Before running the tests please, run the vllm server by:
```
vllm serve meta-llama/Meta-Llama-3.1-8B-Instruct --api-key my_token
```

To run the unit tests, use the following command:

```
python -m unittest tests/test_flask_app.py
```
Note: If you're running the tests from the tests directory, you may need to add the root directory of the repository to your PYTHONPATH. You can do this by running:

```
export PYTHONPATH=..
```
Alternatively, you can avoid modifying the PYTHONPATH by running the tests from the root directory of the repository:

```
python -m unittest discover tests
```
This will automatically discover and run all tests in the tests/ folder.