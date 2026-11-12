"""Model catalogue for the LLM leaderboard: which models are listed, and how source names map to them.

Each entry: id, display name, developer, tier, aliases (names as benchmarks write them; matched after normalising
case, dots, dashes and a trailing reasoning-effort / date label), and the vendor record names to take specs and price from
(content/llm/raw/vendor.models.json, first match wins per field, so list the primary source first).

snapshots (optional): the only snapshot dates accepted for this entry (rows dated otherwise are rejected).
show_snapshot (optional): show the snapshot date in the setting label.

Tier = the model's place in its developer's current line-up:
  Frontier       - the developer's most capable generally offered model(s)
  Mid-size       - a cheaper general model one step down
  Small and fast - the developer's small, low-cost or edge model
"""

F, M, S = "Frontier", "Mid-size", "Small and fast"

CATALOG = [
    # OpenAI
    dict(id="gpt-6-astra", name="GPT-6 Astra", dev="OpenAI", tier=F, aliases=["GPT-6 Astra", "gpt-6-astra"], vendor=["GPT-6 Astra"]),
    dict(id="gpt-6-1-sol", name="GPT-6.1 Sol", dev="OpenAI", tier=F, aliases=["GPT-6.1 Sol", "gpt-6.1-sol"], vendor=["GPT-6.1 Sol"]),
    dict(id="gpt-6-1-terra", name="GPT-6.1 Terra", dev="OpenAI", tier=M, aliases=["GPT-6.1 Terra", "gpt-6.1-terra"], vendor=["GPT-6.1 Terra"]),
    dict(id="gpt-6-luna", name="GPT-6 Luna", dev="OpenAI", tier=S, aliases=["GPT-6 Luna", "gpt-6-luna"], vendor=["GPT-6 Luna"]),
    dict(id="gpt-oss-120b", name="gpt-oss-120b", dev="OpenAI", tier=M, aliases=["gpt-oss-120b", "OpenAI: gpt-oss-120b"], vendor=["gpt-oss-120b", "OpenAI: gpt-oss-120b"]),
    dict(id="gpt-oss-20b", name="gpt-oss-20b", dev="OpenAI", tier=S, aliases=["gpt-oss-20b", "OpenAI: gpt-oss-20b"], vendor=["gpt-oss-20b", "OpenAI: gpt-oss-20b"]),
    # Anthropic
    dict(id="claude-fable-5-2", name="Claude Fable 5.2", dev="Anthropic", tier=F, aliases=["Claude Fable 5.2", "Fable 5.2", "claude-fable-5-2", "claude-fable-5.2"], vendor=["Claude Fable 5.2"]),
    dict(id="claude-mythos-5-2", name="Claude Mythos 5.2", dev="Anthropic", tier=F, aliases=["Claude Mythos 5.2", "Mythos 5.2", "claude-mythos-5-2"], vendor=["Claude Mythos 5.2"]),
    dict(id="claude-opus-5-5", name="Claude Opus 5.5", dev="Anthropic", tier=F, aliases=["Claude Opus 5.5", "Opus 5.5", "claude-opus-5-5", "claude-opus-5.5"], vendor=["Claude Opus 5.5"]),
    dict(id="claude-sonnet-5-5", name="Claude Sonnet 5.5", dev="Anthropic", tier=M, aliases=["Claude Sonnet 5.5", "Sonnet 5.5", "claude-sonnet-5-5", "claude-sonnet-5.5"], vendor=["Claude Sonnet 5.5"]),
    dict(id="claude-haiku-5-5", name="Claude Haiku 5.5", dev="Anthropic", tier=S, aliases=["Claude Haiku 5.5", "Haiku 5.5", "claude-haiku-5-5", "claude-haiku-5.5"], vendor=["Claude Haiku 5.5"]),
    # Google
    dict(id="gemini-4-carbon", name="Gemini 4 Carbon", dev="Google", tier=F, aliases=["Gemini 4 Carbon", "gemini-4-carbon"], vendor=["Gemini 4 Carbon"]),
    dict(id="gemini-4-argon", name="Gemini 4 Argon", dev="Google", tier=F, aliases=["Gemini 4 Argon", "gemini-4-argon"], vendor=["Gemini 4 Argon"]),
    dict(id="gemini-3-8-flash", name="Gemini 3.8 Flash", dev="Google", tier=M, aliases=["Gemini 3.8 Flash", "gemini-3.8-flash"], vendor=["Gemini 3.8 Flash"]),
    dict(id="gemini-3-5-flash-lite", name="Gemini 3.5 Flash-Lite", dev="Google", tier=S, aliases=["Gemini 3.5 Flash-Lite", "gemini-3.5-flash-lite"], vendor=["Gemini 3.5 Flash-Lite"]),
    dict(id="gemma-4-31b", name="Gemma 4 31B", dev="Google", tier=S, aliases=["Gemma 4 31B", "gemma-4-31b-it", "Google: Gemma 4 31B"], vendor=["gemma-4-31B-it", "Google: Gemma 4 31B"]),
    dict(id="gemma-4-26b-a4b", name="Gemma 4 26B A4B", dev="Google", tier=S, aliases=["Gemma 4 26B A4B", "gemma-4-26b-a4b-it", "Google: Gemma 4 26B A4B"], vendor=["gemma-4-26B-A4B-it", "Google: Gemma 4 26B A4B "]),
    # xAI
    dict(id="grok-4-7", name="Grok 4.7", dev="xAI", tier=F, aliases=["Grok 4.7", "grok-4.7", "grok-4-7"], vendor=["Grok 4.7"]),
    dict(id="grok-build-0-1", name="Grok Build 0.1", dev="xAI", tier=M, aliases=["Grok Build 0.1", "grok-build-0.1"], vendor=["Grok Build 0.1"]),
    # Meta
    dict(id="muse-wonder", name="Muse Wonder", dev="Meta", tier=F, aliases=["Muse Wonder", "Muse Wonder 1.0", "muse-wonder"], vendor=["Muse Wonder"]),
    dict(id="muse-spark-1-3", name="Muse Spark 1.3", dev="Meta", tier=M, aliases=["Muse Spark 1.3", "muse-spark-1.3"], vendor=["Muse Spark 1.3"]),
    dict(id="muse-ember", name="Muse Ember", dev="Meta", tier=S, aliases=["Muse Ember", "muse-ember"], vendor=["Muse Ember"]),
    dict(id="muse-spark-open", name="Muse Spark Open", dev="Meta", tier=M, aliases=["Muse Spark Open", "Muse-Spark-Open-816B-A42B", "Meta: Muse Spark Open"], vendor=["Muse Spark Open", "Meta: Muse Spark Open"]),
    dict(id="muse-glimmer-30b", name="Muse Glimmer 30B", dev="Meta", tier=S, aliases=["Muse Glimmer", "Muse Glimmer 30B", "Muse-Glimmer-30B", "Meta: Muse Glimmer 30B"], vendor=["Muse Glimmer-30B", "Meta: Muse Glimmer 30B"]),
    # Mistral
    dict(id="mistral-large-4", name="Mistral Large 4", dev="Mistral AI", tier=F, aliases=["Mistral Large 4", "mistral-large-4", "Mistral-Large-4-1T-A52B"], vendor=["Mistral Large 4"]),
    dict(id="mistral-small-4", name="Mistral Small 4", dev="Mistral AI", tier=S, aliases=["Mistral Small 4", "mistral-small-4", "Mistral-Small-4-119B-2603"], vendor=["Mistral Small 4"]),
    # Cohere
    dict(id="command-a-plus", name="Command A+", dev="Cohere", tier=F, aliases=["Command A+", "command-a-plus", "command-a-plus-05-2026"], vendor=["command-a-plus-05-2026", "CohereLabs/command-a-plus-05-2026-bf16", "Command A+"]),
    # Amazon
    dict(id="nova-2-pro", name="Amazon Nova 2 Pro", dev="Amazon", tier=F, aliases=["Amazon Nova 2 Pro", "Nova 2 Pro", "nova-2-pro"], vendor=["Amazon Nova 2 Pro (Preview)"]),
    dict(id="nova-2-lite", name="Amazon Nova 2 Lite", dev="Amazon", tier=S, aliases=["Amazon Nova 2 Lite", "Nova 2 Lite", "nova-2-lite"], vendor=["Nova 2 Lite", "Amazon Nova 2 Lite"]),
    # DeepSeek
    dict(id="deepseek-v4-pro", name="DeepSeek V4 Pro", dev="DeepSeek", tier=F, aliases=["DeepSeek V4 Pro", "DeepSeek-V4-Pro", "deepseek-v4-pro"], vendor=["DeepSeek-V4-Pro-0813", "deepseek-v4-pro (DeepSeek-V4-Pro-0813)"], snapshots=["0813", "20260813"]),
    dict(id="deepseek-v4-1-flash", name="DeepSeek V4.1 Flash", dev="DeepSeek", tier=M, aliases=["DeepSeek V4.1 Flash", "DS-V4.1-Flash", "DeepSeek-V4.1-Flash", "deepseek-flash"], vendor=["DeepSeek-V4.1-Flash-1017", "deepseek-flash (DeepSeek-V4.1-Flash-1017)"], snapshots=["1017", "20261017"]),
    # Alibaba
    dict(id="qwen3-8-max", name="Qwen3.8-Max", dev="Alibaba (Qwen)", tier=F, aliases=["Qwen3.8-Max", "Qwen3.8 Max", "qwen3.8-max"], vendor=["Qwen3.8-Max"], show_snapshot=True),
    dict(id="qwen3-8-flash-next", name="Qwen3.8-Flash-Next", dev="Alibaba (Qwen)", tier=S, aliases=["Qwen3.8-Flash-Next", "Qwen3.8 Flash Next"], vendor=["Qwen3.8-Flash-Next"]),
    dict(id="qwen3-8-27b", name="Qwen3.8 27B", dev="Alibaba (Qwen)", tier=S, aliases=["Qwen3.8 27B", "Qwen3.8-27B", "qwen3.8-27b"], vendor=["Qwen3.8-27B", "qwen3.8-27b"]),
    # Moonshot
    dict(id="kimi-k3-1-pro", name="Kimi K3.1 Pro", dev="Moonshot AI", tier=F, aliases=["Kimi K3.1 Pro", "Kimi-K3.1-Pro", "kimi-k3.1-pro"], vendor=["Kimi-K3.1-Pro", "kimi-k3.1-pro"]),
    # Z.ai
    dict(id="glm-5-3", name="GLM-5.3", dev="Z.ai", tier=F, aliases=["GLM-5.3", "GLM 5.3", "glm-5.3"], vendor=["GLM-5.3"]),
    dict(id="glm-5-3-flash", name="GLM-5.3-Flash", dev="Z.ai", tier=S, aliases=["GLM-5.3-Flash", "GLM 5.3 Flash"], vendor=["GLM-5.3-Flash"]),
    # MiniMax
    dict(id="minimax-m3-1-flash", name="MiniMax-M3.1-Flash", dev="MiniMax", tier=M, aliases=["MiniMax-M3.1-Flash", "MiniMax M3.1 Flash", "MiniMax-M3.1"], vendor=["MiniMax-M3.1-Flash"]),
    dict(id="minimax-m3", name="MiniMax-M3", dev="MiniMax", tier=F, aliases=["MiniMax-M3", "MiniMax M3"], vendor=["MiniMax-M3"]),
    # NVIDIA
    dict(id="nemotron-3-ultra", name="Nemotron 3 Ultra", dev="NVIDIA", tier=F, aliases=["Nemotron 3 Ultra", "Nemotron 3 Ultra 550B A55B", "NVIDIA-Nemotron-3-Ultra-550B-A55B", "NVIDIA: Nemotron 3 Ultra"], vendor=["NVIDIA-Nemotron-3-Ultra-550B-A55B", "NVIDIA: Nemotron 3 Ultra"]),
    dict(id="nemotron-3-5-super-vl", name="Nemotron 3.5 Super VL", dev="NVIDIA", tier=M, aliases=["Nemotron 3.5 Super VL", "NVIDIA-Nemotron-3.5-Super-VL-120B-A12B", "Nemotron-3.5-Super-VL-120B-A12B", "NVIDIA: Nemotron 3.5 Super VL"], vendor=["NVIDIA-Nemotron-3.5-Super-VL-120B-A12B", "NVIDIA: Nemotron 3.5 Super VL"]),
    dict(id="nemotron-3-5-lightning", name="Nemotron 3.5 Lightning", dev="NVIDIA", tier=S, aliases=["Nemotron 3.5 Lightning", "NVIDIA-Nemotron-3.5-Lightning-30B-A3B", "Nemotron-3.5-Lightning-30B-A3B-BF16", "NVIDIA: Nemotron 3.5 Lightning"], vendor=["NVIDIA-Nemotron-3.5-Lightning-30B-A3B", "NVIDIA: Nemotron 3.5 Lightning"]),
    # Others
    dict(id="phi-4-reasoning-vision", name="Phi-4-reasoning-vision 15B", dev="Microsoft", tier=S, aliases=["Phi-4-reasoning-vision-15B", "Phi-4 reasoning vision"], vendor=["Phi-4-reasoning-vision-15B"]),
    dict(id="granite-4-2-8b", name="Granite 4.2 8B", dev="IBM", tier=S, aliases=["Granite 4.2 8B", "granite-4.2-8b", "IBM: Granite 4.2 8B"], vendor=["granite-4.2-8b", "IBM: Granite 4.2 8B"]),
    dict(id="mimo-v2-6-pro", name="MiMo-V2.6-Pro", dev="Xiaomi", tier=F, aliases=["MiMo-V2.6-Pro", "MiMo V2.6 Pro", "MiMo-V2.6-Pro-RL", "Xiaomi: MiMo-V2.6-Pro"], vendor=["MiMo-V2.6-Pro-RL", "Xiaomi: MiMo-V2.6-Pro"]),
    dict(id="step-5-preview", name="Step 5 Preview", dev="StepFun", tier=F, aliases=["Step 5 Preview", "Step-5-Preview", "StepFun: Step 5 Preview"], vendor=["Step-5-Preview", "StepFun: Step 5 Preview"]),
    dict(id="hy4", name="Tencent Hy4", dev="Tencent", tier=F, aliases=["Tencent Hy4", "Hy4", "Tencent: Hy4"], vendor=["Tencent: Hy4"]),
    dict(id="inkling", name="Inkling", dev="Thinking Machines Lab", tier=F, aliases=["Inkling", "Thinking Machines: Inkling"], vendor=["Inkling", "Thinking Machines: Inkling"]),
    dict(id="beam-1-0", name="Beam 1.0", dev="Reflection AI", tier=F, aliases=["Beam 1.0", "Beam", "Beam-1.0-501B-A23B", "Reflection: Beam 1.0 501B A23B"], vendor=["Beam-1.0-501B-A23B", "Reflection: Beam 1.0 501B A23B"]),
    dict(id="ling-3-1-flash", name="Ling 3.1 Flash", dev="inclusionAI (Ant Group)", tier=M, aliases=["Ling 3.1 Flash", "Ling-3.1-flash", "inclusionAI: Ling 3.1 Flash"], vendor=["Ling-3.1-flash", "inclusionAI: Ling 3.1 Flash"]),
]
