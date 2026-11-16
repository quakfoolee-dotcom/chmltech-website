"""Chmltech Online Journal, Vol. 106, Issue 4: Why the ERP Schedule Fails on the Shop Floor (Nov 16 2026).

Composite case (single-shift vinyl windows-and-doors plant, Lower Mainland). Model: content/journal/ops/models/fcs/ (discrete-event
job-shop simulation, 100 runs of 50 measured weeks per configuration). Red-team checked (model audit and references) before publication."""

SLUG = "why-the-erp-schedule-fails-on-the-shop-floor-finite-capacity-scheduling-rules-for-high-mix-manufacturers"
META = dict(
    volume=106, issue=4,
    title="Why the ERP Schedule Fails on the Shop Floor: Finite-Capacity Scheduling Rules for High-Mix Manufacturers",
    short_title="Finite-Capacity Scheduling for High-Mix Manufacturers",
    meta="A shop-floor simulation shows why ERP lead times miss due dates in high-mix plants, and which dispatch and release rules lift on-time delivery from 77% to 92%.",
    keywords=["finite-capacity scheduling", "dispatching rules", "drum-buffer-rope", "workload control", "modified due date",
              "discrete-event simulation", "high-mix manufacturing", "ERP"],
)
ABSTRACT = ("Most small and mid-sized manufacturers plan with an ERP system that assumes unlimited capacity and fixed lead times, then run the "
            "shop floor first-come, first-served. A discrete-event simulation of a high-mix windows-and-doors plant shows why that combination "
            "misses due dates, and which simple scheduling rules fix it. At 82% load on the bottleneck welder, the ERP-style plan delivers 77% of "
            "orders on time (±3 points, 95% confidence over 100 simulated years). Its average planned lead time of 7.9 working days is longer "
            "than the average actual lead time of 5.7 days: the plan fails on the spread, not the average. Orders spend 75% of their time "
            "waiting, mostly in front of the welder. Sequencing the welder queue by modified due date raises on-time delivery to 90%. A "
            "load-based release rule that holds orders until the welder can absorb them lifts it to 92%, cuts shop-floor lead time by 31% and "
            "absorbs a four-week order spike with a third of the extra late orders of the ERP-style plan. The price is about two very large "
            "orders a year more than 20 working days late; capping lateness removes them but gives back 5 to 7 points of on-time delivery. "
            "Critical ratio performed worst (66% on time), and strict due-date release improved shop-floor flow but not customer service.")

