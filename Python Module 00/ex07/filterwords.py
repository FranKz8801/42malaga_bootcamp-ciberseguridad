import sys
import string

def filter_words(s, n):
    """
    Filters words in a string based on the number of non-punctuation characters.

    Args:
        s (str): The input string
        n (int): The threshold for number of non-punctuation characters

    Returns:
        list: The list of filtered words
    """
    # Remove punctuation from the input string
    s = s.translate(str.maketrans('', '', string.punctuation))
    # Split the string into words
    words = s.split()
    # Use list comprehension to filter words based on the number of non-punctuation characters
    filtered_words = [word for word in words if len([char for char in word if char not in string.punctuation]) > n]
    return filtered_words

# Check if the correct number of arguments are provided
if len(sys.argv) != 3:
    print("ERROR")
else:
    try:
        # Extract input arguments
        s = sys.argv[1]
        n = int(sys.argv[2])
        # Call the filter_words function and print the result
        filtered_words = filter_words(s, n)
        print(filtered_words)
    except ValueError:
        print("ERROR")
