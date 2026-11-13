"""V4.90: The Art of the Deal vs The Art of War rewritten as a two-book review with comparison tables, a figure and
worked examples. Same address, original date kept (2025-04-21); now filed under Book Review and Strategy.

The review treats both books as business advice; it does not comment on the authors' later careers or politics.
Usage: python3 content/articles/v490_articles.py, then python3 content/gen/refresh_article.py <slug>
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from feed_articles import svg, fig, box, txt, DEFS, NAVY, BLUE, GREEND, ORANGE, MUTED, PALE, GREENF, ORANGEF
from v478_articles import table, words, art

SLUG = "the-art-of-the-deal-vs-the-art-of-war-a-strategic-comparison-through-economics-philosophy-and-et"
ORIGINAL = "2025-04-21"


def fig_fit():
    """2 x 2: which book's advice fits, by bargaining strength and length of the relationship."""
    s = DEFS
    x0, y0, w, h = 130, 30, 560, 300
    q = [(x0, y0, "Strong position, one-off deal", ["Deal: use your leverage,", "keep alternatives open,", "aim high but deliver"], PALE, BLUE),
         (x0 + w / 2, y0, "Strong position, long relationship", ["Both: protect the downside,", "win without humiliating,", "keep your word"], GREENF, GREEND),
         (x0, y0 + h / 2, "Weak position, one-off deal", ["War: avoid a head-on contest,", "find the gap, choose", "the time and place"], ORANGEF, ORANGE),
         (x0 + w / 2, y0 + h / 2, "Weak position, long relationship", ["War: know yourself, build", "position slowly, make", "yourself hard to replace"], PALE, BLUE)]
    for x, y, t, lines, fill, col in q:
        s += f'<rect x="{x + 4}" y="{y + 4}" width="{w / 2 - 8}" height="{h / 2 - 8}" rx="10" fill="{fill}" stroke="{col}"/>'
        s += txt(x + w / 4, y + 34, t, "middle", col, 13.5, True)
        for i, ln in enumerate(lines): s += txt(x + w / 4, y + 66 + i * 21, ln, "middle", NAVY, 13)
    s += txt(x0 - 14, y0 + h / 4 + 5, "Strong", "end", NAVY, 13, True) + txt(x0 - 14, y0 + 3 * h / 4 + 5, "Weak", "end", NAVY, 13, True)
    s += f'<text x="34" y="{y0 + h / 2}" text-anchor="middle" font-size="12.5" fill="{MUTED}" transform="rotate(-90 34 {y0 + h / 2})">Your bargaining position</text>'
    s += txt(x0 + w / 4, y0 + h + 24, "One-off", "middle", NAVY, 13, True) + txt(x0 + 3 * w / 4, y0 + h + 24, "Long-term", "middle", NAVY, 13, True)
    s += txt(x0 + w / 2, y0 + h + 46, "Length of the relationship", "middle", MUTED, 12.5)
    return svg("A two-by-two grid showing when each book's advice fits, by bargaining position (strong or weak) and length of the relationship "
               "(one-off or long-term). Strong position, one-off deal: The Art of the Deal's advice to use leverage, keep alternatives open and aim high "
               "but deliver. Strong position, long relationship: both books, protect the downside, win without humiliating the other side and keep your word. "
               "Weak position, one-off deal: The Art of War's advice to avoid a head-on contest, find the gap and choose the time and place. Weak position, "
               "long relationship: The Art of War again, know yourself, build position slowly and make yourself hard to replace.", 720, 390, s, 600)


