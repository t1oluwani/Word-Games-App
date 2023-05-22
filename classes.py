from random import choice
from collections.abc import MutableSet

# Exception Classes
class TooShortError(ValueError):
    pass

class TooLongError(ValueError):
    pass

class NotAlphaError(ValueError):
    pass

class InnapropriateWordError(ValueError):
    pass

class Words(MutableSet):
    '''
    Class that represents...
    '''

    def __init__(self, letters):
        '''Initialize empty set of words, letters refer to chosen length of words, if letters is 0 then length unspecified'''
        self.words = set() # initialized as a set to prevent word duplication
        self.letters = letters

    def __contains__(self, word):
        ''' Returns True if the word is in the list, False otherwise.'''
        return word.upper() in self.words

    def __iter__(self):
        ''' Returns an iterator over all the words in words.'''
        return iter(self.words)

    def __len__(self):
        ''' Returns the number of words in the dictionary.'''
        return len(self.words)

    def add(self, word):
        '''
        Adds word to words set. Raises appropriate error if triggered.
        '''        
        self.check_word(word)
        self.words.add(word.upper())

    def discard(self, word):
        ''' Removes word from words set.'''
        self.words.discard(word.upper())
        
    def check_appropriate(self, word):
        '''HELPER FUNCTION: Raises error is word is inappropriate (curse word, slur or vulgar)'''
        if self.letters == 0:
            with open('inappropriate_words.txt', 'r') as file:
                for line in file:
                    # Extract the first word from the line
                    bad_word = line.strip().split()[0]
                    
                    if word == bad_word:
                        raise InnapropriateWordError ("Word is a slur or vulgar")
                        
        else:
            with open('inappropriate_words.txt', 'r') as file:
                for line in file:
                    # Extract the first word from the line
                    bad_word = line.strip().split()[0]
                    
                    # Checks bad words the same size as self.letters
                    if len(bad_word) == self.letters:
                        if word == bad_word:
                            raise InnapropriateWordError ("Word is a slur or vulgar")
                    

    def check_letter(self, letter):
        '''HELPER FUNCTION: Raises error if letter isn't alphabetic'''
        if not letter.isalpha():
            raise NotAlphaError ("Word contains letter not in the standard alphabet")

    def check_word(self, word):
        '''
        Raises error if word isn't valid, word is valid if:
        - if word is the incorrect length (> or < self.letters)
        - if word is an inappropriate word or slur
        - only contains alphabetic letters
        '''
        if len(word) < self.letters:
            raise TooShortError("Word is too short")
        elif len(word) > self.letters:
            raise TooLongError("Word is too long")
        else:
            self.check_appropriate(word)
            for letter in word:
                self.check_letter(letter)

    def load_filtered(self, data):
        '''
        HELPER FUNCTION: adds words to self.words as long as they meet the 
        specified letter requirements (0 means no specified requirements)
        '''
        for line in data:
            if self.letters == 0:
                self.words.add(line.strip().upper())
            elif len(line.strip()) == self.letters:
                self.words.add(line.strip().upper())
        
    def load_file(self, filename):
        '''Add words from .txt file to set and filter using self.letters'''
        if filename.endswith(".txt"):
            with open(filename) as word_file:
                word_data = word_file.readlines()
                self.load_filtered(word_data)
        else:
            with open(filename+".txt") as word_file:
                word_data = word_file.readlines()
                self.load_filtered(word_data)

    def words(self):
        ''' Returns set of words'''
        return self.words

    def letters(self):
        ''' Returns the number of letters every word should have'''
        return self.letters

    def copy(self):
        ''' Returns second Words instance which contains same words'''
        new_instance = Words(self.letters)
        for word in self.words:
            new_instance.add(word)
        return new_instance


class Attempt():
    def __init__(self, guess, answer):
        '''
        Initializes attempt with the players guess and the correct answer.
        '''
        self.guess = guess
        self.answer = answer

    def guess(self):
        ''' Returns the guess that the player made.'''
        return self.guess

    def answer(self):
        ''' Returns the correct answer.'''
        return self.answer

    def win(self):
        ''' Returns True if the player has guessed correctly    '''
        return self.guess == self.answer

    def fully_correct(self): 
        '''
        Returns a string that is the same length of the answer. Except consists
        of underscores everywhere except for where the player guessed correctly.
        (Green in Wordle) 
        '''
        result_str = ''
        for i in range(len(self.guess)):
            if self.guess[i] == self.answer[i]:
                result_str += self.guess[i]
            else:
                result_str += "_"
        return result_str

    def remove_correct(self):
        '''
        HELPER FUNCTION: Returns list of letters in guess and list of letters in answer
        with all the letters that were correctly placed removed
        '''
        guess_list, answer_list = [], []
        guess_list[:0] = self.guess # initilized guessed word as a list
        answer_list[:0] = self.answer # initialize answer word as a list
        del_list = [] # initilize list of to be deleted letters

        # add all the letters guessed correctly to a list
        for guess_str, answer_str in zip(guess_list, answer_list): 
            if guess_str == answer_str:
                del_list.append(guess_str)
        # remove letters guessed correctly from guess list and answer list
        for str in del_list: 
            guess_list.remove(str)
            answer_list.remove(str)
        return guess_list, answer_list
        

    def partially_correct(self):
        '''
        Returns a ------ string that contains every letter which the player 
        guessed that is also in the answer, but not at the same position.
        (Yellow in Wordle)
        '''
        misplaced_str = ''
        guess_list, answer_list = self.remove_correct()
        # add all the letters that are in the answer but in the wrong position to a list
        for letter in guess_list: 
            if letter in answer_list:
                misplaced_str += letter
        return ''.join(misplaced_str)


    def fully_wrong(self):
        '''
        Returns a ------ string that contains every letter which the player 
        guessed that was not in the answer at all. 
        (Grey in Wordle)
        '''
        incorrect_str = ''
        guess_list, answer_list = self.remove_correct()
        # add all the letters that aren't in the answer to a list
        for letter in guess_list: 
            if not letter in answer_list:
                incorrect_str += letter
        return ''.join(incorrect_str)


class Game():
    def __init__(self, words):
        ''' Take a Words instance and picks a random word for the game.'''
        self.attempts = 0
        self.random_word = choice(tuple(words.words))

    def num_attempts(self):
        ''' Return the number of attempts the player has made so far.'''
        return self.attempts
    
    def answer(self):
        ''' Returns the random word chosen to be the answer'''
        return self.random_word

    def attempt(self, players_guess):
        ''' 
        Returns an Attempt instance object that represents the 
        results of whatever guess the player makes.
        '''
        self.attempts += 1
        return Attempt(players_guess, self.random_word)
    

