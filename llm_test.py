# llm_test.py

# Make sure you have the dependency installed first:
# pip install llama-cpp-python

def test_llm():
    """Test the LLM functionality by generating a response to a test prompt."""

    print("Initializing LLM test...")

    try:
        # Try to import the required module
        from llama_cpp import Llama
    except ImportError:
        print("ERROR: The 'llama-cpp-python' package is not installed.")
        print("Please install it using: pip install llama-cpp-python")
        return

    # Path to your model - update this to match your model file location
    model_path = "C:\\Users\\Derek\\OneDrive\\Desktop\\PythonProj\\DnD_Project\\models\\llama3.1-8b-instruct-q4_K_M.gguf"

    try:
        # Initialize the LLM
        print(f"Loading model from: {model_path}")
        llm = Llama(model_path=model_path, n_ctx=512)

        # Test prompt
        test_prompt = "Describe a mysterious forest in a D&D campaign."
        print(f"\nSending test prompt: '{test_prompt}'")

        # Generate response - corrected access to response structure
        response = llm(test_prompt, max_tokens=128, stop=["\n"])

        # Extract and print the generated text
        generated_text = response["choices"][0]["text"].strip()

        print("\n--- LLM TEST RESULTS ---")
        print(f"Input: {test_prompt}")
        print(f"Output: {generated_text}")
        print("------------------------")

    except FileNotFoundError:
        print(f"ERROR: Model file not found at path: {model_path}")
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")


if __name__ == "__main__":
    test_llm()