"""Figure 1 of Vol. 106, Issue 1 (multi-agent orchestration): one data source, two outputs.

  - content/journal/live/orch5.html   the interactive explorer (data as JSON; script assets/js/orch5.js; styles: the
                                       "Vol. 106 orch5" block at the end of assets/css/journal.css)
  - content/journal/figures/<slug>/fig1-five-models.svg   the static version, used for print, the PDF and readers without script

Run: python3 -I content/journal/figure-scripts/orch5.py
Every property shown comes from Tables 1-3 of the paper. Bid values in the contract-net walk-through are illustrative.
"""
import html, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "..")
SLUG = "multi-agent-ai-orchestration-architectures-five-coordination-models-compared"
E = lambda s: html.escape(s, quote=True)

# Diagram coordinates live in a 560 x 330 box. Node kinds: req (request), lead, sup, agent, gate, board, ledger.
MODELS = [
    dict(id="central", n=1, name="Centralized orchestrator", short="Centralized", color="#0B6FA4", kind="Control topology",
         nodes=[("req", 70, 110, "Request", "req"), ("L", 280, 110, "Orchestrator", "lead"), ("G", 490, 110, "Release gate", "gate"),
                ("W1", 100, 255, "Worker 1", "agent"), ("W2", 220, 255, "Worker 2", "agent"), ("W3", 340, 255, "Worker 3", "agent"), ("W4", 460, 255, "Worker 4", "agent")],
         edges=[("req", "L"), ("L", "G"), ("L", "W1"), ("L", "W2"), ("L", "W3"), ("L", "W4")],
         steps=[("Request arrives", "The goal goes to one orchestrator, which owns it until release.", [("req", "L", "")], ["L"]),
                ("Decompose and dispatch", "The orchestrator splits the goal into typed tasks and sends them out in parallel.", [("L", w, "task") for w in ("W1", "W2", "W3", "W4")], ["L"]),
                ("Workers execute", "Each worker sees only its own task and context. Workers do not talk to each other.", [], ["W1", "W2", "W3", "W4"]),
                ("Artifacts return", "Results come back to the lead as artifact references, not long transcripts.", [(w, "L", "") for w in ("W1", "W2", "W3", "W4")], ["L"]),
                ("Verify and synthesize", "The lead checks each result against its contract and combines the verified ones. It is also the bottleneck.", [], ["L"]),
                ("Release", "An independent gate, often a person, authorizes the result.", [("L", "G", "")], ["G"])],
         control="One accountable lead", comm="Star: lead to workers and back", state="Lead-owned ledger and worker artifacts",
         alloc="Fixed or rule-based routing by the lead", fit="Controlled delivery and source-based synthesis",
         hazard="Lead bottleneck; misdelegation", key="Durable checkpoints, leader failover, idempotent workers",
         combine="Add a blackboard for shared evidence, or contract net for a variable specialist pool."),
    dict(id="hier", n=2, name="Hierarchical orchestration", short="Hierarchical", color="#4D7F12", kind="Control topology",
         nodes=[("req", 70, 45, "Request", "req"), ("T", 280, 45, "Program lead", "lead"), ("G", 490, 45, "Release gate", "gate"),
                ("SA", 160, 145, "Engineering sup.", "sup"), ("SB", 400, 145, "Commercial sup.", "sup"),
                ("A1", 95, 260, "Agent A1", "agent"), ("A2", 225, 260, "Agent A2", "agent"), ("B1", 335, 260, "Agent B1", "agent"), ("B2", 465, 260, "Agent B2", "agent")],
         edges=[("req", "T"), ("T", "G"), ("T", "SA"), ("T", "SB"), ("SA", "A1"), ("SA", "A2"), ("SB", "B1"), ("SB", "B2")],
         steps=[("Request arrives", "The program lead owns the whole deliverable.", [("req", "T", "")], ["T"]),
                ("Delegate workstreams", "Each domain goes to a supervisor with its own permissions, budget and validation rules.", [("T", "SA", "domain"), ("T", "SB", "domain")], ["SA", "SB"]),
                ("Supervisors assign", "Supervisors split their domain among their own specialists. Depth is capped.", [("SA", "A1", ""), ("SA", "A2", ""), ("SB", "B1", ""), ("SB", "B2", "")], ["A1", "A2", "B1", "B2"]),
                ("Results go up one level", "Specialists report to their supervisor, who checks them against domain rules.", [("A1", "SA", ""), ("A2", "SA", ""), ("B1", "SB", ""), ("B2", "SB", "")], ["SA", "SB"]),
                ("Summaries go up again", "Each layer condenses. Source artifacts must travel with the summary or evidence is lost.", [("SA", "T", "summary"), ("SB", "T", "summary")], ["T"]),
                ("Release", "The program lead resolves cross-domain conflicts and passes the result to the gate.", [("T", "G", "")], ["G"])],
         control="Supervisors at several levels", comm="Tree: down and up through each level", state="Tiered state and summaries",
         alloc="Each supervisor routes within its domain", fit="Several distinct domains or teams",
         hazard="Summary loss; management overhead", key="Direct artifact references, maximum delegation depth",
         combine="Add a blackboard so specialists in different branches share one evidence record."),
    dict(id="mesh", n=3, name="Decentralized mesh", short="Mesh", color="#6A4C93", kind="Control topology",
         nodes=[("req", 60, 165, "Request", "req"), ("P1", 280, 60, "Peer 1", "agent"), ("P2", 385, 132, "Peer 2", "agent"), ("P3", 345, 262, "Peer 3", "agent"),
                ("P4", 215, 262, "Peer 4", "agent"), ("P5", 175, 132, "Peer 5", "agent"), ("R", 470, 308, "System of record", "ledger")],
         edges=[("req", "P5"), ("P1", "P2"), ("P1", "P3"), ("P1", "P4"), ("P1", "P5"), ("P2", "P3"), ("P2", "P4"), ("P2", "P5"), ("P3", "P4"), ("P3", "P5"), ("P4", "P5"), ("P3", "R")],
         steps=[("Request reaches a peer", "Any authorized peer can take work in. There is no permanent leader.", [("req", "P5", "")], ["P5"]),
                ("Handoff (hop 1)", "Peer 5 hands responsibility to the peer it judges best placed.", [("P5", "P1", "hop 1")], ["P1"]),
                ("Peers exchange evidence (hop 2)", "Peers message each other directly. Five peers already have 20 possible directed links.", [("P1", "P2", "hop 2"), ("P1", "P4", "hop 2")], ["P2", "P4"]),
                ("Further handoffs (hop 3)", "Without an owner ledger, work can circle back or be done twice.", [("P2", "P3", "hop 3"), ("P4", "P3", "hop 3")], ["P3"]),
                ("Hop budget reached", "A global stopping rule ends the exchange; one peer is recorded as owner.", [], ["P3"]),
                ("Record the outcome", "The decision goes to a system of record, so state does not live only in messages.", [("P3", "R", "")], ["R"])],
         control="Distributed peers and a shared protocol", comm="Direct peer-to-peer messages", state="Federated or shared state",
         alloc="Peers hand work to one another", fit="Dynamic, heterogeneous peer collaboration",
         hazard="Cycles, conflicting owners, uncontrolled chatter", key="Hop budget, owner ledger, stopping rules",
         combine="Keep consequential actions behind an approval gate; the mesh only recommends."),
    dict(id="board", n=4, name="Blackboard", short="Blackboard", color="#B8611D", kind="Mechanism: information sharing",
         nodes=[("S", 280, 40, "Scheduler", "lead"), ("B", 280, 165, "Blackboard", "board"),
                ("K1", 85, 85, "Researcher", "agent"), ("K2", 475, 85, "Analyst", "agent"), ("K3", 85, 260, "Calculator", "agent"), ("K4", 475, 260, "Reviewer", "agent")],
         edges=[("S", "B"), ("K1", "B"), ("K2", "B"), ("K3", "B"), ("K4", "B"), ("S", "K4")],
         steps=[("Post the problem", "The problem record is written to a shared, versioned workspace.", [("S", "B", "v1")], ["B"], "v1"),
                ("A specialist reads and writes", "The researcher reads what is relevant and adds a hypothesis with its source.", [("B", "K1", "read"), ("K1", "B", "write")], ["K1"], "v2"),
                ("Subscribers are notified", "Agents subscribed to that topic hear about the change; nobody broadcasts transcripts.", [("B", "K2", "event"), ("B", "K3", "event")], ["K2", "K3"], "v2"),
                ("Opportunistic contributions", "Two agents write at once. Versions and a concurrency check stop one silently overwriting the other.", [("K2", "B", "write"), ("K3", "B", "write")], ["B"], "v4"),
                ("Scheduler picks who acts next", "Control is a separate decision: the scheduler asks the reviewer to check the evidence.", [("S", "K4", "act")], ["K4"], "v4"),
                ("Verify before use", "The reviewer marks entries verified or retracts them; untrusted content never becomes fact by default.", [("K4", "B", "verify")], ["B"], "v5")],
         control="A separate scheduler or event-driven", comm="Publish–subscribe through the board", state="Shared, versioned workspace",
         alloc="Agents act when the board holds work they can do", fit="Knowledge-intensive collaboration",
         hazard="Stale or corrupted shared state", key="Provenance, validation, access control, versions, rollback",
         combine="Runs inside a centralized, hierarchical or mesh topology; it decides where state lives, not who is in charge."),
    dict(id="cnet", n=5, name="Contract net (market-based)", short="Contract net", color="#A8324F", kind="Mechanism: task allocation",
         nodes=[("req", 70, 55, "Request", "req"), ("M", 280, 55, "Manager", "lead"),
                ("C1", 100, 260, "Bidder 1", "agent"), ("C2", 220, 260, "Bidder 2", "agent"), ("C3", 340, 260, "Bidder 3", "agent"), ("C4", 460, 260, "Bidder 4", "agent")],
         edges=[("req", "M"), ("M", "C1"), ("M", "C2"), ("M", "C3"), ("M", "C4")],
         steps=[("Work package arrives", "The manager writes the task requirements and objective bid fields.", [("req", "M", "")], ["M"]),
                ("Announce", "The task is announced to every potential contractor.", [("M", c, "announce") for c in ("C1", "C2", "C3", "C4")], ["C1", "C2", "C3", "C4"]),
                ("Check eligibility", "Bidder 4 lacks the required tool access and is excluded before any bid is compared.", [], ["C4"], None, ["C4"]),
                ("Bids return", "Eligible bidders reply with cost, duration and evidence of capability (illustrative values).", [("C1", "M", "$6 · 40 s"), ("C2", "M", "$4 · 30 s"), ("C3", "M", "$5 · 55 s")], ["M"], None, ["C4"]),
                ("Award", "The manager scores the bids by a recorded rule and awards the task.", [("M", "C2", "award")], ["C2"], None, ["C4"]),
                ("Execute and report", "The contractor delivers. A timeout triggers re-award if it does not.", [("C2", "M", "result")], ["M"], None, ["C4"])],
         control="Task announcer plus eligible bidders", comm="Announce, bid, award, execute", state="Award record held by the manager",
         alloc="Capability bidding and award", fit="Scarce or variable specialist resources",
         hazard="Auction overhead; poor bid signals", key="Eligibility checks, auditable scoring, timeouts, re-award",
         combine="Runs inside any topology; the announcer can itself be a central lead. Bidding is not decentralization."),
]


