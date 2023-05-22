from classes import Game
from classes import Words
from classes import Attempt
from classes import TooLongError
from classes import TooShortError
from classes import NotAlphaError

class WordGame:
    '''
    This class initializes the components that a word game would need to work
    such as selecting the answer word, comparing it with the players guess and etc
    '''
    def __init__(self):
        self.misplaced = ''
        self.displaced = ''
        self.incorrect = ''
        
    def get_letters(self):
        ''' Returns amount of letters player would like to play with'''
        while True:
            entry = input("How many letters would you like to play with (0 to unspecify):\n")
            try:
                return int(entry)
            except:
                print("Please enter a valid whole number!")
                
    def get_guess(self):
        ''' Returns players guess'''
        while True:
            entry = input("Enter a "+str(self.letters)+" letter word:\n")
            try:
                assert len(entry) == self.letters
                return str(entry)
            except:
                print("Please enter a "+str(self.letters)+" letter string!")
                
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
 

            
    def make_attempt(self):
        ''' Make an attempt by guess a word of the required size'''
        print("")
        print(self.game.answer())
        
        self.guess = self.get_guess()
        self.guess = self.guess.upper()
        self.attempt = self.game.attempt(self.guess)
        
        self.correct = self.merge_dash(self.correct, self.attempt.correct())
        self.displaced += self.attempt.misplaced()
        self.displaced = "".join(sorted(set(self.displaced)))
        self.incorrect += self.attempt.incorrect()
        self.incorrect = "".join(sorted(set(self.incorrect)))
        
        if self.attempt.win():
            self.victory()
        else:
            self.re_attempt()
        
        
    def re_attempt(self):
        print("Your Guess       :", self.guess)
        print("Correct Letters  :", self.correct)
        print("Misplaced Letters:", self.attempt.misplaced())
        print("Displaced Letters:", self.displaced)
        print("Incorrect Letters:", self.incorrect)
        self.make_attempt()
        
        
    def play_again(self):
        again = True
        while again == True:
            entry = input("Would you like to play again Yes(Y) or No(N):\n").lower()
            if entry[0] == "y":
                again = False
                self.new_game()
            elif entry[0] == "n":
                again = False
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
        self.correct = "_"*self.letters
        
        # Make an attempt
        self.make_attempt()
        
        # Asks user if they want to play again with a different word
        self.play_again()
        
        print("newgame")

    


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
                  Nam ornare massa non turpis placerat faucibus. Fusce luctus, 
                  justo a imperdiet lacinia, risus ante scelerisque ex, sodales 
                  eleifend risus mi non leo. Nunc id consectetur augue. Morbi 
                  euismod volutpat neque, vel ullamcorper mauris. Proin ut venenatis 
                  massa. Donec urna augue, laoreet vitae lobortis ut, sagittis in. 
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
    If you know the rule and would like to play, enter Play(P)
    If you do no tknow how to play and would like to learn, enter Help(H)
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