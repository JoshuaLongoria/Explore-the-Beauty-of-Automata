
# This code is a starting point for parsing an NFA definition from a file.
# 
# 
# 
# need to add input line that allows user to input values to test if they are in the 
# accepted languages 
# the max number of states allowed is 100 
# the max number of alphabet allowed is 50 
#
#
#
#
def parse_file(filename):     
    # try/expect error implented to ensure file actually exists 
    try: 
        with open(filename, 'r') as f:
        # function updated to read lines 
        # .strip() removes whitespace/newlines
        # NOT line.startswith('#') filters out comment sections
        # .readlines() gets list of lines in file rather than on big group
            lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"Error: the File {filename} was not found.")
        return {}, []
    

        # Mapping lines to the NFA components
        # We are using .split(',') to turn comma-separated strings into a python list 
    nfa = {
        "alphabet": [a.strip() for a in lines[0].split(',')], # The set of allowed input symbols
        "states":   [s.strip() for s in lines[1].split(',')], # the set of all possible states
        "start":    lines[2].strip(),            # the single starting state 
        "finals":   [f.strip() for f in lines[3].split(',')], # the set of accepting/final states
        "delta":    {}                   # the transition function (empty for now)
    }

    test_strings = []
    # switch for reading file 
    reading_strings = False
    
    # logic for transistions (Delta) Starting from line 4 and on 
    # populates delta from line 4 and on because lines 0-3 are already defined above
    for i in range(4, len(lines)):

        # checks for seperator of NFA and input variables
        if lines[i] == "---":
            reading_strings = True
            # skips the "---" line
            continue

        if reading_strings: 
            # if the switch is ON, we add to the Test_strings
            test_strings.append(lines[i])
        else:
            # if the switch is OFF, we add the Transistion (delta)
            # Ensures the line has exactly 3 parts: [current_state, input, next_state]
            
            parts = [p.strip() for p in lines[i].split(',')]

            if len(parts) == 3:
                curr, inp, nxt = parts

            # Creates nested dictionary levels if do not exist yet 
                if curr not in nfa["delta"]:
                    nfa["delta"][curr] = {}

                if inp not in nfa["delta"][curr]:
                    # We are using a List because in an NFA it can go to multiple states on one input 
                    nfa["delta"][curr][inp] = []

            # Adding the destination staate to the list for this (state, symbol) pair
                nfa["delta"][curr][inp].append(nxt)

    return nfa, test_strings


# Using Depth-First Search to simulate the NFA Stack 
# each item in the stack is (current_state, current_char_index)
def run_nfa_stack(nfa, word):
    stack = [(nfa["start"], 0)]

    # here we are using a set to keep track of (state, index) pairs we have already visited
    # this prevents infinite loops if we have cycles 
    visited = set()

    while stack: 
        curr_state, idx = stack.pop()

        # defines end of string
        if idx == len(word):
            # tests current state - if accepting state, loop completed
            if curr_state in nfa["finals"]:
                return True
            # continues to try other paths from stack
            continue 

        # to avoid re-processing the samestate at the same position in string
        if(curr_state, idx) in visited:
            continue
        visited.add((curr_state, idx))

        # Grabs the next character to process
        char = word[idx]

        # checks if there are any transitions for the state and character
        if curr_state in nfa["delta"] and char in nfa["delta"][curr_state]:
            for next_state in nfa["delta"][curr_state][char]:
                # Push the next state and the next character index onto the stack 
                stack.append((next_state, idx + 1))

    # if the stack is empty and we never found a final state at end of string 
    return False 

# Stack Trace simulates NFA and returns the final state if it is accepted 
def run_nfa_trace(nfa, word):

    # Stack Stores: (current_state, Char_index, Path_taken)
    stack = [(nfa["start"], 0, [nfa["start"]])]

    # while loop to iterate through stack 
    # just like while loop that iterates through .txt file 
    while stack: 
        curr_state, idx, path = stack.pop()

        # checks if we reached end of string
        if idx == len(word):
            if curr_state in nfa["finals"]:
                # returns successful path ("success")
                return True, path 
            continue
        
        char = word[idx]

        if curr_state in nfa["delta"] and char in nfa["delta"][curr_state]:
            for next_state in nfa["delta"][curr_state][char]:
                # creates a new path list for specific branch
                new_path = path + [next_state]
                stack.append((next_state, idx + 1, new_path))

    return False, []

# User I/O loop used to run through tracing logic and 
# if valid we are appending it to the source .txt file and the stack display image on the output 
# this will store all the accepted inputs in the .txt file and display image.


#(4/9) This function allows the user to input a string to test against the NFA.
#If the string is accepted, it updates the NFA's record of accepted strings and appends the string to the source .txt file. 
# The function continues to prompt the user for input until they enter an empty string, at which point it exits.
def process_user_input(nfa, filename):

    user_string = input("Enter a string to test: ").strip()

    while True:  
        if user_string =="":
            print("Bye bye.")
            break

        accepted, trace_result = run_nfa_trace(nfa, user_string)

        if accepted: 
            print(f"String: '{user_string}' is accepted.")

            # updates the dictionary's record of accepted strings
            if 'accepted_list' not in nfa:
                nfa['accepted_list'] = []
            nfa['accepted_list'].append(user_string)

            # saves accepted input value to .txt file
            with open(filename, 'a') as f:
                f.write(f"\n{user_string}")

            print("File and stack updated.")
        else: 
            print(f"String: '{user_string}' is not valid for this NFA")

        user_string = input("Please input another string: ").strip()

# --- MAIN Execution Block ---
if __name__ == "__main__":
    # builds the NFA 
    filename = input("Please input the file name: ")
    nfa, test_strings = parse_file(filename)

    # runs the test 
    print(f"\n{'String':<10} | {'Result':<10} | {'Trace Path'}")
    print("-" * 60)

    for s in test_strings: 

        # calls the Trace functions 
        accepted, path = run_nfa_trace(nfa, s)

        # displays status of NFA (ACCEPTED/REJECTED)
        if accepted: 
            # provides visual trace element ['q0', 'q1'] into "q0 -> q1"
            trace_display = " -> ".join(path)
            print(f"{s:<12} | ACCEPT       | {trace_display}")

        # rejected paths show "No Path Found"
        else:
            print(f"{s:<12} | REJECT       | No path found")

    # calls the user i/o function and allows the user to input a string
    # only runs once and will need to be re-ran to input a new string 
    # still need to figure out how to implement multiple entries for user
    
    success = process_user_input(nfa, filename)

    if success: 
        print("workflow complete.")
        