def data(models=None, profile=None):
    out = []
    for m in (models or MODELS):
        steps = []
        for s in m["steps"]:
            t, d, msgs, hl = s[:4]
            steps.append(dict(t=t, d=d, msgs=[list(x) for x in msgs], hl=hl, board=s[4] if len(s) > 4 else None, dim=s[5] if len(s) > 5 else []))
        out.append(dict(id=m["id"], n=m["n"], name=m["name"], short=m["short"], color=m["color"], kind=m["kind"],
                        nodes=[dict(id=n[0], x=n[1], y=n[2], label=n[3], k=n[4], **({"g": n[5]} if len(n) > 5 else {})) for n in m["nodes"]], edges=m["edges"], steps=steps,
                        profile=[[lab, m[k]] for lab, k in (profile or [("Control", "control"), ("Communication", "comm"), ("Shared state", "state"), ("Allocation", "alloc")])],
                        fit=m["fit"], hazard=m["hazard"], key=m["key"], combine=m["combine"]))
    return out


ORCH_LABELS = dict(group="Choose an orchestration model, or compare all five side by side", all_name="Compare all", all_kind="Side by side",
                   note="All five models side by side. Choose a model above to watch it step by step.",
                   notes=("Best fit", "Chief hazard", "Key controls"), combine="Combines with",
                   tabkind=lambda m: "Topology" if m["kind"].startswith("Control") else "Mechanism",
                   card_rows=(("Control", "control"), ("Communication", "comm"), ("State", "state"), ("Allocation", "alloc"), ("Chief hazard", "hazard")))


