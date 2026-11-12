"""Map a model name as a benchmark writes it to a catalogue id plus a setting label.

Rules (written down after the red-team review, V4.50):
  - A name matches a catalogue alias when it starts with the alias and every remaining word is a reasoning-effort or
    format word (SETTING), a named host (HOSTS) or a snapshot date (4+ digits).
  - Developer or host prefixes ("openai/", "Anthropic: ", "baseten/") are stripped only when they are known (PREFIX, HOSTS).
  - Hosted runs are kept and labelled "via <host>". Quantised builds (FP8, FP4, NVFP4) never match.
  - Snapshot dates are kept in the label ("0902 snapshot"). A catalogue entry may list the snapshots it accepts in
    `snapshots`; rows carrying any other date are rejected, so an earlier or preview build is not folded in.
  - EXCLUDE lists source names that look like a catalogue model but are a different product.
"""
import re
from catalog import CATALOG

SETTING = {"thinking", "think", "reasoning", "non", "nonreasoning", "high", "xhigh", "max", "low", "medium", "minimal", "default", "fallback",
           "effort", "extended", "adaptive", "it", "instruct", "bf", "16", "chat", "latest", "beta", "a", "b", "with", "tools", "no",
           "budget", "k", "tokens", "standard", "reasoner", "mode", "on", "off", "auto", "api", "none", "oss", "v", "1", "0"}
HOSTS = {"together": "Together", "baseten": "Baseten", "fireworks": "Fireworks", "deepinfra": "DeepInfra", "groq": "Groq"}
PREFIX = {"openai", "anthropic", "google", "xai", "x-ai", "grok", "meta", "meta-models", "mistralai", "mistral", "deepseek", "deepseek-ai", "qwen", "alibaba",
          "moonshotai", "kimi", "zai", "zai-org", "z-ai", "minimax", "minimaxai", "nvidia", "microsoft", "ibm", "ibm-granite", "cohere", "coherelabs",
          "amazon", "xiaomi", "stepfun", "stepfun-ai", "tencent", "thinkingmachines", "thinking machines", "reflection", "inclusionai", "liquidai"} | set(HOSTS)
QUANT = re.compile(r"\b(nv)?fp ?[48]\b|\bnvfp4\b|\bint[48]\b|\bawq\b|\bgguf\b", re.I)

EXCLUDE = {
    "Muse Wonder Full", "Muse Wonder Full (Max)", "meta/muse-wonder-full",          # Muse Code only, not on the API
    "Mistral Large 4 Preview", "Mistral Large 4 Preview (high)", "mistral-large-4-0_high",  # preview build (Epoch id)
}
EXCLUDE_BOARD = {("LiveBench", "Mistral Large 4"), ("LiveBench", "Mistral Large 4 1029")}


def norm(s):
    s = s.lower().replace("‑", "-")
    m = re.match(r"^\s*([a-z0-9 -]+?)\s*[/:]\s*", s)
    host = None
    if m and m.group(1) in PREFIX:
        host = HOSTS.get(m.group(1))
        s = s[m.end():]
    s = re.sub(r"[\(\)\[\],+]", " ", s)
    s = re.sub(r"[-_.:/]+", " ", s)
    s = re.sub(r"(?<=[a-z])(?=\d)|(?<=\d)(?=[a-z])", " ", s)  # qwen3 -> qwen 3, v4 -> v 4, 31b -> 31 b
    return s.split(), host


IDX = []
for m in CATALOG:
    for a in m["aliases"] + [m["name"]]:
        IDX.append((norm(a)[0], m))
IDX.sort(key=lambda t: -len(t[0]))  # longest alias first


def match(name, board=""):
    # LiveBench lists two different "Mistral Large 4" entries and which is the released model is unconfirmed, so neither is used.
    if name in EXCLUDE or any(board.startswith(b) and name == n for b, n in EXCLUDE_BOARD):
        return None, None
    if QUANT.search(name):
        return None, None
    t, host = norm(name)
    for a, m in IDX:
        if t[:len(a)] != a:
            continue
        rest, snaps, ok = [], [], True
        for x in t[len(a):]:
            if x.isdigit() and len(x) >= 4:
                snaps.append(x)
            elif x in HOSTS:
                host = HOSTS[x]
            elif x in SETTING:
                if x not in ("default", "fallback", "bf", "16", "it", "oss", "v", "1", "0", "a", "b", "api", "instruct", "chat", "latest"):
                    rest.append(x)
            else:
                ok = False; break
        if not ok:
            continue
        allowed = m.get("snapshots")
        if allowed is not None and any(s not in allowed for s in snaps):
            return None, None
        label = " ".join(rest).capitalize().replace("Xhigh", "X-high").replace("Non reasoning", "Non-reasoning") if rest else ""
        if snaps and m.get("show_snapshot"):
            label = (label + ", " if label else "") + snaps[-1][-4:] + " snapshot"
        if host:
            label = (label + ", " if label else "") + "via " + host
        return m["id"], (label or None)
    return None, None
