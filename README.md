# **TOC Exam 2 – Extra Credit**

Author: **Andrew Cotaj**
Course: **CSE 30151 – Theory of Computing**
Professor: **Prof. Peter Kogge**
- Total Points Earned Back: **40 Points**

This repository contains Python programs implementing all extra-credit tasks for **Exam 2**, including:

1. **Problem 4 (10 points)**
  Program to convert a context-free grammar (CFG) into **Chomsky Normal Form (CNF)**.

2. **Problem 5 (15 points for a–c, +5 points for part d)**
  Programs that construct new CFGs using **union**, **concatenation**, **Kleene star**, and a final composite construction required for **part d**.

3. **Problem 2 (10 points)**
  Program to convert a context-free grammar (CFG) into an equivalent **pushdown automaton (PDA)** using the construction from Sipser’s Lemma 2.21.

All programs read CFGs in a simple text format and **print results directly to the command line**. No external libraries are required.

---

# **Points Earned Back**

### **Problem 4 — CNF Conversion (10 points)**

Writing a program that correctly converts a CFG (with no epsilon rules) into CNF earns back
**up to all 10 points lost on Question 4(c)**.

---

### **Problem 5 — CFG Operations (15 points for a–c + 5 points for part d)**

* Parts **5(a), 5(b), 5(c)** together were worth **15 points**.
  Writing programs for:

  * Union
  * Concatenation
  * Kleene Star

  earns back **up to all 15 points lost on 5(a–c)**.

* **Part 5(d)** (5 additional points) required:
  **Use your procedures to translate the regular expression
  0 ∪ 10(000)*
  into a CFG.**

  This is implemented in the standalone script **`regex_partd.py`**.

---

### **Problem 2 — PDA from CFG (Part C, +10 points)**

For Problem 2 Part C, I implemented a complete Python program (`cfg_to_pda.py`) that converts any given context-free grammar into a pushdown automaton using the standard construction from Sipser’s Lemma 2.21. This corrected submission earns back the full **10 points** originally lost on this question.

Highlights:
* Uses a single state and accepts by empty stack (equivalent to final-state acceptance).
* Initializes with `(q, ε, $ → q, S)`.
* Replaces nonterminals via ε-transitions.
* Matches terminals with `(q, a, a → q, ε)`.
* For every production `A → X1 X2 … Xn`, pushes `Xn … X2 X1` (reverse order) so `X1` is on top, respecting the LIFO stack for left-to-right matching.
* Reads CFGs in the project’s standard format and prints a clean transition table.

Run with:
```
python cfg_to_pda.py <grammarfile.txt>
```

---

# **1. File Overview**

```
convert_to_cnf.py      # Problem 4: CLI that prints CNF grammar

cnf_converter.py       # CNF conversion algorithm (remove units,
                       # introduce terminal wrappers, binarize)

run_operations.py      # Problem 5: union/concat/star/partd CLI

cfg_operations.py      # Implementations of union, concatenation, star

regex_partd.py         # Problem 5(d): Construct CFG for regex 0 ∪ 10(000)*

cfg_utils.py           # CFG class, parser, pretty-printer

cfg_to_pda.py          # Problem 2 Part C: CFG -> PDA (Sipser Lemma 2.21)

examples/CFG1.txt
examples/CFG2.txt
examples/CFG3.txt
examples/CFG4.txt
examples/CFG5.txt      # Test grammars of varying complexity
```

All scripts run using standard Python.

---

# **2. CFG Input Format**

All CFGs follow this simple format:

```
Nonterminals: S,A,B
Terminals: a,b
Start: S
Productions:
S -> A S a | a
A -> a
```

### Rules:

* **Nonterminals** — comma-separated symbols
* **Terminals** — comma-separated symbols
* **Start** — start symbol
* **Productions:**

  * Alternatives separated by `|`
  * Symbols inside RHS separated by spaces
* **ε** is written literally as:

  ```
  ε
  ```

### CNF requirement:

Problem 4 allows assuming **no epsilon productions** except possibly S → ε created by Star operation in Problem 5.

---

# **3. Running Each Program**

From the project directory:

