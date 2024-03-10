#!/usr/bin/env python3                                                                                                                                                                                                                                                                                                                                                                                                                                                         rune_swiss.py                                                                                                                                                                                                                                                                                                                                                                                                                                                                    #!/usr/bin/env python3
import nltk

# Function to check and download necessary NLTK data
def setup_nltk():
    try:
        # Check if 'words' corpus is available
        nltk.data.find('corpora/words')
    except LookupError:
        # If not available, download 'words' corpus
        print("Downloading the 'words' corpus from NLTK, please wait...")
        nltk.download('words')
        print("'words' corpus downloaded.")

# Call the setup function at the beginning of the script
setup_nltk()

import itertools
import string
from sympy import isprime, primerange
from nltk.corpus import words
from nltk.metrics.distance import edit_distance

# Ensure you have NLTK data downloaded:
# import nltk
# nltk.download('words')

# Mapping of runes to decimal values based on the provided table
rune_to_decimal = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11,
    'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22,
    'ᛞ': 23, 'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}
decimal_to_rune = {v: k for k, v in rune_to_decimal.items()}

# Dictionary mapping Elder Futhark runes to English letters
futhark_to_english = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G',
    'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P',
    'ᛉ': 'X', 'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L',
    'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA',
    'ᛠ': 'EA'
}

# Reverse mapping for English transliteration to runes
english_to_futhark = {v: k for k, v in futhark_to_english.items()}

# Function to transliterate text to runes
def transliterate_to_futhark(text):
    # Convert the text from English to Elder Futhark runes
    transliterated_text = ''
    for char in text.upper():
        if char in english_to_futhark:
            transliterated_text += english_to_futhark[char]
        else:
            transliterated_text += char
    return transliterated_text

# Function to transliterate runes to English and replace hyphens with spaces
def transliterate_futhark(runes):
# Convert the runes from Elder Futhark to English
    transliterated_text = ''
    for rune in runes:
        if rune in futhark_to_english:
            transliterated_text += futhark_to_english[rune]
        else:
            transliterated_text += rune  # Non-mapped characters are kept as is
    return transliterated_text

#Function to transliterate and convert
def transliterate_and_convert(runes):
    # Use the existing function to transliterate runes to English
    english_text = transliterate_futhark(runes)
    # Convert runes to decimal values
    decimal_values = [str(rune_to_decimal.get(rune, '?')) for rune in runes]
    # Return both the English transliteration and decimal values
    return english_text, decimal_values

# Example usage:
runes = "ᚦᛖ-ᛚᚩᛋᛋ-ᚩᚠ-ᛞᛁᚢᛁᚾᛁᛏᚣ.ᚦᛖ-ᚳᛁᚱᚳᚢ"
english_text, decimal_values = transliterate_and_convert(runes)
print(f"Transliterated English text: {english_text}")
print(f"Decimal values: {' '.join(decimal_values)}")

# Function to decrypt Atbash cipher
def decrypt_atbash(ciphertext, shift=0):
    # Decrypt the ciphertext using the Atbash cipher method
    decrypted_text = ""
    for rune in ciphertext:
        if rune in rune_to_decimal:
            # Apply the Atbash cipher transformation
            decrypted_value = 28 - rune_to_decimal[rune]
            # Apply the shift
            decrypted_value = (decrypted_value + shift) % 29
            # Map the decrypted value back to a rune
            decrypted_text += decimal_to_rune.get(decrypted_value, '?')
        else:
            # Preserve non-rune characters (such as '-', '/')
            decrypted_text += rune
    return decrypted_text

# Function to decrypt Vigenère cipher
def decrypt_vigenere(ciphertext, key, skip_indices):
    # Convert key to decimal values
    key_decimal = [rune_to_decimal[rune] for rune in key if rune in rune_to_decimal]
    decrypted_text = ""
    key_index = 0

    for index, rune in enumerate(ciphertext):
        if index in skip_indices or rune not in rune_to_decimal:
            decrypted_text += rune
        else:
            # Apply the Vigenère cipher transformation
            decrypted_value = (rune_to_decimal[rune] - key_decimal[key_index]) % 29
            decrypted_text += decimal_to_rune.get(decrypted_value, '?')
            key_index = (key_index + 1) % len(key_decimal)

    return decrypted_text

# Caesar Cipher Encryption and Decryption
def encrypt_caesar(plaintext, shift):
    # Encrypt the plaintext using the Caesar cipher method
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shifted_alphabet)
    return plaintext.translate(table)

def decrypt_caesar(ciphertext, shift):
    # Decrypt the ciphertext using the Caesar cipher method
    return encrypt_caesar(ciphertext, -shift)

# Playfair Cipher Key Generation, Encryption, and Decryption
def generate_playfair_key(keyword):
    # Generate the 5x5 key matrix for Playfair cipher
    matrix = []
    alphabet = 'abcdefghiklmnopqrstuvwxyz'  # 'j' is usually excluded in Playfair
    used_chars = set()

    # Add keyword to the matrix
    for char in keyword.lower():
        if char not in used_chars and char in alphabet:
            matrix.append(char)
            used_chars.add(char)

    # Fill the rest of the matrix with the remaining alphabet
    for char in alphabet:
        if char not in used_chars:
            matrix.append(char)

    return matrix

