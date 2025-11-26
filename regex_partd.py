#!/usr/bin/env python3
"""
regex_partd.py

Builds a CFG equivalent to the regular expression

    R = 0 ∪ 10(000)*   over Σ = {0,1}

using the CFG operations implemented for Problem 5:
- union_cfg
- concat_cfg
- star_cfg

The resulting CFG is printed to stdout in the same textual format as the
other programs.
"""

from cfg_utils import CFG
from cfg_operations import union_cfg, concat_cfg, star_cfg


def make_cfg_for_0() -> CFG:
    """
    Grammar for the language { "0" } over Σ = {0,1}.

    S0 -> 0
    """
    nonterminals = {"S0"}
    terminals = {"0", "1"}  # full alphabet, even though we only use '0'
    start = "S0"
    productions = {
        "S0": [["0"]]
    }
    return CFG(nonterminals=nonterminals,
               terminals=terminals,
               start=start,
               productions=productions)


def make_cfg_for_10() -> CFG:
    """
    Grammar for the single string "10" over Σ = {0,1}.

    S10 -> 1 A10
    A10 -> 0
    """
    nonterminals = {"S10", "A10"}
    terminals = {"0", "1"}
    start = "S10"
    productions = {
        "S10": [["1", "A10"]],
        "A10": [["0"]],
    }
    return CFG(nonterminals=nonterminals,
               terminals=terminals,
               start=start,
               productions=productions)


def make_cfg_for_000() -> CFG:
    """
    Grammar for the single string "000" over Σ = {0,1}.

    S000 -> 0 B000
    B000 -> 0 C000
    C000 -> 0
    """
    nonterminals = {"S000", "B000", "C000"}
    terminals = {"0", "1"}
    start = "S000"
    productions = {
        "S000": [["0", "B000"]],
        "B000": [["0", "C000"]],
        "C000": [["0"]],
    }
    return CFG(nonterminals=nonterminals,
               terminals=terminals,
               start=start,
               productions=productions)


def build_regex_cfg() -> CFG:
    """
    Build a CFG for R = 0 ∪ 10(000)* using the operations from Problem 5:

        - G0        for {0}
        - G10       for {"10"}
        - G000      for {"000"}
        - star_cfg  for (000)*
        - concat_cfg for 10(000)*
        - union_cfg for 0 ∪ 10(000)*
    """
    # {0}
    G0 = make_cfg_for_0()

    # "10"
    G10 = make_cfg_for_10()

    # "000"
    G000 = make_cfg_for_000()

    # (000)*
    G000_star = star_cfg(G000)

    # 10(000)*
    G10_000_star = concat_cfg(G10, G000_star)

    # 0 ∪ 10(000)*
    regex_cfg = union_cfg(G0, G10_000_star)
    return regex_cfg


def print_cfg(cfg: CFG) -> None:
    """
    Print the CFG in the same format used elsewhere:
    Nonterminals, Terminals, Start, Productions.
    """
    print("Nonterminals: " + ",".join(sorted(cfg.nonterminals)))
    print("Terminals: " + ",".join(sorted(cfg.terminals)))
    print("Start: " + cfg.start)
    print("Productions:")
    for left in sorted(cfg.productions.keys()):
        alts = []
        for rhs in cfg.productions[left]:
            if rhs == ["ε"]:
                alts.append("ε")
            else:
                alts.append(" ".join(rhs))
        print(f"{left} -> " + " | ".join(alts))


def main() -> None:
    cfg = build_regex_cfg()
    print_cfg(cfg)


if __name__ == "__main__":
    main()
