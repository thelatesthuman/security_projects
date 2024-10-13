import sys

alph_dict = {
        "A": 1,
        "B": 2,
        "C": 3,
        "D": 4,
        "E": 5,
        "F": 6,
        "G": 7,
        "H": 8,
        "I": 9,
        "J": 10,
        "K": 11,
        "L": 12,
        "M": 13,
        "N": 14,
        "O": 15,
        "P": 16,
        "Q": 17,
        "R": 18,
        "S": 19,
        "T": 20,
        "U": 21,
        "V": 22,
        "W": 23,
        "X": 24,
        "Y": 25,
        "Z": 26
        }


def pad_key(key, message):
    # Repeat the key until it's long enough
    padded_key = (key * (len(message) // len(key) + 1))[:len(message)]
    return padded_key



def vignere_encrypt(pad_key, plaintext):
    cipher_message = ""
    for num in range(len(pad_key)):
        plaintext_char = []
        sub_key_for_num = []
        char_transpose = []
        cipher_list = []

        # Set up list for key to add to cipher
        for char in pad_key:
            sub_key_for_num.append(alph_dict[char.upper()])


        # Transpose plaintext with key
        for plaintext_index,char in enumerate(plaintext):
            plaintext_char.append(alph_dict[char.upper()])
            char_transpose.append(alph_dict[char.upper()] + sub_key_for_num[plaintext_index])
        for trans_enum, trans_num in enumerate(char_transpose):
            if trans_num > 26:
                char_transpose[trans_enum] -= 26
        

        # Compare tranposition to alph_dict to find cipher chars        
        for trans_elem in char_transpose:
            for value_index,alph_value in enumerate(alph_dict.values()):
                if alph_value == trans_elem:
                    cipher_list.append(list(alph_dict.keys())[value_index])

    

    # Convert cipher list to string
    for char in cipher_list:
        cipher_message += char


    return cipher_message


def vignere_decrypt(pad_key, cipher_text):
    plaintext_message = ""
    for num in range(len(pad_key)):
        cipher_char = []
        sub_key_for_num = []
        char_transpose = []
        plaintext_message_list = []

        # Set up list for key to subtract from cipher
        for char in pad_key:
            sub_key_for_num.append(alph_dict[char.upper()])
        
        # Transpose cipher with key
        for cipher_num,char in enumerate(cipher_text):
            cipher_char.append(alph_dict[char.upper()])
            char_transpose.append(alph_dict[char.upper()] - sub_key_for_num[cipher_num])
        for trans_enum, trans_num in enumerate(char_transpose):
            if trans_num < 0:
                char_transpose[trans_enum] += 26

        # Compare tranposition to alph_dict to find plaintext chars        
        for trans_elem in char_transpose:
            for value_index,alph_value in enumerate(alph_dict.values()):
                if alph_value == trans_elem:
                    plaintext_message_list.append(list(alph_dict.keys())[value_index])

    # Convert plaintext list to string
    for char in plaintext_message_list:
        plaintext_message += char
    
    return plaintext_message


def main():
    try:
        if sys.argv[1] == "-e":
            # Still need to add file support
            if sys.argv[3] == "-f":
                key_arg = sys.argv[2]
                message_file = ""
                message = ""
                with open(sys.argv[4], 'r') as f:
                    message_file = f.read().strip().split(" ")
                    for word in message_file:
                        message += word
                with open(sys.argv[4] + ".vig", 'w') as e:        
                    message_encrypt = vignere_encrypt(pad_key(key_arg, message), message)
                    e.write(message_encrypt)
            else:
                key_arg = sys.argv[2]
                message_arg = sys.argv[3]
                print(vignere_encrypt(pad_key(key_arg, message_arg), message_arg))
        elif sys.argv[1] == "-d":
            # Still need to add file support
            if sys.argv[3] == "-f":
                key_arg = sys.argv[2]
                cipher = ""
                with open(sys.argv[4], 'r') as f:
                    cipher = f.read().strip()
                decrypted_message = vignere_decrypt(pad_key(key_arg, cipher), cipher)
                print(decrypted_message)
            else:
                key_arg = sys.argv[2]
                message_arg = sys.argv[3]
                print(vignere_decrypt(pad_key(key_arg, message_arg), message_arg))
        else:
            print("Use vignere_cipher.py -e||-d key [-f] message")
    except OSError as e:
        print(e)


if __name__ == "__main__":
    main()
