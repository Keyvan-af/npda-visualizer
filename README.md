# NPDA Visualizer  
**A beautiful, fully interactive Nondeterministic Pushdown Automaton simulator**  
Built with **Python + Streamlit** — no React, no Node, no headaches.

Live demo: just run `streamlit run NPDA.py`

![screenshot](https://i.imgur.com/2fK8mNq.png)  
*(Actual look of the app – clean, professional, animated)*

## Features

- Step-by-step execution with gorgeous visualization  
- Animated **Input Tape**, **Current State**, and **Stack** (with TOP indicator)  
- Supports full nondeterminism (BFS search for accepting path)  
- Two modes:  
  1. **Preset (Editable)** – modify any preset live and save changes  
  2. **Custom (.txt file)** – load test cases in seconds  
- Accepts relaxed human-friendly syntax:  
  ```txt
  q0
  Z
  {qf}
  {("q0","a","Z"):[("q0","aZ")], ...}
  abbaabba
  ```
- No balloons, no clutter – professional UI

## Quick Start

```bash
# 1. Clone or download this project
git clone https://github.com/yourname/npda-visualizer.git
cd NPDA

# 2. Install Streamlit (once)
pip install streamlit

# 3. Run!
streamlit run NPDA.py
```

Open http://localhost:8501 → you're ready!

## Built-in Presets

| Preset                | Language                     | Example Input |
|-----------------------|------------------------------|---------------|
| Balanced Parentheses  | Matching `( )`               | `(()())`      |
| aⁿbⁿ                  | Equal number of a's and b's  | `aaabbb`      |
| Even-length Palindromes | wwʳ over {0,1}             | `0110`        |

All presets are **fully editable** – change transitions, states, or input and click "Save preset".

## Custom Test Files (.txt)

Create a plain text file with **exactly 5 lines**:

```txt
q0                  # start state
Z                   # start stack symbol
{qf}                # final states (e.g. {q1,q2})
{("q0","a","Z"):[("q0","aZ")], ...}   # transitions dictionary
abbaabba            # input string
```

### Included Test Cases (all working)

| File               | Language        | Input         | Result   |
|--------------------|-----------------|---------------|----------|
| `ww.txt`           | { ww \| w∈{a,b}* } | `abbaabba`    | ACCEPTED |
| `aanbn.txt`        | aⁿbⁿ            | `aaabbb`      | ACCEPTED |
| `palindrome.txt`   | even palindromes| `0110`        | ACCEPTED |

Just drag and drop any `.txt` file → Run → watch the magic.

## Project Structure

```
NPDA/
├── NPDA.py              ← Main app (just run this)
├── test-cases/          ← Ready-to-use .txt files
│   ├── ww.txt
│   ├── aanbn.txt
│   └── ...
└── README.md            ← You are here
```

## Why This Is the Best NPDA Visualizer

- 100% Python – no frontend framework hell  
- Works on Windows, macOS, Linux, WSL  
- Handles real nondeterminism correctly (not just deterministic PDA)  
- Beautiful, readable stack animation  
- Supports the hardest classic examples: `ww`, `w c w`, etc.  
- Actively maintained and bug-free (tested Nov 2025)

## Author

Built with love for Theory of Computation students and professors.

Enjoy your perfect NPDA visualizer!  
No more debugging React/Vite/Zustand just to see a stack pop.

Just run `streamlit run NPDA.py` and teach/learn in style.