REFS = {
    "hopp": ("Hopp, W. J., &amp; Spearman, M. L. (2008). <em>Factory physics</em> (3rd ed.). McGraw-Hill/Irwin.",
             "https://search.worldcat.org/search?q=Hopp+Spearman+Factory+Physics+3rd+edition"),
    "q2c": ("Lee, Q. F. (2026). The quote-to-cash process in manufacturing (Part 1 of the quote-to-cash series). <em>Chmltech Insights</em>.",
            "https://www.chmltech.com/post/quote-to-cash-process-in-manufacturing.html"),
    "q2csim": ("Lee, Q. F. (2026). Quote-to-cash simulation: Run a window factory in 3D (Part 2 of the quote-to-cash series). <em>Chmltech Insights</em>.",
               "https://www.chmltech.com/post/quote-to-cash-simulation-run-a-window-factory-in-3d.html"),
    "q2cfix": ("Lee, Q. F. (2026). Shorten quote to cash: What to fix first and the payback (Part 3 of the quote-to-cash series). <em>Chmltech Insights</em>.",
               "https://www.chmltech.com/post/shorten-quote-to-cash-what-to-fix-first.html"),
    "kingman": ("Kingman, J. F. C. (1961). The single server queue in heavy traffic. <em>Proceedings of the Cambridge Philosophical Society</em>, 57(4), 902–904.",
                "https://doi.org/10.1017/S0305004100036094"),
    "pinedo": ("Pinedo, M. L. (2016). <em>Scheduling: Theory, algorithms, and systems</em> (5th ed.). Springer.",
               "https://doi.org/10.1007/978-3-319-26580-3"),
    "bb": ("Baker, K. R., &amp; Bertrand, J. W. M. (1982). A dynamic priority rule for scheduling against due-dates. <em>Journal of Operations Management</em>, 3(1), 37–42.",
           "https://doi.org/10.1016/0272-6963(82)90020-1"),
    "bk": ("Baker, K. R., &amp; Kanet, J. J. (1983). Job shop scheduling with modified due dates. <em>Journal of Operations Management</em>, 4(1), 11–22.",
           "https://doi.org/10.1016/0272-6963(83)90022-0"),
    "thurer12": ("Thürer, M., Stevenson, M., Silva, C., Land, M. J., &amp; Fredendall, L. D. (2012). Workload control and order release: A lean solution for make-to-order companies. <em>Production and Operations Management</em>, 21(5), 939–953.",
                 "https://doi.org/10.1111/j.1937-5956.2011.01307.x"),
    "wein": ("Wein, L. M. (1991). Due-date setting and priority sequencing in a multiclass M/G/1 queue. <em>Management Science</em>, 37(7), 834–850.",
             "https://doi.org/10.1287/mnsc.37.7.834"),
    "goal": ("Goldratt, E. M., &amp; Cox, J. (1984). <em>The goal</em>. North River Press. (3rd rev. ed., 2004, <em>The goal: A process of ongoing improvement</em>.)",
             "https://search.worldcat.org/search?q=Goldratt+Cox+The+Goal+process+of+ongoing+improvement"),
    "race": ("Goldratt, E. M., &amp; Fox, R. E. (1986). <em>The race</em>. North River Press.",
             "https://search.worldcat.org/search?q=Goldratt+Fox+The+Race+1986"),
    "sr": ("Schragenheim, E., &amp; Ronen, B. (1990). Drum-buffer-rope shop floor control. <em>Production and Inventory Management Journal</em>, 31, 18–23.",
           "https://search.worldcat.org/search?q=Schragenheim+Ronen+Drum-buffer-rope+shop+floor+control"),
    "land": ("Land, M. J. (2006). Parameters and sensitivity in workload control. <em>International Journal of Production Economics</em>, 104(2), 625–638.",
             "https://doi.org/10.1016/j.ijpe.2005.03.001"),
    "thurer10": ("Thürer, M., Silva, C., &amp; Stevenson, M. (2010). Workload control release mechanisms: From practice back to theory building. <em>International Journal of Production Research</em>, 48(12), 3593–3617.",
                 "https://doi.org/10.1080/00207540902922810"),
    "thurer15": ("Thürer, M., Land, M. J., Stevenson, M., Fredendall, L. D., &amp; Godinho Filho, M. (2015). Concerning workload control and order release: The pre-shop pool sequencing decision. <em>Production and Operations Management</em>, 24(7), 1179–1192.",
                 "https://doi.org/10.1111/poms.12304"),
    "conwip": ("Spearman, M. L., Woodruff, D. L., &amp; Hopp, W. J. (1990). CONWIP: A pull alternative to kanban. <em>International Journal of Production Research</em>, 28(5), 879–894.",
               "https://doi.org/10.1080/00207549008942761"),
    "ramasesh": ("Ramasesh, R. (1990). Dynamic job shop scheduling: A survey of simulation research. <em>Omega</em>, 18(1), 43–57.",
                 "https://doi.org/10.1016/0305-0483(90)90017-4"),
}

CODE = {"appendix": open(__file__.replace("paper_v106_i4.py", "models/fcs/fcs_scheduling.py"), encoding="utf-8").read().rstrip()}