def split_into_digraphs(plaintext):
    # Split the plaintext into digraphs for Playfair cipher
    plaintext = plaintext.lower().replace('j', 'i')  # 'j' is usually replaced with 'i'
    digraphs = []

    i = 0
    while i < len(plaintext):
        digraph = plaintext[i]
        i += 1
        if i < len(plaintext) and plaintext[i] != digraph:
            digraph += plaintext[i]
            i += 1
        else:
            digraph += 'x'  # Padding character if needed
        digraphs.append(digraph)

    return digraphs

def find_position(char, matrix):
    # Find the position of a character in the key matrix
    index = matrix.index(char)
    return index // 5, index % 5  # Row, Column

def encrypt_playfair(plaintext, keyword):
    # Encrypt the plaintext using the Playfair cipher method
    matrix = generate_playfair_key(keyword)
    digraphs = split_into_digraphs(plaintext)
    ciphertext = ''

    for digraph in digraphs:
        row1, col1 = find_position(digraph[0], matrix)
        row2, col2 = find_position(digraph[1], matrix)

        if row1 == row2:  # Same row
            ciphertext += matrix[row1 * 5 + (col1 + 1) % 5]
            ciphertext += matrix[row2 * 5 + (col2 + 1) % 5]
        elif col1 == col2:  # Same column
            ciphertext += matrix[((row1 + 1) % 5) * 5 + col1]
            ciphertext += matrix[((row2 + 1) % 5) * 5 + col2]
        else:  # Rectangle
            ciphertext += matrix[row1 * 5 + col2]
            ciphertext += matrix[row2 * 5 + col1]

    return ciphertext

def decrypt_playfair(ciphertext, keyword):
    # Decrypt the ciphertext using the Playfair cipher method
    keyword = keyword.replace(' ', '')
    # Generate the 5x5 key matrix for Playfair cipher
    matrix = generate_playfair_key(keyword)
    digraphs = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]
    plaintext = ''

    for digraph in digraphs:
        row1, col1 = find_position(digraph[0], matrix)
        row2, col2 = find_position(digraph[1], matrix)

        if row1 == row2:  # Same row
            plaintext += matrix[row1 * 5 + (col1 - 1) % 5]
            plaintext += matrix[row2 * 5 + (col2 - 1) % 5]
        elif col1 == col2:  # Same column
            plaintext += matrix[((row1 - 1) % 5) * 5 + col1]
            plaintext += matrix[((row2 - 1) % 5) * 5 + col2]
        else:  # Rectangle
            plaintext += matrix[row1 * 5 + col2]
            plaintext += matrix[row2 * 5 + col1]

    return plaintext

# Function to generate prime numbers within a range
def generate_primes(start, end):
    return list(primerange(start, end))

# Function to calculate Euler's totient function
def euler_totient(n):
    if n == 1:
        return 1
    else:
        phi = 1
        for i in range(2, n):
            if gcd(n, i) == 1:
                phi += 1
        return phi

# Function to calculate the Greatest Common Divisor (Euclid's algorithm)
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Function to check for English coherence with a threshold for unrecognized words
def is_coherent(text, threshold=0.25):
    english_vocab = set(words.words())
    text_words = text.replace('-', ' ').replace('.', ' ').split()  # Split compound words and sentences
    recognized_words = [word.lower() for word in text_words if word.lower() in english_vocab]
    coherence_ratio = len(recognized_words) / len(text_words)
    # Alert the user if the text is coherent based on the threshold
    if coherence_ratio >= threshold:
        print("The transliterated text is mostly coherent in English.")
        return True
    return False

# Function to calculate the edit distance to English words
def englishness_score(text):
    english_vocab = set(words.words())
    text_words = text.split()
    distances = [edit_distance(word.lower(), best_match(word.lower(), english_vocab)) for word in text_words]
    return sum(distances)

def best_match(word, vocab):
    return min(vocab, key=lambda w: edit_distance(word, w))

