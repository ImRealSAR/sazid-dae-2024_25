import sys
import google.generativeai as genai  # Keep this line for now

print(sys.executable)  # Print the full path to the Python executable
print(sys.version)    # Print the Python version
print(sys.path)       # Print the module search path
import os

# Configure the API
api_key = "AIzaSyDDmL8Nw6Bc3nKQJMhWqjwSZI1O3qZjYTE"
genai.configure(api_key=api_key)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to generate content without Flask
def generate_content(user_input):
    try:
        if not user_input:
            return {"error": "Input text is required"}

        # Generate content using Gemini
        response = model.generate_content(user_input)
        return {"generated_text": response.text}

    except Exception as e:
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    # Test input
    test_input = "Hello, AI! Generate some content."
    result = generate_content(test_input)
    print(result)