def body():
    about = [("Written", "1987", "About 2,500 years ago (traditionally the 5th century BC)"),
             ("Author", "Donald J. Trump with journalist Tony Schwartz", "Attributed to Sun Tzu, a Chinese general; probably refined by later editors"),
             ("Setting", "New York real estate and casinos in the 1980s", "Warfare between Chinese states"),
             ("Form", "Memoir: a week in the author's working life, then the stories behind his deals", "Thirteen short chapters of principles"),
             ("Core idea", "Think big, use leverage and promote yourself to win deals", "Win with the least fighting, through preparation, position and adaptability"),
             ("Tone", "Confident, personal, anecdotal", "Spare, general, often paradoxical")]
    deal = [("Think big", "Set ambitious goals; big ideas attract attention and partners", "Bid for the larger contract you can actually deliver"),
            ("Protect the downside", "Plan for the worst case; the upside takes care of itself", "Fixed-price quotes only with a contingency and clear scope"),
            ("Maximize your options", "Never rely on one deal or one plan", "Keep a second customer or supplier in play"),
            ("Know your market", "Trust first-hand observation over consultants' reports", "Talk to customers yourself before launching"),
            ("Use your leverage", "Know what the other side wants or needs from you", "Know what you offer that competitors cannot"),
            ("Enhance your location", "Improve what you have to raise its value", "Upgrade the product or service rather than discounting"),
            ("Get the word out", "Publicity has value; be visible", "Case studies, reviews and local press"),
            ("Fight back", "Respond firmly when treated unfairly", "Enforce contract terms and payment dates"),
            ("Deliver the goods", "Promotion fails if the product does not live up to it", "Under-promise and over-deliver"),
            ("Contain the costs", "Spend what is needed, no more", "Review every recurring cost once a year"),
            ("Have fun", "Enjoy the game; energy matters", "Choose work you will keep doing well")]
    war = [("Win without fighting", "The best result is achieved without a costly battle", "Win the customer through fit and service, not a price war"),
           ("Know yourself and the other side", "Victory comes from knowing both your strengths and theirs", "Honest strengths-and-weaknesses review against two rivals"),
           ("Prepare before you act", "Battles are won in the planning, before they are fought", "Prepare figures and options before every negotiation"),
           ("Avoid strength, strike weakness", "Do not attack where the other side is strongest", "Serve the niche a large competitor neglects"),
           ("Adapt like water", "Change approach as conditions change", "Review plans monthly, not yearly"),
           ("Speed matters", "Long campaigns drain resources", "Short pilots rather than open-ended projects"),
           ("Use information", "Good intelligence prevents expensive mistakes", "Track market prices, tenders and customer feedback")]
    compare = [("Competition", "A contest to win; rivals are obstacles", "A contest best won without a fight"),
               ("Risk", "Protect the downside, then go big", "Do not engage unless the odds favour you"),
               ("Leverage", "What the other side wants from you", "Position: terrain, timing and the other side's weakness"),
               ("Information", "Your own instincts and first-hand observation", "Systematic intelligence about the other side"),
               ("Visibility", "Be seen; publicity is an asset", "Conceal your plans; appear where not expected"),
               ("Conflict", "Fight back hard when attacked", "Fighting is costly; avoid it when possible"),
               ("Leadership", "Personal, charismatic, the leader as the brand", "Disciplined, measured, the leader as strategist"),
               ("Ethics", "Bold, sometimes exaggerated claims (\"truthful hyperbole\")", "Deception towards enemies; benevolence and discipline towards one's own side"),
               ("Time horizon", "The deal in front of you", "The campaign, and the state that must survive it")]
    agree = [("Prepare thoroughly", "Know your market", "Know the enemy and yourself"),
             ("Limit the downside", "Protect the downside", "Do not fight a battle you cannot win"),
             ("Keep options open", "Maximize your options", "Adapt; do not repeat the same tactics"),
             ("Position beats effort", "Leverage and location", "Terrain and timing"),
             ("Deliver", "Deliver the goods", "Discipline and method decide outcomes")]
    prep = [("What do we want?", "Ideal result, acceptable result, walk-away point"),
            ("What are our alternatives?", "Other customers, suppliers or plans if this deal fails (maximize your options)"),
            ("What does the other side need?", "Their pressures, deadlines and alternatives (know the other side; leverage)"),
            ("Where are we strong, where weak?", "Honest view of both sides (know yourself)"),
            ("What could go wrong?", "Worst case and how we limit it (protect the downside)"),
            ("Where and when?", "Timing and setting that favour us (choose the terrain)"),
            ("What will we promise?", "Only what we can deliver (deliver the goods)")]
    return f"""
<p>This review compares two very different books that business readers often set side by side: <em>The Art of the Deal</em> (1987), a memoir of New York real estate deal-making by Donald J. Trump with journalist Tony Schwartz, and <em>The Art of War</em>, the ancient Chinese text on strategy attributed to Sun Tzu. One is about asserting yourself to win; the other about winning without having to fight. This article was first published in April 2025 and has been rewritten with side-by-side tables, a figure and worked examples. It looks at both books as business advice only, not at the authors' later careers.</p>
<h2>The two books at a glance</h2>
{table(["", "The Art of the Deal", "The Art of War"], about)}
<h2>The Art of the Deal in brief</h2>
<p>The book opens with a diary of a busy week of calls and meetings, then tells the stories behind the author's best-known projects. Its practical core is a short list of principles he calls the elements of the deal:</p>
{table(["Principle", "What it means", "Small-business version"], deal)}
<h2>The Art of War in brief</h2>
<p>Sun Tzu's thirteen chapters cover planning, the cost of war, attack, position, energy, manoeuvre, terrain and the use of spies. The text starts with five factors to assess before any campaign: the moral cause that unites people with their leader, the season and conditions, the terrain, the quality of the commander, and organisation and discipline. Its most useful principles for business are these:</p>
{table(["Principle", "What it means", "Small-business version"], war)}
<h2>Head to head</h2>
{table(["Theme", "The Art of the Deal", "The Art of War"], compare)}
<h2>Where they agree</h2>
<p>For all their differences in tone, the books share more than their titles:</p>
{table(["Shared idea", "In The Art of the Deal", "In The Art of War"], agree)}
<h2>When each book's advice fits</h2>
{fig(fig_fit(), 1, "Which book to lean on depends on how strong your position is and how long the relationship will last.")}
<p>The Art of the Deal's style works best when you hold a strong hand in a one-off transaction. The Art of War is more useful when you are the smaller party, or when the relationship will continue after the deal, because it values avoiding fights that leave both sides weaker.</p>
<h2>Lessons for small businesses</h2>
<ol>
<li><strong>Preparation wins.</strong> Both books put most of the work before the meeting: knowing your numbers, the other side's needs and your alternatives.</li>
<li><strong>Protect the downside first.</strong> Avoid commitments that could sink the business if things go wrong; take the bigger risks only once the worst case is survivable.</li>
<li><strong>Your alternatives are your leverage.</strong> A second customer, supplier or plan is worth more in a negotiation than any tactic.</li>
<li><strong>Do not fight where the other side is strongest.</strong> A small firm rarely wins a price war with a large one; it wins on service, speed, specialism or location.</li>
<li><strong>Be visible, but deliver.</strong> Promotion brings opportunities; only delivery keeps them. Exaggerated claims can also breach Canada's Competition Act rules on false or misleading representations.</li>
<li><strong>Keep conflict for when it is needed.</strong> Stand firm on contract terms and payment, but treat most customers, suppliers and staff as long-term partners, not opponents.</li>
</ol>
<h2>A negotiation preparation sheet using both books</h2>
{table(["Question", "What to write down"], prep)}
<h2>Worked example: a large customer asks for a price cut</h2>
<p>A machine shop earns 30% of its revenue from one distributor, which asks for a 10% price reduction at contract renewal. The owner's first instinct is to refuse outright or to give in to keep the volume. Working through the preparation sheet:</p>
<ul>
<li><strong>Alternatives:</strong> two other prospects could take some of the capacity within six months; that is the walk-away option, but not an immediate one.</li>
<li><strong>The other side's needs:</strong> the distributor values short lead times and has had quality problems with a cheaper competitor.</li>
<li><strong>Position:</strong> the shop is strong on speed and quality, weak on price for long production runs.</li>
<li><strong>The offer:</strong> no cut on standard parts, a 5% reduction on high-volume parts in exchange for a two-year agreement and quarterly forecasts that let the shop schedule more efficiently.</li>
<li><strong>Downside:</strong> the owner starts actively winning the two prospects so that one customer never again holds 30% of revenue.</li>
</ul>
<p>The result uses the Art of the Deal's leverage and options and the Art of War's advice to avoid the head-on fight. The figures are illustrative.</p>
<h2>Worked example from daily life: renewing a rental lease</h2>
<p>A tenant's landlord asks them to agree to a rent increase above the provincial limit. Before replying, the tenant checks the rules (in British Columbia, rent can rise only once every 12 months, with three months' written notice, and within the yearly limit set by the Residential Tenancy Branch, 2.3% for 2026; a tenant does not have to agree to more), looks at comparable listings nearby, and notes their own strengths: always paid on time, looked after the unit, would save the landlord a vacancy and the cost of finding a new tenant. They reply politely, decline the above-limit increase, and offer to stay on for the long term, which saves the landlord a vacancy, in return for no more than the allowed increase. There is no confrontation, the tenant knows the terrain, and the landlord gets something they value. The approach is illustrative; check your own province's tenancy rules.</p>
<h2>Criticisms of each</h2>
<ul>
<li><strong>The Art of the Deal</strong> reflects one industry in one decade, and its stories are told from the author's side only. Its comfort with exaggeration and hard-edged tactics does not suit businesses that depend on repeat customers and trust.</li>
<li><strong>The Art of War</strong> is written for war. Taken literally, its emphasis on deception and treating others as enemies is the wrong model for customers, staff and most suppliers. Its value lies in the principles of preparation, position and economy of effort, not the military framing.</li>
</ul>
<h2>Verdict</h2>
<p>Read together, the books cover two halves of strategy. <em>The Art of the Deal</em> is about ambition, leverage and making things happen; <em>The Art of War</em> is about judgment, position and knowing when not to act. For most small businesses, the Art of War's patience and preparation make the better default, with the Art of the Deal's options and leverage applied in the moments that need them, and with both books' shared lesson in mind: protect the downside and deliver what you promise.</p>
<p>Related reviews: <a href="clear-thinking-by-shane-parrish-book-review-lessons-and-how-to-apply-them.html">Clear Thinking</a> on handling decisions under pressure, and <a href="how-to-build-a-predictable-and-scalable-sales-model-lessons-from-predictable-revenue-by-aaron-ros.html">Predictable Revenue</a> on building a sales process.</p>
"""


