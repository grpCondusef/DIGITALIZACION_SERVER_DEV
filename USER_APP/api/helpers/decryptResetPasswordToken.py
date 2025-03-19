def decrypt_token(encrypted_message, shift):
    decrypted_message = ''

    for char in encrypted_message:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            decrypted_message += chr((ord(char) - start - shift) % 26 + start)
        else:
            decrypted_message += char

    return decrypted_message
