#!/usr/bin/env python3
"""
cfg_operations.py

Implements CFG operations needed for Problem 5:
- Union of two CFGs
- Concatenation of two CFGs
- Kleene star of one CFG
- A placeholder "part d" operation built out of the above

Each CFG is represented using the CFG class from cfg_utils.py.
"""

from dataclasses import dataclass
from typing import Dict, List, Set, Tuple
from cfg_utils import CFG


def _rename_cfg(cfg: CFG, prefix: str) -> CFG:
    """
    Return a renamed copy of cfg, where every nonterminal is prefixed
    to avoid collisions when combining grammars.
    Terminals remain unchanged.
    """
    new_nonterminals: Set[str] = set()
    new_productions: Dict[str, List[List[str]]] = {}

    mapping: Dict[str, str] = {}
    for A in cfg.nonterminals:
        mapping[A] = prefix + A
        new_nonterminals.add(mapping[A])

    for A, rhss in cfg.productions.items():
        new_A = mapping[A]
        for rhs in rhss:
            new_rhs: List[str] = []
            for sym in rhs:
                if sym in cfg.nonterminals:
                    new_rhs.append(mapping[sym])
                else:
                    new_rhs.append(sym)
            new_productions.setdefault(new_A, []).append(new_rhs)

    new_start = mapping[cfg.start]

    return CFG(
        nonterminals=new_nonterminals,
        terminals=set(cfg.terminals),
        start=new_start,
        productions=new_productions,
    )


def union_cfg(G1: CFG, G2: CFG) -> CFG:
    """
    Build a CFG for L(G1) ∪ L(G2).
    """
    G1r = _rename_cfg(G1, "G1_")
    G2r = _rename_cfg(G2, "G2_")

    new_nonterminals = set(G1r.nonterminals) | set(G2r.nonterminals)
    new_terminals = set(G1r.terminals) | set(G2r.terminals)
    new_productions: Dict[str, List[List[str]]] = {}

    # Copy productions
    for A, rhss in G1r.productions.items():
        new_productions.setdefault(A, []).extend(rhss)
    for A, rhss in G2r.productions.items():
        new_productions.setdefault(A, []).extend(rhss)

    # New start symbol
    new_start = "S_union"
    while new_start in new_nonterminals:
        new_start = "_" + new_start
    new_nonterminals.add(new_start)
    new_productions[new_start] = [[G1r.start], [G2r.start]]

    return CFG(
        nonterminals=new_nonterminals,
        terminals=new_terminals,
        start=new_start,
        productions=new_productions,
    )


def concat_cfg(G1: CFG, G2: CFG) -> CFG:
    """
    Build a CFG for L(G1) · L(G2) (concatenation).
    """
    G1r = _rename_cfg(G1, "G1_")
    G2r = _rename_cfg(G2, "G2_")

    new_nonterminals = set(G1r.nonterminals) | set(G2r.nonterminals)
    new_terminals = set(G1r.terminals) | set(G2r.terminals)
    new_productions: Dict[str, List[List[str]]] = {}

    # Copy productions
    for A, rhss in G1r.productions.items():
        new_productions.setdefault(A, []).extend(rhss)
    for A, rhss in G2r.productions.items():
        new_productions.setdefault(A, []).extend(rhss)

    # New start symbol for concatenation
    new_start = "S_concat"
    while new_start in new_nonterminals:
        new_start = "_" + new_start
    new_nonterminals.add(new_start)
    new_productions[new_start] = [[G1r.start, G2r.start]]

    return CFG(
        nonterminals=new_nonterminals,
        terminals=new_terminals,
        start=new_start,
        productions=new_productions,
    )


def star_cfg(G: CFG) -> CFG:
    """
    Build a CFG for L(G)* (Kleene star).
    We allow ε via S_star -> ε.
    """
    Gr = _rename_cfg(G, "G_")

    new_nonterminals = set(Gr.nonterminals)
    new_terminals = set(Gr.terminals)
    new_productions: Dict[str, List[List[str]]] = {}

    # Copy productions
    for A, rhss in Gr.productions.items():
        new_productions.setdefault(A, []).extend(rhss)

    # New start symbol
    new_start = "S_star"
    while new_start in new_nonterminals:
        new_start = "_" + new_start
    new_nonterminals.add(new_start)

    # S_star -> ε | S_star Gr.start
    new_productions[new_start] = [["ε"], [new_start, Gr.start]]

    return CFG(
        nonterminals=new_nonterminals,
        terminals=new_terminals,
        start=new_start,
        productions=new_productions,
    )


def part_d_example_cfg(G1: CFG, G2: CFG) -> CFG:
    """
    Placeholder example for "part d" using the basic operations.
    Since the exact question is exam-specific, here we show how to build
    a CFG for (L(G1) ∪ L(G2))* as an example.

    You can modify this construction to match whatever language was
    actually required for part (d) of your exam.
    """
    union = union_cfg(G1, G2)
    starred = star_cfg(union)
    return starred
