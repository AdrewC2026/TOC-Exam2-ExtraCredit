#!/usr/bin/env python3
"""
cnf_converter.py

Implements conversion of a CFG (with no epsilon productions) to
a Chomsky Normal Form (CNF)-style grammar.

Assumptions:
- No epsilon productions in the input (except possibly S -> ε, but
  for the extra credit the professor said we can assume there are none).
- We focus on getting productions into the shapes:
  - A -> a
  - A -> B C
"""

from typing import Dict, List, Set, Tuple
from cfg_utils import CFG


def to_cnf(cfg: CFG) -> CFG:
    """
    Convert the given CFG to a CNF-style equivalent.

    Steps:
    1. Remove unit productions A -> B.
    2. Ensure that in productions of length >= 2, any terminals are
       replaced by new nonterminals that produce those terminals.
    3. Break long right-hand sides (> 2) into chains of binary productions.
    """
    # Start from a copy
    new_cfg = CFG(
        nonterminals=set(cfg.nonterminals),
        terminals=set(cfg.terminals),
        start=cfg.start,
        productions={A: [rhs[:] for rhs in rhss] for A, rhss in cfg.productions.items()},
    )

    remove_unit_productions(new_cfg)
    introduce_terminal_nonterminals(new_cfg)
    binarize_productions(new_cfg)

    return new_cfg


def remove_unit_productions(cfg: CFG) -> None:
    """
    Eliminate unit productions of the form A -> B where A, B are nonterminals.
    Standard closure-based algorithm.
    """
    unit_pairs: Set[Tuple[str, str]] = set()

    # Initialize: (A, B) if A -> B is a unit production
    for A, rhss in cfg.productions.items():
        for rhs in rhss:
            if len(rhs) == 1 and rhs[0] in cfg.nonterminals:
                unit_pairs.add((A, rhs[0]))
        # Also each nonterminal is unit-related to itself
        unit_pairs.add((A, A))

    # Compute transitive closure
    changed = True
    while changed:
        changed = False
        new_pairs = set(unit_pairs)
        for (A, B) in unit_pairs:
            for (C, D) in unit_pairs:
                if B == C and (A, D) not in unit_pairs:
                    new_pairs.add((A, D))
                    changed = True
        unit_pairs = new_pairs

    # Build new productions without unit rules
    new_productions: Dict[str, List[List[str]]] = {A: [] for A in cfg.nonterminals}
    for A in cfg.nonterminals:
        # For all B such that A =>* B with unit productions
        for (X, B) in unit_pairs:
            if X != A or B not in cfg.nonterminals:
                continue
        for (_, B) in [p for p in unit_pairs if p[0] == A]:
            for rhs in cfg.productions.get(B, []):
                # Skip unit A -> B
                if len(rhs) == 1 and rhs[0] in cfg.nonterminals:
                    continue
                if rhs not in new_productions[A]:
                    new_productions[A].append(rhs)

    cfg.productions = new_productions


def introduce_terminal_nonterminals(cfg: CFG) -> None:
    """
    For any production A -> ... a ... where a is a terminal and the RHS length > 1,
    introduce a new nonterminal Ta with rule Ta -> a, and replace a with Ta.

    Reuse existing Ta if already created.
    """
    terminal_map: Dict[str, str] = {}  # terminal -> new nonterminal

    def get_or_create_nt_for_terminal(a: str) -> str:
        if a in terminal_map:
            return terminal_map[a]
        nt = f"T_{a}"
        # Ensure we don't clash
        while nt in cfg.nonterminals:
            nt = "_" + nt
        cfg.nonterminals.add(nt)
        cfg.productions.setdefault(nt, []).append([a])
        terminal_map[a] = nt
        return nt

    for A in list(cfg.productions.keys()):
        new_rhss: List[List[str]] = []
        for rhs in cfg.productions[A]:
            if len(rhs) == 1:
                # A -> a or A -> B already fine for CNF (modulo unit removal we did)
                new_rhss.append(rhs)
            else:
                new_rhs: List[str] = []
                for sym in rhs:
                    if sym in cfg.terminals:
                        nt = get_or_create_nt_for_terminal(sym)
                        new_rhs.append(nt)
                    else:
                        new_rhs.append(sym)
                new_rhss.append(new_rhs)
        cfg.productions[A] = new_rhss


def binarize_productions(cfg: CFG) -> None:
    """
    Break productions with length > 2 into binary chains.
    Example:
        A -> B C D E
    becomes something like:
        A -> B X1
        X1 -> C X2
        X2 -> D E
    """
    new_productions: Dict[str, List[List[str]]] = {A: [] for A in cfg.nonterminals}

    for A, rhss in cfg.productions.items():
        for rhs in rhss:
            if len(rhs) <= 2:
                new_productions[A].append(rhs)
            else:
                # Need to create new intermediate nonterminals
                current_left = A
                symbols = rhs[:]
                while len(symbols) > 2:
                    B = symbols.pop(0)
                    # Create new intermediate nonterminal
                    new_nt = f"X_{'_'.join(symbols)}"
                    # Ensure uniqueness
                    while new_nt in cfg.nonterminals:
                        new_nt = "_" + new_nt
                    cfg.nonterminals.add(new_nt)

                    new_productions.setdefault(current_left, []).append([B, new_nt])
                    current_left = new_nt
                # Last two symbols
                new_productions.setdefault(current_left, []).append(symbols)

    cfg.productions = new_productions