```
python convert_to_cnf.py <input_cfg>
python run_operations.py <operation> <args>
python regex_partd.py
python cfg_to_pda.py <grammarfile.txt>
```

---

# **3.1 Problem 4 — Convert CFG to CNF (10 points)**

Example:

```
python convert_to_cnf.py examples/CFG1.txt
```

The converter outputs a CFG where every production is either:

* `A -> a`
* `A -> B C`

It also removes:

* Unit productions
* Long RHS
* Terminals inside RHS of length ≥ 2 (replacing them with `T_a`, etc.)

---

# **3.2 Problem 5 — CFG Operations (15 points for a–c)**

### **Union**

```
python run_operations.py union CFG1.txt CFG2.txt
```

### **Concatenation**

```
python run_operations.py concat CFG3.txt CFG1.txt
```

### **Kleene Star**

```
python run_operations.py star CFG1.txt
```

### Output

Each operation:

* Performs **prefix renaming** to avoid collisions
* Constructs the correct start symbol
* Prints the full resulting CFG to the command line

---

# **3.3 Problem 5(d) — Regular Expression to CFG (5 points)**

The exam required:

> Use your previously written procedures to translate the regular expression
> **R = 0 ∪ 10(000)***
> over Σ = {0,1} into a CFG.

This is implemented in:

```
regex_partd.py
```

### Usage

```
python regex_partd.py
```

### How it works

The program constructs base CFGs for:

* `{0}`
* `{"10"}`
* `{"000"}`

Then uses the **same operations from Problem 5**:

1. `star_cfg` to obtain `(000)*`
2. `concat_cfg` to obtain `10(000)*`
3. `union_cfg` to obtain `0 ∪ 10(000)*`

### Output Example (structure only)

```
S_union -> G1_S0 | G2_S_concat
G1_S0 -> 0
G2_S_concat -> G2_G1_S10 G2_G2_S_star
G2_G1_S10 -> 1 G2_G1_A10
...
```

The resulting grammar correctly generates:

L = {0} ∪ {10(000)^k ∣ k ≥ 0}

---

# **3.4 Problem 2 — CFG to PDA (Part C, +10 points)**

This program converts any CFG (in the project’s input format) to an equivalent PDA:
* Construction: Sipser Lemma 2.21, single state, accept by empty stack.
* Stack initialization: `(q, ε, $ → q, S)`.
* Nonterminal replacement: ε-transitions pushing RHS in reverse order.
* Terminal matching: `(q, a, a → q, ε)`.

Example:
```
python cfg_to_pda.py examples/CFG1.txt
```

It prints the complete transition table to the console.

---

# **4. Description of Each Operation**

### **Union(G1, G2)**

Adds a new start symbol:

```
S_union -> G1_S | G2_S
```

### **Concatenation(G1, G2)**

Adds a new start:

```
S_concat -> G1_S G2_S
```

### **Kleene Star(G)**

Produces:

```
S_star -> ε | S_star G_S
```

### **Part D Construction**

(L(G₁) ∪ L(G₂))*  
(but here applied only to 0 ∪ 10(000)^*)

---

# **5. Included Test Grammars**

Five CFG files included for testing:

| File         | Description                |
| ------------ | -------------------------- |
| **CFG1.txt** | Simple a* b grammar        |
| **CFG2.txt** | aⁿ bⁿ grammar              |
| **CFG3.txt** | palindromes                |
| **CFG4.txt** | grammar including ε        |
| **CFG5.txt** | expression grammar (E/T/F) |

Example tests:

```
python convert_to_cnf.py CFG2.txt
python run_operations.py union CFG1.txt CFG2.txt
python run_operations.py concat CFG3.txt CFG1.txt
python run_operations.py star CFG1.txt
python regex_partd.py
python cfg_to_pda.py examples/CFG1.txt
```

---

# **6. Implementation Assumptions**

* CNF converter removes unit productions
* Terminal wrappers created as needed (`T_a`, `T_b`, …)
* Binarization creates `X_*` nonterminals
* Operation scripts use prefixing (`G1_`, `G2_`, etc.) to avoid collisions
* All outputs printed directly to terminal
* No external dependencies

*README converted to markdown through use of GPT 5.1*
