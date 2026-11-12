"""Insights article: building a private, local LLM assistant with AnythingLLM and Ollama.

Usage:  python3 content/articles/anythingllm_article.py
Writes content/articles/<slug>.json. Then build the page with
        python3 content/gen/add_article.py <slug>

Figures are inline SVG built with the helpers in feed_articles.py. The "settings screen" figures are
simplified redrawings of the AnythingLLM Desktop settings panels, not captured screenshots.
Table and layout styles come from assets/css/oee.css.
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from feed_articles import (nowrap, svg, fig, box, txt, arrow, DEFS, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, PURPLE, RED,
                           MUTED, LINE, SAND, PALE, GREENF, ORANGEF)

SLUG = "private-ai-assistant-on-your-own-pc-anythingllm-and-ollama"
RAGP = "retrieval-augmented-generation-design-evaluation-and-failure-analysis"
AIOS = "ai-operating-systems-architecture-and-governance-for-enterprise-ai"
COST = "score-versus-cost-per-task-returns-to-reasoning-effort-in-frontier-language-models"
WHITE, DARK, DARK2, DTXT, DMUT = "#FFFFFF", "#1E2430", "#2A3140", "#E8ECF2", "#9AA5B8"

# Worked numbers for the chunking table and figure
DOC_CHARS, OVERLAP, SNIPPETS = 300_000, 20, 4          # a 100-page manual at about 3,000 characters a page
SIZES = [500, 1000, 2000, 4000]
def n_chunks(size, ov=OVERLAP, n=DOC_CHARS): return math.ceil((n - ov) / (size - ov))


# ───────────────────────── Figure 1: the architecture on one PC ─────────────────────────
def fig_arch():
    s = DEFS
    s += f'<rect x="10" y="30" width="700" height="300" rx="12" fill="{WHITE}" stroke="{NAVY}" stroke-width="1.6"/>'
    s += txt(26, 52, "Your Windows PC: nothing below this line needs the internet", fill=NAVY, fs=13, bold=True)
    # AnythingLLM block
    s += f'<rect x="26" y="66" width="404" height="248" rx="10" fill="{PALE}" stroke="#9AB0C8"/>'
    s += txt(40, 88, "AnythingLLM Desktop (the front end)", fill=BLUE, bold=True)
    s += box(40, 100, 116, 54, ["Workspaces", "and chat"], fill=WHITE)
    s += box(170, 100, 116, 54, ["Document", "collector"], fill=WHITE)
    s += box(300, 100, 116, 54, ["Text splitter", "(chunking)"], fill=WHITE)
    s += box(40, 176, 116, 54, ["Agent and", "skills"], fill=WHITE)
    s += box(170, 176, 246, 54, ["LanceDB vector database", "(built in, files on disk)"], fill=GREENF, stroke=GREEND)
    s += box(40, 250, 376, 50, ["Storage folder: documents, vectors, chats, settings"], fill=SAND, stroke=LINE, fs=12.5)
    s += arrow(286, 127, 298, 127) + arrow(358, 154, 358, 174)
    # Ollama block
    s += f'<rect x="452" y="66" width="242" height="248" rx="10" fill="{ORANGEF}" stroke="{ORANGE}"/>'
    s += txt(466, 88, "Ollama (the model runner)", fill=ORANGE, bold=True)
    s += txt(466, 106, "http://127.0.0.1:11434", fill=MUTED, fs=12)
    s += box(466, 120, 214, 62, ["Chat model", "gemma4:12b on the RTX 5070"], fill=WHITE, stroke=ORANGE)
    s += box(466, 198, 214, 62, ["Embedding model", "embeddinggemma"], fill=WHITE, stroke=ORANGE)
    s += txt(573, 290, "GPU: 12 GB VRAM", "middle", MUTED, 12)
    s += f'<line x1="416" y1="140" x2="464" y2="150" stroke="{NAVY}" stroke-width="1.6" marker-end="url(#ah)" marker-start="url(#ah)"/>'
    s += f'<line x1="416" y1="214" x2="464" y2="226" stroke="{NAVY}" stroke-width="1.6" marker-end="url(#ah)" marker-start="url(#ah)"/>'
    # Optional cloud
    s += f'<rect x="60" y="356" width="600" height="44" rx="10" fill="none" stroke="{MUTED}" stroke-dasharray="6 4"/>'
    s += txt(360, 383, "Optional and off by default here: cloud LLMs, web browsing, MCP servers, telemetry", "middle", MUTED, 12.5)
    s += f'<line x1="360" y1="332" x2="360" y2="354" stroke="{MUTED}" stroke-width="1.4" stroke-dasharray="4 3"/>'
    return svg("Block diagram of one Windows PC. AnythingLLM Desktop holds workspaces, a document collector, the text splitter, the agent and the "
               "built-in LanceDB vector database, all saved to a local storage folder. It talks to Ollama at 127.0.0.1 port 11434, which runs "
               "the gemma4 12B chat model and the embeddinggemma embedding model on the RTX 5070 GPU. Cloud services are shown outside the PC, "
               "dashed, as optional.", 720, 410, s, 600, x0=2)


# ───────────────────────── Figure 2: the two RAG pipelines ─────────────────────────
def fig_rag():
    s = DEFS
    s += txt(10, 22, "A. Once per document: ingestion", fill=BLUE, bold=True)
    steps = [["Upload", "PDF, Word,", "web page"], ["Parse", "to plain text"], ["Split", "into chunks"], ["Embed", "each chunk"], ["Store", "vectors in", "LanceDB"]]
    for i, st in enumerate(steps):
        x = 10 + i * 144
        s += box(x, 34, 120, 70, st, fill=PALE if i != 4 else GREENF, stroke="#9AB0C8" if i != 4 else GREEND, fs=12.5)
        if i < 4: s += arrow(x + 120, 69, x + 142, 69)
    s += txt(10, 146, "B. Every question: retrieval and answer", fill=ORANGE, bold=True)
    q = [["Question"], ["Embed the", "question"], ["Find the", "nearest chunks"], ["Build the", "prompt"], ["LLM writes", "the answer"]]
    for i, st in enumerate(q):
        x = 10 + i * 144
        s += box(x, 158, 120, 70, st, fill=ORANGEF if i in (0, 4) else WHITE, stroke=ORANGE, fs=12.5)
        if i < 4: s += arrow(x + 120, 193, x + 142, 193)
    s += f'<path d="M650,104 C650,134 360,124 360,156" fill="none" stroke="{GREEND}" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#ah)"/>'
    s += txt(505, 116, "same database", "middle", GREEND, 12, True)
    s += txt(358, 246, "Top 4 chunks above", "middle", MUTED, 12) + txt(358, 262, "the similarity threshold", "middle", MUTED, 12)
    s += txt(502, 246, "System prompt, chunks,", "middle", MUTED, 12) + txt(502, 262, "history and question", "middle", MUTED, 12)
    s += txt(646, 246, "with citations", "middle", MUTED, 12)
    return svg("Two pipelines. Ingestion runs once per document: upload, parse to plain text, split into chunks, embed each chunk, and store the "
               "vectors in LanceDB. Retrieval runs on every question: embed the question, find the nearest chunks in the same database, "
               "build a prompt from the system prompt, the chunks, the chat history and the question, and the LLM writes an answer with citations.",
               720, 276, s, 620, x0=4)


# ───────────────────────── Redrawn settings screens ─────────────────────────
def window(title, side_on, body, h):
    """A simplified AnythingLLM settings window: dark sidebar on the left, settings panel on the right."""
    items = ["AI Providers", "  LLM", "  Embedder", "  Vector Database", "  Text Splitter", "Agent Skills", "Privacy & Data"]
    s = f'<rect x="4" y="4" width="712" height="{h - 8}" rx="10" fill="{DARK}" stroke="#121620"/>'
    s += f'<circle cx="22" cy="20" r="5" fill="#E5534B"/><circle cx="38" cy="20" r="5" fill="#E2B13C"/><circle cx="54" cy="20" r="5" fill="#57AB5A"/>'
    s += txt(360, 24, title, "middle", DMUT, 12)
    s += f'<rect x="4" y="36" width="168" height="{h - 40}" fill="#171C26"/>'
    for i, it in enumerate(items):
        y = 64 + i * 28; on = it.strip() == side_on
        if on: s += f'<rect x="10" y="{y - 17}" width="156" height="24" rx="5" fill="{BLUE}"/>'
        s += txt(20, y, it.strip() if not it.startswith("  ") else "· " + it.strip(), fill=WHITE if on else DTXT, fs=12.5, bold=on or not it.startswith("  "))
    return s + body


def field(x, y, label, value, w=300, note=None, hi=False):
    s = txt(x, y, label, fill=DTXT, fs=12.5, bold=True)
    s += f'<rect x="{x}" y="{y + 8}" width="{w}" height="30" rx="6" fill="{DARK2}" stroke="{GREEN if hi else "#3A4354"}" stroke-width="{1.8 if hi else 1}"/>'
    s += txt(x + 10, y + 28, value, fill=WHITE, fs=12.5)
    if note: s += txt(x, y + 54, note, fill=DMUT, fs=11.5)
    return s


def fig_llm_screen():
    b = txt(196, 64, "LLM Preference", fill=WHITE, fs=16, bold=True)
    b += txt(196, 84, "The model that writes every answer in every workspace.", fill=DMUT, fs=12)
    b += f'<rect x="196" y="98" width="200" height="56" rx="8" fill="{DARK2}" stroke="{GREEN}" stroke-width="1.8"/>'
    b += txt(212, 122, "Ollama", fill=WHITE, fs=14, bold=True) + txt(212, 141, "Run LLMs locally", fill=DMUT, fs=11.5)
    b += field(196, 180, "Ollama Base URL", "http://127.0.0.1:11434", 240, hi=True)
    b += field(456, 180, "Ollama Model", "gemma4:12b", 236, hi=True)
    b += field(196, 254, "Max Tokens (context window)", "8192", 240, "Match Ollama's context length")
    b += field(456, 254, "Performance Mode", "Base (default)", 236, "Maximum uses more VRAM")
    b += field(196, 338, "Keep model loaded", "5 minutes", 240)
    b += f'<rect x="596" y="356" width="96" height="32" rx="6" fill="{GREEN}"/>' + txt(644, 377, "Save", "middle", NAVY, 13, True)
    return svg("Simplified redrawing of the AnythingLLM LLM Preference screen with Ollama selected as the provider. Fields: Ollama Base URL "
               "http://127.0.0.1:11434, Ollama Model gemma4:12b, Max Tokens 8192, Performance Mode Base, keep model loaded 5 minutes, and a Save button.",
               720, 408, window("Settings · AI Providers · LLM", "LLM", b, 408), 620)


def fig_embed_screen():
    b = txt(196, 64, "Embedder Preference", fill=WHITE, fs=16, bold=True)
    b += txt(196, 84, "Turns each chunk, and each question, into a vector. Changing it means re-embedding.", fill=DMUT, fs=12)
    b += f'<rect x="196" y="98" width="200" height="56" rx="8" fill="{DARK2}" stroke="{GREEN}" stroke-width="1.8"/>'
    b += txt(212, 122, "Ollama", fill=WHITE, fs=14, bold=True) + txt(212, 141, "Embeddings from Ollama", fill=DMUT, fs=11.5)
    b += f'<rect x="410" y="98" width="200" height="56" rx="8" fill="{DARK2}" stroke="#3A4354"/>'
    b += txt(426, 122, "AnythingLLM Embedder", fill=DTXT, fs=13, bold=True) + txt(426, 141, "Built in, runs on the CPU", fill=DMUT, fs=11.5)
    b += field(196, 180, "Ollama Base URL", "http://127.0.0.1:11434", 240)
    b += field(456, 180, "Embedding Model", "embeddinggemma:latest", 236, hi=True)
    b += field(196, 254, "Max Embedding Chunk Length", "8192", 240, "The embedder's input limit, in characters", hi=True)
    b += txt(196, 346, "Do not pick a chat model here: Ollama lists both kinds in the same dropdown.", fill="#F0B44C", fs=12)
    b += f'<rect x="596" y="356" width="96" height="32" rx="6" fill="{GREEN}"/>' + txt(644, 377, "Save", "middle", NAVY, 13, True)
    return svg("Simplified redrawing of the AnythingLLM Embedder Preference screen with Ollama selected. Fields: Ollama Base URL, Embedding Model "
               "embeddinggemma:latest, and Max Embedding Chunk Length 8192 characters. A warning notes that Ollama lists chat and embedding "
               "models in the same dropdown.", 720, 408, window("Settings · AI Providers · Embedder", "Embedder", b, 408), 620)


def fig_split_screen():
    b = txt(196, 64, "Text Splitter & Chunking", fill=WHITE, fs=16, bold=True)
    b += txt(196, 84, "Applies to documents embedded after you save. Existing chunks are not changed.", fill=DMUT, fs=12)
    b += field(196, 112, "Text Chunk Size (characters)", "1000", 240, "Embed model maximum length is 8192", hi=True)
    b += field(456, 112, "Text Chunk Overlap (characters)", "20", 236, "Must be smaller than the chunk size", hi=True)
    b += txt(196, 214, "Vector Database", fill=WHITE, fs=16, bold=True)
    b += f'<rect x="196" y="228" width="200" height="56" rx="8" fill="{DARK2}" stroke="{GREEN}" stroke-width="1.8"/>'
    b += txt(212, 252, "LanceDB", fill=WHITE, fs=14, bold=True) + txt(212, 271, "100% local, no setup", fill=DMUT, fs=11.5)
    for i, (n, d) in enumerate([("Chroma", "Local server"), ("Milvus", "Local server")]):
        x = 410 + i * 146
        b += f'<rect x="{x}" y="228" width="136" height="56" rx="8" fill="{DARK2}" stroke="#3A4354"/>'
        b += txt(x + 14, 252, n, fill=DTXT, fs=13, bold=True) + txt(x + 14, 271, d, fill=DMUT, fs=11.5)
    b += txt(196, 314, "Changing the vector database means embedding every document again.", fill="#F0B44C", fs=12)
    b += f'<rect x="596" y="340" width="96" height="32" rx="6" fill="{GREEN}"/>' + txt(644, 361, "Save", "middle", NAVY, 13, True)
    return svg("Simplified redrawing of two AnythingLLM settings panels. Text Splitter and Chunking: chunk size 1000 characters, overlap 20 "
               "characters, embed model maximum 8192. Vector Database: LanceDB selected, with Chroma and Milvus as local alternatives. A note "
               "says switching the vector database means re-embedding every document.", 720, 392,
               window("Settings · AI Providers · Text Splitter and Vector Database", "Text Splitter", b, 392), 620)


def fig_skills_screen():
    rows = [("RAG search", True, "Search the workspace's documents"), ("Summarize documents", True, "Read a whole document and summarize it"),
            ("List documents", True, "See what the workspace holds"), ("Web browsing", False, "Search the web (DuckDuckGo by default)"),
            ("Web scraping", False, "Fetch and read a web page"), ("Save files", False, "Write a file to your computer"),
            ("SQL agent", False, "Query a database you connect"), ("File system agent", False, "Read and write files in folders you allow")]
    b = txt(196, 64, "Agent Skills", fill=WHITE, fs=16, bold=True)
    b += txt(196, 84, "Each switch decides what the agent may do. Use @agent in a chat to call it.", fill=DMUT, fs=12)
    for i, (n, on, d) in enumerate(rows):
        y = 104 + i * 36
        b += f'<rect x="196" y="{y}" width="496" height="30" rx="6" fill="{DARK2}"/>'
        b += txt(208, y + 20, n, fill=WHITE, fs=12.5, bold=True) + txt(360, y + 20, d, fill=DMUT, fs=11.5)
        b += f'<rect x="650" y="{y + 7}" width="32" height="16" rx="8" fill="{GREEN if on else "#4A5366"}"/>'
        b += f'<circle cx="{674 if on else 658}" cy="{y + 15}" r="6" fill="{WHITE}"/>'
    b += txt(196, 410, "Shown as this article recommends for a private document assistant, not as the defaults.", fill="#F0B44C", fs=12)
    return svg("Simplified redrawing of the AnythingLLM Agent Skills screen. Switched on: RAG search, summarize documents and list documents. "
               "Switched off: web browsing, web scraping, save files, SQL agent and file system agent.", 720, 428,
               window("Settings · Agent Skills", "Agent Skills", b, 428), 620)


# ───────────────────────── Figure: chunking with overlap ─────────────────────────
def fig_chunks():
    s = DEFS
    words = ("The feed pump P-101 trips on low suction pressure. Before restarting, check the tank level and the strainer. "
             "If the strainer is blocked, isolate the pump, drain the casing and clean the basket. Record the event in the log.")
    s += txt(10, 22, "Source paragraph (about 230 characters)", fill=MUTED, fs=12, bold=True)
    s += f'<rect x="10" y="30" width="700" height="52" rx="6" fill="{SAND}"/>'
    s += txt(20, 51, words[:112], fill=NAVY, fs=12.5) + txt(20, 70, words[112:], fill=NAVY, fs=12.5)
    cols = [(BLUE, PALE), (ORANGE, ORANGEF), (GREEND, GREENF)]
    parts = [("Chunk 1", 10, 280, "…trips on low suction pressure. Before restarting,"),
             ("Chunk 2", 220, 300, "Before restarting, check the tank level and the strainer…"),
             ("Chunk 3", 450, 260, "…clean the basket. Record the event in the log.")]
    for i, (n, x, w, t) in enumerate(parts):
        y = 112 + i * 46; c, f = cols[i]
        s += f'<rect x="{x}" y="{y}" width="{w}" height="34" rx="6" fill="{f}" stroke="{c}" stroke-width="1.6"/>'
        s += txt(x + 8, y + 22, f"{n}: {t}" if len(t) < 40 else n, fill=c, fs=12, bold=True)
    s += f'<rect x="220" y="104" width="70" height="96" fill="{ORANGE}" opacity=".12"/>'
    s += f'<rect x="450" y="150" width="70" height="96" fill="{GREEN}" opacity=".18"/>'
    s += txt(255, 270, "overlap", "middle", ORANGE, 12, True) + txt(485, 270, "overlap", "middle", GREEND, 12, True)
    s += txt(10, 300, "The splitter cuts at a paragraph break if it can, then a line break, then a space. The overlap repeats the end of one chunk", fill=MUTED, fs=12)
    s += txt(10, 318, "at the start of the next, so a sentence cut in half still appears whole in one of them.", fill=MUTED, fs=12)
    return svg("A paragraph about a pump trip is split into three overlapping chunks. The shaded bands show where the end of one chunk is repeated "
               "at the start of the next, so a sentence cut at a boundary still appears whole in one chunk.", 720, 330, s, 600, x0=4)


# ───────────────────────── Figure: chunk size trade-off ─────────────────────────
def fig_tradeoff():
    s = ""; X0 = 150; W = 230
    s += txt(X0, 20, "Chunks for a 300,000-character manual", fill=BLUE, fs=12.5, bold=True)
    s += txt(X0 + 290, 20, "Tokens handed to the LLM per question", fill=ORANGE, fs=12.5, bold=True)
    mx1 = n_chunks(SIZES[0]); mx2 = SIZES[-1]
    for i, sz in enumerate(SIZES):
        y = 40 + i * 44; n = n_chunks(sz); tk = sz // 4 * SNIPPETS
        s += txt(X0 - 12, y + 18, f"{sz:,} characters", "end", NAVY, 12.5, True)
        w1 = W * n / mx1; w2 = 190 * tk / mx2
        s += f'<rect x="{X0}" y="{y}" width="{w1:.1f}" height="26" rx="4" fill="{BLUE}" opacity="{0.95 if sz == 1000 else 0.55}"/>' + txt(X0 + w1 + 6, y + 18, f"{n:,}", fill=NAVY, fs=12.5)
        s += f'<rect x="{X0 + 290}" y="{y}" width="{w2:.1f}" height="26" rx="4" fill="{ORANGE}" opacity="{0.95 if sz == 1000 else 0.55}"/>' + txt(X0 + 290 + w2 + 6, y + 18, f"≈{tk:,}", fill=NAVY, fs=12.5)
    s += txt(10, 226, "Darker bars: the 1,000-character default. Four snippets per question, about four characters per token.", fill=MUTED, fs=12)
    return svg("Two bar charts by chunk size. A 300,000-character manual makes 625 chunks at 500 characters, 307 at 1,000, 152 at 2,000 and 76 at "
               "4,000. With four snippets per question, the text handed to the LLM is about 500, 1,000, 2,000 and 4,000 tokens.", 720, 236, s, 600, x0=4)


# ───────────────────────── Figure: context-window budget ─────────────────────────
def fig_budget():
    parts = [("System prompt", 400, NAVY), ("4 document chunks", 1000, BLUE), ("Chat history", 3000, PURPLE),
             ("Question", 100, GREEND), ("Room for the answer", 3692, "#B9C3D1")]
    tot = sum(p[1] for p in parts); X0, W = 10, 700; s = ""; x = X0
    s += txt(X0, 20, f"An 8,192-token context window, filled for one question (illustrative)", fill=NAVY, fs=12.5, bold=True)
    for n, v, c in parts:
        w = W * v / tot
        s += f'<rect x="{x:.1f}" y="32" width="{w:.1f}" height="38" fill="{c}"/>'
        if w > 60: s += txt(x + w / 2, 56, f"{v:,}", "middle", WHITE if c != "#B9C3D1" else NAVY, 12.5, True)
        x += w
    y = 98
    for i, (n, v, c) in enumerate(parts):
        cx = X0 + (i % 3) * 240; cy = y + (i // 3) * 22
        s += f'<rect x="{cx}" y="{cy - 10}" width="12" height="12" rx="2" fill="{c}"/>' + txt(cx + 18, cy, f"{n}: {v:,} tokens", fill=NAVY, fs=12)
    s += txt(X0, 156, "If the window is smaller than the model was loaded with, or the chat runs long, the oldest text is cut first.", fill=MUTED, fs=12)
    return svg("A horizontal bar showing an 8,192-token context window: system prompt 400 tokens, four document chunks 1,000, chat history 3,000, "
               "question 100, leaving about 3,700 tokens for the answer.", 720, 166, s, 600, x0=4)


# ───────────────────────── Figure: what can leave the PC ─────────────────────────
def fig_trust():
    s = DEFS
    s += f'<rect x="10" y="10" width="420" height="250" rx="12" fill="{GREENF}" stroke="{GREEND}" stroke-width="1.6"/>'
    s += txt(26, 34, "Stays on the PC with the setup in this article", fill=GREEND, bold=True)
    for i, t in enumerate(["Your documents and their parsed text", "Chunks and vectors (LanceDB)", "Questions, answers and chat history",
                           "Model weights and every inference (Ollama)", "Settings, workspaces and system prompts"]):
        s += txt(30, 64 + i * 26, "✓  " + t, fill=NAVY, fs=12.5)
    s += txt(26, 210, "Protect it like any local data:", fill=GREEND, fs=12.5, bold=True)
    s += txt(26, 232, "disk encryption, a Windows sign-in, backups.", fill=NAVY, fs=12.5)
    s += f'<rect x="452" y="10" width="258" height="250" rx="12" fill="{ORANGEF}" stroke="{ORANGE}" stroke-width="1.6" stroke-dasharray="6 4"/>'
    s += txt(468, 34, "Can leave the PC if you turn it on", fill=ORANGE, bold=True)
    for i, t in enumerate(["A cloud LLM or embedder", "Web browsing and scraping", "MCP servers and custom skills",
                           "Gmail, Calendar, Outlook skills", "Anonymous telemetry", "Ollama opened to the network"]):
        s += txt(472, 64 + i * 26, "!  " + t, fill=NAVY, fs=12.5)
    s += txt(468, 232, "Each is a deliberate choice.", fill=ORANGE, fs=12.5, bold=True)
    return svg("Two panels. Stays on the PC: documents and parsed text, chunks and vectors, chat history, model weights and inference, and settings. "
               "Can leave the PC if switched on: a cloud LLM or embedder, web browsing and scraping, MCP servers and custom skills, the Gmail, "
               "Calendar and Outlook skills, anonymous telemetry, and an Ollama server opened to the network.", 720, 270, s, 600, x0=4)


# ───────────────────────── The article ─────────────────────────
def article():
    chunk_rows = "".join(
        f'<tr{" class=\"oee-total\"" if sz == 1000 else ""}><td class="num">{sz:,}</td><td class="num">≈{sz // 4:,}</td><td class="num">{n_chunks(sz):,}</td>'
        f'<td class="num">≈{sz // 4 * SNIPPETS:,}</td><td>{use}</td></tr>'
        for sz, use in zip(SIZES, ["FAQs, glossaries, spare-parts lists, short self-contained entries",
                                    "Default. Manuals, procedures, policies, most business documents",
                                    "Reports and papers where an answer needs a whole section",
                                    "Long narrative text; check the embedder limit and context window first"]))
    body = f"""{CSS}<p>A private AI assistant that answers questions from your own documents no longer needs a cloud subscription or a data-sharing agreement. A recent desktop PC with a mid-range graphics card can run a capable open model, read your procedures, reports and contracts, and answer with citations, without a byte leaving the building.</p>
