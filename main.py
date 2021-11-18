__author__ = "Jorge Salgado A01636629, Fernando Muñoz Herrada A0"
__date__ = "October 15"
__version__ = "2.0"

# This program will have the next functions:
# 1) Read a .txt file to create a NDFA and then give the equivalent DFA
# 2) from the same .txt file verify if the input is valid for that NDFA for this we have the next funtcions:
#   a) transition function -> return me where do i get from q0 with a for example
#   b) union -> return the union of two arrays WITHOUT duplicates
#   c) conversor function that makes all the process

import sys
import re
import numpy as np

# Global variables for the correct funcionality of the program
states = []
alphabet = []
initial_state = ""
final_states = []
transition_table = {}

string_to_check = ""
file = ""

new_states = {}
support_states = {}
queue = []
new_final_states = []


# This function will read the .txt and save all the values into the correct variables and create the dictonaries
def read_document(file):
    file = open(file, "r")  # we open the file
    var_globals = globals()  # we call the global variables ls into array

    # In this next lines we are going  to assume that the textfile is correct so we read the first 4 lines
    var_globals['states'] = file.readline().replace("\n", "").split(",")
    var_globals['alphabet'] = file.readline().replace("\n", "").split(",")
    var_globals['initial_state'] = file.readline().replace("\n", "")
    var_globals['final_states'] = file.readline().replace("\n", "").split(",")
    # This cycle is to create the dictionarie
    for line in file:
        line = line.replace("\n", "")
        line = re.split(',|=>', line)

        if var_globals['transition_table'].get(line[0]) is None:
            var_globals['transition_table'][line[0]] = {}
            var_globals['transition_table'][line[0]][line[1]] = line[2:]
        else:
            var_globals['transition_table'][line[0]][line[1]] = line[2:]


# This function will return the states where you can go from state with character
def transition_function(state, character):
    global transition_table
    # This try and except it's to validate that the state exist and the program doesnt break
    try:
        returning = transition_table[state].get(character)
    except:
        returning = []

    return returning


# This function will return the union of two arrays WITHOUT duplicates
def union(state1, state2):
    states = state1 + state2
    return list(dict.fromkeys(states))


# This function is to make the intersection between two arrays
def intersection(state1, state2):
    result = []
    for i in state1:
        if i in state2:
            result.append(i)
    return result


def conversion():
    # For the first step we create the n states based on the alphabet with the transictions of q0
    print("\nNDFA -> DFA...")
    i2 = 0
    new_state = str("q" + str(i2))
    for letter in alphabet:
        if transition_function(new_state, letter) is not None:
            i2 = i2 + 1
            new_state2 = str("q" + str(i2))
            queue.append(new_state2)
            support_states[new_state2] = transition_function(new_state, letter)
            if new_states.get(new_state) is None:
                new_states[new_state] = {}
                new_states[new_state][letter] = new_state2
            else:
                new_states[new_state][letter] = new_state2

    # After we created the queue we iterate over it so we can create the DFA
    for item in queue:
        support_queue = []
        for letter in alphabet:  # For each value we iterate over the alphabet
            # print("con: ", letter)
            support_queue = []
            for stateX in support_states.get(item):  # here we find the values for the set of values in each state
                if transition_function(stateX, letter) is not None:
                    support_queue = union(support_queue, transition_function(stateX, letter))

            verify = False
            for key in support_states:  # we try to find if the values obtained match with some existing set
                if np.array_equal(support_states.get(key), support_queue):
                    # print("ya existe uno asi")
                    verify = True
                    if new_states.get(item) is None:
                        new_states[item] = {}
                        new_states[item][letter] = key
                    else:
                        new_states[item][letter] = key

            if not verify:  # if there is not match we create a new set and new state
                i2 += 1
                new_stateX = str("q" + str(i2))
                queue.append(new_stateX)
                support_states[new_stateX] = support_queue
                if new_states.get(item) is None:
                    new_states[item] = {}
                    new_states[item][letter] = new_stateX
                else:
                    new_states[item][letter] = new_stateX

    # Finally we Determinate the final states
    if "q0" in final_states:
        new_final_states.append("q0")

    for key in support_states.keys():
        for final in final_states:
            if final in support_states.get(key):
                if key not in new_final_states:
                    new_final_states.append(key)


# This is the main function that initializes everything
def main():
    # We call the global vars
    global file, string_to_check
    file = input("Give the name of the file to read: ")
    # string_to_check = input("Give the string you want to verify: ")
    # We call the function for reading the document
    read_document(file)
    # We call  the function to print the global vars
    # This cycle is to ask for the user for new strings to check
    print("The NDFA dictionary is: {}".format(transition_table))
    conversion()
    print("The DFA dictionary is: ", new_states)
    print("Each state is conformed by: ", support_states)
    print("The new final states are: ", new_final_states)

# We call main to starts our program
main()
