import sys

# Define Morse code dictionary
MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', ' ': '/'
}


def encode_morse_code(args):
    # Merge input arguments into a single string
    input_string = ' '.join(args)

    # Encode input string into Morse code
    morse_code = ''
    for char in input_string:
        if char.upper() in MORSE_CODE:
            morse_code += MORSE_CODE[char.upper()] + ' '
        else:
            return 'ERROR'

    return morse_code.strip()


# Check if arguments are provided
if len(sys.argv) > 1:
    morse_code_result = encode_morse_code(sys.argv[1:])
    print(morse_code_result)
else:
    print('USAGE: python3 sos.py <STRING>')
