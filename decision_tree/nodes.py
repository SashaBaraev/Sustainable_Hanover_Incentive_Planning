class Node:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children if children is not None else []

    @property
    def expected_utility(self):
        return 0 # This should be overridden in subclasses

    def visualize_decision_tree(self):
        def visualize_node(node, level=0, p=''):
            print(f"{level * '      '}{p} {type(node).__name__}: {node.name} - {round(node.expected_utility, 2)}")
            if node.children is not None:
                for i, child in enumerate(node.children):
                    p = round(node.probabilities[i], 4) if isinstance(node, ChanceNode) else ''
                    visualize_node(child, level=level + 1, p=p)
        visualize_node(self)

class DecisionNode(Node):
    def __init__(self, name, children=None):
        super().__init__(name, children)
        self.children = children if children is not None else []

    def add_children(self, *children):
        for child in children:
            self.children.append(child)

    @property
    def expected_utility(self):
        return max(child.expected_utility for child in self.children)

class ChanceNode(Node):
    def __init__(self, name, probabilities=None, children=None):
        super().__init__(name, children)
        self.probabilities = probabilities if probabilities is not None else []

    def add_children(self, *children, probabilities):
        for child in children:
            self.children.append(child)
        if isinstance(probabilities, list):
            self.probabilities.extend(probabilities)
        else:
            self.probabilities.append(probabilities)

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
