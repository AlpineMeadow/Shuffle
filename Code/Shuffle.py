#! /usr/bin/env pythons

#A program to create a shuffle set.

def primeFactors(n): 
  import math
  import numpy as np

  i = 2
  factors = []
  while i * i <= n:
    if n % i:
      i += 1
    else:
      n //= i
      factors.append(i)
  #End of while loop
  
  if n > 1:
    factors.append(n)
    
  return factors

##################################################################################

##################################################################################

def getArgs(parser) :
 
  #Get the parameters
  parser.add_argument('-mC', '--maxCards', default = 52,
                      help = 'Choose the maximum number of cards', type = int) 

  args = parser.parse_args()

  #Generate variables from the inputs.
  maxNumCards = args.maxCards

  return maxNumCards
#End of the function getArgs(parser).py

#################################################################################

#################################################################################

def getShuffleSet(maxNumCards) :
  import numpy as np

  #Set up a dictionary for the results.
  shuffleSet = {}

  #Set up the counter for the number of shuffles.
  shuffles = 0

  #Loop through the different card decks.  Since n and n+1 give the same result, just look at
  #the odd values.
  for i in range(2, maxNumCards, 2) :

    #Create a deck of cards.
    deck = np.arange(1, i + 1)
    numShuffles = getNumShuffles(deck)
    
    shuffleSet[i] = numShuffles
  #End of for loop - for i in range(2, maxNumCards) :
  
  return shuffleSet
#End of the function getShuffleSet.py

#####################################################################################

#####################################################################################

def getNumShuffles(deck) :

  #Set counter to one.
  numShuffles = 1

  #initialize the new deck.
  newDeck = deck
  
  #Loop through decks to find the number of shuffles needed to get back to original sequence of
  #cards.
  while(1) :
    newDeck = shuffle(newDeck)
  
    #Check to see if the new deck is the same as the old deck.
    if((deck == newDeck).all()) :
      break
    else :
      numShuffles += 1
    #End of if-else clause.
    
  #End of while loop

  return numShuffles

#End of the function getNumShuffles.py

#################################################################################

#################################################################################

def shuffle(deck) :

  #Get shape of deck.
  m = len(deck)

  #Split the deck in half.
  splitNum = int(m/2)
  firstHalf = deck[:splitNum]
  secondHalf = deck[splitNum:]

  #Shuffle the deck.
  newDeck = []
  for i in range(len(firstHalf)) :
    newDeck.append(firstHalf[i])
    newDeck.append(secondHalf[i])
  #End of for loop - for j in range(len(firstHalf)) :
  
  return newDeck
#End of function shuffle.py

#############################################################################

#############################################################################

def plotShuffle(shuffleSet, outfile) :
  import numpy as np
  import matplotlib.pyplot as plt
  from matplotlib.backends.backend_pdf import PdfPages
  import math


  #Generate arrays from the dictionary.
  #X is an array of even numbers ranging from 2 to 2*len(x).  This is because the odd numbers
  #give the same results as the even numbers.
  x = np.fromiter(shuffleSet.keys(), dtype = int)
  y = np.fromiter(shuffleSet.values(), dtype = int)
  
  m = len(y)
  isPrime = np.ones(m)
  
  #Find maxes and mins.
  xmax = max(x)
  ymax = max(x)
  ymin = min(y)

  
  for i in range(m) :
    pf = primeFactors(y[i])
    if(len(pf) == 1) :
      pass
    else :
      isPrime[i] = 0
    #end of if-else clause
  #End of for loop - for i in range(1, m):
  
  #Generate a title string.
  titleStr = ('Number of Shuffles Needed to Obtain Original Sequence')

  #Plot the set.
  figX = np.max([int(xmax/100.0), 20])
  figY = np.max([int(figX/4.0), 10])

  plt.figure(figsize = (figX, figY))
  plt.rcParams.update({'font.size': 24})
  plt.plot(x, y, '.', color = 'black')
  plt.plot([2.0, xmax], [2.0, np.log2(x[-1])], color = 'red', label = r'$y = log_{2}(x)$')
  plt.plot([2.0, xmax], [2.0, ymax], color = 'black', label = 'y = x')
  plt.plot([2.0, xmax], [2.0, ymax/2.0], color = 'blue', label = 'y = x/2')
  plt.plot([2.0, xmax], [2.0, ymax/3.0], color = 'green', label = 'y = x/3')
  plt.plot([2.0, xmax], [2.0, ymax/4.0], color = 'brown', label = 'y = x/4')
  plt.plot([2.0, xmax], [2.0, ymax/5.0], color = 'orange', label = 'y = x/5')
  
  plt.plot(x[isPrime == 1], y[isPrime == 1], 'o', color = 'magenta')
  plt.title(titleStr)
  plt.grid('on')
  plt.legend(loc = 'upper left')
  plt.xlabel('Number of Values in Sequence')
  plt.ylabel('Number of Shuffles')
           
  #Save the plot to a file.
  pp = PdfPages(outfile)
  pp.savefig()
  pp.close()

  plt.cla()
  plt.clf()
#End of the function plotShuffle.py

######################################################################################

######################################################################################

#Gather our code in a main() function.
def main() :
  import argparse

  #Set up the argument parser.
  parser = argparse.ArgumentParser()

  #Get the maximum number of card sets to be shuffled.
  maxNumCards = getArgs(parser)
  
  #Get the shuffle set.
  shuffleSet = getShuffleSet(maxNumCards)
  
  #Create a output file name to where the plot will be saved.
  outfilepath = '/home/jdw/Computer/Shuffle/Plots/'
  filename = ('Shuffle' + str(maxNumCards) + '.pdf')
  outfile = outfilepath + filename     

  #Now plot the results.
  plotShuffle(shuffleSet, outfile)

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  main()