<p>This guide builds one on a single Windows PC with two free tools: <strong>Ollama</strong>, which runs the models, and <strong>AnythingLLM Desktop</strong>, which handles the documents, the chat and the agents. It covers each setting that decides how well the assistant works: the AI provider, the embedding model, the maximum embedding chunk length, the vector database, the text splitter, agent skills, and finally accuracy and security.</p>
<p class="oee-note"><em>Written against AnythingLLM Desktop v1.19 and Ollama 0.40 in November 2026. Menu names move between releases; the settings themselves have been stable.</em></p>

<h2>What you are building</h2>
<p>AnythingLLM is the front end. It stores your documents, splits them into chunks, keeps their vectors in a built-in database and runs the chat. It does not run the model itself in this setup: it sends requests to Ollama on the same PC, which loads the models onto the graphics card.</p>
{fig(fig_arch(), 1, "The whole system on one PC. AnythingLLM talks to Ollama over the local address 127.0.0.1, so no traffic leaves the machine.")}
<p>The example PC throughout is a Windows 11 desktop with an Intel Core Ultra 7, 32&nbsp;GB of RAM and an NVIDIA RTX 5070 with 12&nbsp;GB of video memory (VRAM). VRAM is the number that matters most: the model has to fit in it to run at full speed.</p>
<table>
<thead><tr><th>Component</th><th>Choice in this guide</th><th>Why</th></tr></thead>
<tbody>
<tr><td>Model runner</td><td>Ollama</td><td>Free, one-line model downloads, uses the GPU automatically</td></tr>
<tr><td>Chat model</td><td>gemma4:12b</td><td>Fits in 12&nbsp;GB of VRAM and runs fully on the GPU</td></tr>
<tr><td>Embedding model</td><td>embeddinggemma</td><td>Small (about 300M parameters), multilingual, 2,048-token input</td></tr>
<tr><td>Front end</td><td>AnythingLLM Desktop</td><td>Documents, chat, agents and settings in one installer</td></tr>
<tr><td>Vector database</td><td>LanceDB (built in)</td><td>No setup; vectors stay in AnythingLLM's own folder</td></tr>
<tr><td>Text splitter</td><td>1,000 characters, 20 overlap</td><td>The defaults, and a sound starting point</td></tr>
</tbody></table>

