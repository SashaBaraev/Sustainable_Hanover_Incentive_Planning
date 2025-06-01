from .nodes import *

class StnblHnvrDT:
    def __init__(self,
                 town_distribution, re, pv,
                 state_names=['NonEn', 'Granite', 'GranitePlus', 'Clean50', 'Clean100', 'Solar'],
                 re_incentive=.3, re_price_plasticity=1.0,
                 pv_incentive=.1, pv_price_plasticity=.71):
        self.state_names = state_names
        self.town_distribution = town_distribution
        self.re = re
        self.re_incentive = re_incentive
        self.re_price_plasticity = re_price_plasticity
        self.pv = pv
        self.pv_incentive = pv_incentive
        self.pv_price_plasticity = pv_price_plasticity

    def incentivize_transition_matrix(self, transition_matrix, incentive, price_plasticity):
        adjusted_matrix = transition_matrix.copy()
        if adjusted_matrix.shape[0] > 2:
            for i in range(len(adjusted_matrix) - 1):
                incentive_state = adjusted_matrix[i, i + 1:].sum()
                adjusted_matrix[i, i + 1:] = 0
                adjusted_matrix[i, -1] = incentive_state

        incentive_boost = (1 + incentive * price_plasticity)
        adjusted_matrix[:-1, -1] *= incentive_boost

        adjusted_matrix[:-1, :-1] /= adjusted_matrix[:-1, :-1].sum(axis=1).reshape(-1, 1)
        adjusted_matrix[:-1, :-1] *= (1 - adjusted_matrix[:-1, -1]).reshape(-1, 1)

        return adjusted_matrix

    @property
    def incentivized_re(self):
        return self.incentivize_transition_matrix(self.re, self.re_incentive, self.re_price_plasticity)

    @property
    def incentivized_pv(self):
        return self.incentivize_transition_matrix(self.pv, self.pv_incentive, self.pv_price_plasticity)

    @property
    def decision_tree(self):
        utilities = [25., 25., 33., 50., 100., 100.]  # Utilities for each state
        utility_nodes = {}
        for state, utility in zip(self.state_names, utilities):
            utility_nodes[state] = UtilityNode(name=f'{state} Utility', utility=utility)

        default_solar_p = ChanceNode(name='Default Solar Adoption Probability',
                                     probabilities=self.pv[0, :],
                                     children=[utility_nodes['NonEn'], utility_nodes['Solar']])

        c100_transition = ChanceNode(name='Clean100 Transition',
                                      probabilities=self.re[-1, :],
                                      children=[default_solar_p, *list(utility_nodes.values())[1:-1]])

        init_states = {}

        for i, init_state in enumerate(self.state_names[:-2]):
            init_states[init_state] = DecisionNode(name=f'{init_state} Incentivization',
                                                   children=[
                                                       ChanceNode(name=f'{init_state} Default Transition',
                                                                  probabilities=self.re[i, :],
                                                                  children=[default_solar_p,
                                                                            *list(utility_nodes.values())[1:-1]]),
                                                       ChanceNode(name=f'{init_state} Incentivized Transition',
                                                                  probabilities=self.incentivized_re[i, :],
                                                                  children=[default_solar_p,
                                                                            *list(utility_nodes.values())[1:-1]])
                                                   ])


        init_states['NonEn'].add_child(ChanceNode(name='NonEn SolarRebate Transition',
                                                  probabilities=self.incentivized_pv[0, :],
                                                  children=[
                                                        ChanceNode(name='NonEn Default Transition',
                                                                   probabilities=self.re[0, :],
                                                                   children=list(utility_nodes.values())[:-1],
                                                                   ),
                                                        utility_nodes['Solar']
                                                  ])
                                       )

        init_states['Clean100'] = c100_transition
        init_states['Solar'] = utility_nodes['Solar']

        decision_tree = ChanceNode(name='Initial State',
                                   probabilities=self.town_distribution / self.town_distribution.sum(),
                                   children=list(init_states.values()))

        return decision_tree

