from classes import Game
from classes import Words
from classes import TooLongError
from classes import TooShortError
from classes import NotAlphaError
from classes import InnapropriateWordError

MAX_LETTERS = 13 # Max size of words

class WordGame:
    '''
    This class initializes the components that a word game would need to work
    such as selecting the answer word, comparing it with the players guess and etc
    '''  
    def __init__(self):
        self.misplaced_pool = ''
        # self.displaced = ''
        self.incorrect_letters = ''
        
    def get_letters(self):
        ''' Returns amount of letters player would like to play with'''
        while True:
            entry = input("How many letters would you like to play with (0 to unspecify):\n")
            try:
                if int(entry) != 1:
                    return int(entry)
            except:
                print("Please enter a valid whole number!")
                            
    def merge_dash(self, dash_str1, dash_str2):
        '''
        HELPER FUNCTION: Combines two dash-hybrid words eg. 
        B _ _ _ + _ _ A T = B _ A T; B _ A T + _ O _ _ = B O A T
        '''
        result_str = ''
        for i in range(len(dash_str1)):
            if dash_str1[i] != "_":
                result_str += dash_str1[i]
            elif dash_str2[i] != "_":
                result_str += dash_str2[i]
            else:
                result_str += "_"
        return result_str
            
    def game_over(self):
        print("Game Over!")
        print("The secret word was:", self.attempt.answer)
        print("Unfortunately, you couldn't get it this time.")
        print("Better luck next time!")
        self.play_again() # Asks user if they want to play again with a different word    
        
    def play_again(self):
        ask = True
        while ask == True:
            entry = input("Would you like to play again Yes(Y) or No(N):\n").lower()
            if entry[0] == "y":
                ask = False
                self.new_game()
            elif entry[0] == "n":
                ask = False
                print("Thank you for playing!")
                start_game()
            else:
                print("Please enter a valid option!")

    def new_game(self):
        '''
        Initialize new game
        '''
        # Gets self.letters from player
        self.letters = self.get_letters()
        
        # Load words to self.words 
        self.words = Words(self.letters)
        self.words.load_file("words.txt") #replace w library
        
        # Initialize game using self.words
        self.game = Game(self.words)
        self.letters = len(self.game.answer()) # reassign value to letter to length of answer word
        self.score = int (1000 + (500*(self.letters/MAX_LETTERS)))
        self.correct_letters = "_"*self.letters
        
        # Make an attempt
        self.make_attempt()



class Hangman(WordGame):
    '''
    This class extends WordGame and uses the Game, Words, and Attempt classes
    to create a Hangman user interface experience on the console
    '''
        
    def get_guess(self):
        ''' Returns players guess'''
        while True:
            entry = input("Guess a letter:\n")
            if entry == 'esc':
                self.game_over()
            try:
                self.words.check_letter(entry)
                return str(entry)
            except NotAlphaError:
                print("Word not alphabetic! Please enter a "+str(self.letters)+" letter string!")          
    
    def make_attempt(self):
        ''' Make an attempt by guessing a letter that may exist in answer word'''
        print("")
        
        self.guess = self.get_guess()
        self.guess = self.guess.upper()
        self.attempt = self.game.attempt(self.guess)
        
        self.correct_letters = self.merge_dash(self.correct_letters, self.attempt.exists_in())
        self.incorrect_letters += self.attempt.not_exist_in()
        self.incorrect_letters = "".join(sorted(set(self.incorrect_letters)))
        
        if self.attempt.success(self.correct_letters):
            print(self.correct_letters)
            self.victory() 
        else:
            self.score -= 50
            self.attempt.hangman(len(self.incorrect_letters))
            if len(self.incorrect_letters) > 6:
                self.game_over()
            self.feedback()
            self.make_attempt()
            
    def feedback(self):
        print("Incorrect Attempts:", self.incorrect_letters)
        print(self.correct_letters)
        
    
    def victory(self):
        attempts = len(self.incorrect_letters)
        if attempts == 1:
            print("Congrats, you have won in "+str(attempts)+" try and with a perfect your score of", self.score)
        else :
            print("Congrats, you have won in "+str(attempts)+" tries, your score is", self.score)
        self.play_again() # Asks user if they want to play again with a different word
    
    
    
