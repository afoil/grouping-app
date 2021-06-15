from copy import deepcopy
from itertools import product
from math import exp
from typing import List, Tuple
import numpy as np


def make_groups(members: List[int], n_groups: int) -> List[List[int]]:
    n_members_per_group = len(members) // n_groups
    new_groups = [
        members[n_members_per_group * i : n_members_per_group * (i + 1)]
        for i in range(n_groups)
    ]
    # 余りの処理
    res_n_members = len(members) % n_groups
    if res_n_members > 0:
        res_members = members[-1 * res_n_members :]
        new_groups[-1] = new_groups[-1] + res_members
    return new_groups


def make_state(n_members: int, groups: List[List[int]]) -> np.ndarray:
    state = np.zeros((n_members, n_members))
    for group in groups:
        for member0, member1 in product(group, repeat=2):
            state[member0][member1] = 1
    # 対角線を0に
    for i in range(n_members):
        state[i][i] = 0
    return state


def calc_cost(tmp_state: np.ndarray, old_state: np.ndarray) -> float:
    cost_ary = np.multiply(tmp_state, old_state)
    cost = (np.sum(cost_ary)) / 2
    return cost


def calc_prob(T: float, diff_cost: float) -> float:
    prob = 1.0
    if diff_cost > 0:
        prob = exp(-diff_cost / T)
    return prob


def to_be_moved(T: float, diff_cost: float) -> bool:
    obs = np.random.rand()
    prob = calc_prob(T, diff_cost)
    return obs > 1 - prob


def annealing(
    n_members: int, n_groups: int, old_groups: List[List[int]], max_iter: int
) -> Tuple[List[List[int]], float]:
    init_members = [i for i in range(n_members)]
    old_state = make_state(n_members, old_groups)
    tmp_members = init_members
    tmp_groups = make_groups(tmp_members, n_groups)
    tmp_state = make_state(n_members, tmp_groups)
    tmp_cost = calc_cost(tmp_state, old_state)
    T_0 = n_members ** 2
    T_1 = 1
    for epoch in range(max_iter):
        candidates0, candidates1 = np.random.choice(n_members, 2, replace=False)
        new_members = deepcopy(tmp_members)
        new_members[candidates0], new_members[candidates1] = (
            new_members[candidates1],
            new_members[candidates0],
        )
        new_groups = make_groups(new_members, n_groups)
        new_state = make_state(n_members, new_groups)
        new_cost = calc_cost(new_state, old_state)
        T_t = ((T_0) ** ((max_iter - epoch) / max_iter)) * (
            (T_1) ** ((epoch) / max_iter)
        )
        diff_cost = new_cost - tmp_cost
        if to_be_moved(T_t, diff_cost):
            tmp_members = new_members
            tmp_groups = new_groups
            tmp_state = new_state
            tmp_cost = new_cost
    return make_groups(tmp_members, n_groups), tmp_cost
