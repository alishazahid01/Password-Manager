# Password Manager
from cryptography.fernet import Fernet

def pwd_store(platform_name, password, cipher):
    # Concatenate platform name and password
    data = f"{platform_name}: {password}"

    # Encrypt the data
    encrypted_data = cipher.encrypt(data.encode())

    # Store encrypted data in a file with a newline character
    with open("Encrypted_passwords.txt", "ab") as encrypted_file:
        encrypted_file.write(encrypted_data + b"\n")  # Append newline character

# Decryptiong and retrieving data
def pwd_retrieve(cipher):
    retrieve_platform = input("Enter the name of the platform (retrieve): ").lower()  # Convert to lowercase
    retrieved_passwords = []

    # Open file and read encrypted data
    with open("Encrypted_passwords.txt", "rb") as encrypted_file:
        encrypted_data = encrypted_file.readlines()

    try:
        # Decrypt and decode the data
        decrypted_data = [cipher.decrypt(line).decode().rstrip('\n') for line in encrypted_data]

        # Iterate over stored passwords
        for password_data in decrypted_data:
            stored_platform_name, stored_password = password_data.split(": ")

            if retrieve_platform == stored_platform_name.lower():  # Compare lowercase versions
                retrieved_passwords.append(f"Platform: {stored_platform_name}, Password: {stored_password}")

        if retrieved_passwords:
            print("Password(s) Found")

        else:
            print("Platform and password not found")
    except Exception as e:
        print("Failed to retrieve password:", str(e))

    # Save retrieved passwords to a file
    with open("Retrieved_passwords.txt", "w") as retrieved_file:
        for password in retrieved_passwords:
            retrieved_file.write(password + "\n")


def main():
    # Generate a key
    key = Fernet.generate_key()

    # Create a Fernet cipher object
    cipher = Fernet(key)

    num_passwords = int(input("Enter the number of passwords you want to store: "))

    for _ in range(num_passwords):
        platform_name = input("Enter the name of the platform: ")
        password = input("Enter password: ")
        pwd_store(platform_name, password, cipher)

    print("Passwords stored successfully.")

    print("Retrieving password.....")
    pwd_retrieve(cipher)

# Calling main function
main()
