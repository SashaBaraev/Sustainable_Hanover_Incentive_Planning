import numpy as np
from decision_tree.model import StnblHnvrDT



initial_distribution = np.array(
    [492, 143, 2288, 55, 112, 375])  # NonEnrolled, Granite, GranitePlus, Clean50, Clean100, Solar

RE = np.array(
    [[0.9794468379337992, 0.0012857337670244854, 0.01783536232757267, 0.0005151557269522573, 0.0010770457611853819],
     [0.016645299088636416, 0.9673037878319581, 0.030163195222732836, 0.0008713586781490621, 0.0018217937836929544],
     [0.01664529908863642, 0.019009008067952443, 0.9487227417359976, 0.010480509235103266, 0.0219478764774796],
     [0.016645299088636413, 0.001306386752237579, 0.018128727858840028, 0.9481411464149603, 0.032583874490495615],
     [0.016645299088636423, 0.0012785472588218356, 0.017743051745109633, 0.000512211648437835, 0.9806263248641649]]
    )

PV = np.array([[0.99367, 0.00633],
                          [0.0, 1.0]])

PV_solarize = np.array([[0.98478, 0.01522],
                           [0.0, 1.0]])


tree = StnblHnvrDT(town_distribution=initial_distribution,
                   re=RE, pv=PV,
                   re_incentive=.3,
                   re_price_plasticity=1,
                   pv_incentive=0.1,
                   pv_price_plasticity=.71)

print(tree.incentivized_pv.round(4))

# policies = {}
# i = 0
# for policy in tree.decision_tree.children[-3].children:
#     print(policy.name)
#     eus = []
#     for u, p in zip(policy.children, policy.probabilities):
#         print('  ', u.name, round(p, 5), u.expected_utility, round(p* u.expected_utility, 5))
#         eus.append(round(p * u.expected_utility, 5))
#
#     policies[i] = np.array(eus)
#     i+=1
