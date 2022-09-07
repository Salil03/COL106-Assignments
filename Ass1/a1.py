# Stack implementation using a linked list of Nodes
# ___________________________________________________________________________

class Node:
    __slots__ = 'data', 'next'

    def __init__(self, data=None, next_node=None):
        self.data = data  # data of node
        self.next = next_node  # next node, None is end of stack


class Stack:
    __slots__ = 'head', 'length'

    def __init__(self):  # init empty stack
        self.head = Node()
        self.length = 0

    def push(self, data):  # push new node in stack
        new_node = Node(data, self.head.next)
        self.head.next = new_node
        self.length += 1

    def __len__(self):  # return length of stack
        return self.length

    def is_empty(self):  # return True if stack is empty
        return (self.length == 0)

    def top(self):  # returns top of stack without popping
        if self.is_empty():
            raise Exception("Can't get top of empty stack")
        return self.head.next.data

    def pop(self):  # returns top of stack and pops the element
        if self.is_empty():
            raise Exception("Can't pop from empty stack")
        deleted = self.head.next
        self.head.next = deleted.next
        self.length -= 1
        return deleted.data

# ____________________________________________________________________________


'''
Gets the operator from top of operator stack, then applies it to the first two elements of value stack. Finally, pushes the result back into value stack
'''


def apply_operation(value_stack, operator_stack):
    operand = operator_stack.pop()
    op1 = value_stack.pop()
    op2 = value_stack.pop()
    if operand == '+':
        value_stack.push([op1[i] + op2[i] for i in range(4)])
    elif operand == '-':
        value_stack.push([op2[0] - op1[0], op2[1] - op1[1],
                          op2[2] - op1[2], op2[3] + op1[3]])  # distance always added
    else:
        value_stack.push([op2 * op1[i] for i in range(4)])


'''
Process the next token and solve the expression using precedence rules

value_stack: stack holding numbers
operator_stack: stack holding operands
'''


def add_token(token, value_stack, operator_stack):
    if token == 'X':
        value_stack.push([1, 0, 0, 1])
    elif token == 'Y':
        value_stack.push([0, 1, 0, 1])
    elif token == 'Z':
        value_stack.push([0, 0, 1, 1])
    elif isinstance(token, int):
        value_stack.push(token)
    elif token == '(':
        operator_stack.push('(')
        value_stack.push([0, 0, 0, 0])  # add further statements to base value
    elif token == ')':
        while operator_stack.top() != '(':  # apply all operations between brackets
            apply_operation(value_stack, operator_stack)
        operator_stack.pop()
    elif token == '+' or token == '-':
        # only apply operators with higher or equal precedence till first bracket
        while not operator_stack.is_empty() and operator_stack.top() != '(':
            apply_operation(value_stack, operator_stack)
        operator_stack.push(token)
    elif token == '*':
        # only apply operators withs higher or equal precedence till first bracket
        while (not operator_stack.is_empty()) and operator_stack.top() == '*':
            apply_operation(value_stack, operator_stack)
        operator_stack.push(token)


def findPositionandDistance(P):
    value_stack = Stack()
    value_stack.push([0, 0, 0, 0])  # initial position
    operator_stack = Stack()
    length = len(P)
    i = 0
    while i < length:
        if P[i].isdigit():
            j = i
            num = 0
            # splice full number from P
            while j < length and P[j].isdigit():
                num *= 10
                num += int(P[j])
                j += 1
            # to indicate the final result after multiplication is to be added
            add_token('+', value_stack, operator_stack)
            # convert the splice to integer
            add_token(num, value_stack, operator_stack)
            # to indicate multiplication after a number
            add_token('*', value_stack, operator_stack)
            i = j
        else:
            add_token(P[i], value_stack, operator_stack)
            i += 1
    # finish remaining operations
    while not operator_stack.is_empty():
        apply_operation(value_stack, operator_stack)
    return value_stack.top()


# assert findPositionandDistance(
#     "+X+Y+X-Y-Z+X+X-Z-Z-Z-Z-Y+Y-X") == [3, 0, -5, 14]
# assert findPositionandDistance("+X2(+Y-X-Z)8(+Y)9(-Z-Z)") == [-1, 10, -20, 33]
# assert findPositionandDistance("") == [0, 0, 0, 0]
# assert findPositionandDistance("4()") == [0, 0, 0, 0]
# assert findPositionandDistance("5(4())") == [0, 0, 0, 0]
# assert findPositionandDistance("5(2(3(+X+X)))") == [60, 0, 0, 60]
# assert findPositionandDistance(
#     "+Z6(+X+Y+X-Y)9(-X+Z-X-Z8(+X+Y-Z)9(+Y-Z-X-Y4(-X+Y-X-Z+X)))") == [-339, 396, -476, 2221]
# assert findPositionandDistance(
#     "1(+X)5(+Y)41(+Z)1805(-X)3263441(-Y)10650056950805(-Z)") == [-1804, -3263436, -10650056950764, 10650060216098]
# assert findPositionandDistance("()999(+X)") == [999, 0, 0, 999]
