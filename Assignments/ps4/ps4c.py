# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
#        pass #delete this line and replace with your code here

        self.message_text = text
        self.valid_words = []
        text_list = text.split(' ')
        for word in text_list:
            if is_word(word_list, word):       # word_list is a global variable, can be accessed inside or outside of the function
                self.valid_words.append(word)

    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
#        pass #delete this line and replace with your code here

        return self.message_text


    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
#        pass #delete this line and replace with your code here

        return self.valid_words[:]

                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        
#        pass #delete this line and replace with your code here

        shift_dictionary = {}

        n = 5           # number of vowels
        m = 21          # number of consonants

        for i in range(n):
            shift_dictionary[VOWELS_LOWER[i]] = vowels_permutation[i]
            shift_dictionary[VOWELS_UPPER[i]] = vowels_permutation.upper()[i]
        for j in range(m):
            shift_dictionary[CONSONANTS_LOWER[j]] = CONSONANTS_LOWER[j]
            shift_dictionary[CONSONANTS_UPPER[j]] = CONSONANTS_UPPER[j]
        
        return shift_dictionary


    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        
#        pass #delete this line and replace with your code here

        text = self.get_message_text()
        text_shifted = ""
        for char in text:
            if char in transpose_dict.keys():
                text_shifted += transpose_dict[char]
            else:
                text_shifted += char
        
        return text_shifted




class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
#        pass #delete this line and replace with your code here

        SubMessage.__init__(self, text)


    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
#        pass #delete this line and replace with your code here
  
        vowels_permutation_list = get_permutations(VOWELS_LOWER)
        best_permutation = VOWELS_LOWER
        best_permutation_performance = 0
        
        for vowels_permutation in vowels_permutation_list:
            transpose_dict = self.build_transpose_dict(vowels_permutation)
            text_shifted = self.apply_transpose(transpose_dict)
            text_shifted_list = text_shifted.split(' ')
            valid_words_list = []
            for word in text_shifted_list:
                if is_word(word_list, word):
                    valid_words_list.append(word)
            if best_permutation_performance < len(valid_words_list):
                best_permutation = vowels_permutation
                best_permutation_performance = len(valid_words_list)
        
        transpose_dict = self.build_transpose_dict(best_permutation)
        best_decrypted_message = self.apply_transpose(transpose_dict)
        
        return best_decrypted_message



if __name__ == '__main__':

    word_list = load_words(WORDLIST_FILENAME)
    
    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

    print('########################################')
     
    #TODO: WRITE YOUR TEST CASES HERE

    # Test case 1a
    message = SubMessage("I am so handsome!")
    permutation = "iueao"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "E im sa hindsamu!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

    print('########################################')

    # Test case 1b
    message = SubMessage("He is so handsome!")
    permutation = "iueao"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hu es sa hindsamu!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

    print('########################################')

    # Test case 2
    message = SubMessage("Data scientist is my dream job~")
    permutation = "uoiea"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Dutu sciontist is my droum jeb~")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

'''

Remarks for Test case 1a:

- Note that the decrypted message is VERY strange
- Reason: both 'A em so hendsomu!' and 'I am so handsome!' have three valid words
- The word/pronoun 'i' is not in the text file words.txt


Remarks for Test case 2: 

- Note that the decrypted message is incorrect, i.e., 'jeb~' is decrypted as 'jub~', but not 'job~'
- Reason: the is_word() helper function does not include '~' as a punctuation to strip off
- As a result, both is_word(word_list, 'jub~') and is_word(word_list, 'job~') give False, and this decryption algorithm does not distinguish between them

I keep these "errors" intentionally to show differences in decryption results of Part 4b & 4c

'''