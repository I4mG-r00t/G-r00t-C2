from os import urandom
import base64

# Define key length for AES-256 (32 bytes) and IV length (16 bytes for AES)
KEY_LENGTH = 32  # AES-256
IV_LENGTH = 16   # IV is always 16 bytes for AES

# Generate a random key and IV
key = urandom(KEY_LENGTH)
iv = urandom(IV_LENGTH)

# Save the key and IV in Base64 format
AESB64 = base64.b64encode(key).decode()
AESIV64 = base64.b64encode(iv).decode()

# Save the key and IV Decoded 
AES_KEY = base64.b64decode(AESB64)
AES_IV = base64.b64decode(AESIV64)


#Print the keys
print('Base64 encoded:')
print("AES-256 Key (Base64):", AESB64)
print("AES IV (Base64):", AESIV64)
print('Decoded:')
print("AES-256 Key (Decoded):", AES_KEY)
print("AES IV (Decoded):", AES_IV)
