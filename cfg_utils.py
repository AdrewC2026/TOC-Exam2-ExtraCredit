#!/usr/bin/env python3
"""
cfg_utils.py

Shared utilities for representing and parsing CFGs used in the extra credit:
- CFG class
- load_cfg(path)
- save_cfg(cfg, path)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set


@dataclass
class CFG:
    nonterminals: Set[str]
    terminals: Set[str]
    start: str
    productions: Dict[str, List[List[str]]] = field(default_factory=dict)

    def add_production(self, left: str, right: List[str]) -> None:
        if left not in self.productions:
            self.productions[left] = []
        self.productions[left].append(right)


def _parse_symbol_list(line: str) -> List[str]:
    """
    Parse a comma-separated list after the colon.
    Example: "Nonterminals: S,A,B" -> ["S", "A", "B"]
    """
    after_colon = line.split(":", 1)[1].strip()
    if not after_colon:
        return []
    return [s.strip() for s in after_colon.split(",") if s.strip()]


def load_cfg(path: str) -> CFG:
    """
    Load a CFG from a text file with the format:

    Nonterminals: S,A,B
    Terminals: a,b
    Start: S
    Productions:
    S -> A S a | a B
    A -> a
    B -> b

    Right-hand sides are space-separated symbols, alternatives split by '|'.
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    nonterminals: Set[str] = set()
    terminals: Set[str] = set()
    start_symbol: str = ""
    productions: Dict[str, List[List[str]]] = {}

    in_productions = False
    for line in lines:
        if line.startswith("Nonterminals:"):
            nonterminals = set(_parse_symbol_list(line))
        elif line.startswith("Terminals:"):
            terminals = set(_parse_symbol_list(line))
        elif line.startswith("Start:"):
            start_symbol = line.split(":", 1)[1].strip()
        elif line.startswith("Productions:"):
            in_productions = True
        elif in_productions:
            # Production line: A -> alpha1 | alpha2 | ...
            if "->" not in line:
                continue
            left, right_part = line.split("->", 1)
            left = left.strip()
            right_alts = right_part.split("|")
            for alt in right_alts:
                symbols = alt.strip()
                if symbols == "ε":
                    rhs: List[str] = ["ε"]
                else:
                    rhs = symbols.split()
                productions.setdefault(left, []).append(rhs)

    if not start_symbol:
        raise ValueError("Start symbol not specified in CFG file.")

    # Infer terminals if not explicitly given
    if not terminals:
        rhs_symbols = set()
        for rhs_list in productions.values():
            for rhs in rhs_list:
                for sym in rhs:
                    rhs_symbols.add(sym)
        # Heuristic: nonterminals are those listed; everything else is terminal/epsilon
        terminals = rhs_symbols - nonterminals - {"ε"}

    cfg = CFG(nonterminals=nonterminals,
              terminals=terminals,
              start=start_symbol,
              productions=productions)
    return cfg


def save_cfg(cfg: CFG, path: str) -> None:
    """
    Save a CFG back to the same textual format.
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write("Nonterminals: " + ",".join(sorted(cfg.nonterminals)) + "\n")
        f.write("Terminals: " + ",".join(sorted(cfg.terminals)) + "\n")
        f.write("Start: " + cfg.start + "\n")
        f.write("Productions:\n")
        for left in sorted(cfg.productions.keys()):
            alts = []
            for rhs in cfg.productions[left]:
                if rhs == ["ε"]:
                    alts.append("ε")
                else:
                    alts.append(" ".join(rhs))
            f.write(f"{left} -> " + " | ".join(alts) + "\n")