<h2>"Training" the model: what actually happens</h2>
<p>People ask how to train their local model on their documents. In almost every case the answer is: you do not. AnythingLLM uses <strong>retrieval-augmented generation (RAG)</strong>. The model's weights never change. Instead, for each question the most relevant passages of your documents are found and placed in front of the model, which writes its answer from them.</p>
<table>
<thead><tr><th>Approach</th><th>What changes</th><th>Effort</th><th>Use it for</th></tr></thead>
<tbody>
<tr><td>RAG (AnythingLLM workspaces)</td><td>Nothing in the model; your documents are searched at question time</td><td>Minutes</td><td>Facts that live in documents and change over time</td></tr>
<tr><td>System prompt</td><td>The standing instructions for one workspace</td><td>Minutes</td><td>Tone, format, role, rules such as "cite the section number"</td></tr>
<tr><td>Fine-tuning</td><td>The model's weights, using hundreds of example question-and-answer pairs</td><td>Days, outside AnythingLLM</td><td>A house style or a narrow task the model keeps getting wrong</td></tr>
</tbody></table>
<p>Start with RAG and a good system prompt. Fine-tune only when you can show, with examples, a failure that better retrieval and instructions cannot fix. A fine-tuned model can be loaded into Ollama and selected in AnythingLLM like any other.</p>
{fig(fig_rag(), 2, "The two halves of RAG. Ingestion runs once for each document; retrieval runs for every question, against the same database.")}

