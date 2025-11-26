#!/usr/bin/env python3
"""
convert_to_cnf.py

Reads a CFG from a file, converts it to CNF, and prints the CNF grammar
directly to the command line.

Usage:
    python convert_to_cnf.py input.cfg
"""

import sys
from cfg_utils import load_cfg, save_cfg
from cnf_converter import to_cnf


def print_cfg(cfg):
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
    if len(sys.argv) != 2:
        print("Usage: python convert_to_cnf.py <input_cfg>")
        sys.exit(1)

    input_path = sys.argv[1]
    cfg = load_cfg(input_path)
    cnf_cfg = to_cnf(cfg)

    print_cfg(cnf_cfg)


if __name__ == "__main__":
    main()