class Wordle(WordGame):
    '''
    This class extends WordGame and uses the Game, Words, and Attempt classes
    to create a Wordle user interface experience on the console
    '''
    
    def get_guess(self):
        ''' Returns players guess'''
        while True:
            entry = input("Make a "+str(self.letters)+" letter guess:\n")
            if entry == 'esc':
                self.game_over()
            try:
                self.words.check_word(entry)
                return str(entry)
            except TooShortError:
                print("Word too Short! Please enter a "+str(self.letters)+" letter string!")
            except TooLongError:
                print("Word too Long! Please enter a "+str(self.letters)+" letter string!")
            except NotAlphaError:
                print("Word not alphabetic! Please enter a "+str(self.letters)+" letter string!")
            except InnapropriateWordError:
                print("Word in inappropriate! Please enter an appropriate "+str(self.letters)+" letter string (No cusses or slurs)!")
    
    def make_attempt(self):
        ''' Make an attempt by guessing a word of the required size'''
        print("")
        
        self.guess = self.get_guess()
        self.guess = self.guess.upper()
        self.attempt = self.game.attempt(self.guess)
        
        self.correct_letters = self.merge_dash(self.correct_letters, self.attempt.fully_correct())
        self.misplaced_pool += self.attempt.partially_correct()
        self.misplaced_pool = "".join(sorted(set(self.misplaced_pool)))
        self.incorrect_letters += self.attempt.fully_wrong()
        self.incorrect_letters = "".join(sorted(set(self.incorrect_letters)))
        
        if self.attempt.success():
            self.victory()
        else:
            self.score -= 50
            self.feedback()
            self.make_attempt()
        
    def feedback(self):
        print("Your Guess             :", self.guess)
        print("Green Letters          :", self.correct_letters)
        print("Yellow Letters         :", self.attempt.partially_correct())
        print("Pool of Yellow Letters :", self.misplaced_pool)
        print("Grey Letters           :", self.incorrect_letters)   
        
    def victory(self):
        attempts = self.game.num_attempts()
        if attempts == 1:
            print("Congrats, you have won in "+str(attempts)+" try and with a perfect your score of", self.score)
        else :
            print("Congrats, you have won in "+str(attempts)+" tries, your score is", self.score)
        self.play_again() # Asks user if they want to play again with a different word

# MAIN FUNCTIONS \/

def learn_rules():
    '''
    Displays rules and synopsis about users selected game
    '''
    choosing = True
    while choosing == True:
        entry = input("What would you like to learn about, Hangman(H), Wordle(W), Esc(E):\n").lower()

        if entry[0] == "h":
            choosing = False
            print("""
            Hangman is a classic word-guessing game where you have to guess a hidden word letter by letter. 
            You have a limited number of attempts to guess the word correctly. To play, follow these steps:

            1. Guess a letter that you think might be in the chosed word.
            2. After each guess, you will receive feedback 
                a correct guess will be revealed in its position in the word, 
                an incorrect guess will cause more details to be added to your hangman
                you have 7 attempts at guessing
            3. Use the feedback to make educated guesses and deduce the word.
            4. Repeat the cycle until one of the following occurs: 
                you guess the entire word correctly and win, 
                your hangman is fully drawn due to 7 attempts, or 
                you choose to exit by pressing "esc" at any time to instantly lose.
            5. Your goal is to guess the word with as few incorrect attempts as 
                possible to achieve a high score.
                  """)
            start_game()
            
        elif entry[0] == "w":
            choosing = False
            print("""
            Wordle is a well-known word-guessing game and this app offers two versions: Classical Wordle and MyWordle. 
            In Classical Wordle, players have six attempts to guess a five-letter word. 
            In MyWordle, you have unlimited attempts, and the word's length can either be random (by inputting 0) 
            or determined by you (by entering a specific number). To play, follow these steps:

            1. Guess a word with the chosen number of letters.
            2. After each guess, you will receive feedback in the form of colors: 
                green for correct letters in the correct position, 
                yellow for correct letters in the wrong position,
                a pool of yellow letters accumulated so far and,
                gray for incorrect letters. 
            3. Use the feedback to make educated guesses and deduce the word.
            4. Repeat the cycle until one of the following occurs: 
                you guess the word correctly and win, 
                your score reaches zero and you lose, or 
                you choose to exit by pressing "esc" at any time to instantly lose. 
            5. Your goal is to guess the word with as few incorrect attempts as 
                possible to achieve a high score.
                  """)
            start_game()
            
        elif entry[0] == "e":
            choosing = False
            start_game()
        else:
            print("Please enter a valid option!")
            
def choose_game():
    '''
    Initializes the word games experience by asking player which game they want to play
    '''
    choosing = True
    while choosing == True:
        entry = input("What would you like to play, Hangman(H), Wordle(W), Esc(E):\n").lower()

        if entry[0] == "h":
            choosing = False
            Hangman().new_game()
        elif entry[0] == "w":
            choosing = False
            Wordle().new_game()
        elif entry[0] == "e":
            choosing = False
            start_game()
        else:
            print("Please enter a valid option!")

def start_game():
    '''
    Initializes the word games experience by asking player if they want to play, see the rules or leave
    '''
    start = True
    while start == True:
        entry = input("""
    Hello and Welcome to Word Games!
    If you know the rules and would like to play, enter Play(P)
    If you don't know how to play and would like to learn, enter Help(H)
    If you would like to exit this experience, enter Esc(E)
    -> """).lower()

        if entry[0] == "p":
            start = False
            print("")
            choose_game()
        elif entry[0] == "h":
            print("")
            start = False
            learn_rules()
        elif entry[0] == "e":
            start = False
        else:
            print("Please enter a valid option!")

def main():
    start_game()
    
if __name__=="__main__":
    main()