<h2>Step 1: Install Ollama and pull two models</h2>
<p>Install Ollama for Windows from ollama.com. It runs in the background and listens on <code>http://127.0.0.1:11434</code>. Then, in a terminal, download a chat model and an embedding model:</p>
<pre><code>ollama pull gemma4:12b
ollama pull embeddinggemma
ollama run gemma4:12b "Reply with OK"
ollama ps</code></pre>
<p><code>ollama ps</code> lists the loaded models. The PROCESSOR column should read <strong>100% GPU</strong>. If it shows a CPU share, the model plus its context window does not fit in VRAM: choose a smaller model or a shorter context, or answers will be several times slower.</p>
<table>
<thead><tr><th>VRAM</th><th>Chat model size that runs fully on the GPU (4-bit)</th><th>Typical use</th></tr></thead>
<tbody>
<tr><td class="nw">6–8&nbsp;GB</td><td>About 3 to 8 billion parameters</td><td>Simple Q&amp;A over short documents</td></tr>
<tr><td class="nw">12&nbsp;GB</td><td>About 8 to 14 billion parameters</td><td>Document Q&amp;A, summaries, drafting; light agent use</td></tr>
<tr><td class="nw">16–24&nbsp;GB</td><td>About 14 to 32 billion parameters</td><td>Better reasoning and more reliable agent tool use</td></tr>
</tbody></table>
<p class="oee-note"><em>Rule of thumb only: a 4-bit model needs roughly 0.6&nbsp;GB per billion parameters, plus room for the context window.</em></p>

