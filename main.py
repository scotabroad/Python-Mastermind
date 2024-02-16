from ui import *
from game import *
#This will handle CLI arguments. Assume GUI before CLI
if __name__ == '__main__':
    ui = CLI()
    game = Game(ui.codemaker, ui.codebreaker, ui, ui.pegs, ui.colors, ui.guesses, ui.with_replacement)
    game.play()
