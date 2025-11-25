# NPDA.py — FINAL CLEAN & PROFESSIONAL VERSION
import streamlit as st
import ast
import re
from collections import deque
from typing import Optional, List, Dict

# ==============================
# 1. NPDA ENGINE
# ==============================
class NPDA:
    def __init__(self, delta, start_state: str, start_stack: str, final_states: set):
        self.delta = delta
        self.q0 = start_state
        self.z0 = start_stack
        self.F = final_states

    def get_success_path(self, input_string: str) -> Optional[List[Dict]]:
        queue = deque([(self.q0, input_string, [self.z0], [])])
        visited = set()

        while queue:
            state, inp, stack, path = queue.popleft()
            current = {"state": state, "input_left": inp, "stack": stack.copy(), "description": ""}

            if not inp and state in self.F:
                path.append({**current, "description": "ACCEPTED"})
                return path + [current]

            sig = (state, inp, tuple(stack))
            if sig in visited: continue
            visited.add(sig)
            if not stack: continue
            top = stack[-1]

            moves = []
            if inp:
                key = (state, inp[0], top)
                if key in self.delta:
                    for ns, push in self.delta[key]:
                        moves.append((ns, inp[1:], push, f"Read '{inp[0]}' → push '{push}'"))
            key = (state, "", top)
            if key in self.delta:
                for ns, push in self.delta[key]:
                    moves.append((ns, inp, push, f"ε-move → push '{push}'"))

            for ns, ni, push, desc in moves:
                new_stack = stack[:-1]
                if push:
                    new_stack.extend(reversed(push))
                new_path = path + [{**current, "description": desc}]
                queue.append((ns, ni, new_stack, new_path))
        return None

# ==============================
# 2. Safe parsers
# ==============================
def parse_final_states(s: str) -> set:
    s = s.strip().strip("{}")
    return {x.strip().strip("'\"") for x in s.split(",") if x.strip()}

def safe_eval_transitions(s: str):
    s = s.strip().replace("'", '"')
    s = re.sub(r"\b([a-zA-Z0-9_]+)\b(?=\s*:|\s*,\s*[\{\}\)])", r'"\1"', s)
    s = re.sub(r"\(\s*([a-zA-Z0-9_]+)\s*,", r'("\1",', s)
    s = re.sub(r",\s*([a-zA-Z0-9_]+)\s*\)", r', "\1")', s)
    return ast.literal_eval(s)

# ==============================
# 3. Editable presets
# ==============================
if "presets" not in st.session_state:
    st.session_state.presets = {
        "Balanced Parentheses": {"start":"q0","stack":"Z","final":"{q1}","trans":'{("q0","(","Z"):[("q0","(Z")],("q0","(","("):[("q0","((")],("q0",")","("):[("q0","")],("q0","","Z"):[("q1","Z")]}',"input":"(()())"},
        "a^n b^n": {"start":"q0","stack":"Z","final":"{q2}","trans":'{("q0","a","Z"):[("q0","aZ")],("q0","a","a"):[("q0","aa")],("q0","b","a"):[("q1","")],("q1","b","a"):[("q1","")],("q1","","Z"):[("q2","Z")]}',"input":"aaabbb"},
        "Even-length Palindromes": {"start":"q0","stack":"Z","final":"{q2}","trans":'{("q0","0","Z"):[("q0","0Z")],("q0","1","Z"):[("q0","1Z")],("q0","0","0"):[("q0","00")],("q0","1","0"):[("q0","10")],("q0","0","1"):[("q0","01")],("q0","1","1"):[("q0","11")],("q0","","Z"):[("q1","Z")],("q0","","0"):[("q1","0")],("q0","","1"):[("q1","1")],("q1","0","0"):[("q1","")],("q1","1","1"):[("q1","")],("q1","","Z"):[("q2","Z")]}',"input":"0110"}
    }

# ==============================
# 4. UI
# ==============================
st.set_page_config(page_title="NPDA Visualizer", layout="wide")
st.title("NPDA Visualizer")
st.markdown("**Nondeterministic Pushdown Automaton – step-by-step execution**")