<h2>Step 2: Install AnythingLLM and choose the AI provider</h2>
<p>Download AnythingLLM Desktop from anythingllm.com and run the installer. No account is needed. The first-run wizard asks for an LLM provider; you can change every choice later under <strong>Settings &gt; AI Providers</strong>.</p>
<p>AnythingLLM can call many providers. The choice decides where your questions and document snippets are sent.</p>
<table>
<thead><tr><th>Provider</th><th>Runs where</th><th>Data leaves the PC?</th><th>Best for</th></tr></thead>
<tbody>
<tr><td>Ollama</td><td>Your PC</td><td>No</td><td>Private use with a GPU; the choice in this guide</td></tr>
<tr><td>LM Studio</td><td>Your PC</td><td>No</td><td>People who prefer a graphical model browser</td></tr>
<tr><td>AnythingLLM built-in</td><td>Your PC</td><td>No</td><td>Trying it out with no other software</td></tr>
<tr><td>LocalAI, KoboldCPP</td><td>Your PC or a local server</td><td>No</td><td>Existing self-hosted setups</td></tr>
<tr><td>OpenAI, Anthropic, Google Gemini, Mistral</td><td>The vendor's cloud</td><td>Yes</td><td>Hardest tasks; pay per token</td></tr>
<tr><td>Azure OpenAI, AWS Bedrock, Google Vertex</td><td>Your company's cloud account</td><td>Yes, to your tenancy</td><td>Firms with existing cloud agreements</td></tr>
<tr><td>OpenRouter, Groq, Together AI</td><td>The vendor's cloud</td><td>Yes</td><td>Trying many open models quickly</td></tr>
</tbody></table>
<p>Select <strong>Ollama</strong>, keep the base URL, and pick <strong>gemma4:12b</strong>. Set the context window (Max Tokens) to the size Ollama loads the model with; a mismatch either wastes the window or lets text be cut without warning.</p>
{fig(fig_llm_screen(), 3, "The LLM settings with Ollama selected. Simplified redrawing of the AnythingLLM screen; field layout differs slightly by version.")}