def live_html(models=None, L=None, profile=None):
    models, L = models or MODELS, L or ORCH_LABELS
    tabs = "".join(
        f'<button type="button" class="o5-tab" id="o5-tab-{m["id"]}" aria-pressed="false" data-m="{m["id"]}" style="--c:{m["color"]}">'
        f'<span class="o5-tab-n">{m["n"]}</span><span class="o5-tab-name">{E(m["short"])}</span>'
        f'<span class="o5-tab-kind">{L["tabkind"](m)}</span></button>' for m in models)
    tabs += ('<button type="button" class="o5-tab o5-tab-all" id="o5-tab-all" aria-pressed="false" data-m="all">'
             f'<span class="o5-tab-n">&#9638;</span><span class="o5-tab-name">{L["all_name"]}</span><span class="o5-tab-kind">{L["all_kind"]}</span></button>')
    cards = "".join(
        f'<article class="o5-card" style="--c:{m["color"]}"><header><span>{m["n"]} · {L["tabkind"](m)}</span>'
        f'<h4>{E(m["name"])}</h4></header><svg viewBox="0 0 230 140" aria-hidden="true">{mini(m, 10, 8)}</svg><dl>'
        + "".join(f'<div{" class=haz" if lab == L["card_rows"][-1][0] else ""}><dt>{lab}</dt><dd>{E(v)}</dd></div>' for lab, v in
                  ((lab, m[k]) for lab, k in L["card_rows"]))
        + '</dl></article>' for m in models)
    return f'''<div class="o5" id="o5" hidden>
<div class="o5-tabs{" o5-many" if len(models) >= 7 else ""}" role="group" aria-label="{L["group"]}" style="--o5n:{len(models)}">{tabs}</div>
<div class="o5-compare" id="o5-compare" hidden><p class="o5-compare-note">{L["note"]}</p><div class="o5-cards" style="--o5c:{len(models) if len(models) <= 5 else 4}">{cards}</div></div>
<div class="o5-panel" id="o5-panel">
<div class="o5-head"><p class="o5-kind" id="o5-kind"></p><h3 class="o5-name" id="o5-name"></h3></div>
<div class="o5-main">
<div class="o5-stage"><svg class="o5-svg" id="o5-svg" viewBox="0 0 560 330" role="img" aria-labelledby="o5-svg-t"><title id="o5-svg-t">Diagram of the selected orchestration model</title></svg></div>
<div class="o5-steps">
<ol class="o5-list" id="o5-list"></ol>
<p class="o5-desc" id="o5-desc" aria-live="polite"></p>
<div class="o5-ctrl"><span class="o5-count" id="o5-count"></span></div>
<div class="o5-prog" aria-hidden="true"><span id="o5-bar"></span></div>
</div>
</div>
<dl class="o5-prof" id="o5-prof"></dl>
<div class="o5-notes">
<p><b>{L["notes"][0]}</b><span id="o5-fit"></span></p>
<p><b>{L["notes"][1]}</b><span id="o5-haz"></span></p>
<p><b>{L["notes"][2]}</b><span id="o5-key"></span></p>
</div>
<p class="o5-combine" id="o5-combine" data-label="{L["combine"]}"></p>
</div>
<script type="application/json" id="o5-data">{json.dumps(data(models, profile), ensure_ascii=False)}</script>
</div>
<script src="../assets/js/orch5.js" defer></script>
'''


