"""V4.84: new book review: Clear Thinking by Shane Parrish (Portfolio, 2023). Review, lessons learned and how to apply it.

Usage: python3 content/articles/v484_articles.py, then python3 content/gen/add_article.py <slug>
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from feed_articles import fig
from v478_articles import table, words, art, steps_fig

CLEAR = "clear-thinking-by-shane-parrish-book-review-lessons-and-how-to-apply-them"


def fig_steps():
    return steps_fig([("1. Define", ["The real problem,", "in plain words"]), ("2. Explore", ["Several options,", "not just two"]),
                      ("3. Evaluate", ["Consequences,", "and then what?"]), ("4. Do it", ["Commit; set", "a kill signal"]),
                      ("5. Margin", ["Room for being", "wrong"]), ("6. Learn", ["Compare with", "your journal"])],
                     "Parrish's decision process in six steps: define the problem, explore possible solutions, evaluate the options, do it, "
                     "build in a margin of safety, and learn from the decision by comparing the outcome with what you wrote down at the time.")


def clear():
    defaults = [("Emotion", "Acting on a feeling before thinking", "Replying to a customer's angry email within minutes, in the same tone"),
                ("Ego", "Protecting how we look and feel about ourselves", "Defending a supplier you chose long after the evidence says change"),
                ("Social", "Going along with the group", "Approving a project in a meeting because nobody else objected"),
                ("Inertia", "Sticking with what we already do", "Keeping a manual process for years because it still more or less works")]
    strengths = [("Self-accountability", "Own your outcomes; no excuses, even when others are at fault"),
                 ("Self-knowledge", "Know your strengths, blind spots and the situations that trigger your defaults"),
                 ("Self-control", "Pause between the impulse and the action"),
                 ("Self-confidence", "Secure enough to change your mind and to be seen not knowing")]
    body = f"""
