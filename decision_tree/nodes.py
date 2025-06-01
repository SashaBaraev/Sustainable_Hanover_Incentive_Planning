class Node:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children

class DecisionNode(Node):
    def __init__(self, name, children=None):
        super().__init__(name, children)
        self.children = children if children is not None else []

    def add_child(self, child):
        self.children.append(child)

    @property
    def expected_utility(self):
        return max(child.expected_utility for child in self.children)

class ChanceNode(Node):
    def __init__(self, name, probabilities, children=None):
        super().__init__(name, children)
        self.probabilities = probabilities

    def add_child(self, child, p):
        self.children.append(child)
        self.probabilities.append(p)

    @property
    def expected_utility(self):
        return sum(child.expected_utility * prob for child, prob in zip(self.children, self.probabilities))

class UtilityNode(Node):
    def __init__(self, name, utility):
        super().__init__(name)
        self.utility = utility

    @property
    def expected_utility(self):
        return self.utility  # In a real scenario, this would be calculated based on the probabilities of reaching this node