# ---------- static SVG ----------
NODE_FILL = {"req": "#FFFFFF", "lead": "#0B2A5A", "sup": "#13366E", "agent": "#FFFFFF", "gate": "#FFFFFF", "board": "#FFF7EC", "ledger": "#F3F1EC"}


def wrap(s, n):
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n and cur: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    return lines + [cur]


def mini(m, ox, oy):
    """Small diagram of model m in a 210 x 124 box at (ox, oy), as SVG elements."""
    c, k, s = m["color"], 210 / 560, []
    P = {n[0]: (ox + n[1] * k, oy + n[2] * k) for n in m["nodes"]}
    kinds = {n[0]: n[4] for n in m["nodes"]}
    for a, b in m["edges"]:
        (x1, y1), (x2, y2) = P[a], P[b]
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#A9B6C6" stroke-width="1.2"/>')
    for a, (x, y) in P.items():
        kk = kinds[a]
        if kk == "board":
            s.append(f'<rect x="{x - 26:.1f}" y="{y - 13:.1f}" width="52" height="26" rx="4" fill="#FFF7EC" stroke="{c}" stroke-width="1.6"/>')
        elif kk in ("req", "gate", "ledger"):
            f = a == m.get("focus")   # the focus node is filled in the model colour, whatever its shape
            s.append(f'<rect x="{x - 9:.1f}" y="{y - 7:.1f}" width="18" height="14" rx="3" fill="{c if f else "#F3F1EC"}" stroke="{c if f else "#8A94A6"}" stroke-width="1.1"/>')
        elif kk in ("lead", "sup"):
            if a == m.get("focus"): s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{15 if kk == "lead" else 13}" fill="none" stroke="{c}" stroke-width="1.6"/>')
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{11 if kk == "lead" else 9}" fill="{c}"/>')
        elif a == m.get("focus"):
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8.5" fill="{c}"/>')
        else:
            dim = m["id"] == "cnet" and a == "C4"
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7.5" fill="#FFFFFF" stroke="{"#B8C1CC" if dim else c}" stroke-width="1.8"{" stroke-dasharray=\"2 2\"" if dim else ""}/>')
    return "".join(s)


