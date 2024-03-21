"""
Question 2: Algorithm
"""

def check_brackets(input_str):
    stack = []
    output = ""

    for char in input_str:
        # iterate through each character in the input string
        if char == '(':
            # store the index at which the bracket is opened
            # if by the end it is not popped out, we can directly insert x
            # based on this index
            stack.append(len(output))
            output += ' '
        elif char == ')':
            # if character is a closing bracket
            if stack:
                # if stack is not empty, we closed the brackets correctly
                stack.pop()
                output += ' '
            else:
                # if stack is empty, this closing bracket is misplaced
                output += '?'
        else:
            # other characters that are not brackets are ignored
            output += ' '

    for index in stack:
        # insert x at positions, stored in the stack
        output = output[:index] + 'x' + output[index:]

    return output

test_cases = [
    "bge)))))))))",
    "((IIII))))))",
    "()()()()(uuu",
    "))))UUUU((()"
]

def main():
    for test_case in test_cases:
        result = check_brackets(test_case)
        print(test_case)
        print(result)
    
if __name__ == "__main__":
    main()