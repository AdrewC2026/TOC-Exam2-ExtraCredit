#!/usr/bin/env python3
"""
run_operations.py

Runs CFG operations and prints the resulting CFG to the command line.

Usage:
    python run_operations.py union  cfg1 cfg2
    python run_operations.py concat cfg1 cfg2
    python run_operations.py star   cfg
    python run_operations.py partd  cfg1 cfg2
"""

import sys
from cfg_utils import load_cfg
from cfg_operations import union_cfg, concat_cfg, star_cfg, part_d_example_cfg


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
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python run_operations.py union  <cfg1> <cfg2>")
        print("  python run_operations.py concat <cfg1> <cfg2>")
        print("  python run_operations.py star   <cfg>")
        print("  python run_operations.py partd  <cfg1> <cfg2>")
        sys.exit(1)

    op = sys.argv[1].lower()

    if op == "union":
        if len(sys.argv) != 4:
            print("Usage: python run_operations.py union <cfg1> <cfg2>")
            sys.exit(1)
        cfg1 = load_cfg(sys.argv[2])
        cfg2 = load_cfg(sys.argv[3])
        result = union_cfg(cfg1, cfg2)
        print_cfg(result)

    elif op == "concat":
        if len(sys.argv) != 4:
            print("Usage: python run_operations.py concat <cfg1> <cfg2>")
            sys.exit(1)
        cfg1 = load_cfg(sys.argv[2])
        cfg2 = load_cfg(sys.argv[3])
        result = concat_cfg(cfg1, cfg2)
        print_cfg(result)

    elif op == "star":
        if len(sys.argv) != 3:
            print("Usage: python run_operations.py star <cfg>")
            sys.exit(1)
        cfg = load_cfg(sys.argv[2])
        result = star_cfg(cfg)
        print_cfg(result)

    elif op == "partd":
        if len(sys.argv) != 4:
            print("Usage: python run_operations.py partd <cfg1> <cfg2>")
            sys.exit(1)
        cfg1 = load_cfg(sys.argv[2])
        cfg2 = load_cfg(sys.argv[3])
        result = part_d_example_cfg(cfg1, cfg2)
        print_cfg(result)

    else:
        print(f"Unknown operation: {op}")
        sys.exit(1)


if __name__ == "__main__":
    main()
