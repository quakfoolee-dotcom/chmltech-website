"""Source for content/courses/prompting-ai-productivity.json (run: python3 content/courses/src/prompting.py)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import step, E, write

M1 = [
step("How AI chat tools work, in practice", 6, """
<p>AI chat assistants, such as ChatGPT, Claude, Gemini and Microsoft Copilot, are built on large language models. They are trained on huge amounts of text to predict likely next words, then tuned to follow instructions and hold a conversation. The result is a tool that can draft, summarize, rewrite, explain, brainstorm and analyze at remarkable speed.</p>
<h3>What they are good at</h3>
<ul><li>First drafts of emails, reports, proposals, job descriptions and procedures.</li>
<li>Summarizing long documents, meeting notes and email threads.</li>
<li>Rewriting for a different audience, tone or length.</li>
<li>Extracting information into tables or lists.</li>
<li>Brainstorming options and checking your thinking.</li>
<li>Explaining unfamiliar topics, formulas or code.</li></ul>
<h3>Where they fall short</h3>
<ul><li><strong>Confident errors:</strong> they can state wrong facts, figures or references fluently, often called hallucinations.</li>
<li><strong>No knowledge of your business</strong> unless you provide it.</li>
<li><strong>Limited or dated knowledge</strong> of recent events, unless the tool can search the web.</li>
<li><strong>Arithmetic and precise counting</strong> can be unreliable unless the tool runs calculations or code.</li>
<li><strong>Varied output:</strong> the same prompt can give different answers each time.</li></ul>
<h3>The right mindset</h3>
<p>Treat an AI assistant like a fast, capable new colleague who knows a lot in general but nothing about your company, and who sometimes makes things up. Give clear instructions and context, review the work, and stay responsible for what you send. Used this way, it saves real time on routine work. This course assumes your organization has approved AI tools; check your policy before using any tool with business information.</p>
""", ["AI assistants draft, summarize, rewrite and analyze quickly.", "They can be confidently wrong and know nothing about your business unless told.", "Treat them as a capable new colleague: instruct clearly, review, stay responsible."],
 "List five tasks you did last week that involved writing, summarizing or reformatting. Mark which an AI assistant could have drafted for you.",
 "Why must you review AI output before using it?", ["AI tools never make mistakes", "They can state wrong facts confidently", "Reviewing is only needed for long documents", "AI output is always copyrighted"], 1,
 "AI tools can produce fluent but incorrect content, so a human must check it."),
step("The anatomy of a good prompt", 8, """
<p>The quality of the answer depends mostly on the quality of the request. Vague prompts get generic answers. A good prompt gives the assistant what a human colleague would need.</p>
<table><thead><tr><th>Element</th><th>What to include</th><th>Example</th></tr></thead><tbody>
<tr><td>Role</td><td>Who the assistant should act as</td><td>"You are an experienced customer service manager."</td></tr>
<tr><td>Context</td><td>Background, audience, purpose, constraints</td><td>"We are a 40-person industrial parts distributor. A long-time customer received the wrong parts twice this month."</td></tr>
<tr><td>Task</td><td>Exactly what you want done</td><td>"Draft a reply that apologizes, explains what we are changing and offers a credit."</td></tr>
<tr><td>Format</td><td>Length, structure, style</td><td>"Under 150 words, three short paragraphs, professional but warm."</td></tr>
<tr><td>Examples</td><td>A sample of the style or output you want</td><td>"Here is a reply we sent last year that the customer liked: ..."</td></tr>
<tr><td>Constraints</td><td>What to avoid or must include</td><td>"Don't promise delivery dates. Mention our new double-check at packing."</td></tr>
</tbody></table>
<h3>Before and after</h3>
<p><strong>Weak:</strong> "Write an email to a customer about the wrong parts."</p>
<p><strong>Strong:</strong> "You are a customer service manager at a 40-person industrial parts distributor. A long-time customer, a food processor, received the wrong parts twice this month, which delayed their maintenance. Draft a reply that apologizes sincerely, explains we've added a barcode check at packing, and offers a 10% credit on the two orders. Keep it under 150 words, professional and warm. Don't promise specific delivery dates."</p>
<p>The strong prompt takes 30 seconds longer to write and usually saves several rounds of editing. You don't need every element every time; context, task and format matter most. The lab after this lesson asks you to judge prompts.</p>
""", ["Give role, context, task, format, examples and constraints.", "Context, task and format matter most.", "A slightly longer prompt saves rounds of editing."],
 "Take a task from your list and write a prompt using at least role, context, task and format. Compare the result with a one-line prompt for the same task.",
 "Which prompt element most often turns a generic answer into a useful one?", ["Using polite words", "Specific context about the audience, purpose and situation", "Writing in capital letters", "Adding emojis"], 1,
 "Context lets the assistant tailor the answer to your real situation."),
step("Iterate: treat it as a conversation", 7, """
<p>The first answer is a draft, not the final product. The biggest productivity gains come from refining the output through a short conversation.</p>
<h3>Useful follow-up moves</h3>
<table><thead><tr><th>Move</th><th>Example follow-up</th></tr></thead><tbody>
<tr><td>Adjust</td><td>"Make it shorter and more direct." "Use simpler language for a non-technical reader."</td></tr>
<tr><td>Add detail</td><td>"Add a sentence about our warranty." "Include a table comparing the three options."</td></tr>
<tr><td>Change perspective</td><td>"Rewrite it from the customer's point of view."</td></tr>
<tr><td>Critique</td><td>"What's weak or unclear in this draft? How would a skeptical CFO react?"</td></tr>
<tr><td>Ask me first</td><td>"Before you write, ask me any questions you need answered."</td></tr>
<tr><td>Alternatives</td><td>"Give me three different subject lines."</td></tr>
</tbody></table>
<h3>Let it ask questions</h3>
<p>For bigger tasks, such as a proposal or a procedure, ask the assistant to list the information it needs before drafting. It will often raise points you had not thought of, and the draft will need fewer corrections.</p>
<h3>Start fresh when needed</h3>
<p>Long conversations can drift. If the assistant keeps repeating a mistake or mixing up details, start a new chat with a clean, complete prompt that includes what you have learned.</p>
<h3>You stay the editor</h3>
<p>Iterating is not about getting the AI to write perfectly; it is about getting a strong draft quickly that you then finish. Many people find the best workflow is AI for the first 80% and their own judgment for the last 20%.</p>
""", ["Treat the first answer as a draft and refine it.", "Ask for critique, alternatives and questions before drafting.", "Start a new chat if a long conversation drifts."],
 "Take one AI draft and improve it with three follow-ups: one adjustment, one critique and one request for alternatives. Note how much better the final version is.",
 "A long chat keeps repeating the same mistake. What is the best move?", ["Keep correcting it in the same chat indefinitely", "Start a new chat with a clean, complete prompt", "Give up on AI", "Type in all capitals"], 1,
 "A fresh chat with a complete prompt avoids accumulated confusion."),
step("Examples and templates", 7, """
<p>Showing is often better than telling. When you want a specific style, structure or format, give the assistant one or more examples. This is sometimes called few-shot prompting.</p>
<h3>When examples help most</h3>
<ul><li>Matching your company's tone of voice in emails or social posts.</li>
<li>Producing a consistent structure, such as a standard quote cover letter or incident report.</li>
<li>Classifying or extracting information in a particular way.</li></ul>
<h3>Example: consistent product descriptions</h3>
<p>"Write product descriptions in the same style as these two examples. Example 1: [text]. Example 2: [text]. Now write one for: stainless steel sanitary ball valve, 2-inch, tri-clamp ends, rated to 150 psi."</p>
<h3>Build reusable templates</h3>
<p>For tasks you do often, save a prompt template with placeholders:</p>
<p><em>"You are our sales coordinator. Write a quote cover email to [customer name] at [company] for [product/service]. Key points: [points]. Our lead time is [lead time]. Keep it under 120 words, friendly and professional, and end with a clear next step."</em></p>
<p>Fill in the brackets each time. Templates make results consistent across the team and save everyone from reinventing prompts. Later lessons show how to share them as a team prompt library.</p>
<h3>Tables and structured output</h3>
<p>Ask for output in a format you can use directly: "Return a table with columns Supplier, Item, Price, Lead time" or "Give me a numbered checklist". Structured output is easier to check and to paste into spreadsheets or documents.</p>
""", ["Give examples when you need a specific style or structure.", "Save reusable prompt templates with placeholders.", "Ask for structured output such as tables and checklists."],
 "Create one prompt template for a task you do every week, with placeholders. Test it three times and refine it.",
 "What is the main benefit of a shared prompt template?", ["It makes the AI faster", "Consistent results across the team without reinventing prompts", "It removes the need to review output", "It lets you share confidential data safely"], 1,
 "Templates give consistent, repeatable results and save time."),
]

M2 = [
step("Writing and editing", 7, """
<p>Writing is the most common and often the most valuable use of AI assistants at work.</p>
<h3>Common writing tasks</h3>
<ul><li><strong>Emails:</strong> replies to customers and suppliers, follow-ups, difficult messages, announcements.</li>
<li><strong>Documents:</strong> reports, proposals, procedures, policies, job descriptions, meeting agendas.</li>
<li><strong>Marketing:</strong> website text, social posts, newsletters, case studies.</li>
<li><strong>Editing:</strong> shortening, simplifying, fixing grammar, changing tone, translating.</li></ul>
<h3>Practical tips</h3>
<ul><li><strong>Start from your notes:</strong> paste your rough bullet points and ask for a polished draft. The content stays yours; the AI handles the wording.</li>
<li><strong>Specify the reader:</strong> "for a plant manager with little time" produces a very different email from "for our technical support team".</li>
<li><strong>Ask for plain language</strong> and short sentences when writing for customers or staff.</li>
<li><strong>Difficult messages:</strong> ask for two or three versions with different tones, then pick and blend.</li>
<li><strong>Translation:</strong> useful for drafts and understanding, but have important customer-facing or legal text checked by a fluent speaker.</li></ul>
<h3>Keep your voice</h3>
<p>AI drafts can sound generic or overly formal. Give an example of your own writing and ask it to match your style, and edit the result so it sounds like you. Remove phrases you would never use. Customers notice when every email sounds the same.</p>
<h3>Accuracy</h3>
<p>Check every name, date, price, promise and technical detail before sending. The assistant may fill gaps with plausible but wrong details.</p>
""", ["Paste rough notes and let AI polish the wording.", "Specify the reader and ask for plain language.", "Edit drafts to keep your voice and check every fact and promise."],
 "Write rough bullet points for an email you need to send this week, then ask an AI assistant to turn them into a polished draft for a named type of reader.",
 "What should you check most carefully before sending an AI-drafted customer email?", ["The font", "Names, dates, prices, promises and technical details", "The number of paragraphs", "Whether it uses the word 'please'"], 1,
 "AI may insert plausible but wrong specifics, which can create commitments or errors."),
step("Summarizing and extracting information", 7, """
<p>AI assistants are very good at condensing long material and pulling out specific information, provided you tell them what you need.</p>
<h3>Summaries that are useful</h3>
<ul><li>Say who the summary is for and what decision it supports: "Summarize this supplier proposal for our owner, who needs to decide whether to proceed. Focus on cost, schedule and risks."</li>
<li>Ask for a structure: key points, decisions made, actions with owners, open questions.</li>
<li>Set a length: "five bullet points" or "under 200 words".</li></ul>
<h3>Meeting notes</h3>
<p>Paste a transcript or rough notes and ask: "List decisions, action items with owners and due dates, and unresolved issues." Many meeting and video-call tools now produce these summaries automatically. Always check that action items and owners are correct before circulating.</p>
<h3>Extracting into tables</h3>
<p>"From these five supplier quotes, extract supplier, item, unit price, minimum order, lead time and payment terms into a table." Extraction saves hours of re-typing, but verify a sample against the source documents, especially numbers.</p>
<h3>Long documents</h3>
<p>For contracts, standards or reports, ask targeted questions rather than for a general summary: "What are the termination clauses?" "What warranty does the supplier offer?" Ask the assistant to quote the section it relied on so you can check it. For legal or safety-critical documents, the summary is a starting point, not a substitute for reading the relevant sections or getting professional advice.</p>
""", ["Say who the summary is for, what it supports and the structure you want.", "Use AI to extract information into tables, then verify a sample.", "Ask targeted questions of long documents and have it point to the source section."],
 "Take a recent long email thread or document and ask an AI assistant for decisions, actions with owners and open questions. Check each item against the original.",
 "What is the best way to use AI on a long contract?", ["Ask for a one-line summary and sign", "Ask targeted questions and have it point to the relevant clauses, then check them", "Never use AI for documents", "Trust the summary completely"], 1,
 "Targeted questions with source references let you verify; important documents still need reading or advice."),
step("Spreadsheets, numbers and analysis", 7, """
<p>AI assistants can help with spreadsheets and analysis, but numbers need extra care.</p>
<h3>Where AI helps</h3>
<ul><li><strong>Formulas:</strong> "Write an Excel formula that looks up the price in sheet Prices by part number in column A and returns 0 if not found."</li>
<li><strong>Explaining:</strong> "Explain what this formula does step by step."</li>
<li><strong>Cleaning data:</strong> "How do I split full names into first and last name columns?" or "Standardize these addresses."</li>
<li><strong>Analysis ideas:</strong> "What charts would best show monthly sales by region and product?"</li>
<li><strong>Uploaded files:</strong> some tools can analyze an uploaded spreadsheet by running code, producing totals, charts and summaries.</li></ul>
<h3>Checking numbers</h3>
<ul><li>Language models are not calculators. When a tool does arithmetic in plain text, check it.</li>
<li>Tools that run code to analyze data are more reliable, but check that they used the right columns, filters and date ranges.</li>
<li>Spot-check results against a few rows you calculate yourself.</li>
<li>Ask the assistant to show its working or the formula it used.</li></ul>
<h3>Example workflow</h3>
<p>A sales manager uploads 12 months of order data and asks: "Show total sales by month and customer type, and flag customers whose orders fell more than 30% compared with the previous six months." The tool produces a table and chart in a minute. The manager checks totals against the accounting report and reviews the flagged customers before calling them.</p>
<p>Before uploading data, check your organization's rules: customer and financial data may need to stay within approved tools.</p>
""", ["AI is great for formulas, explanations, cleaning and analysis ideas.", "Check any arithmetic; prefer tools that run code, and verify their filters and columns.", "Spot-check results and follow data rules before uploading files."],
 "Ask an AI assistant to write one spreadsheet formula you need, then test it on rows where you already know the answer.",
 "An AI assistant gives a total in plain text without running a calculation. What should you do?", ["Trust it; AI is always accurate with numbers", "Check the arithmetic yourself or in the spreadsheet", "Round it up", "Ask it to repeat the same number"], 1,
 "Language models can make arithmetic errors; totals need checking."),
step("Brainstorming, planning and thinking partner", 7, """
<p>Beyond writing, AI assistants are useful partners for thinking: generating options, structuring plans and challenging your assumptions.</p>
<h3>Brainstorming</h3>
<ul><li>"Give me 15 ideas to reduce order-entry errors at a small distributor. Group them by effort."</li>
<li>"Suggest names and taglines for our new maintenance service plan."</li>
<li>"What questions should I ask in an interview for a production supervisor?"</li></ul>
<p>Quantity first, judgment second: ask for many ideas, then pick and refine the best ones yourself.</p>
<h3>Planning</h3>
<ul><li>"Create a project plan for moving our warehouse to a new building in three months, with phases, key tasks and risks."</li>
<li>"Turn these notes into a training plan for new customer service staff over their first two weeks."</li></ul>
<h3>Decision support</h3>
<ul><li>"Compare leasing versus buying a forklift for a small warehouse. List the factors and questions I should answer."</li>
<li>"Here is my plan. What are the three biggest risks, and what am I missing?"</li>
<li>"Argue the opposite of my position as strongly as you can."</li></ul>
<p>Asking the assistant to critique your plan or argue against it is one of the most valuable uses: it surfaces blind spots before you commit.</p>
<h3>Keep decisions human</h3>
<p>Use AI to widen your options and test your thinking, not to make decisions for you. It does not know your customers, team, finances or constraints unless you tell it, and even then it cannot weigh them as you can. The lab after this lesson helps you choose which tasks to try first.</p>
""", ["Use AI to generate many options, then judge them yourself.", "Ask it to structure plans and critique your thinking.", "Keep decisions with people who know the full context."],
 "Take a decision you face this month. Ask an AI assistant for the key factors, the biggest risks and the strongest argument against your preferred option.",
 "What is a particularly valuable way to use AI on a plan you have already drafted?", ["Ask it to approve the plan", "Ask it to identify risks and argue the opposite case", "Ask it to make the final decision", "Ask it to add more pages"], 1,
 "Critique and counterarguments reveal blind spots before you commit."),
]

M3 = [
step("Checking AI output", 7, """
<p>Every AI output needs review before you use it. A simple, consistent check catches most problems.</p>
<h3>A four-step check</h3>
<ol><li><strong>Read it fully.</strong> Don't skim. Does it answer what you asked?</li>
<li><strong>Verify facts and figures.</strong> Names, dates, prices, quantities, technical specifications, regulations and references. Check them against reliable sources or your own records.</li>
<li><strong>Fix it.</strong> Correct errors, remove anything you can't verify, adjust the tone and add what's missing.</li>
<li><strong>Own it.</strong> Once you send it, it is your work and your responsibility.</li></ol>
<h3>Typical errors to watch for</h3>
<table><thead><tr><th>Error</th><th>Example</th></tr></thead><tbody>
<tr><td>Invented facts or references</td><td>A regulation number, a study or a quote that does not exist</td></tr>
<tr><td>Outdated information</td><td>Old prices, tax rates or rules</td></tr>
<tr><td>Wrong details filled in</td><td>An assumed delivery date, price or product feature</td></tr>
<tr><td>Calculation mistakes</td><td>Totals or percentages that do not add up</td></tr>
<tr><td>Overconfidence</td><td>Firm statements on uncertain or contested topics</td></tr>
</tbody></table>
<h3>Higher stakes, more checking</h3>
<p>A brainstorm list needs little checking. A customer quote, a safety procedure, a contract clause or anything about health, legal or financial matters needs careful verification, and often an expert's review. Match the depth of the check to the consequences of an error.</p>
<h3>Ask for sources</h3>
<p>Tools with web search can provide links. Open them: the source may not say what the summary claims. Without search, ask the assistant to flag anything it is unsure of, and treat unverified claims as unverified.</p>
""", ["Read, verify, fix and own every output.", "Watch for invented facts, outdated information, filled-in details and calculation errors.", "Match the depth of checking to the stakes."],
 "Use the four-step check on every AI output for the next two weeks. Keep a short note of each error you catch.",
 "An AI draft cites a specific regulation number. What should you do?", ["Use it as is", "Verify it against an official source before relying on it", "Remove all regulations from documents", "Ask the AI if it is sure and accept its answer"], 1,
 "AI can invent references; official sources must confirm them."),
step("Protecting data and using approved tools", 7, """
<p>What you type into an AI tool may be stored, reviewed or used to improve the service, depending on the tool and your settings. Protecting business and personal information is essential.</p>
<h3>Approved tools</h3>
<p>Business and enterprise versions of AI tools usually offer stronger data protections, such as not using your data to train models, admin controls and data retention settings. Your organization should decide which tools are approved for which kinds of information. Use those, signed in with your work account.</p>
<h3>A simple data rule</h3>
<table><thead><tr><th>Information</th><th>Public or consumer AI tools</th><th>Approved business AI tools</th></tr></thead><tbody>
<tr><td>Public information, general questions</td><td>Generally fine</td><td>Fine</td></tr>
<tr><td>Internal, non-sensitive work (draft emails, procedures)</td><td>Avoid</td><td>Fine within policy</td></tr>
<tr><td>Customer and employee personal information</td><td>Never</td><td>Only if policy allows and necessary</td></tr>
<tr><td>Confidential financials, pricing, contracts, trade secrets</td><td>Never</td><td>Only if policy allows</td></tr>
<tr><td>Passwords, access keys, banking details</td><td>Never</td><td>Never</td></tr>
</tbody></table>
<h3>Practical habits</h3>
<ul><li>Remove or replace names and identifying details when they aren't needed: "Customer A" instead of the real name.</li>
<li>Don't paste whole databases or customer lists.</li>
<li>Check retention and sharing settings, and be careful with shared chats and links.</li>
<li>Ask when unsure.</li></ul>
<p>Canadian privacy law, including PIPEDA, applies to personal information wherever it is processed, including in AI tools. When in doubt, leave it out. The Private and Local AI course covers options for keeping sensitive data in-house.</p>
""", ["Use approved business AI tools with your work account.", "Never put passwords, banking details or confidential data into consumer tools.", "Anonymize when possible, and when in doubt leave it out."],
 "Find out which AI tools your organization approves and for what data. If there is no policy, draft a one-page proposal using the table above.",
 "Which should never be pasted into any AI tool?", ["A public news article", "Passwords and banking details", "A general question about grammar", "A draft agenda with no confidential content"], 1,
 "Credentials and banking details must never be shared with AI tools."),
step("Bias, fairness, disclosure and copyright", 7, """
<p>Responsible use goes beyond accuracy and data protection.</p>
<h3>Bias and fairness</h3>
<p>AI models learn from human-written text and can reflect its biases. This matters most in decisions about people. Be especially careful when using AI for:</p>
<ul><li>Screening résumés or writing job advertisements.</li>
<li>Performance reviews or disciplinary matters.</li>
<li>Credit, pricing or service decisions about customers.</li></ul>
<p>Check outputs for stereotypes and unfair assumptions, keep a human responsible for decisions about people, and follow employment and human rights law.</p>
<h3>Disclosure</h3>
<p>Your organization should decide when AI use should be disclosed. Many companies don't require it for routine drafting that a person reviews, but do for content presented as personal or expert work, research or anything where the reader would reasonably expect to know. Never present AI-generated content as something it is not, such as a personal testimonial.</p>
<h3>Copyright and ownership</h3>
<ul><li>Don't ask AI to reproduce copyrighted material such as articles, books or song lyrics.</li>
<li>Be cautious with AI-generated images and text for logos or key brand assets; ownership and originality questions are still developing.</li>
<li>Check tool terms on how outputs may be used commercially.</li>
<li>Respect confidentiality agreements: material shared with you under an NDA should not go into AI tools unless permitted.</li></ul>
<h3>Accountability</h3>
<p>Whatever the tool produced, the person and organization using it remain accountable. "The AI wrote it" is not a defence for a wrong quote, a biased decision or a privacy breach.</p>
""", ["Watch for bias, especially in decisions about people.", "Follow your organization's disclosure rules and never misrepresent AI content.", "Respect copyright and confidentiality; you remain accountable."],
 "Review one people-related task where your team uses or might use AI, such as job ads or résumé screening. Write down how a human stays responsible for the decision.",
 "A manager wants AI to rank job applicants automatically. What is the key safeguard?", ["Let the AI decide alone to save time", "Keep a human responsible for decisions and check for bias", "Hide the use of AI from candidates", "Only use AI for senior roles"], 1,
 "Decisions about people need human responsibility and bias checks."),
step("A team prompt library and AI guidelines", 7, """
<p>Individual experiments become team productivity when good prompts and practices are shared.</p>
<h3>Build a prompt library</h3>
<p>Create a shared document or page with tested prompt templates for common tasks. For each, include:</p>
<ul><li>The task and when to use it.</li>
<li>The prompt template with placeholders.</li>
<li>An example of good output.</li>
<li>Checks to do before using the output.</li>
<li>The owner who maintains it.</li></ul>
<p>Start with five to ten high-value prompts, such as customer reply drafts, meeting summaries, quote cover emails, job descriptions and procedure drafts. Add more as people find what works.</p>
<h3>Simple team guidelines</h3>
<ul><li>Which tools are approved, and for what information.</li>
<li>The four-step check before using any output.</li>
<li>Never share passwords, banking details or confidential data in unapproved tools.</li>
<li>Humans stay responsible for decisions about people and for anything sent externally.</li>
<li>Whom to ask with questions or to report a problem.</li></ul>
<h3>Learn together</h3>
<p>Hold a short monthly session where team members share a prompt that saved time or a mistake they caught. Appoint one or two enthusiastic "AI champions" to help colleagues and keep the library current. Celebrate time saved, and be honest about tasks where AI did not help.</p>
""", ["Share tested prompt templates in a team library with examples and checks.", "Write one page of simple AI guidelines.", "Learn together through short sessions and AI champions."],
 "Start a team prompt library with three tested templates. Ask two colleagues to add one each within a month.",
 "What should each entry in a team prompt library include?", ["Only the AI tool's name", "The task, template, example output, checks and an owner", "Customer passwords", "A list of banned words only"], 1,
 "A complete entry makes prompts reusable and safe."),
]

M4 = [
step("Custom assistants and reusable instructions", 7, """
<p>Most AI tools let you save standing instructions so you don't repeat the same context every time.</p>
<h3>Options</h3>
<ul><li><strong>Custom instructions or memory:</strong> tell the tool about your role, company and preferred style once.</li>
<li><strong>Projects or workspaces:</strong> group chats with shared files and instructions, for example all work on one proposal or client.</li>
<li><strong>Custom assistants:</strong> many tools let you create an assistant for a specific job, with instructions and reference files, such as a "Quote Writer" that knows your products, terms and tone.</li></ul>
<h3>Designing a custom assistant</h3>
<ol><li>Pick one repeated task with clear inputs and outputs.</li>
<li>Write instructions: role, purpose, steps, tone, what to avoid, when to ask questions.</li>
<li>Add reference material: product sheets, price rules, examples of good output, style guide. Only include information approved for that tool.</li>
<li>Test with real cases and refine the instructions.</li>
<li>Share it with the team and name an owner to keep its files current.</li></ol>
<h3>Example</h3>
<p>A distributor creates a "Customer Reply Assistant" with its returns policy, shipping terms, tone guide and five example replies. Staff paste a customer's email and get a draft reply that follows policy, which they review and send. Replies become faster and more consistent, and new staff learn the policies by seeing them applied.</p>
<h3>Keep it current</h3>
<p>A custom assistant with outdated price lists or policies gives confidently wrong answers. Review its reference files whenever policies change.</p>
""", ["Save context with custom instructions, projects or custom assistants.", "Design an assistant for one task with instructions, references and examples.", "Name an owner to keep reference files current."],
 "Choose one repeated task and write the instructions for a custom assistant: role, steps, tone and what to avoid. Test it on three real cases.",
 "What is the main risk of a custom assistant with outdated reference files?", ["It runs slower", "It gives confidently wrong answers based on old policies or prices", "It stops working completely", "It uses more electricity"], 1,
 "Stale reference material produces confident but wrong outputs."),
step("AI inside your everyday tools", 7, """
<p>AI is increasingly built into software you already use: office suites, email, meeting tools, CRM, accounting and customer service platforms. These built-in features can save time without switching tools.</p>
<h3>Common built-in features</h3>
<table><thead><tr><th>Tool</th><th>Typical AI features</th></tr></thead><tbody>
<tr><td>Email and calendar</td><td>Draft replies, summarize threads, suggest meeting times</td></tr>
<tr><td>Documents and slides</td><td>Draft from notes, rewrite, summarize, create slides from a document</td></tr>
<tr><td>Spreadsheets</td><td>Explain data, suggest formulas and charts</td></tr>
<tr><td>Meetings</td><td>Transcribe, summarize, list action items</td></tr>
<tr><td>CRM and help desk</td><td>Draft customer responses, summarize account history, suggest next steps</td></tr>
</tbody></table>
<h3>Simple automations</h3>
<p>Some tasks can be automated end to end with AI as one step, for example: incoming supplier invoices are read, key fields are extracted and a draft entry is created in accounting for a person to approve. Workflow tools connect apps and add AI steps without coding. Start with tasks that are frequent, rule-based and easy to check, and keep a human approval step for anything with financial or customer impact. The Workflow Automation course covers this in more depth.</p>
<h3>Before turning features on</h3>
<ul><li>Check the cost: some AI features are paid add-ons per user.</li>
<li>Check data settings and where data is processed.</li>
<li>Pilot with a small group and measure the time saved before rolling out to everyone.</li></ul>
""", ["Many everyday tools now include AI features for drafting, summarizing and analysis.", "Automate frequent, rule-based tasks with a human approval step.", "Check cost and data settings and pilot before rolling out."],
 "List the AI features available in the tools you already pay for. Pick one to pilot with two colleagues for a month.",
 "Which task is a good first candidate for an automation with an AI step?", ["A one-off strategic decision", "A frequent, rule-based task that is easy to check, with human approval", "Firing an employee", "Signing contracts automatically"], 1,
 "Frequent, checkable tasks with human approval are lower risk and higher value."),
step("Measuring time saved", 7, """
<p>To decide where to invest in AI tools and training, measure the benefit honestly.</p>
<h3>A simple method</h3>
<ol><li>Pick a task, such as drafting customer replies or writing weekly reports.</li>
<li>Estimate how long it takes now, per instance and per week, across the people who do it.</li>
<li>Try AI on the task for two to four weeks, including the time spent reviewing and fixing output.</li>
<li>Estimate the new time per instance.</li>
<li>Note quality effects: fewer errors, faster responses, more consistency, or the reverse.</li></ol>
<h3>Value the time realistically</h3>
<p>Time saved has value only if it is used: more customers served, faster quotes, less overtime, a hire avoided or time redirected to higher-value work. Don't count saved minutes as cash savings unless costs actually fall.</p>
<h3>Example</h3>
<p>A customer service team of four spends about 20 hours a week in total writing replies. With an assistant and templates, drafting time falls by about 40% after including review time, freeing roughly 8 hours a week, or over 400 hours a year. The team uses the time to call back customers with open issues, and response times improve. Tool licences cost a few hundred dollars a month.</p>
<h3>Watch for hidden costs</h3>
<ul><li>Time spent checking and correcting output.</li>
<li>Errors that reach customers.</li>
<li>Training and change effort.</li>
<li>Licence costs for users who rarely use the tool.</li></ul>
<p>The lab after this lesson calculates hours freed, savings and payback for one task.</p>
""", ["Measure before and after, including review and correction time.", "Value time only if it is redirected or costs fall.", "Count hidden costs: checking, errors, training and unused licences."],
 "Pick one task, time it for a week without AI and a week with AI, including review. Calculate the difference and decide what you will do with the time.",
 "When can saved time from AI be counted as a cash saving?", ["Always, for every minute saved", "Only when costs actually fall, such as less overtime or a hire avoided", "Never", "Only if the AI tool is free"], 1,
 "Time freed is valuable when used; it becomes cash only when costs drop."),
step("Your 30-day AI productivity plan", 7, """
<p>Turn what you have learned into habits with a 30-day plan.</p>
<table><thead><tr><th>Week</th><th>Focus</th><th>Actions</th></tr></thead><tbody>
<tr><td>1</td><td>Set up</td><td>Confirm approved tools and data rules; set custom instructions; list ten tasks that could use AI</td></tr>
<tr><td>2</td><td>Practise</td><td>Use the prompt anatomy daily on two or three tasks; iterate with follow-ups; apply the four-step check</td></tr>
<tr><td>3</td><td>Templates</td><td>Turn the three most useful prompts into templates; try one custom assistant or project</td></tr>
<tr><td>4</td><td>Share and measure</td><td>Add templates to a team library; measure time saved on one task; share results and lessons</td></tr>
</tbody></table>
<h3>Daily habits</h3>
<ul><li>Start routine writing with AI from your notes, then edit.</li>
<li>Ask for critique on important drafts and plans.</li>
<li>Check facts, figures and promises every time.</li>
<li>Keep sensitive data out of unapproved tools.</li></ul>
<h3>Where to go next</h3>
<p>The Large Language Models for Business Leaders course explains how these tools work in more depth and how to choose and govern them; AI Agents for Business Operations shows how AI can carry out multi-step tasks; and Private and Local AI for SMEs covers keeping sensitive work in-house.</p>
""", ["Week 1 set up, week 2 practise, week 3 templates, week 4 share and measure.", "Build daily habits: draft from notes, ask for critique, check facts, protect data.", "Continue with the LLM, AI Agents or Private and Local AI courses."],
 "Put the four weekly focuses in your calendar and choose the ten tasks for week 1 now.",
 "What is the focus of week 4 in the 30-day plan?", ["Buying new hardware", "Sharing templates with the team and measuring time saved", "Stopping AI use", "Writing a company AI strategy alone"], 1,
 "Week 4 spreads what works and measures the benefit."),
]

course = dict(
 id="prompting-and-ai-productivity",
 title="Prompting and AI Productivity for Office Work",
 tagline="Write prompts that get useful results, save hours on everyday writing and analysis, and use AI safely and responsibly at work.",
 summary="A hands-on course for office, sales, operations and management staff who want to get real value from AI assistants such as ChatGPT, Claude, Gemini and Microsoft Copilot. You will learn how these tools behave, how to write strong prompts, iterate, use examples and templates, and apply AI to writing, summarizing, spreadsheets and planning. You will also learn to check outputs, protect data, handle bias and copyright, build a team prompt library, use custom assistants and built-in AI features, and measure time saved.",
 audience=["Office, administrative, sales and customer service staff",
           "Supervisors and managers who write reports, emails and plans",
           "Owners who want their team to use AI productively and safely",
           "Anyone who has tried AI tools but finds the results generic"],
 outcomes=["Write prompts with role, context, task, format, examples and constraints",
           "Refine outputs through iteration, critique and templates",
           "Apply AI to writing, summarizing, extraction, spreadsheets and planning",
           "Check outputs reliably and protect business and personal data",
           "Build a team prompt library and custom assistants",
           "Measure time saved and run a 30-day productivity plan"],
 modules=[
  dict(title="Prompting Fundamentals", summary="How AI assistants behave, the anatomy of a good prompt, iterating as a conversation, and examples and templates.", steps=M1),
  dict(title="Everyday Tasks", summary="Writing and editing, summarizing and extracting, spreadsheets and analysis, and brainstorming and planning.", steps=M2),
  dict(title="Quality and Responsibility", summary="Checking output, protecting data, bias, disclosure and copyright, and a team prompt library with guidelines.", steps=M3),
  dict(title="Productivity at Scale", summary="Custom assistants, AI inside everyday tools, measuring time saved and a 30-day plan.", steps=M4)],
 labs=[
  dict(id="prompt-judge", type="classify", title="Too vague, missing context, or strong?", after_step=2,
       intro="Judge twelve prompts: is each too vague to get a useful answer, does it have a task but miss key context, or is it a strong prompt? Then check your answers.",
       config=dict(categories=["Too vague", "Missing key context", "Strong prompt"], items=[
        dict(text="Write an email.", answer=0, why="No audience, purpose or content: the answer will be generic."),
        dict(text="Make this better.", answer=0, why="'Better' how? Shorter, clearer, more formal? Say what you want."),
        dict(text="Tell me about marketing.", answer=0, why="Too broad to produce anything useful for your situation."),
        dict(text="Give me ideas.", answer=0, why="Ideas for what, for whom, and how many?"),
        dict(text="Write a job ad for a warehouse worker.", answer=1, why="The task is clear, but location, shifts, pay range, duties and company details are missing."),
        dict(text="Summarize this report.", answer=1, why="Who is it for, what decision does it support and how long should it be?"),
        dict(text="Draft a reply to this customer complaint.", answer=1, why="Missing what you are willing to offer, the tone and what to avoid promising."),
        dict(text="Create a training plan for new staff.", answer=1, why="Which role, how long, what they must learn and who delivers it?"),
        dict(text="You are a sales coordinator at a 30-person HVAC distributor. Write a 120-word quote cover email to a property manager for rooftop unit replacement, friendly and professional, ending with an offer to book a site visit.", answer=2, why="Role, context, task, length, tone and next step are all clear."),
        dict(text="Summarize this 20-page supplier proposal for our owner, who must decide by Friday. Use five bullets on cost, schedule, risks, warranty and open questions.", answer=2, why="Audience, purpose, structure and length are specified."),
        dict(text="Here are two product descriptions we like [examples]. Write one in the same style for a 2-inch stainless sanitary ball valve with tri-clamp ends rated to 150 psi.", answer=2, why="Examples set the style and the product details are given."),
        dict(text="Before drafting our safety procedure for forklift charging, ask me the questions you need answered about our site, equipment and staff.", answer=2, why="Inviting questions first gathers the missing context for a complex task."),
       ])),
  dict(id="prompt-task-matrix", type="matrix", title="Which tasks should you try AI on first?", after_step=8,
       intro="Place seven common office tasks on a grid of time spent against how well AI fits, to find the best first candidates.",
       config=dict(x="How well AI fits the task", y="Time spent per week", x_low="Poor fit", x_high="Good fit", y_low="Little time", y_high="Lots of time",
        quadrants=dict(top_left="Improve the process instead", top_right="Start here", bottom_left="Leave as is", bottom_right="Quick wins when convenient"),
        items=[dict(name="Drafting routine customer replies", x=5, y=5),
               dict(name="Weekly status report from notes", x=4, y=3),
               dict(name="Meeting minutes and action lists", x=5, y=4),
               dict(name="Negotiating with a key supplier", x=1, y=3),
               dict(name="Re-keying data between two systems", x=2, y=5),
               dict(name="Writing job descriptions", x=4, y=1),
               dict(name="Approving staff overtime", x=1, y=1)])),
  dict(id="prompt-time-savings", type="calc", title="What AI saves on one task", after_step=15,
       intro="Enter the weekly hours a task takes, the share AI saves after review time, your loaded hourly cost and tool costs to estimate hours freed, savings and payback.",
       config=dict(calc="automation_roi", note="Include review and correction time when estimating the share saved. Savings are real only when the freed time is used or costs fall.")),
 ],
 figures=[
  dict(step=2, type="stack", title="Anatomy of a strong prompt", caption="Click each layer, from the bottom up. Context, task and format matter most.",
       config=dict(top_label="A useful first draft", layers=[
        dict(label="Role", text="Who the assistant should act as."),
        dict(label="Context", text="Background, audience, purpose and situation."),
        dict(label="Task", text="Exactly what you want done."),
        dict(label="Format", text="Length, structure, tone."),
        dict(label="Examples and constraints", text="Samples of the style you want; what to include or avoid.")])),
  dict(step=3, type="cycle", title="The iteration loop", caption="Click each stage. The first answer is a draft; a few rounds produce a strong result.",
       config=dict(center="Draft", stages=[
        dict(label="Prompt", text="Give role, context, task and format."),
        dict(label="Review", text="Read the draft against what you need."),
        dict(label="Refine", text="Adjust length, tone, detail or perspective."),
        dict(label="Critique", text="Ask what is weak, unclear or missing."),
        dict(label="Finish", text="Edit the last 20% yourself and own the result.")])),
  dict(step=4, type="compare", title="Vague prompt vs strong prompt", caption="Toggle between the two and compare what the assistant has to work with.",
       config=dict(left=dict(title="Vague prompt", points=["'Write an email to a customer about the wrong parts.'", "No audience or relationship", "No remedy or tone specified", "Generic result that needs heavy editing"]),
                   right=dict(title="Strong prompt", points=["Role: customer service manager", "Context: long-time customer, two wrong shipments", "Task: apologize, explain fix, offer 10% credit", "Format: under 150 words, warm; no delivery promises"]))),
  dict(step=9, type="flow", title="The four-step check", caption="Click each step. Use it on every AI output; go deeper as the stakes rise.",
       config=dict(steps=[
        dict(label="Read", text="Read it fully: does it answer what you asked?"),
        dict(label="Verify", text="Check names, dates, prices, figures, references and rules."),
        dict(label="Fix", text="Correct errors, remove the unverifiable, adjust tone, add what's missing."),
        dict(label="Own", text="Once you send it, it is your work and responsibility.")])),
  dict(step=15, type="bars", title="Example: weekly hours on four tasks, before and after", caption="Illustrative team of four, with AI drafting and review time included. Your results will differ; measure your own.",
       config=dict(unit="hours per week", items=[dict(label="Customer replies before", value=20), dict(label="Customer replies with AI", value=12, highlight=True), dict(label="Meeting notes before", value=6), dict(label="Meeting notes with AI", value=2, highlight=True)],
        note="In this example the team frees about 12 hours a week across the two tasks after review time.")),
  dict(step=16, type="timeline", title="A 30-day AI productivity plan", caption="Click each week to see its focus.",
       config=dict(phases=[
        dict(label="Week 1", title="Set up", items=["Approved tools and data rules", "Custom instructions", "List ten tasks"]),
        dict(label="Week 2", title="Practise", items=["Prompt anatomy daily", "Iterate with follow-ups", "Four-step check"]),
        dict(label="Week 3", title="Templates", items=["Three templates", "One custom assistant or project"]),
        dict(label="Week 4", title="Share and measure", items=["Team prompt library", "Measure time saved", "Share lessons"])])),
 ],
 exam=[
  E("What are AI chat assistants built on?", ["Large language models trained to predict text and tuned to follow instructions", "Databases of verified facts only", "Search engines with no language ability", "Spreadsheets"], 0, "Chat assistants are built on large language models."),
  E("Which is a known limitation of AI assistants?", ["They cannot write emails", "They can state wrong facts confidently", "They only work in English", "They never vary their answers"], 1, "Confident errors, or hallucinations, are a key limitation."),
  E("Which three prompt elements matter most?", ["Emojis, length and politeness", "Role, examples and constraints only", "Context, task and format", "Font, colour and size"], 2, "Context, task and format have the biggest effect on usefulness."),
  E("What is few-shot prompting?", ["Asking only short questions", "Using the tool a few times a day", "Limiting answers to a few words", "Giving examples of the output style you want"], 3, "Examples show the assistant the style or structure to follow."),
  E("Before a complex task such as drafting a procedure, what can you ask the assistant to do?", ["Ask you the questions it needs answered first", "Skip the context", "Write as long as possible", "Use only capital letters"], 0, "Inviting questions gathers missing context."),
  E("A long conversation keeps repeating an error. What should you do?", ["Keep correcting it forever", "Start a new chat with a clean, complete prompt", "Switch off your computer", "Delete your account"], 1, "A fresh, complete prompt avoids accumulated confusion."),
  E("What is the best starting point for an AI-drafted email?", ["A blank prompt with no details", "A competitor's email", "Your own rough notes and the reader you are writing for", "A random template from the internet"], 2, "Your notes keep the content yours; the reader shapes the tone."),
  E("When summarizing a document with AI, what should you specify?", ["Nothing; summaries are automatic", "The font size", "Only the word count", "Who it is for, what decision it supports, the structure and length"], 3, "Audience, purpose, structure and length make summaries useful."),
  E("An AI tool reports a total from data without running a calculation. What should you do?", ["Check the arithmetic against the data", "Assume it is right", "Round it", "Ask it to repeat the number"], 0, "Language models are not reliable calculators unless they run code."),
  E("What is a valuable way to use AI on a plan you have written?", ["Ask it to approve the plan", "Ask it to find risks and argue the opposite case", "Let it decide for you", "Ask it to make the plan longer"], 1, "Critique and counterarguments expose blind spots."),
  E("What are the four steps of the output check?", ["Copy, paste, send, forget", "Write, print, sign, file", "Read, verify, fix, own", "Ask, wait, accept, share"], 2, "Read fully, verify facts, fix errors and own the result."),
  E("An AI draft cites a regulation number. What should you do?", ["Use it", "Remove all references", "Ask the AI if it is sure", "Verify it against an official source"], 3, "AI can invent references; verify with official sources."),
  E("Which information should never go into any AI tool?", ["Passwords and banking details", "A public press release", "A grammar question", "A general brainstorm"], 0, "Credentials and banking details must never be shared."),
  E("What is a good habit when a task does not need real names?", ["Use the real names anyway", "Replace names and identifying details, for example 'Customer A'", "Add more personal details for accuracy", "Use employees' home addresses"], 1, "Anonymizing reduces privacy risk."),
  E("Where is bias in AI output most important to watch for?", ["Formatting a table", "Choosing a font", "Decisions about people, such as hiring and performance", "Spell-checking"], 2, "Decisions about people carry the highest fairness risk."),
  E("Who is accountable for content produced with AI and sent to a customer?", ["The AI vendor", "Nobody", "The customer", "The person and organization that sent it"], 3, "Users remain accountable for what they send."),
  E("What should each entry in a team prompt library include?", ["Task, template, example output, checks and an owner", "Only the tool name", "Confidential customer data", "A list of banned words"], 0, "Complete entries make prompts reusable and safe."),
  E("What is the main risk of a custom assistant with outdated reference files?", ["It becomes slower", "It gives confident but wrong answers", "It deletes itself", "It costs more"], 1, "Stale references produce wrong answers."),
  E("Which task is a good first automation candidate with an AI step?", ["A one-off strategic decision", "Signing contracts automatically", "A frequent, rule-based task that is easy to check, with human approval", "Disciplinary decisions"], 2, "Frequent, checkable tasks with approval are lower risk."),
  E("When does time saved with AI become a cash saving?", ["Always", "Never", "Only if the tool is free", "When costs actually fall, such as less overtime or a hire avoided"], 3, "Freed time saves cash only when costs drop."),
 ],
)

if __name__ == "__main__":
    write(course, "prompting-ai-productivity", __file__, balance=True)
