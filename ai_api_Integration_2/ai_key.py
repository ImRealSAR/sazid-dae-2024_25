# import sys 
# import google.generativeai as genai  # Keep this line for now

# print(sys.executable)  # Print the full path to the Python executable
# print(sys.version)    # Print the Python version
# print(sys.path)       # Print the module search path
# import os

# # Configure the API
# api_key = "AIzaSyDDmL8Nw6Bc3nKQJMhWqjwSZI1O3qZjYTE"
# genai.configure(api_key=api_key)

# # Initialize the Gemini model
# model = genai.GenerativeModel("gemini-1.5-flash")

# # Function to generate content without Flask
# def generate_content(user_input):
#     try:
#         if not user_input:
#             return {"error": "Input text is required"}

#         # Generate content using Gemini
#         response = model.generate_content(user_input)
#         return {"generated_text": response.text}

#     except Exception as e:
#         return {"error": str(e)}

# # Example usage
# if __name__ == "__main__":
#     # Test input
#     test_input = "Hello! How are you? Who are you?."
#     result = generate_content(test_input)
#     print(result)
import sys
import google.generativeai as genai  # Keep this line for now
import os
import tkinter as tk
from tkinter import scrolledtext

# Print system information
print(sys.executable)  # Print the full path to the Python executable
print(sys.version)    # Print the Python version
print(sys.path)       # Print the module search path

# Configure the API
api_key = "AIzaSyDDmL8Nw6Bc3nKQJMhWqjwSZI1O3qZjYTE"
genai.configure(api_key=api_key)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to generate content
def generate_content():
    user_input = input_text.get("1.0", tk.END).strip()
    if not user_input:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Error: Input text is required")
        return
    
    try:
        response = model.generate_content(user_input)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, response.text)
    except Exception as e:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Error: {str(e)}")

# GUI Setup
root = tk.Tk()
root.title("Gemini API GUI")

# Input Text Area
input_label = tk.Label(root, text="Enter your prompt:")
input_label.pack()
input_text = scrolledtext.ScrolledText(root, height=5, width=50)
input_text.pack()

# Generate Button
generate_button = tk.Button(root, text="Generate", command=generate_content)
generate_button.pack()

# Output Text Area
output_label = tk.Label(root, text="Generated Response:")
output_label.pack()
output_text = scrolledtext.ScrolledText(root, height=10, width=50)
output_text.pack()

# Run GUI
root.mainloop()
