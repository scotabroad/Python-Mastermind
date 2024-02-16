from codebreaker import *
from codemaker import *
from ui import *
#This will hold game logic, but not ui

class Game():

    def __init__(self, codemaker, codebreaker, ui, pegs=4, colors=['R', 'O', 'Y', 'G', 'B', 'V'], guesses=10, with_replacement=True):
        self.answers = generate_all_answers(pegs, colors, with_replacement)
        
        self.codemaker = CodeMaker()
        if codemaker.lower() == "human":
            self.codemaker = HumanMaker()
        elif codemaker.lower() == "random":
            self.codemaker = RandomMaker()
        elif codemaker.lower() == "adversarial":
            self.codemaker = AdversarialMaker()
        
        self.codebreaker = CodeBreaker(self.answers)
        if codebreaker.lower() == "human":
            self.codebreaker = HumanBreaker(self.answers)
        elif codebreaker.lower() == "random":
            self.codebreaker = RandomBreaker(self.answers)
        elif codebreaker.lower() == "optimal":
            self.codebreaker = OptimalBreaker(self.answers)
        
        self.ui = ui
        
        self.pegs = pegs
        self.colors = colors
        self.guesses = guesses
        self.with_replacement = with_replacement
        self.isWon = False

    def play(self):
        if self.codemaker.isHuman:
            self.ui.show_board([], self.codebreaker.previous_guesses, self.codebreaker.previous_clues, self.pegs)
            self.codemaker.make_code(self.ui.ask_code(self.answers))
        else:
            self.codemaker.make_code(self.answers)
        self.ui.show_board([], self.codebreaker.previous_guesses, self.codebreaker.previous_clues, self.pegs)
        while (self.codebreaker.attempt <= self.guesses) and (not self.isWon):
            self.one_ply()
        self.ui.show_board(self.codemaker.code, self.codebreaker.previous_guesses, self.codebreaker.previous_clues, self.pegs)

    def one_ply(self):
        guess = []
        if self.codebreaker.isHuman:
            guess = self.codebreaker.make_guess(self.ui.ask_guess(self.pegs, self.colors, self.answers, self.with_replacement))
        else:
            guess = self.codebreaker.make_guess(self.pegs, self.colors, self.answers, self.with_replacement)
        self.ui.show_board([], self.codebreaker.previous_guesses, self.codebreaker.previous_clues, self.pegs)
        clue = ()
        if self.codemaker.isHuman:
            self.ui.show_board(self.codemaker.code, self.codebreaker.previous_guesses, self.codebreaker.previous_clues, self.pegs)
            clue, self.answers = self.codemaker.make_clue(self.ui.ask_clue(), guess, self.answers)
        else:
            clue, self.answers = self.codemaker.make_clue(guess, self.answers)
        self.codebreaker.receive_clue(clue, self.answers)
        if clue[0] == self.pegs:
            self.isWon = True
        self.ui.show_board([], self.codebreaker.previous_guesses, self.codebreaker.previous_clues, self.pegs)
        

