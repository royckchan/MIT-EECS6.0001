# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

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

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
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

        return self.message_text        # string is immutable (unlike list below), so can be returned directly


    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
#        pass #delete this line and replace with your code here

        return self.valid_words[:]


    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
#        pass #delete this line and replace with your code here
        
        shift_dictionary = {}
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        
        n = 26          # size of English alphabet, to loop over the above strings
        
        for i in range(n):
            shift_dictionary[lower[i]] = lower[(i+shift)%n]
            shift_dictionary[upper[i]] = upper[(i+shift)%n]
            
        return shift_dictionary


    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
#        pass #delete this line and replace with your code here
        
        text = self.get_message_text()
        text_shifted = ""
        shift_dictionary = self.build_shift_dict(shift)
        for char in text:
            if char in shift_dictionary.keys():
                text_shifted += shift_dictionary[char]
            else:
                text_shifted += char
                
        return text_shifted



class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
#        pass #delete this line and replace with your code here

        Message.__init__(self, text)        # make use of the superclass constructor
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
#        pass #delete this line and replace with your code here

        return self.shift


    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
#        pass #delete this line and replace with your code here

        return self.encryption_dict.copy()


    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
#        pass #delete this line and replace with your code here

        return self.message_text_encrypted


    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
#        pass #delete this line and replace with your code here

        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)



class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
#        pass #delete this line and replace with your code here

        Message.__init__(self, text)



    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
#        pass #delete this line and replace with your code here

        n = 26  # size of English alphabet, to loop over this number of possibilities
        best_shift = 0
        best_shift_performance = 0
        for i in range(n):
            valid_words_list = []
            text_shifted = self.apply_shift(i)
            text_shifted_list = text_shifted.split(' ')
            for word in text_shifted_list:
                if is_word(word_list, word):               # word_list is a global variable, can be accessed inside or outside of the function
                    valid_words_list.append(word)
            if best_shift_performance < len(valid_words_list):
                best_shift = i
                best_shift_performance = len(valid_words_list)
        
        return (best_shift, self.apply_shift(best_shift))
                



if __name__ == '__main__':

    word_list = load_words(WORDLIST_FILENAME)
    
    #Example test case (PlaintextMessage)
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    #Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())

    #TODO: WRITE YOUR TEST CASES HERE

    #TODO: best shift value and unencrypted story 

#    pass #delete this line and replace with your code here

    print('########################################')

    # Test case 1
    plaintext = PlaintextMessage('I am so handsome!', 1)
    print('Expected Output: J bn tp iboetpnf!')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    ciphertext = CiphertextMessage('J bn tp iboetpnf!')
    print('Expected Output:', (25, 'I am so handsome!'))
    print('Actual Output:', ciphertext.decrypt_message())
    
    print('########################################')
    
    # Test case 2
    plaintext = PlaintextMessage('Data scientist is my dream job~', 24)
    print('Expected Output: Byry qagclrgqr gq kw bpcyk hmz~')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    ciphertext = CiphertextMessage('Byry qagclrgqr gq kw bpcyk hmz~')
    print('Expected Output:', (2, 'Data scientist is my dream job~'))
    print('Actual Output:', ciphertext.decrypt_message())


    print('########################################')

    ciphertext = CiphertextMessage(get_story_string())
    print('Unencrypted Story:', ciphertext.decrypt_message())
    
    # Best shift = 12
    # Unencrypted story is:
    # Jack Florey is a mythical character created on the spur of a moment to help
    # cover an insufficiently planned hack. He has been registered for classes at
    # MIT twice before, but has reportedly never passed aclass. It has been the
    # tradition of the residents of East Campus to become Jack Florey for a few
    # nights each year to educate incoming students in the ways, means, and ethics
    # of hacking.