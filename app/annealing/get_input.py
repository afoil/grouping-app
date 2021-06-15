from functools import reduce
from operator import add
from typing import Dict, List, Tuple


def extract_groups(s: str) -> List[List[str]]:
    s = s.rstrip()
    raw_groups = s.split("\n")
    groups = [raw_group.split(",") for raw_group in raw_groups]
    stripped_groups = list(
        map(lambda group: list(map(lambda member: member.strip(), group)), groups)
    )
    return stripped_groups


def make_members_dict(str_groups: List[List[str]]) -> Dict[str, int]:
    members_dict = {member: idx for idx, member in enumerate(reduce(add, str_groups))}
    return members_dict


def make_int_groups(
    str_groups: List[List[str]], members_dict: Dict[str, int]
) -> List[List[int]]:
    fn = lambda group: [members_dict[member] for member in group]
    int_groups = list(map(fn, str_groups))
    return int_groups


def extract_members_groups(s: str) -> Tuple[Dict[str, int], List[List[int]]]:
    str_groups = extract_groups(s)
    members_dict = make_members_dict(str_groups)
    int_groups = make_int_groups(str_groups, members_dict)
    return members_dict, int_groups
