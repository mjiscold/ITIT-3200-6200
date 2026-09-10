import hashlib
import json
import os

HASH_FILE = "hash_table.json"

#uses SHA-256 to calculate cryptographic hash for 1 file
def hash_file(filepath):
    sha256 = hashlib.sha256()

    with open(filepath, "rb") as file:
        while True:
            data = file.read(4096)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()

#finds all files in the selected directory and calls hash_file() for each one
def traverse_directory(directory):
    hashes = {}

    for root, folders, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)

            
            if filename == HASH_FILE:
                continue

            hashes[filepath] = hash_file(filepath)

    return hashes

#stores original file paths and hashes inside hash_table.json
def generate_table():
    directory = input("Enter directory path: ").strip()

    if not os.path.isdir(directory):
        print("Directory does not exist.")
        return

    hashes = traverse_directory(directory)

    hash_table = {
        "directory": directory,
        "files": hashes
    }

    output_path = os.path.join(directory, HASH_FILE)

    with open(output_path, "w") as file:
        json.dump(hash_table, file, indent=4)

    print("Hash table generated.")
    print("Saved to:", output_path)

#hashes the files again and and compares the new values to the saved ones 
def validate_hash():
    directory = input("Enter directory path: ").strip()

    hash_table_path = os.path.join(directory, HASH_FILE)

    if not os.path.isfile(hash_table_path):
        print("Hash table not found.")
        return

    with open(hash_table_path, "r") as file:
        hash_table = json.load(file)

    old_hashes = hash_table["files"]
    current_hashes = traverse_directory(directory)

    print("\nHash Verification Results:")

    #check original
    for filepath, stored_hash in old_hashes.items():

        if filepath not in current_hashes:
            print(filepath, "- FILE DELETED")

        elif current_hashes[filepath] == stored_hash:
            print(filepath, "- HASH VALID")

        else:
            print(filepath, "- HASH INVALID")

    #check new 
    for filepath in current_hashes:

        if filepath not in old_hashes:
            print(filepath, "- NEW FILE ADDED")


def main():
    while True:
        print("\n--- File Hash Program ---")
        print("1. Generate new hash table")
        print("2. Verify hashes")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            generate_table()

        elif choice == "2":
            validate_hash()

        elif choice == "3":
            print("Exiting program.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()