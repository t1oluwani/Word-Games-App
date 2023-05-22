from classes import Game
from classes import Words
from classes import TooLongError
from classes import TooShortError
from classes import NotAlphaError
from classes import InnapropriateWordError

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
                
    def get_guess(self):
        ''' Returns players guess'''
        while True:
            entry = input("Enter a "+str(self.letters)+" letter word:\n")
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
                
    def merge_dash(self, dash_str1, dash_str2):
        ''' TOWRITE'''
        result_str = ''
        for i in range(len(dash_str1)):
            if dash_str1[i] != "_":
                result_str += dash_str1[i]
            elif dash_str2[i] != "_":
                result_str += dash_str2[i]
            else:
                result_str += "_"
        return result_str
        
        
    def victory(self):
        attempts = self.game.num_attempts()
        if attempts == 1:
            print("Congrats, you have won in "+str(attempts)+" try and with a perfect your score of ----")
        else :
            print("Congrats, you have won in "+str(attempts)+" tries, your score is ----")
        # Asks user if they want to play again with a different word
        self.play_again()
    
            
    def game_over(self):
        # score = ...
        # if score == 0:
        print("Game Over, your score has reached 0 and you have lost")
        # else :
        print("Game Over, unfortunately you have lost with a final score of ----")
        # Asks user if they want to play again with a different word
        self.play_again()

            
    def make_attempt(self):
        ''' Make an attempt by guess a word of the required size'''
        print("")
        print(self.game.answer()) # DEBUG LINE
        
        self.guess = self.get_guess()
        self.guess = self.guess.upper()
        self.attempt = self.game.attempt(self.guess)
        
        self.correct_letters = self.merge_dash(self.correct_letters, self.attempt.fully_correct())
        self.misplaced_pool += self.attempt.partially_correct()
        self.misplaced_pool = "".join(sorted(set(self.misplaced_pool)))
        self.incorrect_letters += self.attempt.fully_wrong()
        self.incorrect_letters = "".join(sorted(set(self.incorrect_letters)))
        
        if self.attempt.win():
            self.victory()
        else:
            self.feedback()
            self.make_attempt()
        
        
    def feedback(self):
        print("Your Guess             :", self.guess)
        print("Green Letters          :", self.correct_letters)
        print("Yellow Letters         :", self.attempt.partially_correct())
        print("Pool of Yellow Letters :", self.misplaced_pool)
        print("Grey Letters           :", self.incorrect_letters)
        
        
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
        self.score = 1000*200
        self.correct_letters = "_"*self.letters
        
        # Make an attempt
        self.make_attempt()

    


class Hangman(WordGame):
    '''
    This class extends WordGame and uses the Game, Words, and Attempt classes
    to create a Hangman user interface experience on the console
    '''
    ...

class Wordle(WordGame):
    '''
    This class extends WordGame and uses the Game, Words, and Attempt classes
    to create a Wordle user interface experience on the console
    '''
    ...

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
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
            Proin egestas, sapien vel ornare vestibulum, felis urna 
            volutpat tellus, in rutrum ex massa eu lorem. Cras at 
            aliquam sem. Lorem ipsum dolor sit amet, consectetur 
            adipiscing elit. Proin vel lorem at orci elementum.
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
            3. Utilize the feedback to make educated guesses and deduce the word.
            4. Repeat the cycle until one of the following occurs: 
                you guess the word correctly and win, 
                your score reaches zero and you lose, or 
                you choose to exit by pressing "esc" at any time to instantly lose. 
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