def static_svg(models=None, rows=None, tabkind=None, PH=400):
    models = models or MODELS
    rows = rows or (("Control", "control"), ("Communication", "comm"), ("State", "state"), ("Chief hazard", "hazard"))
    tabkind = tabkind or ORCH_LABELS["tabkind"]
    PW = 230
    W = 6 + len(models) * (PW + 9)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {PH}" font-family="Inter, Segoe UI, Arial, sans-serif">']
    s.append('<defs><marker id="o5a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="#5A6B82"/></marker></defs>')
    for i, m in enumerate(models):
        x0 = 6 + i * (PW + 9)
        c = m["color"]
        s.append(f'<g transform="translate({x0},0)">')
        s.append(f'<rect x="0" y="0" width="{PW}" height="{PH - 2}" rx="10" fill="#FFFFFF" stroke="#DDE6F0"/>')
        s.append(f'<path d="M0 10a10 10 0 0 1 10-10h{PW - 20}a10 10 0 0 1 10 10v44h-{PW}z" fill="{c}"/>')
        s.append(f'<text x="14" y="24" fill="#FFFFFF" font-size="12" font-weight="700" opacity=".85">{m["n"]} · {tabkind(m).upper()}</text>')
        s.append(f'<text x="14" y="44" fill="#FFFFFF" font-size="15.5" font-weight="700">{E(m["short"] if len(m["name"]) > 24 else m["name"])}</text>')
        s.append(mini(m, 10, 66))
        y = 214
        for lab, val in ((lab, m[k]) for lab, k in rows):
            s.append(f'<text x="14" y="{y}" fill="{c if lab != rows[-1][0] else "#9A3412"}" font-size="10.5" font-weight="700" letter-spacing=".04em">{lab.upper()}</text>')
            y += 16
            for ln in wrap(val, 32):
                s.append(f'<text x="14" y="{y}" fill="#26324A" font-size="12.5">{E(ln)}</text>'); y += 16
            y += 9
        s.append('</g>')
    s.append('</svg>')
    return "\n".join(s)


if __name__ == "__main__":
    os.makedirs(os.path.join(J, "live"), exist_ok=True)
    open(os.path.join(J, "live", "orch5.html"), "w", encoding="utf-8").write(live_html())
    d = os.path.join(J, "figures", SLUG); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "fig1-five-models.svg"), "w", encoding="utf-8").write(static_svg())
    print("wrote live/orch5.html and fig1-five-models.svg")
