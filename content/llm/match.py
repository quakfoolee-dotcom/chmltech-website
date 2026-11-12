"""Map a model name as a benchmark writes it to a catalogue id plus a setting label."""
import re
from catalog import CATALOG

SETTING = {"thinking", "think", "reasoning", "non", "nonreasoning", "high", "xhigh", "max", "low", "medium", "minimal", "default", "fallback",
           "effort", "extended", "adaptive", "it", "instruct", "bf16", "fp8", "fp4", "chat", "latest", "full", "beta", "a", "b", "with", "tools", "no",
           "budget", "k", "tokens", "standard", "reasoner", "mode", "on", "off", "auto", "api", "none", "bf"}
PREFIX = {"openai", "anthropic", "google", "xai", "meta", "mistralai", "deepseek", "deepseek-ai", "qwen", "moonshotai", "zai", "zai-org", "minimax",
          "minimaxai", "nvidia", "microsoft", "ibm", "ibm-granite", "x-ai", "meta-models", "cohere", "coherelabs", "amazon"}


def norm(s):
    s = s.lower().replace("‑", "-")
    s = re.sub(r"^([a-z0-9-]+)[/:]\s*", lambda m: "" if m.group(1) in PREFIX or True else m.group(0), s)  # drop "openai/" or "OpenAI: "
    s = re.sub(r"[\(\)\[\],]", " ", s)
    s = re.sub(r"[-_.:/]+", " ", s)
    s = re.sub(r"(?<=[a-z])(?=\d)|(?<=\d)(?=[a-z])", " ", s)  # qwen3 -> qwen 3, v4 -> v 4, 31b -> 31 b
    return s.split()


IDX = []
for m in CATALOG:
    for a in m["aliases"] + [m["name"]]:
        IDX.append((norm(a), m["id"]))
IDX.sort(key=lambda t: -len(t[0]))  # longest alias first


def ok_rest(toks):
    for t in toks:
        if t in SETTING or (t.isdigit() and (len(t) >= 4 or t in ("1", "2", "3", "4", "5", "8", "16", "32", "64", "128"))):
            continue
        return False
    return True


def match(name):
    t = norm(name)
    for a, mid in IDX:
        if t[:len(a)] == a and ok_rest(t[len(a):]):
            rest = [x for x in t[len(a):] if not (x.isdigit() and len(x) >= 4) and x not in ("default", "fallback", "bf", "16", "it")]
            return mid, (" ".join(rest).capitalize().replace("Xhigh", "X-high").replace("Non reasoning", "Non-reasoning") if rest else None)
    return None, None
