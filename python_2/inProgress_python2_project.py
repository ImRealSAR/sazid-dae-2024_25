import random

# All the possible characters one can input for their password. 
CHARS = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()")

# Function to generate a password
def generate_password(length):
    password = ""
    for _ in range(length):
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

# Function to manage user input, generate a password, and save it to a file
def main():
    while True:
        try:
            user_input = int(input("Enter the desired password length (minimum 6): "))
            if user_input < 6:
                print("Password length must be 6 or more. Please try again.")
            else:
                password = generate_password(user_input)
                print(f"Generated Password: {password}")
                print(f"Password Strength: {check_password_strength(password)}")
                
                # Save the password to a file
                with open("generated_password.txt", "w") as file:
                    file.write(f"Generated Password: {password}\n")
                    file.write(f"Password Strength: {check_password_strength(password)}\n")
                
                print("Password has been saved to 'generated_password.txt'")
                break  # Exit the loop after successful generation
        except ValueError:
            print("Invalid input. Please enter an integer for the password length.")

# Main call
if __name__ == "__main__":
    main()