<h2>Step 3: The embedding model and its maximum chunk length</h2>
<p>The embedding model turns text into a vector: a list of numbers that places similar meanings close together. Every chunk of every document is embedded once; every question is embedded when it is asked, and the nearest chunks are retrieved. Retrieval quality depends more on the embedder than most people expect.</p>
<p>Under <strong>Settings &gt; AI Providers &gt; Embedder</strong>, choose Ollama and select <strong>embeddinggemma</strong>. Ollama lists chat and embedding models in the same dropdown, so make sure you pick the embedder.</p>
{fig(fig_embed_screen(), 4, "The embedder settings. Simplified redrawing of the AnythingLLM screen.")}
<p><strong>Max Embedding Chunk Length</strong> tells AnythingLLM the largest piece of text, in characters, that the embedding model accepts. It is a ceiling, not the chunk size. If the text splitter's chunk size is set above it, AnythingLLM quietly uses this limit instead and logs a warning. Set it from the model's token limit at about four characters per token: embeddinggemma reads 2,048 tokens, or roughly 8,000 characters of English. With 1,000-character chunks you are far below it either way.</p>
<table>
<thead><tr><th>Embedding model</th><th>Runs on</th><th>Input limit</th><th>Vector size</th><th>Notes</th></tr></thead>
<tbody>
<tr><td>AnythingLLM built-in</td><td>CPU</td><td>Short</td><td class="num">384</td><td>Zero setup; adequate for small libraries</td></tr>
<tr><td>embeddinggemma</td><td>Ollama</td><td>2,048 tokens</td><td class="num">768</td><td>Small, fast, over 100 languages</td></tr>
<tr><td>nomic-embed-text</td><td>Ollama</td><td>8,192 tokens</td><td class="num">768</td><td>Popular English default</td></tr>
<tr><td>mxbai-embed-large</td><td>Ollama</td><td>512 tokens</td><td class="num">1,024</td><td>Strong retrieval; keep chunks short</td></tr>
<tr><td>bge-m3</td><td>Ollama</td><td>8,192 tokens</td><td class="num">1,024</td><td>Multilingual, long inputs</td></tr>
</tbody></table>
<p class="oee-takeaway">Changing the embedding model makes every stored vector meaningless, because the old and new models place text in different spaces. Pick the embedder before you load your library, and re-embed everything if you change it.</p>

<h2>Step 4: The vector database</h2>
<p>The vector database stores each chunk's vector next to its original text and finds the nearest ones to a question. AnythingLLM ships with <strong>LanceDB</strong> built in. It needs no configuration, keeps its files inside AnythingLLM's storage folder, and handles libraries of many thousands of documents on one PC.</p>
<table>
<thead><tr><th>Option</th><th>Where it runs</th><th>When to choose it</th></tr></thead>
<tbody>
<tr><td>LanceDB (default)</td><td>Inside AnythingLLM</td><td>Single PC, private use. The right choice for this guide</td></tr>
<tr><td>Chroma, Milvus</td><td>A local server you run</td><td>Several apps sharing one vector store</td></tr>
<tr><td>Pinecone, Qdrant, Weaviate, Zilliz, AstraDB, Chroma Cloud</td><td>Vendor cloud</td><td>Team servers at scale; your text is stored with the vendor</td></tr>
</tbody></table>
<p>Like the embedder, a change of vector database starts with an empty store, and every document has to be embedded again.</p>

