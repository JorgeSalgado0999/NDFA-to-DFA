__author__ = "Jorge Salgado A01636629, Fernando Muñoz Herrada A0"
__date__ = "October 15"
__version__ = "2.0"

# This program will have the next functions:
# 1) Read a .txt file to create a NDFA
# 2) from the same .txt file verify if the input is valid for that NDFA for this we have the next funtcions:
#   a) transition function -> return me where do i get from q0 with a for example
#   b) union -> return the union of two arrays WITHOUT duplicates
#   c) extended transition function -> main function that has the recursion®®

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
new_initial_state = ""
new_final_states = []
new_transition_table = {}


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
    try: returning = transition_table[state].get(character)
    except: returning = []

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


# This is the main function that has the recursion to verify if the input is valid
def extended_transition_function(state, word):
    print("The string is: ", word)
    if len(word) == 0:  # we check if is an empty string
        print(state)
        return state
    elif len(word) == 1:  # we check if is the base case
        print("\nThe last character: ", word)
        trans = transition_table[state].get(word)
        return trans
    else:  # this is the recursion case were all the operations are made
        return_states = extended_transition_function(state,
                                                     word[0:-1])  # This calls itself with all except the last character
        if return_states is None: return {}  # if the return_states are None that means that there are no path to that character

        char_verify = word[-1]  # we check with the last character
        print("\ncharacter to review: ", char_verify)
        print("return states: ", return_states)

        final_states = []
        for state_temp in return_states:  # cycle to travel each value of the return_states
            container = transition_function(state_temp, char_verify)  # we save the values in a container variable

            print("state_temp: ", state_temp, "word: ", char_verify)
            print("its transition is: ", container)

            if container is not None: final_states = union(final_states, container)

        print("final states: ", final_states)
        return final_states


# This function recive the states and check if the string is valid or invalid
def solver(stateX, stringX):
    print("\nProcess starts... \n")
    result = extended_transition_function(stateX, stringX)
    print("\nfinal result: ", result)
    # Here we made the interesection with the result and the final states
    intersection_result = intersection(final_states, result)
    # Here we check if the string is valid
    if len(result) == 0:
        print("The string: {} is not valid\n".format(stringX))
    elif len(intersection_result) > 0:
        print("The string: {} is valid\n".format(stringX))
    else:
        print("The string: {} is not valid\n".format(stringX))


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

    #print("new states: ", new_states)
    #print("support states: ", support_states)
    #print("queue: ", queue)

    for item in queue:
        #print("\nevaluando:", item)
        support_queue = []
        for letter in alphabet:
            #print("con: ", letter)
            support_queue = []
            for stateX in support_states.get(item):
                if transition_function(stateX, letter) is not None:
                    support_queue = union(support_queue, transition_function(stateX, letter))

            verify = False
            for key in support_states:
                if np.array_equal(support_states.get(key), support_queue):
                    #print("ya existe uno asi")
                    verify = True
                    if new_states.get(item) is None:
                        new_states[item] = {}
                        new_states[item][letter] = key
                    else:
                        new_states[item][letter] = key

            if not verify:
               i2 += 1
               new_stateX = str("q" + str(i2))
               queue.append(new_stateX)
               support_states[new_stateX] = support_queue
               if new_states.get(item) is None:
                   new_states[item] = {}
                   new_states[item][letter] = new_stateX
               else:
                   new_states[item][letter] = new_stateX



    print("the DFA dictionary is: ", new_states)
    print("each state is conformed by: ", support_states)
    #print("queue: ", queue)


    return 0

# This function print the global values
def print_globals():
    var_globals = globals()
    # print("\nThe global variables are: ")
    # print("The states are: {}".format(var_globals['states']))
    # print("The alphabet is: {}".format(var_globals['alphabet']))
    # print("The initial state is: {}".format(var_globals['initial_state']))
    # print("The final states are: {}".format(var_globals['final_states']))
    print("The NDFA dictionary is: {}".format(var_globals['transition_table']))


# This is the main function that initializes everything
def main():
    # We call the global vars
    global file, string_to_check
    file = "test3.txt" #input("Give the name of the file to read: ")
    # string_to_check = input("Give the string you want to verify: ")
    # We call the function for reading the document
    read_document(file)
    # We call  the function to print the global vars
    print_globals()
    # We call the function to check if the string is valid or not
    # solver(initial_state, string_to_check)
    # This cycle is to ask for the user for new strings to check
    conversion()


# We call main to starts our program
main()