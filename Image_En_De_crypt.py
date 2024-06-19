from PIL import Image
import numpy as np
import os

def generate_key(seed, size):
    np.random.seed(seed)
    return np.random.permutation(size)

def encrypt(image_path, seed):
    img = Image.open(image_path)

    # Convert image to numpy array
    img_array = np.array(img)
    flat_array = img_array.flatten()
    
    # Generate a random key for shuffling based on the seed
    key = generate_key(seed, len(flat_array))

    # Shuffle the flat array using the key
    shuffled_array = flat_array[key]

    # XOR operation for encryption
    encrypted_array = np.bitwise_xor(shuffled_array, seed % 256)
    
    # Reshape to original image shape
    encrypted_array = encrypted_array.reshape(img_array.shape)
    
    # Convert back to an image
    encrypted_img = Image.fromarray(encrypted_array.astype('uint8'))

    return encrypted_img, key

def decrypt(encrypted_image_path, seed, key):
    img = Image.open(encrypted_image_path)
    img_array = np.array(img)
    
    flat_array = img_array.flatten()
    
    # XOR operation for decryption
    decrypted_array = np.bitwise_xor(flat_array, seed % 256)
    
    # Reverse the shuffling using the key
    inverse_key = np.argsort(key)
    original_array = decrypted_array[inverse_key]
    
    # Reshape to original image shape
    original_array = original_array.reshape(img_array.shape)
    
    # Convert back to an image
    decrypted_img = Image.fromarray(original_array.astype('uint8'))
    
    return decrypted_img

def main():
    while True:
        choice = input("Do you want to (E)ncrypt, (D)ecrypt, or (Q)uit? ").upper()
        if choice == 'Q':
            break
        if choice not in ['E', 'D']:
            print("Invalid choice. Please enter E, D, or Q.")
            continue

        image_path = input("Enter the path to the image file: ").strip()
        
        # Check if the file exists
        if not os.path.isfile(image_path):
            print(f"The file {image_path} does not exist. Please provide a valid file path.")
            continue
        
        seed = int(input("Enter the seed value (an integer): "))

        if choice == 'E':
            encrypted_img, key = encrypt(image_path, seed)
            encrypted_img_path = "encrypted_image.png"
            encrypted_img.save(encrypted_img_path)
            print(f"Encrypted image saved as {encrypted_img_path}")
            np.save("key.npy", key)
            print("Encryption key saved as key.npy")
        elif choice == 'D':
            try:
                key = np.load("key.npy")
            except FileNotFoundError:
                print("Key file not found. Ensure that you have the key.npy file in the directory.")
                continue

            decrypted_img = decrypt(image_path, seed, key)
            decrypted_img_path = "decrypted_image.png"
            decrypted_img.save(decrypted_img_path)
            print(f"Decrypted image saved as {decrypted_img_path}")

if __name__ == "__main__":
    main()
