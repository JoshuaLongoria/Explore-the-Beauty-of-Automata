
# This code is a starting point for parsing an NFA definition from a file.

# The `tokenize` function breaks the file content into meaningful tokens.
def tokenize(content):        # define this FIRST, this is
    tokens = []               #characters that are not whitespace or special characters are accumulated into a "current" token, which is added to the tokens list when a delimiter is encountered.  
    current = ""                # The function iterates through each character in the content, checking for whitespace and special characters. When it encounters a delimiter, it adds the current token to the list of tokens and resets the current token. Finally, it returns the list of tokens.    
    
    for char in content:
        if char in (' ', '\n', '\t'):
            if current:
                tokens.append(current)
                current = ""
        elif char in ('(', ')', ','):
            if current:
                tokens.append(current)
                current = ""
            tokens.append(char)
        else:
            current += char
    
    if current:    #
        tokens.append(current)
    
    return tokens

# The `parse_file` function reads the file, tokenizes its content, and initializes the NFA structure and test strings.
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
        
        tokens = tokenize(content)   # ← calls tokenize from inside parse_file

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


# --- MAIN Execution Block ---
if __name__ == "__main__":
    # builds the NFA 
    nfa, test_strings = parse_file("proj-1-machine.txt")

    #defines strings to test are read from file 
    #Test the tokenizer separately
    print("tokens worked!")
    print("test strings:", test_strings)
    print("nfa:", nfa) 

    # runs the test 
    print(f"\n{'String':<10} | {'Result':<10} | {'Traace Path'}")
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
        