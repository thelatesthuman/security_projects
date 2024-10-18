import sys

BIFID_grid = [['B', 'G', 'W', 'K', 'Z'],
              ['Q', 'P', 'N', 'D', 'S'],
              ['I', 'O', 'A', 'X', 'E'],
              ['F', 'C', 'L', 'U', 'M'],
              ['T', 'H', 'Y', 'V', 'R']]

def encrypt(plaintext):
    # Normalize plaintext
    plaintext_list = plaintext.split(" ")
    plaintext_list_normalized = []
    for word in plaintext_list:
        word.split()
        for char in word:
            plaintext_list_normalized.append(char)

    # Compare plaintext to BIFID grid
    plaintext_row = []
    plaintext_col = []
    for char in plaintext_list_normalized:
        for row_index,row in enumerate(BIFID_grid):
            for col_index,col in enumerate(row):
                if char.upper() == BIFID_grid[row_index][col_index]:
                    plaintext_row.append(row_index)
                    plaintext_col.append(col_index)
    
    # Transpose plaintext to ciphertext
    transpose_list = plaintext_row + plaintext_col
    cipher = ""
    for even_elem,odd_elem in zip(transpose_list[::2], transpose_list[1::2]):
        cipher += BIFID_grid[even_elem][odd_elem]

    return cipher


def decrypt(ciphertext):
    # Compare ciphertext to BIFID grid
    plaintext = ""
    ciphertext_row = []
    ciphertext_col = []
    for char in ciphertext:
        for row_index,row in enumerate(BIFID_grid):
            for col_index,col in enumerate(row):
                if char.upper() == BIFID_grid[row_index][col_index]:
                    ciphertext_row.append(row_index)
                    ciphertext_col.append(col_index)

    # transpose ciphertext to plaintext
    transpose_list = []
    for even_elem,odd_elem in zip(ciphertext_row,ciphertext_col):
        transpose_list.append(even_elem)
        transpose_list.append(odd_elem)

    for even_elem,odd_elem in zip(transpose_list[:len(transpose_list)//2], transpose_list[len(transpose_list)//2:]):
        plaintext += BIFID_grid[even_elem][odd_elem]
    
    return plaintext


def main():
    try:
        if sys.argv[1] == "-e":
            plaintext = sys.argv[2]
            print(encrypt(plaintext))
        elif sys.argv[1] == "-d":
            ciphertext = sys.argv[2]
            print(decrypt(ciphertext))
        else:
            print("Syntax is: python3 bifid_cipher.py -e|-d plaintext|ciphertext")
    except OSError as e:
        print(e)

if __name__ == "__main__":
    main()

