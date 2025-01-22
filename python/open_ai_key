import openai
import json
import os

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);

# Set your OpenAI API Key (replace 'your-api-key' with your actual key)
openai.api_key = "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"

# Example 1: GET Request - Fetch models from OpenAI API
def fetch_models():
    try:
        response = openai.Model.list()
        models = response.get("data", [])
        formatted_models = [model["id"] for model in models]
        print("Available Models:")
        for model in formatted_models:
            print(f"- {model}")
    except Exception as e:
        print(f"Error fetching models: {e}")

# Example 2: POST Request - Generate text using ChatGPT
def generate_text(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        generated_text = response["choices"][0]["message"]["content"]
        print("\nGenerated Text:")
        print(generated_text)
    except Exception as e:
        print(f"Error generating text: {e}")

# Main Function to Demonstrate API Calls
def main():
    print("Fetching Models...")
    fetch_models()

    print("\nGenerating Text...")
    user_prompt = "Write a short story about a robot learning to code."
    generate_text(user_prompt)

# Run the main function
if __name__ == "__main__":
    main()

