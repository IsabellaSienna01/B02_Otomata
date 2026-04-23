import tkinter as tk
import math

BG       = "#050810"
PANEL    = "#080d1a"
CARD     = "#0a1020"
BORDER   = "#0f2040"
BORDER_H = "#1e3a6e" 

CYAN     = "#00e5ff"
GREEN    = "#00ff9f"
RED      = "#ff2d55"  
PURPLE   = "#c400ff"  
YELLOW   = "#ffe600" 
ORANGE   = "#ff8800" 
PINK     = "#ff4da6"  

TEXT     = "#b8d4ff"
TEXT_D   = "#2e4a6a" 
TEXT_M   = "#14243a"  

STATE_THEME = {
    "S": ("#0b0f20", PURPLE,    "#1a0047", PURPLE),
    "A": ("#071510", "#00bb66", "#003820", GREEN),
    "B": ("#020c1c", "#1890dd", "#002850", CYAN),
    "C": ("#180408", "#bb1133", "#380010", RED),
}

TRANSITIONS = {
    "S": {"0": "A", "1": "B"},
    "A": {"0": "C", "1": "B"},
    "B": {"0": "A", "1": "B"},
    "C": {"0": "C", "1": "C"},
}
START_STATE   = "S"
ACCEPT_STATES = {"B"}
DEAD_STATES   = {"C"}

STATE_DESC = {
    "S": ("Start",         "No input read yet"),
    "A": ("Middle",        "last='0', no '00' seen"),
    "B": ("Accept  ✓",     "last='1', no '00' seen"),
    "C": ("Dead trap  ✗",  "'00' encountered"),
}


def fsm_run(s: str) -> tuple[bool, str, list]:
    state = START_STATE
    trace = []                    
    for step, ch in enumerate(s, 1):
        frm   = state
        state = TRANSITIONS[state][ch]
        trace.append((step, frm, ch, state))
        if state in DEAD_STATES:
            for i, c in enumerate(s[step:], step + 1):
                trace.append((i, state, c, state))
            break
    return state in ACCEPT_STATES, state, trace


def fsm_validate(s: str) -> str | None:
    if not s:
        return "Input cannot be empty."
    bad = set(s) - {"0", "1"}
    if bad:
        return f"Invalid character(s): {', '.join(sorted(bad))}  —  only '0' and '1' are allowed."
    return None


def reject_reason(final: str, s: str) -> str:
    if final == "C":
        idx = s.find("00")
        return f'Forbidden substring "00" found at index {idx}.'
    if final == "A":
        return "Last character is '0' — language requires last char = '1'."
    return "Does not satisfy language rules."


def edge_pt(cx1, cy1, cx2, cy2, r):
    dx, dy = cx2 - cx1, cy2 - cy1
    d = math.hypot(dx, dy) or 1
    return cx1 + r * dx / d, cy1 + r * dy / d


def bezier3(p0, p1, p2, p3, steps=28):
    pts = []
    for i in range(steps + 1):
        t  = i / steps
        mt = 1 - t
        x  = mt**3*p0[0] + 3*mt**2*t*p1[0] + 3*mt*t**2*p2[0] + t**3*p3[0]
        y  = mt**3*p0[1] + 3*mt**2*t*p1[1] + 3*mt*t**2*p2[1] + t**3*p3[1]
        pts += [x, y]
    return pts


def mix_hex(c1: str, c2: str, t: float) -> str:
    r1, g1, b1 = int(c1[1:3],16), int(c1[3:5],16), int(c1[5:7],16)
    r2, g2, b2 = int(c2[1:3],16), int(c2[3:5],16), int(c2[5:7],16)
    return "#{:02x}{:02x}{:02x}".format(
        int(r1 + (r2-r1)*t), int(g1 + (g2-g1)*t), int(b1 + (b2-b1)*t))