# Brute-force function to try all ciphers with prime shifts
def brute_force_decrypt(runes, key=None, keyword=None):
    # Transliterate runes to English and print the transliteration
    transliterated_text = transliterate_futhark(runes)
    print(f"Transliterated text: {transliterated_text}")

    primes = generate_primes(0, 100)  # Generate prime numbers for shifts
    possible_results = []

    # Split the runes into lines for multi-line handling
    lines = runes.split('\n')

    # Process each line with brute force decryption
    for line in lines:
        for prime in primes:
            # Try Atbash with prime shift for each line and print the attempt
            atbash_result = decrypt_atbash(line, prime)
            print(f"Atbash attempt with shift {prime}: {atbash_result}")
            if is_coherent(atbash_result):
                possible_results.append((atbash_result, 'Atbash', prime))

            # Try Caesar with prime shift for each line and print the attempt
            caesar_result = decrypt_caesar(line, prime)
            print(f"Caesar attempt with shift {prime}: {caesar_result}")
            if is_coherent(caesar_result):
                possible_results.append((caesar_result, 'Caesar', prime))

        # If a key is provided, try Vigenère decryption with the user-provided key and print the attempt
        if key:
            vigenere_result = decrypt_vigenere(line, key, [])
            print(f"Vigenère attempt with key {key}: {vigenere_result}")
            if is_coherent(vigenere_result):
                possible_results.append((vigenere_result, 'Vigenère', key))

        # If a keyword is provided, try Playfair decryption with the user-provided keyword and print the attempt
        if keyword:
            playfair_result = decrypt_playfair(line, keyword)
            print(f"Playfair attempt with keyword {keyword}: {playfair_result}")
            if is_coherent(playfair_result):
                possible_results.append((playfair_result, 'Playfair', keyword))

    # If no coherent result is found for any line, return the line with the best Englishness score
    best_result = min(possible_results, key=lambda x: englishness_score(x[0]), default=("No coherent result found", "None", None))
    return best_result

# Main function with additional brute-force option
def main():
    print("Welcome to the Rune Cipher Swiss Army Knife!")
    print("Choose an operation from the following options:")
    print("1 - Transliterate English to Runes (Transliteration)")
    print("2 - Transliterate Runes to English")
    print("3 - Decrypt Runes with Atbash Cipher (Decryption)")
    print("4 - Decrypt Runes with Vigenère Cipher (Decryption)")
    print("5 - Encrypt Text with Caesar Cipher (Encryption)")
    print("6 - Decrypt Text with Caesar Cipher (Decryption)")
    print("7 - Encrypt Text with Playfair Cipher (Encryption)")
    print("8 - Decrypt Text with Playfair Cipher (Decryption)")
    print("9 - Brute-force Decryption with Prime Shifts (Decryption)")
    print("10 - Brute-force Decryption with User-Provided Key (Vigenère Cipher)")
    choice = input("Enter your choice (1-9): ")

    if choice == '1':
        text = input("Enter the text to transliterate to runes: ")
        result = transliterate_to_futhark(text)
        print(f"Transliterated text: {result}")
    elif choice == '2':
        runes = input("Enter the runes to transliterate to English: ")
        result = transliterate_futhark(runes)
        print(f"Transliterated English text: {result}")
    elif choice == '3':
        runes = input("Enter the runes to decrypt with Atbash: ")
        shift = int(input("Enter the shift amount (0-28): "))
        result = decrypt_atbash(runes, shift)
        print(f"Decrypted text: {result}")
    elif choice == '4':
        runes = input("Enter the runes to decrypt with Vigenère: ")
        key = input("Enter the Vigenère key (in runes): ")
        skip_indices_input = input("Enter indices to skip (comma-separated, no spaces): ")
        skip_indices = [int(index) for index in skip_indices_input.split(',')]
        result = decrypt_vigenere(runes, key, skip_indices)
        print(f"Decrypted text: {result}")
    elif choice == '5':
        text = input("Enter the text to encrypt with Caesar: ")
        shift = int(input("Enter the shift amount (0-25): "))
        result = encrypt_caesar(text, shift)
        print(f"Encrypted text: {result}")
    elif choice == '6':
        runes = input("Enter the runes to decrypt with Caesar: ")
        shift = int(input("Enter the shift amount (0-25): "))
        result = decrypt_caesar(runes, shift)
        print(f"Decrypted text: {result}")
    elif choice == '7':
        text = input("Enter the text to encrypt with Playfair: ")
        keyword = input("Enter the keyword for the Playfair cipher: ")
        result = encrypt_playfair(text, keyword)
        print(f"Encrypted text: {result}")
    elif choice == '8':
        runes = input("Enter the runes to decrypt with Playfair: ")
        keyword = input("Enter the keyword for the Playfair cipher: ")
        result = decrypt_playfair(runes, keyword)
        print(f"Decrypted text: {result}")
    elif choice == '9':
        runes = input("Enter the runes to decrypt: ")
        key = input("Enter the Vigenère key (in runes), or press Enter to skip: ")
        keyword = input("Enter the Playfair keyword (in English), or press Enter to skip: ")
        # Convert English keyword to runes if necessary
        if keyword and not all(char in rune_to_decimal for char in keyword):
            keyword = transliterate_to_futhark(keyword)
        result, cipher, detail = brute_force_decrypt(runes, key, keyword)
        print(f"Decrypted message: {result}")
        print(f"Method used: {cipher}")
        print(f"Detail (shift, key, or keyword): {detail}")
    elif choice == '10':
        runes = input("Enter the runes to decrypt: ")
        key = input("Enter your key (in English or runes): ")
        # Convert English key to runes if necessary
        if not all(char in rune_to_decimal for char in key):
            key = transliterate_to_futhark(key)
        result = decrypt_vigenere(runes, key, [])
        print(f"Decrypted text: {result}")
# This line calls the main function when the script is executed
if __name__ == "__main__":
    main()
