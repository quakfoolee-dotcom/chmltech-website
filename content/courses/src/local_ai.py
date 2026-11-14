"""Source for content/courses/local-ai.json (run: python3 content/courses/src/local_ai.py)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import step, E, write

POST = '<a href="../post/private-ai-assistant-on-your-own-pc-anythingllm-and-ollama.html">Private AI assistant on your own PC</a>'

M1 = [
step("Cloud AI and private options", 7, """
<p>Most people meet AI through cloud services such as ChatGPT, Claude, Gemini or Microsoft Copilot. These are powerful and easy to use, but your prompts and files are processed on the provider's servers. For many tasks that is fine. For some, such as confidential contracts, customer records, health information or proprietary designs, businesses want more control.</p>
<h3>A spectrum of options</h3>
<table><thead><tr><th>Option</th><th>Where data is processed</th><th>Control</th><th>Typical use</th></tr></thead><tbody>
<tr><td>Consumer AI apps</td><td>Provider's cloud; data may be used to improve services depending on settings</td><td>Low</td><td>Public information, personal use</td></tr>
<tr><td>Business and enterprise AI plans</td><td>Provider's cloud, with contractual data protections and admin controls</td><td>Medium</td><td>Most everyday business work under policy</td></tr>
<tr><td>Cloud AI in your own cloud account</td><td>Models hosted in your cloud tenant or region</td><td>Medium-high</td><td>Data residency needs, custom applications</td></tr>
<tr><td>Local or on-premises AI</td><td>Your own computers or servers</td><td>High</td><td>Highly sensitive data, offline use, full control</td></tr>
</tbody></table>
<h3>What "local AI" means</h3>
<p>Local AI runs an <strong>open-weight</strong> language model, one whose model files can be downloaded, on hardware you control: a desktop with a capable graphics card, a laptop, or a small server for a team. Prompts and documents never leave your premises unless you send them elsewhere.</p>
<h3>Not all or nothing</h3>
<p>Most organizations use a <strong>hybrid</strong> approach: approved business cloud AI for everyday work, and local AI for the most sensitive tasks. This course helps you decide where local AI fits, set it up, connect it to your documents, run it safely and measure whether it is worth it.</p>
""", ["AI options range from consumer apps to business cloud plans to fully local models.", "Local AI runs open-weight models on hardware you control.", "Most businesses use a hybrid: business cloud for everyday work, local for the most sensitive."],
 "List five AI tasks your team does or wants to do. For each, note how sensitive the data is and which option on the spectrum fits.",
 "What is the main difference between local AI and consumer cloud AI?", ["Local AI is always more accurate", "With local AI, prompts and documents are processed on hardware you control", "Cloud AI cannot summarize documents", "Local AI needs no hardware"], 1,
 "Local AI keeps processing on your own systems."),
step("When local AI makes sense", 7, """
<p>Local AI brings control, but also responsibility and some limits. It makes most sense when one or more of these apply.</p>
<h3>Reasons to consider local AI</h3>
<ul><li><strong>Sensitive data:</strong> legal, financial, health, personnel or proprietary technical information that your policy or clients don't allow in third-party services.</li>
<li><strong>Client or contract requirements:</strong> customers who require that their data stays on your systems.</li>
<li><strong>Data residency:</strong> a need to keep data in Canada or on-premises.</li>
<li><strong>Offline or remote work:</strong> field sites, plants or vessels with poor connectivity.</li>
<li><strong>Cost at volume:</strong> heavy, repetitive use, such as processing thousands of documents, where per-use cloud fees add up.</li>
<li><strong>Control:</strong> a fixed model version that won't change behaviour without notice.</li></ul>
<h3>Reasons to stay with business cloud AI</h3>
<ul><li>You need the most capable models for complex reasoning, writing or coding.</li>
<li>You have no one to set up and maintain local systems.</li>
<li>Usage is light, so subscriptions cost less than hardware and time.</li>
<li>Enterprise plans already meet your data protection needs.</li></ul>
<h3>Be honest about trade-offs</h3>
<p>Open-weight models that run on modest hardware are capable for many tasks, such as summarizing, drafting, extraction and document Q&amp;A, but typically less capable than the largest frontier cloud models on difficult reasoning. Local AI also needs setup, updates, security and support. The lab after this lesson asks you to decide where different data belongs.</p>
""", ["Consider local AI for sensitive data, client requirements, residency, offline work, high volume or control.", "Stay with business cloud AI when you need top capability or lack support capacity.", "Local models on modest hardware are capable but usually behind frontier models on hard tasks."],
 "For your most sensitive AI use case, write down which of the six reasons apply and what would happen if the data went to a cloud provider.",
 "Which situation most strongly favours local AI?", ["Writing a public blog post", "A client contract requires that its confidential data stays on your systems", "Translating a public product sheet", "Brainstorming event names"], 1,
 "Contractual data-location requirements are a clear case for local processing."),
step("Open-weight models explained", 7, """
<p><strong>Open-weight models</strong> are language models whose trained parameters (weights) are published for download. Several AI labs and research groups release them in families of different sizes, such as Meta's Llama, Mistral, Alibaba's Qwen, Google's Gemma and OpenAI's open-weight models, among others. New versions appear frequently.</p>
<h3>Size and capability</h3>
<p>Model size is measured in <strong>parameters</strong>, usually billions (B). Larger models are generally more capable but need more memory and run more slowly. Small models (a few billion parameters) run on laptops and handle simple tasks; medium models (roughly 7 to 15B) run on a single good graphics card and handle most office tasks well; larger models (30B and up) need high-end hardware but come closer to cloud quality.</p>
<h3>Specialized models</h3>
<ul><li><strong>Chat or instruct models:</strong> tuned to follow instructions and converse.</li>
<li><strong>Coding models:</strong> tuned for writing and explaining code.</li>
<li><strong>Embedding models:</strong> turn text into numerical vectors for search; essential for chatting with documents.</li>
<li><strong>Vision models:</strong> can read images and scanned documents.</li></ul>
<h3>Licences matter</h3>
<p>"Open-weight" doesn't always mean "open source" or "free for any use". Licences vary: some allow broad commercial use, others restrict use above a certain number of users or for certain purposes. Read the licence before using a model in your business.</p>
<h3>Source and integrity</h3>
<p>Download models from the publisher or reputable repositories through established tools. Model files from unknown sources can be tampered with. Record which model and version you use, so results can be reproduced and issues traced.</p>
""", ["Open-weight models can be downloaded and run locally in various sizes.", "Larger models are more capable but need more memory; embedding models power document search.", "Check licences and download from reputable sources."],
 "Pick two open-weight model families and look up their sizes and licence terms. Note any commercial use restrictions.",
 "What does an embedding model do?", ["Writes long essays", "Turns text into numerical vectors so documents can be searched by meaning", "Draws images", "Compresses video"], 1,
 "Embeddings let systems find relevant passages by meaning."),
step("Hardware: memory, GPUs and quantization", 8, """
<p>The main hardware limit for local AI is <strong>memory</strong>: the model must fit in the memory of the graphics card (GPU) or, more slowly, in system memory.</p>
<h3>Quantization</h3>
<p>Models are usually run in <strong>quantized</strong> form, storing each parameter with fewer bits, commonly 4 to 8 bits instead of 16. This cuts memory needs several-fold with a modest loss of quality. As a rough guide, a 4-bit quantized model needs about 0.5 to 0.7 GB of memory per billion parameters, plus extra for the conversation context.</p>
<table><thead><tr><th>Model size</th><th>Approximate memory at 4-bit</th><th>Typical hardware</th></tr></thead><tbody>
<tr><td>3–4B</td><td>2–3 GB</td><td>Recent laptops, even without a dedicated GPU (slower)</td></tr>
<tr><td>7–8B</td><td>5–6 GB</td><td>Graphics card with 8 GB or more</td></tr>
<tr><td>12–14B</td><td>8–10 GB</td><td>Graphics card with 12 to 16 GB</td></tr>
<tr><td>30–32B</td><td>18–22 GB</td><td>Graphics card with 24 GB, or a high-memory workstation</td></tr>
<tr><td>70B</td><td>40 GB or more</td><td>Multiple GPUs, a workstation GPU or a high-memory unified-memory computer</td></tr>
</tbody></table>
<p>These are approximate; actual needs vary with the model, quantization method and context length.</p>
<h3>Other options</h3>
<ul><li><strong>Unified memory computers</strong>, such as Apple silicon Macs, share memory between processor and graphics and can run fairly large models.</li>
<li><strong>CPU only:</strong> works for small models but is much slower.</li>
<li><strong>Small servers</strong> with one or more GPUs can serve a team.</li></ul>
<h3>Speed</h3>
<p>Speed is measured in tokens per second. For interactive chat, a reply that streams at reading speed or faster feels comfortable. Models that spill out of GPU memory into system memory slow down sharply, so choose a model that fits.</p>
""", ["Memory is the main constraint; the model must fit in GPU or unified memory.", "4-bit quantization needs roughly 0.5 to 0.7 GB per billion parameters plus context.", "A 12–16 GB graphics card comfortably runs 7–14B models."],
 "Check the GPU memory or unified memory of a computer you could use. Using the table, list the model sizes it could run comfortably.",
 "Roughly how much memory does a 4-bit quantized 8B model need?", ["About 1 GB", "About 5 to 6 GB", "About 40 GB", "About 200 GB"], 1,
 "At about 0.5 to 0.7 GB per billion parameters, an 8B model needs roughly 5 to 6 GB plus context."),
]

M2 = [
step("Tools for running local AI", 7, """
<p>You don't need to write code to run local AI. Several free tools make it straightforward.</p>
<table><thead><tr><th>Tool</th><th>What it does</th><th>Good for</th></tr></thead><tbody>
<tr><td>Ollama</td><td>Downloads and runs models with one command; provides a local API other apps can use</td><td>A simple model engine on a PC or server</td></tr>
<tr><td>LM Studio</td><td>Desktop app to find, download and chat with models, with a local API</td><td>Individuals trying models on a desktop</td></tr>
<tr><td>llama.cpp</td><td>The efficient engine behind many tools; runs on CPU and GPU</td><td>Technical users and custom setups</td></tr>
<tr><td>Open WebUI</td><td>A web chat interface for local models, with users and document features</td><td>Team access through a browser</td></tr>
<tr><td>AnythingLLM</td><td>Desktop or server app for chatting with documents (RAG), workspaces and agents, using local or cloud models</td><td>Private document Q&amp;A without coding</td></tr>
</tbody></table>
<h3>A simple starting setup</h3>
<ol><li>Install Ollama on a computer with a suitable graphics card.</li>
<li>Download a medium-sized instruct model and an embedding model.</li>
<li>Install a front end such as AnythingLLM or Open WebUI and point it at Ollama.</li>
<li>Create a workspace, upload a few non-critical documents and test questions.</li></ol>
<p>The Chmltech Insights article """ + POST + """ walks through this setup step by step, including choosing models, embeddings, chunking and security settings.</p>
<h3>Keep it up to date</h3>
<p>These tools change quickly. Update them regularly for security fixes and improvements, and check release notes before updating a system the team depends on.</p>
""", ["Ollama and LM Studio run models; Open WebUI and AnythingLLM add chat and document features.", "Start with one PC, a medium instruct model, an embedding model and a front end.", "Update tools regularly and check release notes first."],
 "Install a local model engine and one front end on a test computer, download one instruct model and chat with it about a public document.",
 "What does Ollama mainly provide?", ["Cloud hosting for websites", "A simple way to download and run models locally, with a local API", "An accounting system", "A firewall"], 1,
 "Ollama is a model engine for running models locally."),
step("Choosing a model for the task", 7, """
<p>No single model is best at everything. Choose by task, hardware and licence, then test with your own examples.</p>
<h3>Match model to task</h3>
<table><thead><tr><th>Task</th><th>What to look for</th></tr></thead><tbody>
<tr><td>Summarizing and drafting</td><td>A good general instruct model in the size your hardware allows</td></tr>
<tr><td>Document Q&amp;A</td><td>A general instruct model plus a good embedding model; long-context support helps</td></tr>
<tr><td>Extracting data into tables</td><td>Models that follow formatting instructions well</td></tr>
<tr><td>Coding help</td><td>A coding-tuned model</td></tr>
<tr><td>Scanned documents and images</td><td>A vision-capable model, or OCR before the language model</td></tr>
<tr><td>French or other languages</td><td>Models trained well in those languages; test them</td></tr>
</tbody></table>
<h3>Build a small test set</h3>
<p>Collect 10 to 20 realistic tasks from your work, with what a good answer looks like. Run each candidate model on the set and score the results for accuracy, completeness, format and speed. This takes an afternoon and is far more reliable than general rankings, because it reflects your documents and your questions.</p>
<h3>Settings that matter</h3>
<ul><li><strong>Context length:</strong> how much text the model can consider at once; longer contexts use more memory.</li>
<li><strong>Temperature:</strong> lower values give more consistent, focused answers, which suit business tasks.</li>
<li><strong>System prompt:</strong> standing instructions such as "answer only from the provided documents and say when you don't know".</li></ul>
<h3>Revisit regularly</h3>
<p>New open-weight models are released often, and a newer model of the same size may be much better. Re-run your test set when a promising model appears.</p>
""", ["Choose models by task, hardware and licence.", "Test candidates on 10 to 20 of your own tasks rather than relying on rankings.", "Tune context, temperature and system prompt, and retest when new models appear."],
 "Write ten realistic test tasks from your work with notes on a good answer. Run two candidate models and score them.",
 "What is the most reliable way to choose between local models for your business?", ["Pick the newest model", "Test candidates on a small set of your own realistic tasks", "Choose the largest file", "Ask a friend"], 1,
 "Your own test set reflects your real documents and questions."),
step("Chatting with your documents: RAG", 8, """
<p>Language models don't know your company's documents. <strong>Retrieval-augmented generation (RAG)</strong> lets a model answer questions using your files, such as procedures, contracts, manuals and reports, without retraining it.</p>
<h3>How RAG works</h3>
<ol><li><strong>Ingest:</strong> documents are loaded and converted to text.</li>
<li><strong>Chunk:</strong> text is split into passages, for example a few hundred words each, often with some overlap.</li>
<li><strong>Embed:</strong> an embedding model converts each chunk into a vector that represents its meaning.</li>
<li><strong>Store:</strong> vectors are saved in a vector database.</li>
<li><strong>Retrieve:</strong> when a user asks a question, the question is embedded and the most similar chunks are found.</li>
<li><strong>Generate:</strong> the model receives the question plus the retrieved chunks and writes an answer, ideally citing the sources.</li></ol>
<h3>Why it works well locally</h3>
<p>All steps can run on your own hardware: the embedding model, the vector database and the language model. Documents never leave your systems. Tools such as AnythingLLM and Open WebUI handle these steps for you.</p>
<h3>Good uses</h3>
<ul><li>"What is our procedure for returning a damaged shipment?" from the quality manual.</li>
<li>"What are the termination terms in the Acme contract?" from a contract library.</li>
<li>"What torque does the maintenance manual specify for this pump?"</li></ul>
<h3>Limits</h3>
<p>RAG answers are only as good as the documents and the retrieval. If the right passage isn't retrieved, the model may answer from general knowledge or guess. Always show sources so users can check the original. The next lesson covers making RAG more accurate.</p>
""", ["RAG lets a model answer from your documents without retraining.", "Steps: ingest, chunk, embed, store, retrieve, generate with sources.", "All steps can run locally; answers depend on document quality and retrieval."],
 "Choose a small, non-critical document set, such as one procedure manual, load it into a local RAG tool and ask ten questions you know the answers to.",
 "In RAG, what does the retrieval step do?", ["Trains a new model", "Finds the document chunks most relevant to the question", "Deletes old documents", "Translates the documents"], 1,
 "Retrieval selects relevant passages for the model to use."),
step("Making document answers accurate", 7, """
<p>Most RAG accuracy problems come from documents and settings, not the model. A few practices make a large difference.</p>
<h3>Prepare documents</h3>
<ul><li>Use clean, text-based files; run OCR on scanned PDFs and check the result.</li>
<li>Remove outdated versions and duplicates so old answers don't appear.</li>
<li>Keep headings and structure; they help chunking and retrieval.</li>
<li>Organize documents into separate workspaces by topic or department so retrieval searches the right set.</li></ul>
<h3>Tune retrieval</h3>
<ul><li><strong>Chunk size:</strong> too small loses context, too large dilutes relevance. A few hundred words with some overlap is a common start.</li>
<li><strong>Number of chunks retrieved:</strong> enough to cover the answer without flooding the model; test a few values.</li>
<li><strong>Embedding model:</strong> a better embedding model often improves accuracy more than a bigger language model.</li></ul>
<h3>Instruct the model</h3>
<p>Use a system prompt such as: "Answer only from the provided documents. Quote or cite the source. If the answer isn't in the documents, say so." This reduces made-up answers.</p>
<h3>Evaluate</h3>
<p>Create 20 to 30 test questions with known answers and their source documents. Run them after each change and track how many are answered correctly with the right source. Ask users to flag wrong answers, and add those questions to the test set.</p>
<p>Document Q&amp;A supports people; for decisions with legal, safety or financial consequences, users should read the cited source.</p>
""", ["Prepare clean, current, well-structured documents in focused workspaces.", "Tune chunk size, number of chunks and the embedding model.", "Instruct the model to cite and admit gaps, and evaluate with a test set."],
 "Write 20 test questions with answers and sources for your document set. Run them, change one setting, and compare the score.",
 "A RAG system keeps quoting an outdated procedure. What is the most likely fix?", ["Use a bigger language model", "Remove outdated versions from the document set", "Increase the temperature", "Turn off citations"], 1,
 "Old versions in the document set produce old answers; remove them."),
]

M3 = [
step("Securing local AI", 7, """
<p>Local AI keeps data in-house, but the system itself must be secured like any other server or application.</p>
<h3>Key practices</h3>
<ul><li><strong>Don't expose it to the internet.</strong> Local model servers and chat interfaces should be reachable only on your internal network or through a VPN, never directly from the internet.</li>
<li><strong>Require logins</strong> with strong passwords and multi-factor authentication where the tool supports it; give each person their own account.</li>
<li><strong>Limit access by workspace:</strong> HR documents should only be searchable by HR, contracts by those who need them.</li>
<li><strong>Keep software updated:</strong> the model engine, front end, operating system and drivers.</li>
<li><strong>Protect the machine:</strong> disk encryption, endpoint protection and physical security for the computer or server.</li>
<li><strong>Back up</strong> configurations and the document store, and keep the original documents in their normal managed location.</li></ul>
<h3>Model and tool provenance</h3>
<p>Download models and plug-ins only from reputable sources. Prefer widely used tools with active maintenance. Be careful with community add-ons that run code.</p>
<h3>Prompt injection</h3>
<p>Documents can contain hidden or malicious instructions, such as text telling the AI to ignore its rules. This matters most when the AI can take actions, such as sending email or running tools. Limit what local agents can do, require human approval for actions and treat content from outside sources with caution.</p>
<p>The Cybersecurity and Ransomware Basics for SMEs course covers broader security practices that apply here.</p>
""", ["Never expose local AI directly to the internet; use internal networks or VPN.", "Require individual logins, limit workspaces by role and keep everything updated.", "Use reputable models and tools, and guard against prompt injection when AI can act."],
 "Check where your local AI tool listens on the network and who can log in. Close any internet exposure and set up per-user accounts.",
 "How should a local AI server be accessed by remote staff?", ["Open it directly to the internet for convenience", "Through a VPN or internal network with individual logins", "By sharing one password with everyone", "By emailing prompts to the IT person"], 1,
 "A VPN and individual accounts keep the system off the open internet and accountable."),
step("Privacy and compliance", 7, """
<p>Running AI locally helps with privacy, but it doesn't remove legal duties for the personal information you process.</p>
<h3>Privacy principles still apply</h3>
<p>Canadian privacy law, including PIPEDA, applies to personal information wherever it is processed. Key principles:</p>
<ul><li><strong>Purpose:</strong> use personal information only for the purposes it was collected for, or with consent.</li>
<li><strong>Minimization:</strong> load only the documents and information the use case needs.</li>
<li><strong>Safeguards:</strong> protect it with security appropriate to its sensitivity.</li>
<li><strong>Access:</strong> limit who can query workspaces containing personal information.</li>
<li><strong>Retention:</strong> remove documents and chat logs when no longer needed.</li></ul>
<h3>Logs and chat history</h3>
<p>Local tools often store every prompt and answer. Those logs can contain sensitive information. Decide whether to keep them, for how long and who can see them, and configure the tool accordingly.</p>
<h3>Client and contract obligations</h3>
<p>If clients have shared confidential information under agreements, check whether using it in any AI system, even a local one, is permitted, and whether you must tell them.</p>
<h3>Document your approach</h3>
<p>Write a short record of each local AI use case: purpose, data used, who has access, retention and safeguards. It helps answer client questions, supports privacy obligations and makes reviews easier. Get privacy or legal advice for high-risk uses, such as health information or decisions about individuals.</p>
""", ["Privacy law applies to personal information processed by local AI too.", "Minimize data, limit access, and manage logs and retention.", "Check client agreements and document each use case."],
 "Write a one-page record for one local AI use case: purpose, data, access, retention and safeguards.",
 "Does running AI locally remove obligations under privacy law?", ["Yes, completely", "No; privacy principles still apply to the personal information processed", "Only for large companies", "Only outside Canada"], 1,
 "Local processing helps but does not remove privacy duties."),
step("Desktop or team server", 7, """
<p>Local AI can start on one person's computer and grow into a shared team service. Each has its place.</p>
<table><thead><tr><th></th><th>Personal desktop</th><th>Team server</th></tr></thead><tbody>
<tr><td>Users</td><td>One person</td><td>Several people through a browser</td></tr>
<tr><td>Hardware</td><td>A PC or laptop with a suitable GPU or unified memory</td><td>A server or workstation with one or more GPUs</td></tr>
<tr><td>Setup</td><td>Simple; desktop apps</td><td>Needs IT skills: networking, accounts, backups</td></tr>
<tr><td>Concurrency</td><td>Not an issue</td><td>Several simultaneous users slow responses; size hardware accordingly</td></tr>
<tr><td>Governance</td><td>Personal discipline</td><td>Workspaces, permissions, logs and support</td></tr>
</tbody></table>
<h3>Start small</h3>
<p>Many SMEs begin with a pilot on one capable desktop used by a few people for a defined use case, such as searching the quality manual or summarizing contracts. If it proves useful, they move to a small server with proper accounts and backups.</p>
<h3>Operating a team server</h3>
<ul><li>Name an owner responsible for updates, access and support.</li>
<li>Monitor usage and response times to know when hardware needs upgrading.</li>
<li>Plan for power, cooling and noise: GPUs under load use significant power.</li>
<li>Keep a simple runbook: how to restart services, update models and restore from backup.</li></ul>
<h3>Managed private options</h3>
<p>Some providers offer private AI hosted in Canadian data centres or in your own cloud account, managed for you. These can give much of the control of local AI without running hardware yourself. Compare them on data location, contract terms and cost.</p>
""", ["Start with a desktop pilot; move to a team server when value is proven.", "Team servers need an owner, accounts, backups, monitoring and a runbook.", "Consider managed private hosting in Canada as an alternative to running hardware."],
 "Decide whether a desktop pilot or a team server suits your first use case, and name the owner who will look after it.",
 "What usually happens when several people use one local AI server at the same time?", ["Nothing changes", "Responses slow down, so hardware must be sized for concurrent users", "The model becomes more accurate", "The server shuts down"], 1,
 "Concurrent requests share the GPU, slowing responses."),
step("Limits and the hybrid approach", 7, """
<p>Local AI is a valuable tool, not a replacement for every cloud service. Knowing its limits avoids disappointment.</p>
<h3>Common limits</h3>
<ul><li><strong>Capability:</strong> models that fit on modest hardware typically trail the largest frontier models on complex reasoning, nuanced writing and advanced coding.</li>
<li><strong>Hallucination:</strong> local models can make things up, like any model; RAG with citations helps but doesn't eliminate it.</li>
<li><strong>Speed:</strong> large models on limited hardware can be slow.</li>
<li><strong>Features:</strong> cloud services often include web search, advanced file handling, voice and integrations out of the box.</li>
<li><strong>Maintenance:</strong> someone must update, secure and support the system.</li></ul>
<h3>A sensible hybrid</h3>
<table><thead><tr><th>Work</th><th>Where to run it</th></tr></thead><tbody>
<tr><td>Public information, general writing, research</td><td>Approved business cloud AI</td></tr>
<tr><td>Internal non-sensitive documents</td><td>Business cloud AI under policy, or local</td></tr>
<tr><td>Confidential client, legal, HR or technical documents</td><td>Local or private-hosted AI</td></tr>
<tr><td>Credentials and banking details</td><td>Never in any AI tool</td></tr>
</tbody></table>
<h3>Watch the trend</h3>
<p>Open-weight models have improved quickly, and hardware keeps getting more capable. Tasks that needed cloud models a year ago can often run locally today. Revisit your split every six to twelve months using your test set.</p>
""", ["Local models usually trail frontier models on hard tasks and need maintenance.", "Use a hybrid: cloud for general work, local for confidential documents, never for credentials.", "Re-test every six to twelve months as models improve."],
 "Draft a one-page hybrid AI policy for your team using the table in this lesson as a starting point.",
 "Which work belongs on local or private-hosted AI in a hybrid approach?", ["Public blog drafts", "Confidential client, legal, HR or technical documents", "Credentials and banking details", "General web research"], 1,
 "Sensitive documents are the main case for local processing; credentials never go into AI tools."),
]

M4 = [
step("Use cases for SMEs", 7, """
<p>The best local AI use cases combine sensitive or proprietary information with repeated, text-heavy work.</p>
<table><thead><tr><th>Use case</th><th>Example</th></tr></thead><tbody>
<tr><td>Internal knowledge assistant</td><td>Staff ask questions of procedures, quality manuals, HR policies and technical documents, with cited answers</td></tr>
<tr><td>Contract and document review</td><td>Summarize contracts, find key clauses, compare versions, keeping documents in-house</td></tr>
<tr><td>Confidential drafting</td><td>Draft proposals, reports and letters that include client data or pricing</td></tr>
<tr><td>Technical and engineering support</td><td>Search past project files, specifications and maintenance manuals</td></tr>
<tr><td>Data extraction</td><td>Pull fields from invoices, certificates or forms into structured records</td></tr>
<tr><td>Coding help</td><td>Code assistance on proprietary software without sending code to the cloud</td></tr>
<tr><td>Offline field use</td><td>A laptop assistant with manuals and procedures at remote sites</td></tr>
</tbody></table>
<h3>Choosing the first use case</h3>
<ul><li>Clear value: time saved or faster answers for a defined group.</li>
<li>Sensitive data that justifies local processing.</li>
<li>A manageable, well-organized document set.</li>
<li>Easy to check answers, at least during the pilot.</li>
<li>An enthusiastic owner in the business.</li></ul>
<p>An internal knowledge assistant over a quality manual or procedures library is often an ideal first project: high value, well-defined documents and answers that can be checked. The lab after this lesson asks you to rank use cases by value and sensitivity.</p>
""", ["The best local use cases combine sensitive data with repeated text-heavy work.", "Knowledge assistants, contract review and confidential drafting are common starters.", "Pick a first use case with clear value, sensitive data, organized documents and an owner."],
 "List three possible local AI use cases in your business and score each on value, sensitivity, document readiness and ease of checking.",
 "Which is often an ideal first local AI project?", ["Replacing the accounting system", "An internal knowledge assistant over a well-organized procedures or quality manual", "Generating marketing videos", "Automating payroll decisions"], 1,
 "It offers high value, defined documents and checkable answers."),
step("Comparing the cost of local and cloud AI", 7, """
<p>Local AI swaps per-user or per-use fees for upfront hardware and ongoing upkeep. Compare them honestly over a realistic period.</p>
<h3>Local costs</h3>
<ul><li><strong>Hardware:</strong> a capable GPU workstation or small server; possibly upgrades later.</li>
<li><strong>Setup time:</strong> installation, model testing, document preparation, security configuration.</li>
<li><strong>Running costs:</strong> electricity, maintenance, updates, support time and backups.</li></ul>
<h3>Cloud costs</h3>
<ul><li>Per-user subscriptions for business AI plans, or per-use fees for API-based tools.</li>
<li>Possible add-ons for document features, higher usage or admin controls.</li></ul>
<h3>Example</h3>
<p>Fifteen users on a business AI plan at $40 a month each cost $7,200 a year, or $21,600 over three years. A local setup with $4,000 of hardware, 40 hours of setup at $90 an hour and $150 a month of upkeep costs $7,600 upfront and $5,400 in upkeep over three years: $13,000 in total. In this example local breaks even in about 17 months. With fewer users or more upkeep, cloud wins.</p>
<h3>Not just cost</h3>
<p>The comparison isn't only financial. Cloud plans often give access to more capable models and features; local gives control and privacy. Many businesses keep both, using local only for sensitive work, which changes the numbers: compare the cost of the local system with the value of being able to use AI on documents you otherwise couldn't use it on at all.</p>
<p>The lab after this lesson compares the two for your own numbers.</p>
""", ["Local swaps subscriptions for hardware, setup time and upkeep.", "Compare over a realistic period, such as three years.", "Weigh capability and the value of using AI on otherwise off-limits data, not only cost."],
 "Estimate your own three-year cost for cloud and local options using the lab, and write down what non-financial factors matter most.",
 "15 users at $40 per user per month. What is the cloud cost over three years?", ["$7,200", "$14,400", "$21,600", "$1,800"], 2,
 "15 × $40 × 36 months = $21,600."),
step("Local agents and connecting tools", 7, """
<p>Beyond chat and document Q&amp;A, local models can power <strong>agents</strong>: AI that uses tools to take steps, such as searching files, querying a database, filling a form or drafting an email for approval.</p>
<h3>How local agents connect to tools</h3>
<ul><li><strong>Function or tool calling:</strong> many models can request a specific tool with structured inputs, which the application then runs.</li>
<li><strong>Model Context Protocol (MCP):</strong> an open standard for connecting AI applications to tools and data sources. Some local front ends support MCP servers.</li>
<li><strong>Built-in skills:</strong> tools such as AnythingLLM offer agent skills like web search, file saving and summarization.</li></ul>
<h3>Start with read-only tools</h3>
<p>The safest first agents only read: search documents, look up an order status in a read-only database view, or summarize files. Tools that change data, send messages or spend money carry more risk.</p>
<h3>Safeguards</h3>
<ul><li>Give agents the minimum permissions they need, with separate service accounts.</li>
<li>Require human approval for any action with external, financial or irreversible effects.</li>
<li>Log every tool call and review the logs during pilots.</li>
<li>Test with tricky inputs, including documents containing misleading instructions.</li></ul>
<h3>Capability matters</h3>
<p>Reliable multi-step tool use is demanding, and smaller local models are often less reliable at it than large cloud models. Keep local agents to simple, well-defined tasks and test them thoroughly. The AI Agents for Business Operations course covers agent design in depth.</p>
""", ["Local models can act as agents through tool calling and MCP.", "Start with read-only tools and require human approval for consequential actions.", "Smaller models are less reliable at multi-step tool use; keep tasks simple and test."],
 "Pick one read-only task an agent could do with your local setup, such as searching a document library. Write the permissions it needs and how you would log its actions.",
 "What is the safest first kind of local AI agent?", ["One that sends payments automatically", "One that only reads, such as searching documents", "One with administrator access to all systems", "One that deletes old files"], 1,
 "Read-only agents carry far less risk than agents that change or send things."),
step("Your 90-day private AI pilot", 7, """
<p>A structured pilot proves whether local AI delivers value before you invest further.</p>
<table><thead><tr><th>Days</th><th>Focus</th><th>Actions</th></tr></thead><tbody>
<tr><td>1–30</td><td>Choose and prepare</td><td>Pick one use case and owner; write the use case record (purpose, data, access, retention); select hardware; install engine and front end; prepare and clean the document set; build a 20-question test set</td></tr>
<tr><td>31–60</td><td>Pilot</td><td>Test two or three models and settings against the test set; secure the system (internal access only, individual logins, workspace permissions); train 3 to 10 pilot users; collect feedback and wrong answers weekly</td></tr>
<tr><td>61–90</td><td>Measure and decide</td><td>Measure accuracy on the test set and time saved; compare costs with cloud options; decide to stop, continue on a desktop, move to a team server or use private hosting; write the hybrid AI policy</td></tr>
</tbody></table>
<h3>Success measures</h3>
<ul><li>Share of test questions answered correctly with the right source.</li>
<li>Time saved per week for pilot users.</li>
<li>User satisfaction and frequency of use.</li>
<li>No security or privacy incidents.</li></ul>
<h3>Where to go next</h3>
<p>The LLMs for Business Leaders course covers model choice and governance; AI Agents for Business Operations covers agent design; Building Your AI Operating System shows how local and cloud AI fit into a company-wide AI layer; and Cybersecurity and Ransomware Basics covers protecting the systems that run it.</p>
""", ["Days 1–30: choose a use case, prepare documents and a test set.", "Days 31–60: test models, secure the system and pilot with a small group.", "Days 61–90: measure accuracy, time saved and cost, then decide."],
 "Put the 90-day pilot into your calendar with an owner and choose the use case and the 20 test questions now.",
 "Which is the best measure of a document Q&A pilot's accuracy?", ["Number of documents loaded", "Share of test questions answered correctly with the right source", "GPU temperature", "Number of models downloaded"], 1,
 "A test set with known answers and sources measures accuracy directly."),
]

course = dict(
 id="private-and-local-ai-for-smes",
 title="Private and Local AI for SMEs",
 tagline="Run AI on your own hardware so sensitive documents stay in-house: choose models, chat with your files securely and decide when local beats cloud.",
 summary="A practical course for owners, managers and technically minded staff who want to use AI with sensitive information. You will learn the spectrum from consumer cloud AI to fully local models, when local AI makes sense, how open-weight models and quantization work, what hardware you need, and how to set up tools such as Ollama, LM Studio, Open WebUI and AnythingLLM. You will build accurate document Q&A with retrieval-augmented generation, secure the system, meet privacy obligations, compare costs with cloud services, connect tools safely and run a 90-day pilot.",
 audience=["Owners and managers who handle confidential client, legal, HR or technical documents",
           "IT staff and technically minded employees setting up private AI",
           "Engineering, consulting and professional firms with strict client confidentiality",
           "Teams that want AI at remote or offline sites"],
 outcomes=["Compare cloud, private-hosted and local AI options and decide where each fits",
           "Explain open-weight models, licences, quantization and hardware sizing",
           "Set up a local model engine and front end and choose models with your own test set",
           "Build and tune document Q&A with retrieval-augmented generation",
           "Secure local AI, meet privacy obligations and plan desktop or team deployments",
           "Compare local and cloud costs, connect tools safely and run a 90-day pilot"],
 modules=[
  dict(title="Why Private AI", summary="Cloud and private options, when local AI makes sense, open-weight models, and hardware and quantization.", steps=M1),
  dict(title="Setting Up", summary="Tools for running local AI, choosing models, retrieval-augmented generation and making document answers accurate.", steps=M2),
  dict(title="Running It Safely", summary="Security, privacy and compliance, desktop versus team server, and limits and the hybrid approach.", steps=M3),
  dict(title="Value and Roadmap", summary="SME use cases, cost comparison with cloud, local agents and tools, and a 90-day pilot.", steps=M4)],
 labs=[
  dict(id="local-where-data-goes", type="classify", title="Where should this work run?", after_step=2,
       intro="Decide where twelve AI tasks should run: any approved cloud AI, business cloud AI with data protections, or local / private AI only. Then check your answers.",
       config=dict(categories=["Any approved cloud AI", "Business cloud AI with data protections", "Local or private AI only"], items=[
        dict(text="Drafting a blog post from public industry news", answer=0, why="Public information carries little risk in any approved tool."),
        dict(text="Brainstorming names for a trade show booth theme", answer=0, why="No sensitive information is involved."),
        dict(text="Summarizing a published government guideline", answer=0, why="The source is public."),
        dict(text="Rewriting an internal newsletter with no personal details", answer=1, why="Internal but non-sensitive content suits business plans with data protections."),
        dict(text="Drafting a standard operating procedure from internal notes", answer=1, why="Internal know-how is best kept in tools with contractual protections."),
        dict(text="Summarizing a team meeting about next quarter's priorities", answer=1, why="Internal business information belongs in protected business tools."),
        dict(text="Turning an internal sales report into slides", answer=1, why="Business-confidential but not highly sensitive data, under policy."),
        dict(text="Reviewing a client contract shared under a strict confidentiality agreement", answer=2, why="Client agreements may require that data stays on your systems."),
        dict(text="Searching employee performance reviews and disciplinary records", answer=2, why="Highly sensitive personnel information is a strong case for local processing with tight access."),
        dict(text="Summarizing a client's proprietary process design package", answer=2, why="Proprietary client technical data should stay in-house."),
        dict(text="Answering questions on patient or health records", answer=2, why="Health information is highly sensitive and often regulated."),
        dict(text="Analyzing a confidential bid with pricing and margins", answer=2, why="Commercially sensitive pricing is best kept local."),
       ])),
  dict(id="local-use-case-matrix", type="matrix", title="Picking a first local AI use case", after_step=13,
       intro="Place seven possible use cases on a grid of business value against data sensitivity to find the best candidates for a local AI pilot.",
       config=dict(x="Data sensitivity", y="Business value", x_low="Public or low", x_high="Highly sensitive", y_low="Low value", y_high="High value",
        quadrants=dict(top_left="Use business cloud AI", top_right="Best local pilot", bottom_left="Not a priority", bottom_right="Local, but low priority"),
        items=[dict(name="Q&A over the quality and procedures manual", x=3, y=5),
               dict(name="Confidential client contract review", x=5, y=5),
               dict(name="Marketing copy from public information", x=1, y=3),
               dict(name="HR policy questions for staff", x=4, y=3),
               dict(name="Summarizing public industry news", x=1, y=1),
               dict(name="Searching past engineering project files", x=4, y=5),
               dict(name="Archive of old personnel letters", x=5, y=1)])),
  dict(id="local-cost-compare", type="calc", title="Local vs cloud AI: three-year cost", after_step=14,
       intro="Enter users, the cloud subscription price, local hardware and setup costs and monthly upkeep to compare totals and see when local breaks even.",
       config=dict(calc="local_ai_cost", note="Costs only. Cloud plans may offer more capable models and features; local gives control and lets you use AI on data you otherwise couldn't. Include realistic support time in upkeep.")),
 ],
 figures=[
  dict(step=1, type="compare", title="Business cloud AI vs local AI", caption="Toggle between the two and compare what each offers.",
       config=dict(left=dict(title="Business cloud AI", points=["Most capable models and rich features", "No hardware to run", "Data processed by the provider under contract", "Per-user subscription"]),
                   right=dict(title="Local AI", points=["Data stays on your hardware", "Works offline and with fixed model versions", "Usually smaller, less capable models", "Upfront hardware plus upkeep"]))),
  dict(step=4, type="bars", title="Approximate memory needed at 4-bit", caption="Rough guide for quantized models; actual needs vary with model, quantization and context length.",
       config=dict(unit="GB", items=[dict(label="4B model", value=3), dict(label="8B model", value=6, highlight=True), dict(label="14B model", value=10, highlight=True), dict(label="32B model", value=20), dict(label="70B model", value=42)],
        note="A graphics card with 12 to 16 GB runs 8B to 14B models comfortably.")),
  dict(step=7, type="flow", title="How retrieval-augmented generation works", caption="Click each step to see what happens to your documents and the question.",
       config=dict(steps=[
        dict(label="Ingest", text="Load documents and convert them to text."),
        dict(label="Chunk and embed", text="Split into passages and turn each into a vector."),
        dict(label="Store", text="Save vectors in a local vector database."),
        dict(label="Retrieve", text="Find the passages most similar to the question."),
        dict(label="Answer with sources", text="The model answers from the passages and cites them.")])),
  dict(step=8, type="cycle", title="The RAG accuracy loop", caption="Click each stage. Repeat after every change to documents or settings.",
       config=dict(center="Test set", stages=[
        dict(label="Prepare", text="Clean, current, well-structured documents in focused workspaces."),
        dict(label="Configure", text="Chunk size, number of chunks, embedding model, system prompt."),
        dict(label="Test", text="Run 20 to 30 questions with known answers and sources."),
        dict(label="Review", text="Find wrong answers and why they happened."),
        dict(label="Improve", text="Fix documents or settings and add failures to the test set.")])),
  dict(step=9, type="stack", title="Securing a local AI system", caption="Click each layer, from the bottom up.",
       config=dict(top_label="Private AI you can trust", layers=[
        dict(label="Protected machine", text="Disk encryption, endpoint protection, physical security."),
        dict(label="Internal network only", text="No direct internet exposure; VPN for remote users."),
        dict(label="Individual logins", text="Strong passwords and MFA where supported."),
        dict(label="Workspace permissions", text="Each team sees only its own documents."),
        dict(label="Updates, logs and backups", text="Patch regularly, manage chat logs, back up configuration.")])),
  dict(step=16, type="timeline", title="A 90-day private AI pilot", caption="Click each phase to see its main actions.",
       config=dict(phases=[
        dict(label="Days 1–30", title="Choose and prepare", items=["Use case, owner and record", "Hardware and tools", "Clean documents", "20-question test set"]),
        dict(label="Days 31–60", title="Pilot", items=["Test models and settings", "Secure the system", "Train pilot users", "Weekly feedback"]),
        dict(label="Days 61–90", title="Measure and decide", items=["Accuracy and time saved", "Cost vs cloud", "Stop, continue or scale", "Hybrid AI policy"])])),
 ],
 exam=[
  E("What defines local AI?", ["Running an open-weight model on hardware you control", "Using any AI app on a phone", "A cloud AI subscription", "AI that only works in Canada"], 0, "Local AI keeps processing on your own systems."),
  E("Which situation most strongly favours local AI?", ["Writing a public blog post", "A client agreement requires its confidential data stays on your systems", "Brainstorming slogans", "Summarizing public news"], 1, "Contractual data location requirements point to local processing."),
  E("What is a typical trade-off of local models on modest hardware?", ["They are always more capable than cloud models", "They cannot read text", "They usually trail the largest frontier models on hard reasoning tasks", "They never make mistakes"], 2, "Smaller local models are capable but generally less so than frontier models."),
  E("Why must you check an open-weight model's licence?", ["Licences are all identical", "Licences only matter for images", "Open-weight models are always public domain", "Licences vary and some restrict commercial use"], 3, "Terms differ between models."),
  E("What does quantization do?", ["Stores parameters with fewer bits to cut memory needs", "Makes models larger", "Encrypts documents", "Translates models into other languages"], 0, "Quantization reduces memory with modest quality loss."),
  E("Roughly how much memory does a 4-bit 14B model need?", ["About 1 GB", "About 8 to 10 GB", "About 100 GB", "About 500 MB"], 1, "At about 0.5 to 0.7 GB per billion parameters, roughly 8 to 10 GB plus context."),
  E("Which tool is mainly a model engine that runs models locally with an API?", ["AnythingLLM", "Open WebUI", "Ollama", "A vector database"], 2, "Ollama runs models; front ends connect to it."),
  E("What is the most reliable way to choose a local model?", ["The largest download", "The newest release", "General leaderboard rank alone", "Testing candidates on your own realistic tasks"], 3, "Your own test set reflects your real needs."),
  E("In RAG, what does the embedding step do?", ["Converts text chunks into vectors that represent meaning", "Deletes duplicates", "Prints documents", "Trains the language model"], 0, "Embeddings enable search by meaning."),
  E("A RAG system cites an outdated procedure. What should you do first?", ["Use a bigger model", "Remove outdated versions from the document set", "Raise the temperature", "Disable citations"], 1, "Old documents produce old answers."),
  E("Which system prompt instruction reduces made-up answers in document Q&A?", ["Be creative", "Answer as long as possible", "Answer only from the provided documents, cite sources and say when the answer isn't there", "Ignore the documents"], 2, "Grounding and admitting gaps reduce hallucination."),
  E("How should remote staff reach a local AI server?", ["Directly over the internet", "With one shared password", "By email", "Through a VPN or internal network with individual logins"], 3, "Avoid internet exposure and use individual accounts."),
  E("What is prompt injection?", ["Hidden or malicious instructions in content that try to override the AI's rules", "A way to speed up models", "A type of GPU", "A licence term"], 0, "Injected instructions are a key risk when AI can act."),
  E("Does local AI remove privacy law obligations?", ["Yes", "No; privacy principles still apply to personal information processed", "Only for small firms", "Only for public data"], 1, "Privacy duties apply wherever personal data is processed."),
  E("Why manage chat logs in local AI tools?", ["They slow the GPU", "They are required to train models", "They can contain sensitive information and need retention and access rules", "They are always empty"], 2, "Logs may hold sensitive prompts and answers."),
  E("What is a common way to start with local AI?", ["Buy a large GPU cluster first", "Deploy to all staff on day one", "Replace all cloud tools", "Pilot one use case on a capable desktop with a few users"], 3, "Start small and prove value."),
  E("In a hybrid approach, where should credentials and banking details go?", ["Never into any AI tool", "Local AI only", "Business cloud AI", "Any AI tool"], 0, "Credentials never belong in AI tools."),
  E("15 users at $40 a month for 36 months. What is the cloud cost?", ["$1,440", "$21,600", "$7,200", "$14,400"], 1, "15 × 40 × 36 = $21,600."),
  E("What is the safest first local AI agent?", ["One that sends payments", "One with admin rights everywhere", "A read-only agent that searches documents", "One that deletes files"], 2, "Read-only tools carry the least risk."),
  E("Which measure best shows a document Q&A pilot's accuracy?", ["Number of files loaded", "GPU temperature", "Models downloaded", "Share of test questions answered correctly with the right source"], 3, "A test set with known answers measures accuracy."),
 ],
)

if __name__ == "__main__":
    write(course, "local-ai", __file__, balance=True)
