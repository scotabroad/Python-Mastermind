
# Python Mastermind

## About
This is a simple mastermind game where a codemaker makes a code, and a codebreaker has to figure it out by making guesses. For each wrong guess, the codemaker must provide hints towards what the correct code is. The game is fully customizable in terms of number of pegs, the set of colors to use, how many guesses will be allowed before the game ends, and if repeats of colors are allowed in the code or if each color can appear in the code at most once.

I have developed it with the ability to be played between two humans, a human and an AI, or even two AIs. There are four AI options: two for the codebreaker role and two for the codemaker role.

### Codemaker AIs
The first is an AI agent that randomly picks a code from the pool of all possible codes given the provided constraints. For every guess, the random AI agent will compare each guess to its code and provide hints.

The second is an adversarial AI agent. Instead of making a code, it uses the codebreaker's guesses to decrease the size of the answer pool. It does so by sorting all codes by what hints it may give and selecting the largest answer pool. If there is a tie, it will choose the group of answers that has the least informative hint. The game is won after the AI has decreased the answer pool to a set of one.

### Codebreaker AIs
The first is an AI agent that randomly picks a guess from the pool of all possible code that it has not guessed yet. It tends to perform poorly is the answer pool is large.

The second is an optimal AI agent. Given a code with the constraints of 4 pegs and 6 colors, it can crack the code in no more than 5 moves.

