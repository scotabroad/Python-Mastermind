from utils import *
#Defines GUI and TUI classes

class UI():
    def __init__(self):
        self.pegs = 0
        self.colors = []
        self.guesses = 0
        self.with_replacement = False
        self.codemaker = ""
        self.codebreaker = ""

    def show_board(self, passcode, guesses, clues, pegs):
        pass

    def ask_code(self, answers):
        pass

    def ask_guess(self, pegs, colors, answers):
        pass

    def ask_clue(self):
        pass

class CLI(UI):
    def __init__(self):
        self.pegs = 0
        self.colors = []
        self.guesses = 0
        self.with_replacement = False
        self.codemaker = ""
        self.codebreaker = ""
        loop = True
        while loop:
            if self.codemaker == "":
                self.codemaker = input(f"Please choose a codemaker [human/adversarial/random]: ")
                if self.codemaker != "human" and self.codemaker != "adversarial" and self.codemaker != "random":
                    clear()
                    print(f"ValueError: Choice {self.codemaker} was not in list [human/adversarial/random]")
                    self.codemaker = ""
                    continue
            if self.codebreaker == "":
                self.codebreaker = input(f"Please choose a codebreaker [human/optimal/random]: ")
                if self.codebreaker != "human" and self.codebreaker != "optimal" and self.codebreaker != "random":
                    clear()
                    print(f"ValueError: Choice {self.codebreaker} was not in list [human/optimal/random]")
                    self.codebreaker = ""
                    continue
            if self.pegs <= 0:
                try:
                    self.pegs = int(input(f"Please enter how many pegs you want: "))
                except ValueError:
                    clear()
                    print("TypeError: Values were not of type int")
                    continue
                if self.pegs <= 0:
                    clear()
                    print("SizeError: Must have at least one peg")
                    continue
            if len(self.colors) <= 0:
                try:
                    self.colors = list(map(str, input(f"Please input colors as single characters, " +
                                                      "separated by spaces. Results are case sensitive: ").split()))
                except ValueError:
                    clear()
                    print("TypeError: Values were not of type string")
                    continue
                if len(self.colors) <= 0:
                    clear()
                    print("SizeError: Must have at least one color in list")
                    continue
            if self.guesses <= 0:
                try:
                    self.guesses = int(input(f"Please enter how many guesses you want: "))
                except ValueError:
                    clear()
                    print("TypeError: Values were not of type int")
                    continue
                if self.guesses <= 0:
                    clear()
                    print("SizeError: Must have at least one chance at guessing the answer")
                    continue
            if len(self.colors) >= self.pegs:
                response = input(f"Do you want to allow duplicate colors in guesses? [Y/n]: ")
                if response.upper() == "Y":
                    self.with_replacement = True
                    loop = False
                    break
                elif response.lower() == "n":
                    self.with_replacement = False
                    loop = False
                    break
                else:
                    clear()
                    print("TypeError: Please either input Y or n")
                    loop = False
                    continue
            else:
                response = input(f"Warning: You have less pegs than colors, duplicates will be used. Press ENTER to begin ")
                self.with_replacement = True
                loop = False
                break

    def show_board(self, passcode, prev_guesses, prev_clues, pegs):
        clear()
        print("Colors: ", end = "")
        for x in self.colors:
            print(x, end = " ")
        print()
        print(f"Duplicates: {self.with_replacement}")
        print("--------" * pegs + "--" + "--" * pegs)
        print(" " + "     " * (pegs - 1) + "MASTERMIND")
        print("--------" * pegs + "--" + "--" * pegs)
        #Remember dictionaries are indexed by attempt, which you made start at 1!!!
        guesses = [['-' for x in range(pegs)] for x in range(self.guesses)]
        clues = [['-' for x in range(pegs)] for x in range(self.guesses)]
        code = ['-' for x in range(pegs)]
        for attempt in range(len(prev_guesses)):
            guesses[attempt] = prev_guesses[attempt+1]
        for attempt in range(len(prev_clues)):
            correct = prev_clues[attempt+1][0]
            wrong = prev_clues[attempt+1][1]
            for i in range(pegs):
                if correct > 0:
                    clues[attempt][i] = 'R'
                    correct -= 1
                elif wrong > 0:
                    clues[attempt][i] = 'W'
                    wrong -= 1
        if len(passcode) > 0:
            code = passcode
        for i in range(len(guesses)):
            for x in guesses[i]:
                print(x[:pegs], end="\t")
            print(end="| ")
            for x in clues[i]:
                print(x[:pegs], end=" ")
            print() 
            print("--------" * pegs + "--" + "--" * pegs)
        
        for x in code:
            print(x[:pegs], end="\t")
        print(end="|")
        print()
        print("--------" * pegs + "--" + "--" * pegs)

    def ask_code(self, answers):
        code = []
        cinput = ()
        while cinput not in answers:
            cinput = tuple(map(str, input(f"Please enter your code here: ").split()))
            if cinput not in answers:
                print("Error: Your code is invalid")
            else:
                code = list(cinput)
                break
        clear()
        return code

    def ask_guess(self, pegs, colors, answers, with_replacement):
        guess = []
        ginput = ()
        while ginput not in answers:
            ginput = tuple(map(str, input(f"Please enter your guess here: ").split()))
            if ginput not in answers:
                print("Error: Your guess is invalid")
            else:
                guess = ginput
                break
        clear()
        return guess

    def ask_clue(self):
        cinput = tuple(map(int, input(f"Please enter number of correct pegs followed by number of wrong pegs: ").split()))
        return cinput

#class GUI(UI):
