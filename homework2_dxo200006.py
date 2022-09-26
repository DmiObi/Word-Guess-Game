# Dmitrii Obideiko
# DXO200006

from collections import defaultdict
import pathlib
import sys
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from random import seed
from random import randint

def printLexicalDiversity(text):
    tokens = nltk.word_tokenize(text) 
    uniqueTokens = set(tokens)
    lexicalDiversity = len(uniqueTokens) / len(tokens)
    # prints the lexical diversity formated to 2 decimal places
    print('\nLexical diversity: %.2f' % lexicalDiversity)

def preprocessRawText(text):
    # checks if the the tag is a noun
    def isNoun(val):
        if(val == 'NN' or val == 'NNS' or val == 'NNPS' or val == 'NNP'):
            return True
        return False
    
    # tokenize the lower-case text 
    tokens = nltk.word_tokenize(text.lower())
    # checks if each token is a letter, not a stop word, and its length is greater than 5
    processedTokens = [t for t in tokens if t.isalpha() and 
                       t not in stopwords.words('english') and 
                       len(t) > 5]
    
    # lemmatize tokens
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in processedTokens]
    # choose unique tokens
    unique_lemmas = list(set(lemmas))
    # do pos tagging on unique_elements    
    taggedTokens = nltk.pos_tag(unique_lemmas)
    print('\nTagged tokens:\n', taggedTokens[:20])
    
    nounTokens = [t[0] for t in taggedTokens if isNoun(t[1])]
    
    print('\nNumber of tokens: ', len(tokens))    
    print('\nNumber of noun tokens: ', len(nounTokens))
    
    return processedTokens, nounTokens
        
def mostCommonWords(tokens, n):
    count = defaultdict(int)
    # counts the frequency of each token
    for token in tokens:
        count[token] += 1
    # sorts the dictionary in a reverse order based on the frequency and puts the values into a list
    sortedCount = list(dict(sorted(count.items(), key=lambda item: item[1], reverse = True)))
    # return the first n values from the list
    return sortedCount[:n]

# returns all indexes where the letter is present in the word
def getIndexesOfAllOccurrences(word, letter):
    indexes = []
    index = word.find(letter)
    # continue to look for the letter until none remains
    while index != -1:
        indexes.append(index)
        index = word.find(letter, index + 1)
    return indexes
    
def game(tokens):
    print('\n\n\nLet\'s play a word guessing game!')
    commonWords = mostCommonWords(tokens, 50)
    points = 5
    # set the starting number that the random number generator uses
    seed(1234)
    # choose a random word from the commonWords list
    randomWord = commonWords[randint(0, 50)]
    userGuess = ''
    output = list('-' * len(randomWord))
    # the game stops if the player dones't has a negative number of points, guess the word, or inputs '!'
    while points > 0 and userGuess != '!':
        # prints which letters were guessed and which weren't
        print(''.join(output))    
        userGuess = input('Enter a letter: ')
        if userGuess == '!':
            break
        
        indexes = getIndexesOfAllOccurrences(randomWord, userGuess)
        # checks if ther letter that the user gussed occurs at least once in the randomWord
        if indexes:
            print('Right!')
            print('Score is ', points)
            # updates the output
            # replaces the dashes with the letter that was guessed correctly
            for ind in indexes:
                # only give a point if the letter hasn't been guessed before
                if output[ind] != randomWord[ind]:
                    points += 1
                    output[ind] = randomWord[ind]
        else:
            points -= 1
            print('Sorry, guess again')
            print('Score is ', points)
        
        # checks if the randomWord is guessed yet
        if ''.join(output) == randomWord:
            print(randomWord)
            print('You solved it!')
            # sets a new randomWord
            randomWord = commonWords[randint(0, 50)]
            # updates the output
            output = list('-' * len(randomWord))
            print('\nCurrent score: ', points)
            
    # tells the user if they won, lost, or quit the game
    if userGuess == '!':
        print('You quit the game')
    elif ''.join(output) == randomWord:
        print('Congradulations! You guessed the word', randomWord)
        print('Your score is: ', points)
    else:
        print('Unfortunately, you lost')
        print('The word was', randomWord)
              
# is called when the program starts
if __name__ == '__main__':
    # checks if the user put a system argument
    if len(sys.argv) < 2:
        print('Error: Please enter a filename as a system argument')
        quit()
    
    # opens the file and saves all lines that are present in it
    filePath = sys.argv[1]
    with open(pathlib.Path.cwd().joinpath(filePath), 'r') as f:
        text_in = f.read()
    
    printLexicalDiversity(text_in)
    noun_tokens = preprocessRawText(text_in)[1]
    print('\nMost Common Words\n',mostCommonWords(noun_tokens, 50))
    game(noun_tokens)