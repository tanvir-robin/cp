from anytree import Node, RenderTree

# ----------- Top-Down Parse Tree for "id + id * id" ------------
def top_down_parse():
    # Start symbol
    E = Node("E")

    # E -> E + T
    E1 = Node("E", parent=E)
    plus = Node("+", parent=E)
    T = Node("T", parent=E)

    # Left E -> T
    T1 = Node("T", parent=E1)
    id1 = Node("id", parent=T1)

    # Right T -> T * F
    T2 = Node("T", parent=T)
    mul = Node("*", parent=T)
    F = Node("F", parent=T)

    id2 = Node("id", parent=T2)
    id3 = Node("id", parent=F)

    print("Top-Down Parse Tree for id + id * id:\n")
    for pre, fill, node in RenderTree(E):
        print(f"{pre}{node.name}")


# ----------- Bottom-Up Parse Tree for "id * id" ------------
def bottom_up_parse():
    # Start from input: id * id
    T = Node("T")   # final reduced form

    F1 = Node("F", parent=T)
    mul = Node("*", parent=T)
    F2 = Node("F", parent=T)

    id1 = Node("id", parent=F1)
    id2 = Node("id", parent=F2)

    print("\nBottom-Up Parse Tree for id * id:\n")
    for pre, fill, node in RenderTree(T):
        print(f"{pre}{node.name}")


# Run both
top_down_parse()
bottom_up_parse()