BODY = r"""
## Introduction

Every plant manager knows the scene: the ERP system shows a clean production schedule, while the shop floor runs from a whiteboard, a hot list and the loudest customer's phone call. Orders the system says are on track ship late; orders nobody was watching ship early.

The cause is rarely the people or the software licence. It is the planning logic. Material requirements planning (MRP), the engine inside most ERP systems, plans each operation with a fixed lead time and assumes every work centre can take whatever load arrives. That is called infinite-capacity planning [@hopp]. It produces dates that look precise but ignore queues, and queues are where most of an order's time goes.

Finite-capacity scheduling closes the gap by deciding, at each machine, which waiting order to run next, and, at the front door, when to release new orders to the floor. Neither decision needs expensive software. This paper tests the common rules on a simulated high-mix plant and answers three practical questions:

- How far does an ERP-style plan drift from reality as the bottleneck gets busier?
- Which sequencing rule should the bottleneck use?
- Does holding orders back before release help, and how big should the buffer be?

The plant is a windows-and-doors manufacturer, the same type of business followed in the Chmltech quote-to-cash series [@q2c, @q2csim, @q2cfix]. This paper covers the step between order entry and shipping: planning and making.

## Why Infinite-Capacity Planning Fails

ERP lead times are fixed numbers, but real lead times grow sharply as the bottleneck gets busy, and the spread grows faster than the average.

A typical ERP routing gives each operation a planned lead time, often one day, and adds a safety margin. The planned lead time is the same whether the plant is half empty or flooded with orders. Queueing theory says otherwise. Kingman's approximation for the average waiting time W<sub>q</sub> at a single work centre is given by Eq. (1):

TEX W_q \approx \left(\frac{c_a^{2} + c_s^{2}}{2}\right)\left(\frac{u}{1-u}\right)t_s

Here u is utilization, t<sub>s</sub> is the average effective processing time including setups, and c<sub>a</sub> and c<sub>s</sub> are the coefficients of variation of arrivals and processing times. The formula is exact only for the simplest queue but is a good approximation near saturation [@kingman, @hopp]. The u/(1 − u) term is the problem: at 50% utilization it equals 1, at 80% it equals 4, and at 90% it equals 9. Variability multiplies it. High-mix shops have plenty of both: orders arrive in clumps when builders release jobs, which raises c<sub>a</sub>, and a two-unit door order and a 30-unit window order share the same machines, which raises c<sub>s</sub>.

FIG fig1-leadtime-vs-load || Actual order lead time against welder load, mean and 95th percentile, compared with the average ERP planned lead time of 7.9 working days; 100 runs of 50 measured weeks per load level. || Two rising curves against welder load from 53% to 90%: mean lead time from 3.3 to 7.7 days and 95th-percentile lead time from 7.8 to 19.9 days, crossing a flat planned lead time of 7.9 days near 55% load. ||

Figure 1 draws two lessons. First, the ERP plan is not wrong on average: at 82% welder load, the average order takes 5.7 working days against an average plan of 7.9. Second, the average does not matter to the customer whose order is in the tail. Almost one order in four (23%) takes longer than its planned lead time, and the slowest 5% take 14 days or more. In the simulated plant, an order spends 75% of its time waiting and only 25% being worked on, and 2.8 of its 4.3 waiting days are in front of the welder. Scheduling is the management of that queue.

## The Case: A Windows-and-Doors Plant

The plant is a composite built for this paper: a single-shift vinyl window and door maker in the Lower Mainland that takes about 620 orders in a 50-week year, 12.4 a week, from builders, renovators and dealers. One four-head vinyl welder is the bottleneck, loaded to 82%. Table 1 gives the product mix and Table 2 the load on each work centre.

TABLE Product families and routings.
| Product family | Share of orders | Average units per order | Routing |
| Casement windows | 35% | 10 | Cut, Weld, Clean, Glaze, Assemble, Pack |
| Slider windows | 25% | 10 | Cut, Weld, Clean, Glaze, Pack |
| Patio doors | 15% | 3 | Cut, CNC, Weld, Clean, Glaze, Assemble, Pack |
| Entry doors | 15% | 3 | CNC, Door prep, Glaze, Assemble, Pack |
| Custom shapes | 10% | 4 | Cut, CNC, Weld, Clean, Glaze, Assemble, Pack |

TABLE Work centre loads. || Each work centre has one machine or station on a single 40-hour shift.
| Work centre | Average load |
| Weld | 82% |
| Glaze | 62% |
| Assemble | 61% |
| Clean | 46% |
| Cut | 41% |
| Pack | 28% |
| CNC | 23% |
| Door prep | 12% |

Three features make the plant high-mix and hard to schedule:

- **Order sizes vary widely.** Units per order follow a geometric distribution, so most orders are small but a few are large. Each operation takes a setup (15 minutes, 24 minutes at the welder) plus a time per unit, with random variation (coefficient of variation 40%). Because order sizes vary so much, total job times at the welder vary far more than that: their squared coefficient of variation is about 1.
- **Orders arrive in clumps.** Builders release several orders at once; on average, orders arrive in groups of two.
- **Not every order uses the bottleneck.** Entry doors skip the welder entirely, so a rule that only watches the welder must still keep doors moving.

Due dates follow ERP logic: one working day per operation plus two days of margin. A slider window is promised in 7 working days, a patio door in 9. The average promise is 7.9 working days. This rule ignores order size: a 50-window order gets the same promise as a 5-window order of the same type.

## Simulation Method and the Rules Tested

A discrete-event simulation follows every order through every work centre, so queues, clumped arrivals and order interactions emerge on their own rather than being assumed.

Each run simulates 68 weeks: a 10-week warm-up, 50 measured weeks, and 8 weeks to let the last measured orders finish. Each configuration is run 100 times with different random seeds, so every result is an average over 100 simulated years. Every rule sees exactly the same orders in the same run, which isolates the effect of the rule from luck. On time means an order finishes on or before its promised date. On-time rates are reported with 95% confidence intervals across runs, and percentiles are taken over all orders from all runs.

Two kinds of decision are tested. **Dispatching rules** choose which waiting order a work centre runs next [@pinedo]. Table 3 lists the five tested.

TABLE Dispatching rules tested.
| Rule | Picks the order with | Common in practice because |
| First in, first out (FIFO) | The earliest arrival at the queue | It feels fair; it is how most shop floors run by default |
| Earliest due date (EDD) | The earliest promised date | It is the obvious due-date rule |
| Critical ratio (CR) | The lowest ratio of time left to work left | Several ERP packages offer it as a standard priority option |
| Shortest processing time (SPT) | The shortest current operation | It clears the most orders fastest |
| Modified due date (MDD) | The lowest of max(due date, now + remaining work) | It blends EDD and shortest remaining work |

Modified due date was introduced by Baker and Bertrand [@bb] and extended to job shops by Baker and Kanet [@bk]. This paper uses the job-based version, in which remaining work is all the processing the order still needs. For an order that is not yet urgent, its priority is its due date. Once an order can no longer finish by its due date, its priority becomes the time it could finish, so late orders with little work left go first. The rule therefore behaves like EDD in calm periods and like shortest remaining work in a crisis.

**Release rules** decide when an order leaves the office for the floor:

- **Push (ERP default).** Every order is released the moment it is entered.
- **Strict drum-buffer-rope (DBR).** Orders wait in an office pool, sorted by due date. The next order is released only when the welding work already on the floor is below a buffer, measured in hours of welder work. Orders that skip the welder are released at once.
- **Load-based release.** The same buffer, but if the next order is too large to fit, a smaller one behind it that does fit may go first. This is a simple load-limited release in the spirit of workload control [@thurer12].

The Appendix gives a short Python version of the model.

## Results: Which Dispatching Rule Wins

Shortest processing time and modified due date ship the most orders on time, 93% to 94%, and MDD at the welder alone gets 90% (Figure 2). Both leave a handful of very large orders badly late, a price Section 5.1 sets out.

FIG fig2-ontime-by-rule || Share of orders delivered on time by dispatching rule under push release, with 95% confidence intervals; 100 runs of 50 measured weeks. || Horizontal bars of on-time delivery: critical ratio 66%, FIFO and EDD 77%, MDD at the welder only 90%, MDD at all work centres 93% and SPT 94%. ||

TABLE Lead time and lateness by dispatching rule, push release.
| Rule | Mean lead time (working days) | 95th-percentile lead time (days) | Mean tardiness per order (days) | Lateness of the worst 1% (days) | Orders more than 20 days late, per year |
| FIFO | 5.7 | 14.1 | 0.9 | 11.5 | 0.1 |
| EDD | 5.8 | 14.1 | 0.9 | 11.6 | 0.1 |
| Critical ratio | 6.2 | 12.6 | 0.8 | 8.7 | 0.5 |
| SPT | 3.6 | 9.1 | 0.5 | 12.2 | 3.2 |
| MDD, all work centres | 5.0 | 8.9 | 0.3 | 6.4 | 2.0 |
| MDD at the welder only | 5.0 | 9.4 | 0.3 | 6.1 | 2.0 |

Table 4 and Figure 2 give four findings:

- **EDD and FIFO are statistically identical here** (difference −0.04 ± 0.26 points). That is a property of this plant, not of EDD in general: promise dates depend only on the number of operations, so within a product type EDD ranks orders much as FIFO does. Planners who sort an ERP dispatch list by due date under such a rule gain little.
- **Critical ratio is the worst rule tested,** 10.5 ± 0.7 points below FIFO. Because the promise ignores order size, a large order has the least time per hour of remaining work, so it gets the lowest ratio and jumps the welder queue while many small orders miss. Published results on CR are mixed, and Baker and Kanet found modified due date rules better on tardiness [@bk]; CR's failure here reflects the size-blind promise.
- **SPT and MDD lead on the count.** SPT ships 0.9 ± 0.6 points more orders on time than MDD and cuts mean lead time by a third. MDD keeps the worst 1% of orders about half as late as FIFO or SPT.
- **The bottleneck carries most of the benefit.** MDD at the welder only, with FIFO everywhere else, adds 12.8 ± 1.9 points over FIFO. Using it at every work centre adds another 3.2 ± 0.5.

### 5.1 The price: a few very large orders

The high-performing rules buy their on-time rate partly at the expense of the largest orders. Under SPT and MDD, about two to three orders a year finish more than 20 working days late, and the worst order in a typical year is 37 to 41 days late. Under FIFO, the worst order in a typical year is about 8 days late.

The mechanism is simple. Once a large order is late, MDD ranks it by when it could finish, which is far off because it needs many hours of work. In busy weeks there is always another order close to its due date that can still be saved, so the large order keeps losing its turn. The affected orders are rare, under 0.5% of the total, but they are often a builder's biggest job. Splitting large orders into batches of 20 units did not remove the effect in the simulation.

A lateness cap removes the extremes: once an order is 10 working days late, it goes to the front of the welder queue, and no order waits in the release pool for more than 10 days. Table 5 shows the cost.

TABLE Effect of a lateness cap on the worst orders.
| Option | On time | Orders more than 10 days late, per year | Orders more than 20 days late, per year | Worst order in a typical year (days late) |
| FIFO (ERP default) | 76.7% | 10.7 | 0.1 | 8 |
| MDD at the welder | 89.5% | 4.2 | 2.0 | 38 |
| MDD at the welder, with lateness cap | 84.6% | 12.0 | 0.2 | 15 |
| Load-based release, MDD at the welder | 92.3% | 5.8 | 2.6 | 40 |
| Load-based release, MDD at the welder, with caps | 85.5% | 10.8 | 0.2 | 13 |

The cap gives back 5 to 7 points of on-time delivery and creates more orders that are moderately late. The better answer in practice is to treat these orders as exceptions: review every order more than five days late once a week, and quote large orders by their workload rather than by the routing, since the size-blind ERP promise is what makes them late in the first place [@wein].

## Controlling Release: Drum-Buffer-Rope and Load-Based Release

Holding orders in the office until the welder can absorb them shortens the time orders spend on the floor by about a third. It improves on-time delivery only when the release rule lets smaller orders through first.

Drum-buffer-rope comes from the Theory of Constraints. Its ideas appear in <em>The Goal</em> [@goal]; it was named and formalised later [@race, @sr]. The bottleneck is the drum that sets the pace, a time buffer of work protects it from starving, and a rope ties order release to the drum so that work does not pile up on the floor. Table 6 compares the release options.

TABLE Release options with a buffer of 24 welder hours.
| Release and sequencing | On time | Mean lead time from order entry (days) | Mean time on the shop floor (days) | 95th-percentile lead time (days) |
| Push, FIFO (ERP default) | 76.7% | 5.7 | 5.7 | 14.1 |
| Strict DBR, FIFO | 72.3% | 6.4 | 3.8 | 17.0 |
| Load-based release, FIFO | 92.0% | 4.6 | 3.8 | 9.6 |
| Load-based release, MDD at the welder | 92.3% | 4.8 | 3.9 | 9.3 |

Strict DBR does what its theory promises on the floor: shop-floor time falls from 5.7 to 3.8 days, which means less clutter, less handling damage and faster quality feedback. Customers do not see it, though. The waiting has only moved from the welder queue into the office pool, and on-time delivery falls by 4.4 ± 0.8 points. The workload-control literature reports the same effect: release control can shorten shop-floor time without shortening total lead time [@land, @thurer10].

Load-based release adds one freedom: when the next order is too large to fit under the buffer, a smaller order behind it may go first. That change acts like SPT at the front door and lifts on-time delivery to 92%, even with FIFO on the floor. That is 2.7 ± 0.7 points better than MDD at the welder alone, the best single dispatching change. Adding MDD at the welder on top of load-based release makes no measurable difference to the on-time rate (+0.2 ± 0.4 points) and trims the worst 1% slightly. The gate does the work, and it shares SPT's weakness: the largest orders wait longest in the pool, as the literature warns [@thurer10]. Sequencing the pool by planned release date is the literature's remedy [@thurer15].

### 6.1 How big should the buffer be?

A buffer that is too small starves the welder (Figure 3): at 8 welder hours, one day of work, on-time delivery collapses under both release rules, because the welder sits idle while orders wait in the office. The load-based rule is on a flat top of 92% between 20 and 28 hours, about three days of welder work; the differences inside that range are within simulation noise. Larger buffers slowly hand back both the on-time gain and the shop-floor gain. As a starting rule, the buffer can be set at about three days of bottleneck work, then tuned by watching whether the bottleneck ever runs out of work.

FIG fig3-buffer-sweep || On-time delivery against buffer size for strict DBR and load-based release, with the ERP default for comparison; 100 runs per buffer size. || Two lines against buffer size from 8 to 64 welder hours: load-based release rises from 66% to a flat top of 92% between 20 and 28 hours, then eases to 90%; strict DBR rises from 24% to 77%; a dashed ERP default line sits at 77%. ||

## Stress Tests: An Order Spike and a Welder Breakdown

Load-based release with MDD at the welder absorbs disruptions with a quarter to a third of the extra late orders of the ERP-style plan.

Two disruptions were added in week 20 of each run: a four-week spike in which orders arrive 40% faster, typical of a spring building season, and a separate two-day welder breakdown. Table 7 counts late orders among those entered in the ten weeks from week 20, averaged over 100 runs, with 95% confidence intervals on the difference.

TABLE Late orders after a disruption.
| Scenario | Late orders, ERP default (push, FIFO) | Late orders, load-based release with MDD at the welder | Extra late orders caused by the event: ERP default vs recommended |
| No disruption | 32.6 | 9.7 | — |
| Two-day welder breakdown | 39.3 | 11.2 | +6.7 vs +1.5 (difference 5.2 ± 2.6) |
| Four-week order spike (+40%) | 65.5 | 20.7 | +32.8 vs +11.0 (difference 21.8 ± 4.8) |

FIG fig4-spike-weekly || Weekly on-time delivery by week of order entry through a four-week order spike, ERP default against load-based release (24 welder hours) with MDD at the welder; mean of 100 runs. || Two weekly lines through a shaded four-week spike starting in week 20: the ERP default falls from about 80% to 39% and is still near 66% nine weeks later; the recommended rules dip to about 83% and recover to 90% by week 33. ||

The spike shows the difference most clearly (Figure 4). Under the ERP default, on-time delivery falls from about 80% to 39% for orders entered in the week after the spike ends, and is still near 66% nine weeks later: every new order joins the back of a long welder queue. Under the recommended rules, it bottoms out near 83% and is back at 90% by week 33, against a normal level of about 92%. MDD pulls short, recoverable orders through first, and the load-based gate keeps the floor from flooding.

## Implementation Guide for SMEs

A plant can apply these results in five steps over about two months, using its existing ERP data and a spreadsheet; scheduling software is optional.

1. **Find the real bottleneck (weeks 1 to 2).** Compare each work centre's planned hours with its available hours over the last three months, then walk the floor: the bottleneck is where work waits. It is not always the most expensive machine, and it can move with the product mix.
2. **Change the bottleneck's sequence (week 3).** Replace FIFO or the ERP due-date sort at the bottleneck with modified due date. In a spreadsheet: for each waiting order, take the later of its due date and today plus its remaining hours converted to days; run the earliest first. Leave other work centres on FIFO.
3. **Gate the release (weeks 4 to 6).** Keep new orders in an office pool. Each morning, release orders until the bottleneck work on the floor reaches about three days. Allow a smaller order to go ahead of a large one that does not fit. CONWIP, a simple cap on the number of orders on the floor, is a workable alternative where bottleneck hours are hard to estimate [@conwip].
4. **Manage the large late orders by exception (from week 4).** Once a week, review every order more than five days late and decide how to recover it: expedite it, split it or renegotiate the date. An automatic cap also works but, in the simulation, costs 5 to 7 points of on-time delivery.
5. **Quote from the queue and the workload, not the routing (weeks 6 to 8).** Replace fixed ERP lead times with the current bottleneck backlog plus the order's own work content and a margin. When the queue is long or the order is large, quote longer; customers prefer an honest date to a missed one. Due-date setting can matter as much as sequencing [@wein].

### 8.1 What to measure

Table 8 lists the five measures that show whether the new rules are working.

TABLE Measures to track.
| Measure | Why it matters | Target direction |
| On-time delivery to promised date | What customers feel | Up, toward 90% to 95% |
| Bottleneck idle hours with work in the plant | A starved bottleneck means the buffer is too small | Near zero |
| Hours of bottleneck work on the floor | The rope; it shows whether release is controlled | Inside the buffer band |
| Lateness of the worst 5% of orders | Catches rules that starve large orders | Down |
| Shop-floor lead time | Shows clutter and work in progress | Down |

### 8.2 Pitfalls

- **Expediting around the rules.** A hot list that jumps the bottleneck queue every day undoes any rule. Real priorities belong in the due dates instead.
- **Gating orders that skip the bottleneck.** Entry doors in this plant never touch the welder; holding them back only makes them late.
- **Running the bottleneck below capacity to protect a schedule.** Lost bottleneck hours are lost plant output. Breaks and shift changes at the bottleneck should be covered first.
- **Trusting a packaged rule untested.** Critical ratio performed worst in this plant, where promise dates ignore order size. Any rule should be tested against the plant's own order history first.
- **Watching only the average.** SPT, MDD and load-based release all raise the on-time rate while leaving a few large orders weeks late. The worst orders need tracking, not just the percentage.
- **Ignoring load.** Dispatching rules redistribute waiting; they cannot remove it. Above about 90% bottleneck load, every rule's worst orders run weeks late, and the answer is more capacity, fewer orders accepted or longer quotes. Figure 1 shows how fast lead times climb.

## Conclusions

The ERP schedule fails on the shop floor because it plans fixed lead times while real lead times are queues, and the queue at one bottleneck decides most due dates.

- In the simulated windows-and-doors plant at 82% bottleneck load, the ERP-style plan shipped 77% of orders on time, although its average planned lead time was longer than the average actual lead time. The misses come from the spread: the slowest 5% of orders took 14 days or more against a promise of about 8.
- Sorting by due date (EDD) did exactly as well as first-come, first-served in this plant, and critical ratio did markedly worse.
- Modified due date at the welder alone raised on-time delivery to 90%. Load-based release with a buffer of about three days of welder work reached 92% and cut shop-floor lead time by 31%.
- Release control by itself is not enough. Strict due-date release shortened shop-floor time but lowered on-time delivery; the gain comes from letting smaller orders through first, at the gate or at the bottleneck.
- The size-aware rules leave about two very large orders a year more than 20 days late. Capping lateness removes them at a cost of 5 to 7 points of on-time delivery; managing them by exception and quoting large orders realistically is the better fix.
- The recommended rules cut the extra late orders caused by a four-week spike by two thirds, and those caused by a two-day breakdown by three quarters.

The results come from one composite plant, and the levels will differ elsewhere. The model leaves out sequence-dependent setups at the welder (profile and colour changes), bottlenecks that shift with the product mix, and the finite-capacity planning software that many vendors sell. It also shows how much of the problem comes from clumped order arrivals: with orders arriving one at a time, FIFO alone reaches about 91% on time. The direction of the findings agrees with decades of simulation research [@ramasesh, @bk]: find the bottleneck, sequence it with a rule that respects both due dates and job size, release work at the pace the bottleneck can absorb, and watch the largest orders. A plant can test all of it on its own data with the code in the Appendix before changing anything on the floor.

## Appendix: Python Code

The compact model below reproduces the paper's main results exactly with the same 100 random seeds: FIFO 76.7% on time, critical ratio 66.3%, MDD at the welder only 89.5%, and load-based release with MDD at the welder 92.3%. It runs in about 12 seconds. Individual sets of 20 seeds vary by several points (FIFO ranges from about 72% to 79%), which is why the paper uses 100.

CODE appendix || Compact finite-capacity job-shop simulation with FIFO, critical ratio, MDD and load-based release (Python 3 with NumPy).
"""
