import random

#Generic class
class CodeBreaker():
    #All will have these, accessed by self.variable_name
    def __init__(self, answers):
        #These are dictionaries, indexed by attempt
        #{attempt: [colors in guess]}
        self.previous_guesses = {}
        self.previous_clues = {}
        self.attempt = 1
        self.isHuman = False

    def make_guess(self):
        pass

    def receive_clue(self, clue, answers):
        self.previous_clues[self.attempt] = clue
        self.attempt += 1

class HumanBreaker(CodeBreaker):
    #All will have these, accessed by self.variable_name
    def __init__(self, answers):
        #These are dictionaries, indexed by attempt
        #{attempt: [colors in guess]}
        self.previous_guesses = {}
        self.previous_clues = {}
        self.attempt = 1
        self.isHuman = True

    def make_guess(self, guess):
        #Input sanitization is done in UI
        self.previous_guesses[self.attempt] = guess
        return guess

class RandomBreaker(CodeBreaker):
    #Selects a random answer from list of answers that hasn't been guessed
    def make_guess(self, pegs, colors, answers, with_replacement):
        guess = list(random.choice(answers))
        self.previous_guesses[self.attempt] = guess
        return guess

#This one uses Knuth's algorithm
#https://stackoverflow.com/questions/62430071/donald-knuth-algorithm-mastermind
#https://theses.liacs.nl/pdf/2018-2019-GraafSde.pdf
class OptimalBreaker(CodeBreaker):
    #All will have these, accessed by self.variable_name
    def __init__(self, answers):
        #These are dictionaries, indexed by attempt
        #{attempt: [colors in guess]}
        self.previous_guesses = {}
        self.previous_clues = {}
        self.attempt = 1
        self.isHuman = False
        self.knuth_codes = [x for x in answers]

    def make_clue(self, guess, code):
        correct = 0
        wrong = 0
        answer_copy = [x for x in code]
        for i in range(len(guess)):
            if guess[i] in answer_copy:
                if guess[i] == code[i]:
                    correct += 1
                else:
                    wrong += 1
                answer_copy.remove(guess[i])
        clue = (correct, wrong)
        return clue

    def max_value(self, dictionary):
        max = float('-inf')
        for key, value in dictionary.items():
            if value > max:
                max = value
        return max

    def min_value(self, dictionary):
        min = float('inf')
        for key, value in dictionary.items():
            if value < min:
                min = value
        return min

    def minimax(self, answers):
        possible_codes = [x for x in answers]
        minimax_guesses = []
        scores = {}
        for guess in possible_codes:
            occurrences = {}
            for code in self.knuth_codes:
                clue = self.make_clue(guess, code)
                if clue in occurrences:
                    occurrences[clue] += 1
                else:
                    occurrences[clue] = 1
            max = self.max_value(occurrences)
            scores[guess] = max
        min = self.min_value(scores)
        for guess in possible_codes:
            if scores[guess] == min:
                minimax_guesses.append(guess)
        return minimax_guesses


    def make_guess(self, pegs, colors, answers, with_replacement):
        guess = []
        guess_pool = self.minimax(answers)
        if self.attempt == 1:
            if with_replacement:
                #The following provides best entropy
                if pegs % 2 == 0:
                    half1 = [colors[0] for x in range(int(pegs/2))] 
                    half2 = [colors[1] for x in range(int(pegs/2))]
                    guess = [y for x in [half1, half2] for y in x]
                elif (pegs % 2 == 1) and len(colors) > 1:
                    half1 = [colors[0] for x in range(int(pegs/2))] 
                    half2 = [colors[1] for x in range(int(pegs/2))]
                    guess = [colors[0]] + [y for x in [half1, half2] for y in x]
                else:
                    guess = [colors[0]]
            else:
                guess = list(answers[0])
        else:
            if len(self.knuth_codes) > 0:
                for code in guess_pool:
                    if code in self.knuth_codes:
                        guess = list(self.knuth_codes[0])
                        break
                if guess == []:
                    guess = list(guess_pool[0])
            else:
                guess = list(guess_pool[0])
        self.previous_guesses[self.attempt] = guess
        return guess

    def receive_clue(self, clue, answers):
        guess = self.previous_guesses[self.attempt]
        answer_pools = {}
        for answer in self.knuth_codes:
            feedback = self.make_clue(guess, answer)
            if feedback in answer_pools:
                answer_pools[feedback].append(answer)
            else:
                answer_pools[feedback] = [answer]
        self.knuth_codes = answer_pools[clue]
        self.previous_clues[self.attempt] = clue
        self.attempt += 1