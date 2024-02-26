import random

#Generic class
class CodeMaker():

    def __init__(self):
        self.code = []
        self.isHuman = False

    def make_code(self):
        pass

    def make_clue(self, guess, answers):
        pass

class HumanMaker(CodeMaker):
    
    def __init__(self):
        self.code = []
        self.isHuman = True
    
    def make_code(self, code):
        #Input sanitization is in UI
        self.code = code

    def make_clue(self, clue, guess, answers):
        answers.remove(tuple(guess))
        return clue, answers

class RandomMaker(CodeMaker):
    #Selects a random answer from list of answers to be the code
    def make_code(self, answers):
        self.code = list(random.choice(answers))

    def make_clue(self, guess, answers):
        correct = 0
        wrong = 0
        guess_copy = []
        code_copy = []
        for i in range(len(guess)):
            if guess[i] == self.code[i]:
                correct += 1
            else:
                guess_copy.append(guess[i])
                code_copy.append(self.code[i])
        for i in range(len(guess_copy)):
            if guess_copy[i] in code_copy:
                wrong += 1
                code_copy.remove(guess_copy[i])
        clue = (correct, wrong)
        answers.remove(tuple(guess))
        return clue, answers

class AdversarialMaker(CodeMaker):
    #This one only makes a code if the answer set is equal to one
    def make_code(self, answers):
        if len(answers) == 1:
            self.code = [x for x in answers[0]]
        else:
            self.code = []

    def make_clue(self, guess, answers):
        answer_pools = {}
        #Lists and dictionaries can be modified without returning
        for answer in answers:
            correct = 0
            wrong = 0
            guess_copy = []
            answer_copy = []
            for i in range(len(guess)):
                if guess[i] == answer[i]:
                    correct += 1
                else:
                    guess_copy.append(guess[i])
                    answer_copy.append(answer[i])
            for i in range(len(guess_copy)):
                if guess_copy[i] in answer_copy:
                    wrong += 1
                    answer_copy.remove(guess_copy[i])
            clue = (correct, wrong)

            if clue in answer_pools:
                answer_pools[clue].append(answer)
            else:
                answer_pools[clue] = [answer]
        #Find largest group of least informative responses
        clue = (0, 0)
        new_answers = []
        for key in answer_pools:
            if len(answer_pools[key]) > len(new_answers):
                new_answers = answer_pools[key]
                clue = key
            elif len(answer_pools[key]) == len(new_answers):
                pool_c = key[0]
                pool_w = key[1]
                answer_c = clue[0]
                answer_w = clue[1]
                #Choose the group that provides the least information
                #RW-- is better than WWW-
                if (answer_c + answer_w) < (pool_c + pool_w):
                    new_answers = new_answers
                    clue = clue
                elif (pool_c + pool_w) < (answer_c + answer_w):
                    new_answers = answer_pools[key]
                    clue = key
                #Anything below here has equal information
                #WW-- is better than RW--
                #W--- is better than R---
                elif answer_w > pool_w:
                    new_answers = new_answers
                    clue = clue
                elif pool_w > answer_w:
                    new_answers = answer_pools[key]
                    clue = key
                #These have the same number of wrong answers
                #Either wrong answers are 0, or the two sets are identical
                #Checking for correct is here below, but might be redundant
                elif answer_c < pool_c:
                    new_answers = new_answers
                    clue = clue
                elif pool_c < answer_c:
                    new_answers = answer_pools[key]
                    clue = key
        answers = new_answers
        if len(answers) == 1:
            self.code = [x for x in answers[0]]
        return clue, answers
