
import datetime
import os
from cryptography.fernet import Fernet
from datetime import datetime, timedelta

class DigitalTimeCapsule:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        self.capsules_dir = "time_capsules"
        
        if not os.path.exists(self.capsules_dir):
            os.makedirs(self.capsules_dir)

    def create_capsule(self, content, unlock_date, title):
        """Create an encrypted time capsule that can only be opened after the specified date"""
        if datetime.strptime(unlock_date, "%Y-%m-%d") <= datetime.now():
            raise ValueError("Unlock date must be in the future!")

        capsule_data = {
            "content": content,
            "unlock_date": unlock_date,
            "creation_date": datetime.now().strftime("%Y-%m-%d"),
            "title": title
        }

        # Encrypt the content
        encrypted_data = self.cipher_suite.encrypt(str(capsule_data).encode())
        
        # Save the encrypted capsule
        filename = f"{self.capsules_dir}/{title}_{unlock_date}.capsule"
        with open(filename, "wb") as f:
            f.write(encrypted_data)
        
        return filename

    def open_capsule(self, filename):
        """Try to open a time capsule"""
        if not os.path.exists(filename):
            return "Capsule not found!"

        with open(filename, "rb") as f:
            encrypted_data = f.read()

        # Decrypt the content
        decrypted_data = eval(self.cipher_suite.decrypt(encrypted_data).decode())
        
        # Check if it's time to open
        if datetime.strptime(decrypted_data["unlock_date"], "%Y-%m-%d") > datetime.now():
            days_remaining = (datetime.strptime(decrypted_data["unlock_date"], "%Y-%m-%d") - datetime.now()).days
            return f"This capsule cannot be opened for {days_remaining} more days!"

        return decrypted_data["content"]

def main():
    capsule = DigitalTimeCapsule()
    
    while True:
        print("\n=== Digital Time Capsule ===")
        print("1. Create new time capsule")
        print("2. Open existing capsule")
        print("3. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            title = input("Enter capsule title: ")
            content = input("Enter your message: ")
            unlock_date = input("Enter unlock date (YYYY-MM-DD): ")
            
            try:
                filename = capsule.create_capsule(content, unlock_date, title)
                print(f"Capsule created successfully! Saved as: {filename}")
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "2":
            filename = input("Enter capsule filename: ")
            result = capsule.open_capsule(filename)
            print(f"Result: {result}")
            
        elif choice == "3":
            break

if __name__ == "__main__":
    main()