<p><em>Clear Thinking: Turning Ordinary Moments into Extraordinary Results</em> by Shane Parrish (Portfolio, October 2023, 288 pages) is a book about the decisions we do not notice we are making: the email answered in anger, the meeting where we go along with the room, the habit we never question. Parrish, a Canadian who worked at an intelligence agency before founding the Farnam Street blog and its Brain Food newsletter, argues that results are shaped less by a few big decisions than by how we handle these ordinary moments. This review summarises the book, sets out the lessons we took from it for running a small or mid-sized business, and gives a practical way to apply them.</p>
<h2>What the book covers</h2>
{table(["Part", "Theme", "In one line"], [
    ("1. The enemies of clear thinking", "Four defaults", "Instincts that act before we think"),
    ("2. Building strength", "Four strengths", "Character traits that create space to think"),
    ("3. Managing weakness", "Safeguards and mistakes", "Systems that protect us when strength is not enough"),
    ("4. Decisions", "A decision process", "Define, explore, evaluate, act, allow for error, learn"),
    ("5. Wanting what matters", "Goals", "Good judgment includes knowing what is worth wanting"),
])}
<h2>The four defaults</h2>
<p>Parrish's starting point is that much bad thinking is not thinking at all. We react on autopilot, driven by instincts that served our ancestors well. He names four of them:</p>
{table(["Default", "What it does", "What it looks like at work"], defaults)}
<p>Defaults cannot be removed, but they can be anticipated. Parrish's practical advice is to change the environment rather than rely on willpower: work with people whose habits you want to copy, and build routines so that the automatic behaviour is the good one.</p>
<h2>The four strengths</h2>
{table(["Strength", "What it means"], strengths)}
<p>The thread through all four is creating a gap between what happens and how we respond. In that gap, reasoning has a chance to work. Parrish is clear that this is character, not technique: no decision tool helps someone who is not honest with themselves.</p>
<h2>Managing weakness</h2>
<p>Strength is not always enough. We are more reactive when tired, hungry, stressed or rushed, so Parrish recommends safeguards: rules decided in advance, checklists, cooling-off periods, and asking someone else to look at the problem. He also offers a simple way to handle mistakes: take responsibility, learn what caused the error, decide what you will do differently, and repair any damage done to others.</p>
<h2>The decision process</h2>
{fig(fig_steps(), 1, "The decision process in Part 4 of the book, as we apply it.")}
<p>The process is sensible rather than new, but two parts stand out. Defining the problem gets more time than most of us give it, on the grounds that a well-stated problem often points to its own answer. And the margin of safety, borrowed from engineering and value investing, asks you to plan for being wrong: keep reserves, avoid decisions that cannot be undone, and set in advance the signal that tells you to stop.</p>
<p>Parrish also recommends writing down your reasoning when you decide, because memory rewrites the past to flatter us. A short decision journal lets you judge the decision on what you knew at the time, not only on how it turned out.</p>
<h2>What works, and what does not</h2>
<ul>
<li><strong>Strengths:</strong> short chapters, memorable stories, and a framework that is easy to recall under pressure. The emphasis on ordinary moments rather than big strategic choices is useful and less common in decision books.</li>
<li><strong>Weaknesses:</strong> regular readers of Farnam Street will recognise much of the material. Some readers find the advice more inspiring than step-by-step, and the final part on what to want in life is a change of register from the practical middle of the book.</li>
</ul>
<h2>Lessons learned</h2>
<p>These are the lessons we took for owners and managers of small and mid-sized businesses.</p>
<ol>
<li><strong>Most damage comes from unforced errors.</strong> In operations work we see more value lost to rushed replies, avoided conversations and unexamined habits than to wrong strategies. Avoiding the obvious mistakes is the first gain.</li>
<li><strong>Design the environment, do not rely on willpower.</strong> A rule such as "no pricing decisions on the call; we reply the next morning" works better than resolving to stay calm.</li>
<li><strong>Inertia is the expensive default in a small business.</strong> Spreadsheets, manual re-keying and "the way we've always done it" survive because nobody decides to keep them; nobody decides to change them either. A regular review of recurring processes breaks this.</li>
<li><strong>Meetings amplify the social default.</strong> Ask for written views before the meeting, and ask the most junior person to speak first.</li>
<li><strong>Write decisions down.</strong> A few lines at the time of a decision make later reviews honest and turn experience into learning.</li>
<li><strong>Leave a margin of safety.</strong> Cash reserves, a second supplier, a pilot before a full rollout and a clear stop signal all buy time to recover from being wrong.</li>
</ol>
<h2>How to implement it</h2>
<h3>Week 1: notice the defaults</h3>
<p>For one week, note each time you acted before thinking: which default, what triggered it, and what it cost. Most people find two or three recurring triggers, such as late-afternoon email, a particular customer or a weekly meeting.</p>
<h3>Week 2: set three safeguards</h3>
{table(["Trigger", "Safeguard", "Example rule"], [
    ("Angry or urgent messages", "Cooling-off period", "Draft the reply, send it after a break or the next morning"),
    ("Big purchases or hires", "Second opinion", "Any decision over a set amount is reviewed by one other person"),
    ("Group decisions", "Independent views first", "Everyone writes their view before discussion starts"),
])}
<h3>Week 3: start a decision journal</h3>
{table(["Field", "What to write"], [
    ("Decision and date", "What you decided, in one sentence"),
    ("Problem", "The problem you are solving, stated plainly"),
    ("Options considered", "At least three, including doing nothing"),
    ("Why this option", "The main reasons and what you expect to happen"),
    ("How you feel", "Tired, rushed, confident, under pressure?"),
    ("Kill signal", "What result would make you stop or change course"),
    ("Review date", "When you will compare the outcome with this entry"),
])}
<h3>Week 4: review and repeat</h3>
<p>Review the journal entries that have reached their review date. Separate bad luck from bad judgment: a good decision can have a bad outcome, and the reverse. Keep the safeguards that helped, drop the ones that did not, and add one more.</p>
<h2>Worked example: replacing a key supplier</h2>
<p>A fabricator's main steel supplier has been late three times in a quarter. The owner's first impulse is to switch immediately (emotion), but he chose the supplier himself and is reluctant to admit it is not working (ego), and switching means new paperwork and relationships (inertia). Using the process from the book:</p>
<ul>
<li><strong>Define:</strong> the problem is not "a bad supplier" but late deliveries that delay two key customers' orders.</li>
<li><strong>Explore:</strong> switch suppliers; add a second supplier for critical items; hold more stock of those items; agree a delivery-performance review with the current supplier.</li>
<li><strong>Evaluate:</strong> a full switch is hard to reverse and carries quality risk; a second source for critical items reduces risk at a small cost.</li>
<li><strong>Do it, with a margin:</strong> qualify a second supplier for the ten most critical items and hold two weeks of extra stock of them while the change beds in. Kill signal: if the current supplier is late again in the next 60 days, move half the volume.</li>
<li><strong>Learn:</strong> the journal entry is reviewed after 90 days.</li>
</ul>
<p>The example is illustrative; the point is that each default is named, and a reversible option with a stop signal is chosen over a dramatic one.</p>
<h2>Who should read it</h2>
<p>Owners, managers and anyone who makes frequent decisions under time pressure. It suits readers who want a framework they can remember rather than a textbook on cognitive bias. Readers who already follow Farnam Street closely may prefer to skim the first half and read Parts 3 and 4 carefully.</p>
<h2>Verdict</h2>
<p><em>Clear Thinking</em> does not offer many new techniques, but it makes a convincing case that better results start with handling ordinary moments well, and it gives a simple vocabulary for doing so. Its practical value comes from the safeguards and the decision journal; used for a month, they are likely to change how you decide more than the book's stories alone.</p>
<p>Related reviews: <a href="atomic-habits-by-james-clear-a-deep-dive-review-and-guide-to-habit-transformation.html">Atomic Habits</a>, which covers building the routines Parrish recommends; <a href="the-psychology-of-money-by-morgan-housel-a-thought-provoking-review-on-wealth-behavior-and-happin.html">The Psychology of Money</a>; and our guide to <a href="ooda-loop-vs-pdca-cycle-which-framework-drives-faster-and-smarter-decisions.html">OODA and PDCA decision cycles</a>. For a structured approach to decisions in a team, see our <a href="../leadership-operating-system.html">leadership operating system</a>.</p>
"""
    r = [("first-principles-thinking-the-core-of-breakthrough-problem-solving-in-business", "First principles thinking for business problems"),
         ("the-one-thing-by-gary-keller-and-jay-papasan-a-deep-dive-review-for-achieving-extraordinary-results", "The ONE Thing: book review"),
         ("6-mckinsey-principles-to-unlock-creative-thinking-and-innovation", "Six practices to build innovation in a small business")]
    s = [("Penguin Random House: Clear Thinking by Shane Parrish", "https://www.penguinrandomhouse.com/books/611709/clear-thinking-by-shane-parrish/9780593086117"),
         ("Farnam Street", "https://fs.blog/")]
    a = art(CLEAR, "Clear Thinking by Shane Parrish: Book Review, Lessons Learned and How to Apply Them",
            "Review of Clear Thinking by Shane Parrish: the four defaults, four strengths, safeguards and decision process, lessons for small businesses and a four-week plan to apply it.",
            ["book-review", "strategy"], ["Clear Thinking", "Shane Parrish", "decision making", "book review", "decision journal", "Farnam Street"], body, "Book Review", r, s)
    return a


if __name__ == "__main__":
    a = clear()
    json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(a["slug"], words(a["body"]), "words", a["read"])