class FSMApp:
    CW, CH = 624, 272  
    R      = 36 
    ANIM_MS = 420

    POS = {
        "S": ( 88, 136),
        "A": (268,  72),
        "B": (268, 192),
        "C": (464,  72),
    }

    def __init__(self, root: tk.Tk):
        self.root       = root
        self.history    = []
        self.stats      = {"total": 0, "accept": 0, "reject": 0}
        self._anim_job  = None
        self._active_st = None
        self._last_trace: list = []

        self._setup_window()
        self._build_fonts()
        self._build_ui()
        self._draw_diagram()

    def _setup_window(self):
        self.root.title("FSM Recognizer")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        W, H = 980, 710
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{W}x{H}+{(sw-W)//2}+{(sh-H)//2}")

    def _build_fonts(self):
        self.F = {
            "title":  ("Courier New", 14, "bold"),
            "head":   ("Courier New", 10, "bold"),
            "body":   ("Courier New",  9),
            "input":  ("Courier New", 14, "bold"),
            "state":  ("Courier New", 17, "bold"),
            "small":  ("Courier New",  8),
            "badge":  ("Courier New",  9, "bold"),
        }

    def _build_ui(self):
        topbar = tk.Frame(self.root, bg="#07101f", height=50)
        topbar.pack(fill="x"); topbar.pack_propagate(False)

        tk.Label(topbar, text="◈  FSM RECOGNIZER", font=self.F["title"],
                 fg=CYAN, bg="#07101f").pack(side="left", padx=18, pady=12)

        tk.Label(topbar, text="L = { x ∈ (0+1)⁺  |  last(x)='1'  ∧  '00' ∉ sub(x) }",
                 font=self.F["body"], fg=TEXT_D, bg="#07101f").pack(side="left", padx=6)

        self.lbl_stats = tk.Label(topbar, text="", font=self.F["small"],
                                  fg=TEXT_D, bg="#07101f")
        self.lbl_stats.pack(side="right", padx=18)

        tk.Frame(self.root, bg=CYAN, height=1).pack(fill="x")

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True)

        left = tk.Frame(body, bg=BG)
        left.pack(side="left", fill="both", expand=True, padx=(10,4), pady=10)

        right = tk.Frame(body, bg=BG, width=304)
        right.pack(side="right", fill="y", padx=(4,10), pady=10)
        right.pack_propagate(False)

        self._build_left(left)
        self._build_right(right)
        self._update_stats()

    def _build_left(self, p):
        d_card = self._card(p, pady=(0,8))
        self._card_header(d_card, "◇ STATE DIAGRAM", PURPLE,
                          right_txt="S=start  ·  B=accept  ·  C=dead")

        self.canvas = tk.Canvas(d_card, width=self.CW, height=self.CH,
                                bg=PANEL, highlightthickness=0)
        self.canvas.pack(padx=8, pady=(2,8))

        # Input card
        i_card = self._card(p, pady=(0,8))
        self._card_header(i_card, "◇ INPUT", CYAN,
                          right_txt="Enter a binary string, then press Enter or ▶ RUN")

        inp_row = tk.Frame(i_card, bg=CARD)
        inp_row.pack(fill="x", padx=10, pady=(2,4))

        tk.Label(inp_row, text="❯", font=("Courier New",15,"bold"),
                 fg=CYAN, bg=CARD).pack(side="left", padx=(0,6))

        self.inp_var = tk.StringVar()
        self.inp_var.trace_add("write", self._on_input_change)
        self.entry = tk.Entry(inp_row, textvariable=self.inp_var,
                              font=self.F["input"],
                              bg="#060e1e", fg=TEXT,
                              insertbackground=CYAN,
                              relief="flat", bd=0,
                              highlightthickness=1,
                              highlightcolor=CYAN,
                              highlightbackground=BORDER_H)
        self.entry.pack(side="left", fill="x", expand=True, ipady=7, padx=(0,8))
        self.entry.bind("<Return>", lambda _: self._run())
        self.entry.focus_set()

        self.btn_run = self._btn(inp_row, "▶  RUN",
                                 fg=BG, bg=CYAN, abg="#00c0e0", afg=BG,
                                 cmd=self._run, padx=16, font=self.F["badge"])
        self.btn_run.pack(side="left", padx=(0,4))

        self.btn_clr = self._btn(inp_row, "✕",
                                 fg=TEXT_D, bg=CARD, abg=PANEL, afg=TEXT,
                                 cmd=self._clear, padx=10, font=self.F["body"])
        self.btn_clr.pack(side="left")

        self.lbl_err = tk.Label(i_card, text="", font=self.F["small"],
                                fg=RED, bg=CARD)
        self.lbl_err.pack(anchor="w", padx=14, pady=(0,5))

        # Result banner (canvas so we can draw freely)
        self.res_canvas = tk.Canvas(p, height=58, bg=BG, highlightthickness=0)
        self.res_canvas.pack(fill="x", pady=(0,8))
        self.res_canvas.bind("<Configure>", lambda _: self._redraw_result())

        # Trace card
        t_card = self._card(p, expand=True, fill="both", pady=(0,0))
        t_hdr  = self._card_header(t_card, "◇ TRACE LOG", YELLOW)

        self.btn_anim = self._btn(t_hdr, "⏵ ANIMATE",
                                  fg=YELLOW, bg=CARD, abg=PANEL, afg=YELLOW,
                                  cmd=self._start_animation, padx=8,
                                  font=self.F["small"])
        self.btn_anim.pack(side="right")
        self.btn_anim.config(state="disabled")

        self.trace_txt = tk.Text(t_card, font=("Courier New", 9),
                                 bg=PANEL, fg=TEXT,
                                 relief="flat", bd=0, padx=10, pady=6,
                                 selectbackground=BORDER_H,
                                 state="disabled", height=9, wrap="none")
        self.trace_txt.pack(fill="both", expand=True, padx=8, pady=(2,8))

        # Colour tags for trace log
        for tag, col in [
            ("hdr",    TEXT_D),  ("sep",  TEXT_M),
            ("s_S",    PURPLE),  ("s_A",  "#00cc77"),
            ("s_B",    CYAN),    ("s_C",  RED),
            ("sym",    YELLOW),  ("ok",   GREEN),
            ("bad",    RED),     ("warn", YELLOW),
        ]:
            self.trace_txt.tag_config(tag, foreground=col)

        sb_h = tk.Scrollbar(t_card, orient="horizontal",
                            command=self.trace_txt.xview,
                            bg=PANEL, troughcolor=BG,
                            highlightbackground=PANEL, bd=0)
        sb_h.pack(fill="x", padx=8, pady=(0,2))
        self.trace_txt.config(xscrollcommand=sb_h.set)

    def _build_right(self, p):
        s_card = self._card(p, pady=(0,8))
        self._card_header(s_card, "◇ STATES", PURPLE)
        for name, (title, desc) in STATE_DESC.items():
            ring = STATE_THEME[name][1]
            row  = tk.Frame(s_card, bg=CARD)
            row.pack(fill="x", padx=10, pady=3)
            tk.Label(row, text="●", font=("Courier New",11,"bold"),
                     fg=ring, bg=CARD).pack(side="left")
            f = tk.Frame(row, bg=CARD)
            f.pack(side="left", padx=6)
            tk.Label(f, text=f"{name}  —  {title}", font=self.F["badge"],
                     fg=TEXT, bg=CARD, anchor="w").pack(fill="x")
            tk.Label(f, text=desc, font=self.F["small"],
                     fg=TEXT_D, bg=CARD, anchor="w").pack(fill="x")
        tk.Frame(s_card, bg=BG, height=6).pack()

        t_card = self._card(p, pady=(0,8))
        self._card_header(t_card, "◇ TRANSITIONS", CYAN)

        tbl = tk.Frame(t_card, bg=CARD)
        tbl.pack(fill="x", padx=8, pady=(2,8))

        for col_txt, col_fg, c in [
            ("STATE", TEXT_D, 0), ("→  '0'", TEXT_D, 1), ("→  '1'", TEXT_D, 2)
        ]:
            tk.Label(tbl, text=col_txt, font=self.F["small"],
                     fg=col_fg, bg=PANEL, anchor="w",
                     padx=8, pady=3).grid(row=0, column=c, sticky="ew", padx=1, pady=1)

        for r, state in enumerate(["S","A","B","C"], 1):
            marker = "★" if state==START_STATE else ("✓" if state in ACCEPT_STATES else ("✗" if state in DEAD_STATES else "·"))
            ring   = STATE_THEME[state][1]
            bg2    = mix_hex(CARD, ring, 0.06)

            tk.Label(tbl, text=f"{marker} {state}",
                     font=self.F["badge"], fg=ring, bg=bg2,
                     anchor="w", padx=8, pady=4).grid(row=r, column=0, sticky="ew", padx=1, pady=1)

            for c, sym in [(1,"0"), (2,"1")]:
                dest = TRANSITIONS[state][sym]
                dcol = STATE_THEME[dest][1]
                tk.Label(tbl, text=f"→ {dest}",
                         font=self.F["body"], fg=dcol, bg=bg2,
                         anchor="w", padx=8, pady=4).grid(row=r, column=c, sticky="ew", padx=1, pady=1)

        tbl.columnconfigure(0,weight=1); tbl.columnconfigure(1,weight=1); tbl.columnconfigure(2,weight=1)

        h_card = self._card(p, expand=True, fill="both", pady=(0,0))
        h_hdr  = self._card_header(h_card, "◇ HISTORY", ORANGE)
        self._btn(h_hdr, "clear all", fg=TEXT_D, bg=CARD,
                  abg=PANEL, afg=TEXT, cmd=self._clear_history,
                  padx=6, font=self.F["small"]).pack(side="right")

        self.hist_txt = tk.Text(h_card, font=("Courier New",9),
                                bg=PANEL, fg=TEXT,
                                relief="flat", bd=0, padx=8, pady=4,
                                state="disabled", wrap="none")
        self.hist_txt.pack(fill="both", expand=True, padx=8, pady=(2,8))

        for tag, col in [("acc", GREEN), ("rej", RED), ("s", TEXT), ("d", TEXT_D)]:
            self.hist_txt.tag_config(tag, foreground=col)

    def _card(self, parent, expand=False, fill="x", pady=(0,0)):
        f = tk.Frame(parent, bg=CARD,
                     highlightbackground=BORDER_H, highlightthickness=1)
        f.pack(fill=fill, expand=expand, pady=pady)
        return f

    def _card_header(self, card, text, color, right_txt=""):
        row = tk.Frame(card, bg=CARD)
        row.pack(fill="x", padx=10, pady=(8,2))
        tk.Label(row, text=text, font=self.F["head"],
                 fg=color, bg=CARD).pack(side="left")
        if right_txt:
            tk.Label(row, text=right_txt, font=self.F["small"],
                     fg=TEXT_D, bg=CARD).pack(side="right")
        return row

    def _btn(self, parent, text, fg, bg, abg, afg, cmd, padx=12, font=None):
        if font is None: font = self.F["body"]
        return tk.Button(parent, text=text, font=font,
                         fg=fg, bg=bg, activebackground=abg,
                         activeforeground=afg, relief="flat", bd=0,
                         padx=padx, pady=5, cursor="hand2", command=cmd)


    def _draw_diagram(self):
        cv = self.canvas
        cv.delete("all")
        self._draw_grid(cv)
        self._draw_all_arrows(cv)
        for s in ["S","A","B","C"]:
            self._draw_state(cv, s, active=(s == self._active_st))

    def _draw_grid(self, cv):
        step = 30
        for x in range(0, self.CW + 1, step):
            cv.create_line(x, 0, x, self.CH, fill="#0b1828", width=1)
        for y in range(0, self.CH + 1, step):
            cv.create_line(0, y, self.CW, y, fill="#0b1828", width=1)

    def _draw_state(self, cv, name, active=False):
        tag = f"st_{name}"
        cv.delete(tag)
        cx, cy = self.POS[name]
        r      = self.R
        idle_fill, idle_ring, act_fill, act_ring = STATE_THEME[name]

        fill = act_fill  if active else idle_fill
        ring = act_ring  if active else idle_ring

        if active:
            for gr, alpha in [(r+18, 0.07), (r+11, 0.13), (r+5, 0.22)]:
                gc = mix_hex(PANEL, ring, alpha)
                cv.create_oval(cx-gr, cy-gr, cx+gr, cy+gr,
                               fill=gc, outline="", tags=tag)

        cv.create_oval(cx-r, cy-r, cx+r, cy+r,
                       fill=fill, outline=ring,
                       width=2.5 if active else 1.5, tags=tag)

        if name in ACCEPT_STATES:
            ir = r - 7
            cv.create_oval(cx-ir, cy-ir, cx+ir, cy+ir,
                           fill="", outline=ring, width=1, tags=tag)

        cv.create_text(cx, cy, text=name,
                       font=("Courier New", 17, "bold"),
                       fill=ring, tags=tag)

        if name == "S":
            ax = cx - r - 32
            cv.create_line(ax, cy, cx - r - 2, cy,
                           fill=PURPLE, width=1.8,
                           arrow="last", arrowshape=(9,11,4), tags=tag)
            cv.create_text(ax - 4, cy - 11, text="start",
                           font=("Courier New", 7), fill=PURPLE, tags=tag)

    def _draw_all_arrows(self, cv):
        POS, R = self.POS, self.R

        def ep(a, b, off=0):
            ax, ay = POS[a]; bx, by = POS[b]
            if off:
                dx, dy = bx-ax, by-ay
                d = math.hypot(dx,dy) or 1
                ox, oy = -dy/d*off, dx/d*off
                ax,ay,bx,by = ax+ox,ay+oy,bx+ox,by+oy
            sx,sy = edge_pt(ax,ay,bx,by,R)
            ex,ey = edge_pt(bx,by,ax,ay,R)
            return sx,sy,ex,ey

        # S → A  (0)  — curved above
        self._curved_arrow(cv, *ep("S","A"), label="0",
                           bend=-55, color=TEXT_D)
        # S → B  (1)  — curved below
        self._curved_arrow(cv, *ep("S","B"), label="1",
                           bend=55, color=TEXT_D)
        # A → C  (0)  — straight, red (dead transition)
        self._straight_arrow(cv, *ep("A","C"), label="0", color=RED)
        # A → B  (1)  — downward, offset right
        self._straight_arrow(cv, *ep("A","B", off=9),  label="1", color=TEXT_D)
        # B → A  (0)  — upward, offset left
        self._straight_arrow(cv, *ep("B","A", off=-9), label="0", color=TEXT_D)
        # B self-loop (1)
        self._self_loop(cv, "B", "1", above=False, color=TEXT_D)
        # C self-loop (0,1)
        self._self_loop(cv, "C", "0,1", above=True, color=RED)

    def _arrowhead(self, cv, x1, y1, x2, y2, color):
        dx, dy = x2-x1, y2-y1
        d  = math.hypot(dx,dy) or 1
        ux, uy = dx/d, dy/d
        size = 9
        left  = (x2 - size*ux + size*0.38*uy,
                 y2 - size*uy - size*0.38*ux)
        right = (x2 - size*ux - size*0.38*uy,
                 y2 - size*uy + size*0.38*ux)
        cv.create_polygon((x2,y2), left, right,
                          fill=color, outline="")

    def _curved_arrow(self, cv, x1, y1, x2, y2, label, bend, color):
        mx, my = (x1+x2)/2, (y1+y2)/2
        dx, dy = x2-x1, y2-y1
        d = math.hypot(dx,dy) or 1
        px, py = -dy/d, dx/d
        cpx, cpy = mx + px*bend, my + py*bend

        pts = bezier3((x1,y1),
                      (x1*.33 + cpx*.67, y1*.33 + cpy*.67),
                      (cpx*.67 + x2*.33, cpy*.67 + y2*.33),
                      (x2,y2))
        cv.create_line(*pts, fill=color, width=1.6, smooth=True)
        self._arrowhead(cv, pts[-4],pts[-3], pts[-2],pts[-1], color)
        lx = .25*x1 + .5*cpx + .25*x2
        ly = .25*y1 + .5*cpy + .25*y2
        lx += px*12; ly += py*12
        cv.create_text(lx, ly, text=label,
                       font=("Courier New", 9, "bold"), fill=YELLOW)

    def _straight_arrow(self, cv, x1, y1, x2, y2, label, color):
        cv.create_line(x1,y1,x2,y2, fill=color, width=1.6)
        self._arrowhead(cv, x1,y1, x2,y2, color)
        # Perpendicular label offset
        dx, dy = x2-x1, y2-y1
        d = math.hypot(dx,dy) or 1
        px, py = -dy/d, dx/d
        mx, my = (x1+x2)/2 + px*11, (y1+y2)/2 + py*11
        cv.create_text(mx, my, text=label,
                       font=("Courier New", 9, "bold"), fill=YELLOW)

    def _self_loop(self, cv, name, label, above, color):
        cx, cy = self.POS[name]
        r  = self.R
        off = -52 if above else 52

        # Attachment points on the circle
        p0 = (cx - 18, cy + (-r if above else r))
        p3 = (cx + 18, cy + (-r if above else r))

        # Control points — splay outward
        cp_mult = 1.5 if above else 1.5
        p1 = (cx - 46, cy + off * cp_mult)
        p2 = (cx + 46, cy + off * cp_mult)

        pts = bezier3(p0, p1, p2, p3)
        cv.create_line(*pts, fill=color, width=1.6, smooth=True)
        self._arrowhead(cv, pts[-4],pts[-3], pts[-2],pts[-1], color)

        # Label at loop apex
        label_y = cy + off * 1.48
        cv.create_text(cx, label_y, text=label,
                       font=("Courier New", 9, "bold"), fill=YELLOW)

    def _highlight_state(self, name):
        """Redraw only the necessary states (fast)."""
        prev = self._active_st
        self._active_st = name
        if prev and prev != name:
            self._draw_state(self.canvas, prev, active=False)
        self._draw_state(self.canvas, name, active=True)

    def _reset_highlights(self):
        if self._active_st:
            self._draw_state(self.canvas, self._active_st, active=False)
            self._active_st = None

    def _redraw_result(self):
        """Called on resize or after a new result."""
        if not hasattr(self, "_last_result"):
            return
        accepted, s, final = self._last_result
        cv = self.res_canvas
        cv.delete("all")
        W  = cv.winfo_width() or 620
        H  = 58

        color  = GREEN if accepted else RED
        label  = "✓  ACCEPTED" if accepted else "✗  REJECTED"
        detail = (f'"{s}"  ∈  L   —   ends in accept state B'
                  if accepted else
                  f'"{s}"  ∉  L   —   {reject_reason(final, s)}')

        bg = mix_hex(BG, color, 0.07)
        cv.create_rectangle(0, 0, W, H, fill=bg, outline=color, width=1)
        cv.create_text(16, 18, text=label,
                       font=("Courier New",12,"bold"), fill=color, anchor="w")
        cv.create_text(16, 40, text=detail[:90],
                       font=("Courier New",8), fill=TEXT, anchor="w")


    def _show_trace(self, trace, s, accepted, final):
        t = self.trace_txt
        t.config(state="normal")
        t.delete("1.0","end")

        # Header
        t.insert("end",
                 f'  String: "{s}"   Steps: {len(trace)}   '
                 f'Final state: {final}\n', "hdr")
        sep = "  " + "─"*62 + "\n"
        t.insert("end", sep, "sep")
        t.insert("end",
                 f'  {"Step":>4}   {"From":^5}   {"Sym":^4}   {"To":^5}   Note\n', "hdr")
        t.insert("end", sep, "sep")

        # Initial state row
        t.insert("end", f'  {"0":>4}   ', "hdr")
        t.insert("end", f'{"─":^5}', "sep")
        t.insert("end", f'   {"─":^4}', "sep")
        t.insert("end", f'   {"S":^5}', "s_S")
        t.insert("end", "   (start)\n", "hdr")

        # Transition rows
        for step, frm, sym, to in trace:
            note_tag = "ok" if to in ACCEPT_STATES else \
                       "bad" if to in DEAD_STATES else \
                       ("warn" if to=="A" else "hdr")
            note = ("✓ in accept state" if to in ACCEPT_STATES else
                    "✗ DEAD — '00' detected!" if to in DEAD_STATES else
                    "last='0'" if to=="A" else "")

            t.insert("end", f"  {step:>4}   ", "hdr")
            t.insert("end", f"{frm:^5}", f"s_{frm}")
            t.insert("end", f"   {sym:^4}", "sym")
            t.insert("end", f"   {to:^5}", f"s_{to}")
            t.insert("end", f"   {note}\n", note_tag)

        t.insert("end", sep, "sep")
        verdict = (f'  ✓ ACCEPTED  —  "{s}" is a member of L\n' if accepted else
                   f'  ✗ REJECTED  —  {reject_reason(final, s)}\n')
        t.insert("end", verdict, "ok" if accepted else "bad")
        t.config(state="disabled")

    def _start_animation(self):
        if self._anim_job:
            self.root.after_cancel(self._anim_job)
        self.btn_anim.config(state="disabled")
        self._reset_highlights()
        self._highlight_state(START_STATE)
        self._anim_idx = 0
        self._anim_tick()

    def _anim_tick(self):
        if self._anim_idx >= len(self._last_trace):
            self.btn_anim.config(state="normal")
            return
        _, _, _, to = self._last_trace[self._anim_idx]
        self._highlight_state(to)
        self._anim_idx += 1
        self._anim_job = self.root.after(self.ANIM_MS, self._anim_tick)

    def _run(self):
        if self._anim_job:
            self.root.after_cancel(self._anim_job)
            self._anim_job = None

        s   = self.inp_var.get().strip()
        err = fsm_validate(s)
        if err:
            self.lbl_err.config(text=f"  ⚠  {err}")
            return
        self.lbl_err.config(text="")

        accepted, final, trace = fsm_run(s)
        self._last_trace  = trace
        self._last_result = (accepted, s, final)

        # Show result banner
        self.root.update_idletasks()
        self._redraw_result()

        # Trace log
        self._show_trace(trace, s, accepted, final)

        # Diagram: highlight final state
        self._reset_highlights()
        final_st = trace[-1][3] if trace else START_STATE
        self._highlight_state(final_st)

        # History & stats
        self.history.insert(0, (s, accepted))
        self._refresh_history()
        self.stats["total"]  += 1
        self.stats["accept"] += int(accepted)
        self.stats["reject"] += int(not accepted)
        self._update_stats()

        self.btn_anim.config(state="normal")
        self.inp_var.set("")
        self.entry.focus_set()

    def _clear(self):
        if self._anim_job:
            self.root.after_cancel(self._anim_job)
            self._anim_job = None
        self.inp_var.set("")
        self.lbl_err.config(text="")
        self.trace_txt.config(state="normal")
        self.trace_txt.delete("1.0","end")
        self.trace_txt.config(state="disabled")
        self.res_canvas.delete("all")
        self._reset_highlights()
        self.btn_anim.config(state="disabled")
        if hasattr(self, "_last_result"):
            del self._last_result
        self.entry.focus_set()

    def _refresh_history(self):
        t = self.hist_txt
        t.config(state="normal")
        t.delete("1.0","end")
        for s, ok in self.history[:30]:
            badge = " ACC " if ok else " REJ "
            t.insert("end", badge, "acc" if ok else "rej")
            t.insert("end", f"  {s}\n", "s")
        t.config(state="disabled")
        t.see("1.0")

    def _clear_history(self):
        self.history.clear()
        self.hist_txt.config(state="normal")
        self.hist_txt.delete("1.0","end")
        self.hist_txt.config(state="disabled")

    def _update_stats(self):
        st = self.stats
        self.lbl_stats.config(
            text=f"Tested: {st['total']}   "
                 f"✓ {st['accept']}   "
                 f"✗ {st['reject']}")

    def _on_input_change(self, *_):
        bad = set(self.inp_var.get()) - {"0","1"}
        self.lbl_err.config(
            text=f"  ⚠  Invalid character: '{next(iter(bad))}'" if bad else "")

if __name__ == "__main__":
    root = tk.Tk()
    app  = FSMApp(root)
    root.mainloop()