
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
    with open(filename, 'r') as f:
        content = f.read()
    
    tokens = tokenize(content)   # ← calls tokenize from inside parse_file
    
    nfa = {
        "alphabet": [],
        "states":   [],
        "start":    "",
        "finals":   [],
        "delta":    {}
    }
    
    test_strings = []
    
    return nfa, test_strings

nfa, test_strings = parse_file("proj-1-machine.txt")

#Test the tokenizer separately
print("tokens worked!")
print("test strings:", test_strings)
print("nfa:", nfa) 