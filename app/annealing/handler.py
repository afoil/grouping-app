from typing import Dict, List
from annealing.get_input import extract_members_groups
from annealing.logic import annealing


def annealing_handler(s: str, n_groups: int, max_iter: int) -> str:
    members_dict, old_groups = extract_members_groups(s)
    n_members = len(members_dict)
    if not (0 < n_groups <= n_members):
        raise InvalidNumberGroupError
    new_groups, cost = annealing(n_members, n_groups, old_groups, max_iter)
    str_groups = decode(members_dict, new_groups)
    ret = make_output(str_groups)
    return ret


def decode(members_dict: Dict[str, int], groups: List[List[int]]) -> List[List[str]]:
    rev_dict: dict = {val: key for key, val in members_dict.items()}
    fn = lambda group: [rev_dict[idx] for idx in group]
    str_groups = list(map(fn, groups))
    return str_groups


def make_output(str_groups: List[List[str]]) -> str:
    ret = ""
    for idx, group in enumerate(str_groups):
        tmp_str = ", ".join(group)
        tmp_str = tmp_str.rstrip()
        tmp_str = "group" + str(idx) + " " + tmp_str + "\n"
        ret = ret + tmp_str
    ret = ret.rstrip()
    return ret


class InputError(Exception):
    pass


class InvalidNumberGroupError(InputError):
    def __str__(self):
        msg = "グループ数の数が不正です．"
        return msg