<h2>Step 5: Text splitting and chunking</h2>
<p>Before a document is embedded it is cut into chunks. Each chunk becomes one vector, and chunks, not whole documents, are what the model sees when it answers. AnythingLLM uses a recursive splitter: it tries to cut at a paragraph break, then at a line break, then at a space, and splits a word only as a last resort. Two settings control it, under <strong>Settings &gt; AI Providers &gt; Text Splitter &amp; Chunking</strong>.</p>
<ul>
<li><strong>Text Chunk Size</strong>: the maximum length of a chunk, in characters (not tokens). The default is 1,000, about 250 tokens.</li>
<li><strong>Text Chunk Overlap</strong>: how many characters each chunk repeats from the end of the one before. The default is 20.</li>
</ul>
{fig(fig_chunks(), 5, "How overlap protects a sentence that falls on a chunk boundary.")}
{fig(fig_split_screen(), 6, "Text splitter and vector database settings. Simplified redrawing of the AnythingLLM screens.")}
<p>The chunk size is a trade-off. Small chunks match precisely but may lose the sentence that gives them meaning. Large chunks keep context together but bring irrelevant text with them, and fewer fit in the model's context window. The table works through one example: a 100-page manual of about 300,000 characters, with four chunks retrieved per question.</p>
<table>
<thead><tr><th>Chunk size (characters)</th><th>Tokens per chunk</th><th>Chunks in the manual</th><th>Tokens sent per question</th><th>Suits</th></tr></thead>
<tbody>{chunk_rows}</tbody></table>
{fig(fig_tradeoff(), 7, "Smaller chunks mean more vectors to search; larger chunks mean more text in every prompt.")}
<p>Three practical points. Change one setting at a time and test with the same questions. New settings apply only to documents embedded afterwards, so remove and re-add documents to compare. And raise the overlap to 10% to 20% of the chunk size (100 to 200 characters at the default) for procedures and contracts, where one sentence often depends on the one before it.</p>
<p>Clean input matters as much as the numbers. Scanned PDFs without a text layer, multi-column layouts, and tables flattened into a stream of numbers all produce poor chunks. Converting important documents to clean text or Markdown before uploading usually helps more than any slider.</p>

<h2>Step 6: Create a workspace and tune retrieval</h2>
<p>A workspace is a separate assistant with its own documents, system prompt and settings. The model can only see documents embedded in that workspace. Create one per subject (for example "Plant procedures" and "Client contracts") rather than one for everything; a smaller pool of chunks gives cleaner matches.</p>
<p>Drag documents into the workspace and choose <strong>Move to Workspace</strong> to embed them. Then open the workspace settings:</p>
<table>
<thead><tr><th>Workspace setting</th><th>What it does</th><th>Suggested start</th></tr></thead>
<tbody>
<tr><td>Chat mode</td><td><em>Chat</em> mixes your documents with the model's general knowledge; <em>Query</em> answers only from documents and says so when nothing relevant is found</td><td>Query, for document Q&amp;A</td></tr>
<tr><td>System prompt</td><td>Standing instructions for every answer</td><td>Role, sources only, cite the document and section</td></tr>
<tr><td>Max context snippets</td><td>How many chunks are retrieved per question</td><td>4 to 6</td></tr>
<tr><td>Document similarity threshold</td><td>Drops chunks that match too weakly</td><td>Low; raise it if answers drift off topic</td></tr>
<tr><td>Search preference</td><td>Accuracy-optimized adds a re-ranking step after the search</td><td>Accuracy-optimized</td></tr>
<tr><td>LLM temperature</td><td>Randomness of the wording</td><td>0.1 to 0.3 for factual answers</td></tr>
</tbody></table>
<p>Two more tools help. <strong>Pinning</strong> a document sends its full text with every question instead of a few chunks, which suits one short, critical document if it fits the context window. <strong>Attaching</strong> a file to a single chat does the same for a one-off question without adding it to the library.</p>
{fig(fig_budget(), 8, "Everything sent to the model shares one context window. Long chats crowd out document chunks first.")}

<h2>Step 7: Agent skills</h2>
<p>A normal chat only answers. An agent can act: search the documents again, summarize a whole file, browse the web, save a file, query a database or call another program. Start one by typing <code>@agent</code> in a chat. Under <strong>Settings &gt; Agent Skills</strong> each skill has its own switch.</p>
<table>
<thead><tr><th>Skill</th><th>What it does</th><th>For a private document assistant</th></tr></thead>
<tbody>
<tr><td>RAG search</td><td>Searches the workspace's documents on demand</td><td>On</td></tr>
<tr><td>Summarize documents, list documents</td><td>Reads a whole document; lists what the workspace holds</td><td>On</td></tr>
<tr><td>Chart generation</td><td>Draws a chart from data in the chat</td><td>Optional</td></tr>
<tr><td>Web browsing, web scraping</td><td>Searches and reads the internet</td><td>Off, unless needed: queries leave the PC</td></tr>
<tr><td>Save files, file system agent</td><td>Writes and reads files on your computer</td><td>Off, or limited to one folder</td></tr>
<tr><td>SQL agent</td><td>Runs queries on a connected database</td><td>Read-only account only</td></tr>
<tr><td>Gmail, Google Calendar, Outlook</td><td>Reads and acts on mail and calendars</td><td>Off for a document assistant</td></tr>
<tr><td>Scheduled jobs</td><td>Runs an agent task on a timetable</td><td>Optional</td></tr>
</tbody></table>
{fig(fig_skills_screen(), 9, "Agent skills switched for a private document assistant. Simplified redrawing of the AnythingLLM screen.")}
<p>Beyond the built-in skills, AnythingLLM can load <strong>custom skills</strong> (small JavaScript programs placed in the <code>plugins/agent-skills</code> folder of its storage directory), connect to <strong>MCP servers</strong> that expose other tools, and run <strong>Agent Flows</strong>, fixed step-by-step workflows built without code. Its intelligent tool selection sends only the tools relevant to each request to the model, which keeps prompts short for local models.</p>
<p>Agents ask more of the model than plain Q&amp;A: it has to decide which tool to call and format the call correctly. A 12-billion-parameter model handles simple, single-tool requests well and becomes unreliable on long multi-step tasks. If the agent ignores its tools, try a model trained for tool use or a larger one before blaming the settings.</p>