with st.sidebar:
    mode = st.radio("Mode", ["Preset (Editable)", "Custom (.txt file)"])

    if mode == "Preset (Editable)":
        name = st.selectbox("Preset", list(st.session_state.presets.keys()))
        p = st.session_state.presets[name]
        with st.expander("Edit configuration", True):
            start = st.text_input("Start state", p["start"], key=f"s_{name}")
            stack = st.text_input("Start stack symbol", p["stack"], key=f"k_{name}")
            final = st.text_input("Final states {q1,q2,…}", p["final"], key=f"f_{name}")
            trans = st.text_area("Transitions", p["trans"], height=300, key=f"t_{name}")
            inp   = st.text_input("Input string", p["input"], key=f"i_{name}")
        if st.button("Save preset"):
            st.session_state.presets[name] = {"start":start,"stack":stack,"final":final,"trans":trans,"input":inp}
            st.success("Saved")
    else:
        uploaded = st.file_uploader("Upload .txt test case (5 lines)", type="txt")
        if uploaded:
            lines = [l.strip() for l in uploaded.read().decode().splitlines() if l.strip()]
            if len(lines) != 5:
                st.error("Exactly 5 lines required")
            else:
                start, stack, final, trans, inp = lines
                st.code("\n".join(lines))
        else:
            start = stack = final = trans = inp = ""

    disabled = (mode == "Custom (.txt file)" and not uploaded)
    if st.button("Run Simulation", type="primary", disabled=disabled):
        st.session_state.config = {"start":start,"stack":stack,"final":final,"trans":trans,"input":inp}
        st.session_state.run = True

# ==============================
# 5. Simulation
# ==============================
if st.session_state.get("run"):
    cfg = st.session_state.config
    with st.spinner("Running NPDA…"):
        try:
            delta = safe_eval_transitions(cfg["trans"])
            finals = parse_final_states(cfg["final"])
            npda = NPDA(delta, cfg["start"], cfg["stack"], finals)
            trace = npda.get_success_path(cfg["input"])

            st.session_state.trace = trace
            st.session_state.word   = cfg["input"]

            if trace:
                st.success(f"**{cfg['input']}** → ACCEPTED")
            else:
                st.error(f"**{cfg['input']}** → REJECTED")
        except Exception as e:
            st.error("Configuration error")
            st.code(str(e))

# ==============================
# 6. Visualization
# ==============================
if st.session_state.get("trace"):
    trace = st.session_state.trace
    word  = st.session_state.word
    step  = st.slider("Step", 0, len(trace)-1, 0, key="step_slider")
    s     = trace[step]

    c1, c2, c3 = st.columns([3, 2, 2])

    with c1:
        st.subheader("Input Tape")
        pos = len(word) - len(s["input_left"])
        tape = "".join(
            f"<span style='color:#888'>{c}</span>" if i < pos else
            f"<span style='background:#ef4444;color:white;padding:0 8px;border-radius:4px'>{c}</span>" if i == pos else c
            for i, c in enumerate(word)
        )
        st.markdown(f"<div style='font-family:monospace;font-size:28px;background:#111;padding:20px;border-radius:12px'>{tape}</div>", unsafe_allow_html=True)
        st.caption(s["description"] or "Initial configuration")

    with c2:
        st.subheader("State")
        st.metric("Current", s["state"])
        if step == len(trace)-1:
            st.success("Final state – ACCEPTED")

    with c3:
        st.subheader("Stack (Top →)")
        html = "<div style='display:flex;flex-direction:column-reverse;gap:12px;align-items:center'>"
        for i, sym in enumerate(s["stack"]):
            top   = i == len(s["stack"])-1
            color = "#dc2626" if top else ("#16a34a" if sym=="Z" else "#3b82f6")
            border = "4px solid gold" if top else "2px solid #555"
            size   = "32px" if top else "26px"
            html += f"<div style='background:{color};color:white;padding:14px 28px;border-radius:16px;font-weight:bold;font-size:{size};border:{border};box-shadow:0 8px 20px #0004'>{sym}</div>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
        st.caption("Bottom ← → Top")