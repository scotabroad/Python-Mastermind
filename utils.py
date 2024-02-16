from itertools import product, permutations
import os

def clear():
    os.system("clear")

def generate_all_answers(pegs, colors, with_replacement=True):
    #Returns a list of tuples
    if with_replacement:
        return list(product(colors, repeat=pegs))
    else:
        return list(permutations(colors, pegs))
