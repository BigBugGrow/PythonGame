# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 08:12:47 2015

@author: DongAn
"""

# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

num_range = 100
secret_number = 0
remaining_count = 0
# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global num_range
    num_range = 100
    global secret_number 
    secret_number = random.randrange(0,num_range)
    # remove this when you add your code    
  
# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global remaining_count
    remaining_count = 7
    new_game()
    print "New game. Range is from 0 to 100"
    print "Number of remaining guesses is 7"
    print
    # remove this when you add your code    
    

def range1000():
    # button that changes the range to [0,1000) and starts a new game 
    global remaining_count
    remaining_count = 10
    global num_range
    num_range = 1000
    global secret_number
    secret_number = random.randrange(0,num_range)
    print "New game. Range is from 0 to 1000"
    print "Number of remaining guesses is 10"
    print
    
    
def input_guess(guess):
    # main game logic goes here	
    # remove this when you add your code
    global remaining_count
    global num_range
    global secret_number
    remaining_count = remaining_count - 1
    guess = int(guess)

    print "guess was",guess
    print "Number of remaining guesses is",remaining_count
    if (guess > secret_number):
        print "Lower!"
    elif (guess < secret_number):
        print "Higher!"
    else:
        print "Correct!"
    
    print
    
    if(remaining_count <= 0 and num_range == 100):
        range100()
    if(remaining_count <= 0 and num_range == 1000):
        range1000()
        
    
    
    

    
# create frame
f = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements and start frame
f.add_button("Range is [0,100)", range100, 200)
f.add_button("Range is [0,1000)", range1000, 200)
f.add_input("Enter a guess", input_guess, 200)

# call new_game 
new_game()   
range100()


# always remember to check your completed program against the grading rubric
