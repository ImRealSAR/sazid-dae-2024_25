import random

# All the possible characters one can input for their password. 
CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"

# Function to generate a password
def generate_password(length):
    password = ""
    for passkey in range(length):
        password += random.choice(CHARS)
    return password

# Function to check password strength based on length
def check_password_strength(password):
    if len(password) >= 12:
        return "Strong"
    elif len(password) >= 8:
        return "Moderate"
    else:
        return "Weak"

# Function to manage user input and generate a password
def main():
    user_input = int(input("Enter the desired password length (minimum 6): "))
    if user_input < 6:
        print("Password length must be 6 or more.")
    else:
        password = generate_password(user_input)
        print(f"Generated Password: {password}")
        print(f"Password Strength: {check_password_strength(password)}")

# Main function call
if __name__ == "__main__":
    main()
