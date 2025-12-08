#!/usr/bin/env python3
"""
cfg_to_pda.py

Minimal converter: CFG -> PDA transition table (single-state, accept by EMPTY STACK).

Usage:
    python cfg_to_pda.py <cfg_file>

Input CFG format example:
Nonterminals: S A B
Terminals: a b
Start: S
Productions:
S -> a S | b
A -> a
B -> b

Important convention (fixed):
- For production A -> X1 X2 ... Xn, this script emits the push sequence
  that the PDA performs (first push -> last push). To ensure the stack top
  is X1 (so it matches the input left-to-right), the PDA must **push the RHS
  in reverse order**: push Xn, ..., push X2, push X1. The script prints that
  push sequence (first->last) explicitly.
  Example: For S -> a S  (RHS = [a, S]) the push sequence printed will be:
    S a
  meaning: push S (first), then push a (last) — leaving 'a' on top.

- Acceptance: single-state PDA accepting by EMPTY STACK (initial transition
  replaces $ with S, so $ is not preserved).

No CLI extras — just supply the CFG filename on the command line.
"""

import sys
from collections import defaultdict

# ---------------------------
# Parse CFG (simple whitespace-separated tokens)
# ---------------------------
def parse_cfg(text):
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    nonterminals = []
    terminals = []
    start = None
    productions = defaultdict(list)
    mode = None

    for ln in lines:
        if ln.startswith("Nonterminals:"):
            nonterminals = ln.split(":", 1)[1].strip().split()
            continue
        if ln.startswith("Terminals:"):
            terminals = ln.split(":", 1)[1].strip().split()
            continue
        if ln.startswith("Start:"):
            start = ln.split(":", 1)[1].strip()
            continue
        if ln.startswith("Productions:"):
            mode = "prods"
            continue

        if mode == "prods":
            if "->" not in ln:
                continue
            left, right = ln.split("->", 1)
            left = left.strip()
            alternatives = [alt.strip() for alt in right.split("|")]
            for alt in alternatives:
                if alt in ("", "ε", "epsilon"):
                    productions[left].append([])  # epsilon
                else:
                    symbols = alt.split()
                    productions[left].append(symbols)

    return {"V": nonterminals, "Σ": terminals, "S": start, "P": dict(productions)}

# ---------------------------
# Convert CFG -> PDA transitions
# ---------------------------
# Transition format: (state, input_symbol, stack_top, next_state, push_list)
def cfg_to_pda(cfg):
    state = "q"
    transitions = []

    S = cfg["S"]
    Sigma = cfg["Σ"]
    P = cfg["P"]

    # Initial: replace bottom marker $ with start symbol S
    transitions.append((state, "ε", "$", state, [S]))

    # For each production A -> X1 X2 ... Xn,
    # PDA should push Xn,...,X2,X1 in that order so X1 is on top.
    # We output that push sequence (first pushed -> last pushed).
    for A, rhss in P.items():
        for rhs in rhss:
            if len(rhs) == 0:
                # A -> ε : pop A and push nothing
                transitions.append((state, "ε", A, state, []))
            else:
                # push RHS in reverse so leftmost symbol becomes top:
                # If rhs = [X1, X2, ..., Xn], we want push sequence = [Xn, ..., X2, X1]
                push_sequence = list(reversed(rhs))
                transitions.append((state, "ε", A, state, push_sequence))

    # Terminal consumption transitions: (q, a, a) -> (q, ε)
    for a in Sigma:
        transitions.append((state, a, a, state, []))

    return transitions

# ---------------------------
# Printing
# ---------------------------

def print_transitions(transitions):
    headers = ["state", "input", "stack_top", "next_state", "stack_replacement (push seq)"]
    rows = []
    for (s, inp, top, ns, push) in transitions:
        push_str = " ".join(push) if push else "ε"
        rows.append((s, inp, top, ns, push_str))

    # compute column widths
    col_widths = []
    for i in range(len(headers)):
        max_len = len(headers[i])
        for r in rows:
            if len(r[i]) > max_len:
                max_len = len(r[i])
        col_widths.append(max_len)

    # print header
    print(" | ".join(headers[i].ljust(col_widths[i]) for i in range(len(headers))))
    print("-+-".join("-" * col_widths[i] for i in range(len(headers))))

    # print rows
    for r in rows:
        print(" | ".join(r[i].ljust(col_widths[i]) for i in range(len(headers))))

# ---------------------------
# Main
# ---------------------------
def main():
    if len(sys.argv) != 2:
        print("Usage: python cfg_to_pda.py <cfg_file>")
        return

    filename = sys.argv[1]
    try:
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: cannot open file '{filename}'")
        return

    cfg = parse_cfg(text)
    if not cfg["S"]:
        print("Error: Start symbol missing (include a 'Start:' line).")
        return

    transitions = cfg_to_pda(cfg)

    print(f"PDA transitions for CFG in '{filename}':\n")
    print_transitions(transitions)

if __name__ == "__main__":
    main()
