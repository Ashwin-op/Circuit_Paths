import collections

from tt import BooleanExpression, to_primitives


# Function to print information
def printInfo():
    print("\t\t\tCombinational Circuit Paths")

    print("-" * 70)

    print("Available operators: and, iff, impl, nand, nor, not, nxor, or, xnor, xor")
    print("(You can use parentheses for indicating precedence)\n")
    print("Example: A and B or not C xor D")

    print("-" * 70, end="\n")


def getInput():
    # Get boolean expression string
    be = str(input("Enter a boolean expression: "))

    # Check if the string is a valid Boolean Expression
    exprIn = None
    try:
        exprIn = to_primitives(BooleanExpression(be))
    except:
        print("Error: Not a valid boolean expression")
        exit(0)

    return exprIn


# Return all the possible paths from root to all the leafs
# bfs + queue
def treePaths(root):
    res, queue = [], collections.deque([(root, "")])
    while queue:
        node, ls = queue.popleft()
        if not node.l_child and not node.r_child:
            res.append(ls + str(node.symbol_name))
        if node.l_child:
            queue.append((node.l_child, ls + str(node.symbol_name) + "->"))
        if node.r_child:
            queue.append((node.r_child, ls + str(node.symbol_name) + "->"))
    return [f"OUTPUT->{i}" for i in res]


if __name__ == "__main__":
    # Print initial information
    printInfo()

    # Get the boolean expression from the user
    expr = getInput()

    # Print the tree
    print(expr.tree)
    print("-" * 70)

    # Print all paths from root to leaf
    print("All possible paths are:")
    for temp in treePaths(expr.tree):
        path = temp.split("->")
        path.reverse()
        print(*path, sep='->')