def article():
    r = [("clear-thinking-by-shane-parrish-book-review-lessons-and-how-to-apply-them", "Clear Thinking by Shane Parrish: book review"),
         ("6-essential-steps-to-streamline-and-enhance-your-sales-process", "How to build and streamline a sales process"),
         ("adapting-business-operations-for-enhanced-agility-and-market-competitiveness", "Operational agility for small and mid-sized businesses")]
    s = [("Sun Tzu, The Art of War, translated by Lionel Giles (1910), Project Gutenberg", "https://www.gutenberg.org/ebooks/132"),
         ("Competition Bureau Canada: false or misleading representations", "https://competition-bureau.canada.ca/deceptive-marketing-practices"),
         ("Government of British Columbia: rent increases", "https://www2.gov.bc.ca/gov/content/housing-tenancy/residential-tenancies/rent-rtb/rent-increases")]
    return art(SLUG, "The Art of the Deal vs The Art of War: Two Books on Strategy Compared",
               "A side-by-side review of The Art of the Deal and The Art of War: core principles, where they agree and differ, when each fits, lessons for small businesses and worked examples.",
               ["book-review", "strategy"], ["The Art of the Deal", "The Art of War", "Sun Tzu", "negotiation", "strategy", "book review"], body(), "Book Review", r, s)


if __name__ == "__main__":
    op = os.path.join(HERE, "original_dates.json")
    od = json.load(open(op, encoding="utf-8")); od[SLUG] = ORIGINAL
    note = od.pop("_note"); json.dump({"_note": note, **dict(sorted(od.items()))}, open(op, "w", encoding="utf-8"), indent=1)
    a = article()
    json.dump(a, open(os.path.join(HERE, SLUG + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(SLUG[:40], words(a["body"]), "words", a["read"])