<h2>Accuracy: testing and fixing answers</h2>
<p>Do not judge a setup on three questions. Write 20 to 30 questions whose answers you know and whose source page you can name. Run them after every change and record, for each one, whether the right chunk was retrieved (shown in the citations) and whether the answer was right. Those are two different failures with different fixes.</p>
<table>
<thead><tr><th>Symptom</th><th>Likely cause</th><th>Fix</th></tr></thead>
<tbody>
<tr><td>"I couldn't find that" when the answer is in a document</td><td>Document not embedded in this workspace, or threshold too high</td><td>Check the workspace's document list; lower the threshold</td></tr>
<tr><td>Citations point to the wrong passages</td><td>Weak embedder, poor text extraction, chunks too large</td><td>Clean the source text; try a stronger embedder; reduce chunk size</td></tr>
<tr><td>Right passage cited, wrong answer</td><td>Model too small, temperature too high, context cut</td><td>Lower temperature; check the context window; try a larger model</td></tr>
<tr><td>Answer mixes in outside "facts"</td><td>Chat mode lets the model use general knowledge</td><td>Switch to Query mode; tell it to answer only from sources</td></tr>
<tr><td>Questions like "how many" or "list all" fail</td><td>RAG retrieves 4 to 6 chunks, never the whole library</td><td>Use an agent to summarize the document, or pin it</td></tr>
<tr><td>Quality drops late in a long chat</td><td>History crowds the context window</td><td>Start a new thread for a new topic</td></tr>
<tr><td>Changed settings made no difference</td><td>Old chunks are still in the database</td><td>Remove and re-embed the documents</td></tr>
</tbody></table>
<p class="oee-takeaway">A local assistant can still be wrong, fluently. Keep a person accountable for any answer that feeds a decision, and make the assistant show its sources so that person can check them in seconds.</p>
<p>For a deeper treatment of retrieval design and evaluation, see the journal paper <a href="{RAGP}.html">Retrieval-Augmented Generation: Design, Evaluation and Failure Analysis</a>.</p>

<h2>Security: what stays private, and what you must still do</h2>
<p>With Ollama, the built-in embedder or an Ollama embedder, and LanceDB, your documents, vectors, chats and model inference all stay on the PC. That removes the largest risk of cloud AI. It does not make the setup secure by itself.</p>
{fig(fig_trust(), 10, "The privacy boundary. Everything on the left is local by design; everything on the right is a switch you control.")}
<table>
<thead><tr><th>Area</th><th>Action</th></tr></thead>
<tbody>
<tr><td>The PC</td><td>Use a Windows sign-in and turn on device encryption or BitLocker. AnythingLLM Desktop is single-user and has no password of its own, so anyone at the unlocked PC can read every workspace.</td></tr>
<tr><td>Ollama's network port</td><td>Leave it on 127.0.0.1. Do not set it to listen on all addresses unless a firewall limits who can reach it; Ollama has no login.</td></tr>
<tr><td>Telemetry</td><td>AnythingLLM sends anonymous usage data by default. Turn it off under Settings &gt; Privacy &amp; Data if your policy requires.</td></tr>
<tr><td>Cloud switches</td><td>Confirm the LLM, embedder and vector database are all local. One cloud setting sends document text out.</td></tr>
<tr><td>Agent skills</td><td>Switch off web, file-writing and mail skills you do not need. Treat web pages and documents as untrusted: hidden text in them can try to steer the agent (prompt injection).</td></tr>
<tr><td>Custom skills and MCP servers</td><td>Install only code you have read or trust. They run with your Windows permissions.</td></tr>
<tr><td>Deleting data</td><td>Removing a document from a workspace keeps it in My Documents. Delete it from My Documents to erase the text and its cached vectors.</td></tr>
<tr><td>Several users</td><td>Use the Docker (server) edition instead: it adds multi-user mode with admin, manager and default roles.</td></tr>
<tr><td>Backups and updates</td><td>Back up AnythingLLM's storage folder with your other data, and keep both apps updated.</td></tr>
</tbody></table>

<h2>The checklist</h2>
<ol>
<li>Install Ollama, pull a chat model that fits your VRAM and an embedding model, and confirm 100% GPU with <code>ollama ps</code>.</li>
<li>Install AnythingLLM Desktop. Set the LLM provider to Ollama and match the context window.</li>
<li>Set the embedder to the Ollama embedding model and its maximum chunk length to the model's limit, before loading documents.</li>
<li>Keep LanceDB and the default chunking (1,000 characters) to start; raise the overlap for procedures.</li>
<li>Create one workspace per subject, use Query mode, a sources-only system prompt and a low temperature.</li>
<li>Switch on only the agent skills you need.</li>
<li>Build a 20-question test set and rerun it after every change.</li>
<li>Encrypt the disk, keep Ollama on localhost, review telemetry and back up the storage folder.</li>
</ol>
<p>A private assistant like this is often the first building block of a company's own AI operating system. The journal paper <a href="{AIOS}.html">AI Operating Systems: A Reference Architecture and Governance Model</a> describes how the pieces fit together at company scale, and <a href="{COST}.html">Score Versus Cost Per Task</a> covers when a cloud model is worth paying for instead.</p>
<p class="oee-note"><em>Settings screens in this article are simplified redrawings, not screenshots, and some field names vary by version. Hardware guidance is a rule of thumb; check the model's page for its actual memory use.</em></p>
"""
    for t in ("<thead>", "</thead>", "<tbody>", "</tbody>"): body = body.replace(t, "")   # nowrap() reads <thead> as a cell
    body = nowrap(body, [(1, 0, 16), (5, 0, 22), (11, 0, 30)])
    return {
        "slug": SLUG,
        "title": "Your Own Private AI Assistant: Building a Local LLM with AnythingLLM and Ollama",
        "cats": ["artificial-intelligence", "digital-technology"],
        "desc": "Set up a private document assistant on one PC: AI providers, embedding model, chunk length, vector database, text splitting, agent skills, accuracy and security.",
        "tags": ["AnythingLLM", "Ollama", "local LLM", "RAG", "embeddings", "vector database", "AI agents", "AI security"],
        "body": body,
        "related": [RAGP, AIOS, COST],
        "date": "2026-11-12",
        "author": "Quak Foo Lee",
        "read": "14 min read",
        "cover_label": "Artificial Intelligence",
    }


if __name__ == "__main__":
    a = article()
    p = os.path.join(HERE, a["slug"] + ".json")
    json.dump(a, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    words = len(__import__("re").sub(r"<[^>]+>", " ", a["body"]).split())
    print(f"wrote {p} ({words} words in body)")
