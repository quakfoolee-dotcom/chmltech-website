"""Chmltech Online Journal, Vol. 106, Issue 6: Quoting Lead Times You Can Keep: Due-Date Setting for Make-to-Order Manufacturers (Nov 17 2026).

Composite case (single-shift vinyl windows-and-doors plant, Lower Mainland), the plant of Vol. 106(4). Model:
content/journal/ops/models/quote/ (job-shop simulation with a quote hook, 100 runs of 50 measured weeks per setting).
Red-team checked (model audit and references) before publication."""

SLUG = "quoting-lead-times-you-can-keep-due-date-setting-for-make-to-order-manufacturers"
META = dict(
    volume=106, issue=6,
    title='Quoting Lead Times You Can Keep: Due-Date Setting for Make-to-Order Manufacturers',
    short_title='Due-Date Quoting for Make-to-Order Manufacturers',
    meta='Quotes built from the bottleneck backlog keep 95% of delivery promises with lead times 38% shorter than fixed ERP lead times, in a plant simulation.',
    keywords=['due-date quoting', 'lead time', 'make-to-order', 'order promising', 'workload control', 'discrete-event simulation', 'high-mix manufacturing', 'ERP'],
)
ABSTRACT = "Most make-to-order SMEs quote delivery dates from fixed ERP lead times: a set number of days per operation, the same for a two-unit order as for a fifty-unit order, and the same in a quiet week as in a rush. This paper tests better quoting rules on the windows-and-doors plant from the Chmltech scheduling paper, where the ERP rule keeps 77% of promises. To keep 95% of promises with a fixed rule, the plant must quote 13.7 working days on average. A quote built from the current welder backlog plus the order's own planned work keeps 95% of promises with an average quote of 8.5 days, 38% shorter, because it quotes long only when the shop is busy or the order is large. With the scheduling rules from the earlier paper, a lead-time formula fitted to the plant's own history quotes 7.3 days on average for 95% on time: shorter quotes than today's 7.9 days, and far more of them kept. Backlog-based quotes also hold their service level through a four-week order spike (95% against 85% for the fixed routing rule with first-in, first-out dispatch) and across welder loads from 66% to 90%. With first-in, first-out dispatch, backlog-based quotes leave no order more than 10 days late, whereas load-based release with due-date sequencing leaves one or two very late orders a year, mostly large orders held back at release."

REFS = {
    'bb81': ('Baker, K. R., &amp; Bertrand, J. W. M. (1981). A comparison of due-date selection rules. <em>AIIE Transactions</em>, 13(2), 123–131.',
        'https://doi.org/10.1080/05695558108974544'),
    'bk': ('Baker, K. R., &amp; Kanet, J. J. (1983). Job shop scheduling with modified due dates. <em>Journal of Operations Management</em>, 4(1), 11–22.',
        'https://doi.org/10.1016/0272-6963(83)90022-0'),
    'cg': ('Cheng, T. C. E., &amp; Gupta, M. C. (1989). Survey of scheduling research involving due date determination decisions. <em>European Journal of Operational Research</em>, 38(2), 156–166.',
        'https://doi.org/10.1016/0377-2217(89)90100-8'),
    'hrs': ('Hopp, W. J., &amp; Roof Sturgis, M. L. (2000). Quoting manufacturing due dates subject to a service level constraint. <em>IIE Transactions</em>, 32(9), 771–784.',
        'https://doi.org/10.1080/07408170008967437'),
    'hopp': ('Hopp, W. J., &amp; Spearman, M. L. (2008). <em>Factory physics</em> (3rd ed.). McGraw-Hill/Irwin.',
        'https://search.worldcat.org/search?q=Hopp+Spearman+Factory+Physics+3rd+edition'),
    'kt': ('Keskinocak, P., &amp; Tayur, S. (2004). Due date management policies. In D. Simchi-Levi, S. D. Wu, &amp; Z.-J. Shen (Eds.), <em>Handbook of quantitative supply chain analysis</em> (pp. 485–554). Springer.',
        'https://doi.org/10.1007/978-1-4020-7953-5_12'),
    'q2c': ('Lee, Q. F. (2026). The quote-to-cash process in manufacturing (Part 1 of the quote-to-cash series). <em>Chmltech Insights</em>.',
        'https://www.chmltech.com/post/quote-to-cash-process-in-manufacturing.html'),
    'fcs': ('Lee, Q. F. (2026). Why the ERP schedule fails on the shop floor: Finite-capacity scheduling rules for high-mix manufacturers. <em>Chmltech Online Journal</em>, 106(4).',
        'https://www.chmltech.com/post/why-the-erp-schedule-fails-on-the-shop-floor-finite-capacity-scheduling-rules-for-high-mix-manufacturers.html'),
    'rm': ('Ragatz, G. L., &amp; Mabert, V. A. (1984). A simulation analysis of due date assignment rules. <em>Journal of Operations Management</em>, 5(1), 27–39.',
        'https://doi.org/10.1016/0272-6963(84)90005-6'),
    'thurer13': ('Thürer, M., Stevenson, M., Silva, C., &amp; Land, M. J. (2013). Towards an integrated workload control (WLC) concept: The performance of due date setting rules in job shops with contingent orders. <em>International Journal of Production Research</em>, 51(15), 4502–4516.',
        'https://doi.org/10.1080/00207543.2013.774485'),
    'vig': ('Vig, M. M., &amp; Dooley, K. J. (1991). Dynamic rules for due-date assignment. <em>International Journal of Production Research</em>, 29(7), 1361–1377.',
        'https://doi.org/10.1080/00207549108948016'),
    'wein': ('Wein, L. M. (1991). Due-date setting and priority sequencing in a multiclass M/G/1 queue. <em>Management Science</em>, 37(7), 834–850.',
        'https://doi.org/10.1287/mnsc.37.7.834'),
}

CODE = {"appendix": open(__file__.replace("paper_v106_i6.py", "models/quote/quote_appendix.py"), encoding="utf-8").read().rstrip()}

DOWNLOADS = [  # served from assets/journal/code/ (V5.42)
    dict(file='quote_appendix.py', label='Appendix script', note='Compact due-date quoting model (Python 3, NumPy)'),
    dict(file='chmltech-due-date-quoting-model.zip', label='Full model', note='Job-shop simulation, regression fit, margin sweeps and stress tests, README'),
]

BODY = r"""
## Introduction

The delivery date quoted at order entry is the first promise a manufacturer makes, and most SMEs set it with a rule that ignores the state of the shop. The Chmltech scheduling paper [@fcs] showed why: an ERP system plans a fixed lead time per operation, while real lead times are mostly queue time at the bottleneck, which grows sharply as the bottleneck fills [@hopp]. That paper fixed the shop-floor side with dispatch and release rules. This paper fixes the promise.

Due-date setting has a long research record. Early simulation studies compared constant allowances, allowances based on an order's work content and allowances based on the shop's current load [@bb81, @rm, @cg], and rules that use information about the current state of the shop generally set more reliable due dates [@rm]. Later work showed how to quote the shortest lead times that still meet a service target [@wein, @hrs], and how due-date setting fits with order release [@thurer13]. The findings have reached few SME quoting desks, where the lead time printed on a quote is still usually a number from the item master.

This paper asks three practical questions:

- How much shorter can quotes be, for the same on-time delivery, if they use the current backlog and the order's size?
- Does better quoting still matter once the shop floor uses better scheduling rules?
- Do backlog-based quotes stay reliable when demand spikes or the plant gets busier?

Quoting sits between the order entry and production steps of the quote-to-cash process described in the Chmltech quote-to-cash series [@q2c].

## The Quoting Rules Tested

Five rules are tested, from the fixed ERP lead time to a formula fitted to the plant's own history; each has one margin, m, that the plant sets to reach its on-time target. Every rule uses only what is known when the order is entered: its routing, its planned hours from the ERP routing, and the current backlog of planned work at the bottleneck (Table 1).

TABLE Quoting rules tested.
| Rule | Quoted lead time (working days) | What it knows |
| Routing (ERP default) | operations + m | Number of operations |
| Flat | m, the same for every order | Nothing |
| Routing plus backlog | operations + m + backlog ÷ 8 | Number of operations; bottleneck backlog |
| Backlog plus work | (backlog + own planned hours) ÷ 8 + m | Bottleneck backlog; order size and routing |
| Fitted | regression prediction + m | All of the above, weighted by the plant's history |

The backlog is the planned welder hours of every order already in the plant that has not yet been welded, divided by 8 hours a day for a single-shift welder. The backlog-plus-work rule is the simplest version of a queue-based quote, written as Eq. (1):

TEX \text{Quote}_j = \frac{B_t + W_j}{h} + m

Here Bₜ is the welder backlog in planned hours when order j is entered, Wⱼ is the order's own planned hours across all its operations, h is the working hours per day (8), and m is the margin in days. It needs two numbers most ERP systems already hold: open work orders and routing hours. Margins can be negative: the routing-plus-backlog rule reaches 95% with m of about −1.3 days, because its operations count already includes a day per operation.

The fitted rule regresses actual lead time on the backlog, the order's planned welder hours, its total planned hours and its number of operations, using 50 simulated years of order history that are not used for testing. This mirrors the statistical approach of Hopp and Roof Sturgis [@hrs], simplified to an ordinary least-squares line plus a margin. With first-in, first-out dispatch, the four inputs explain 80% of the variation in actual lead time; the number of operations alone, which is all the ERP rule uses, explains 6%.

## The Case and Simulation Method

The plant and the simulation are those of the Chmltech scheduling paper [@fcs]: a composite single-shift vinyl windows-and-doors plant in the Lower Mainland taking about 620 orders a year, with one four-head welder loaded to 82%. Orders arrive in clumps, most are small and a few are large, and entry doors skip the welder. With the ERP routing rule (operations + 2 days), the plant quotes 7.9 days on average and keeps 76.7% of its promises with first-in, first-out (FIFO) dispatch, reproducing the earlier paper exactly.

Each quoting rule is tested with two shop-floor policies from that paper:

- **FIFO:** orders released as entered, every work centre first-in, first-out. Here the quote affects only the promise, not the sequence.
- **Recommended:** load-based release with a buffer of 24 welder hours, and modified due date (MDD) sequencing at the welder. Here the quote also sets each order's priority, so quoting and scheduling interact.

Each configuration runs 100 times with the same seeds as the scheduling paper: a 10-week warm-up, 50 measured weeks and 8 weeks to clear the last orders. The margin m of each rule is swept to trace a curve of on-time delivery against average quoted lead time. Rules are compared at the quote each needs to reach 90% and 95% on time, interpolated between swept margins. The margins that reach 95% in the base case are then held fixed for the stress tests. Near the 95% target, 95% confidence intervals on on-time delivery are ±0.3 to ±0.7 points for the backlog-based rules and about ±1.7 to ±1.9 points for the fixed rules with FIFO: a fixed quote's service level swings more from year to year.

## Results: Shorter Quotes, More Promises Kept

Rules that know the backlog keep 95% of promises with average quotes 38% shorter than fixed rules: 8.5 working days instead of 13.7 (Figure 1, Table 2).

FIG fig1-quote-tradeoff || On-time delivery against average quoted lead time for five quoting rules, FIFO dispatch. Each point is the mean of 100 simulated years at one margin. || Five curves of on-time delivery against average quote from 4 to 17 days: the three rules that use the welder backlog reach 95% near 8.5 days, while the routing and flat rules need about 13.7 to 13.9 days; today's routing rule sits at 7.9 days and 76.7% on time. ||

TABLE Average quoted lead time (working days) each rule needs to reach 90% and 95% on time.
| Quoting rule | FIFO dispatch: 90% on time | FIFO dispatch: 95% on time | Recommended scheduling: 90% on time | Recommended scheduling: 95% on time |
| Routing (ERP default) | 11.2 | 13.7 | 7.4 | 8.9 |
| Flat | 11.4 | 13.9 | 7.8 | 9.4 |
| Routing plus backlog | 7.9 | 8.6 | 7.4 | 8.4 |
| Backlog plus work | 7.8 | 8.5 | 7.0 | 8.0 |
| Fitted | 7.8 | 8.6 | 6.3 | 7.3 |

Table 2 gives the average quoted lead time, in working days, each rule needs to reach 90% or 95% on time. Today the plant quotes 7.9 days and keeps 77% of promises.

Three findings stand out:

- **A fixed quote buys reliability with time.** To move from 77% to 95% on time with the routing rule, the plant must add almost six days to every quote. The flat rule is no better: once every order gets the same allowance, the order's routing adds almost nothing.
- **Knowing the backlog is what matters.** Adding the welder backlog to the routing rule does nearly all the work: 8.6 days for 95% against 13.7. The backlog tells the quoting desk what the routing cannot: how long the order will wait at the welder. Orders spend 75% of their time waiting, about two-thirds of it in front of the welder [@fcs].
- **Quotes vary, as they should.** With FIFO, the backlog-plus-work rule's quotes run from 4.4 days or less for the shortest 10% (small orders in quiet weeks) to 13.2 days or more for the longest 10%, with a median of 7.4 days; the routing rule set for 95% quotes 12.9 to 14.9 days whatever the shop's state. Its average is lower because most orders arrive when the shop is not at its busiest.

The fitted rule adds little over the simple backlog-plus-work rule with FIFO dispatch, because the simple rule already captures the queue. Its advantage appears with due-date dispatch, in Section 5.

## Quoting and Scheduling Together

Better scheduling and better quoting each close most of the gap on their own, but they leave different orders late, and that difference decides which combination to choose (Table 3).

With the recommended scheduling rules, even the fixed routing rule reaches 95% on time at 8.9 days, because the welder queue is shorter and better ordered. The fitted rule then cuts the average quote to 7.3 days. That is shorter than the 7.9 days the plant quotes today, with 95% of promises kept instead of 77%. With due-date dispatch the fitted rule earns its keep: MDD changes which orders wait, so a simple backlog count predicts lead time less well (the four inputs explain 36% of the variation, or about 53% if the few orders held back at release are excluded, against 80% under FIFO), and a formula fitted to the plant's own history does better. The formula was fitted to history under today's ERP quotes; a plant adopting it should refit after the first few months under the new quotes.

The average hides the tail. With load-based release, an order too large to fit under the welder buffer waits in the release pool while smaller orders go ahead of it; modified due-date sequencing [@bk] then puts it behind orders that can still be saved. Every order more than 10 days late under the recommended scheduling spent more than half of its lateness waiting for release (the scheduling paper attributed the tail mainly to MDD [@fcs]; holding at release is the larger cause). With MDD at the welder but no release gate, orders more than 20 days late fall from 1.7 to 0.5 a year:

TABLE Late orders and large orders at 95% on time, by quoting and scheduling option.
| Option at 95% on time | Average quote (working days) | Orders more than 10 days late, per year | Orders more than 20 days late, per year | Worst order in a typical year (days late) | Large orders on time |
| FIFO, routing rule | 13.7 | 1.1 | 0 | 1.5 | 93% |
| FIFO, backlog plus work | 8.5 | 0 | 0 | 2.9 | 98% |
| Recommended scheduling, routing rule | 8.9 | 5.2 | 2.4 | 28 | 74% |
| Recommended scheduling, backlog plus work | 8.0 | 3.2 | 1.6 | 24 | 84% |
| Recommended scheduling, fitted | 7.3 | 3.4 | 1.7 | 22 | 85% |

Large orders are those with 24 or more planned hours of work, about 10% of orders; their on-time rates come from 50 simulated years, the other columns from 100. The typical year is the median of 100 simulated years. The average of each year's worst order is higher, 33 to 39 days late under the recommended scheduling, and in the worst simulated year one large order waited about six months for release.

FIFO with backlog-plus-work quotes is the only option with no order more than 10 days late. It quotes large orders longer (11.1 days on average, against 7.5 for orders under 8 planned hours and 8.0 for all others) and then keeps those quotes, because FIFO serves orders in the sequence their quotes assumed. Load-based release with due-date sequencing quotes shorter on average but breaks a few big promises badly.

The choice is a business one:

- **Shortest quotes:** recommended scheduling with fitted quotes, plus a weekly review that covers orders still waiting for release as well as orders on the floor, and releases any order once its due date minus its planned work is reached.
- **Simplest and fairest:** FIFO with backlog-plus-work quotes. It needs no change on the shop floor, one formula at the quoting desk, and quotes about 1.2 days longer on average (8.5 against 7.3).

For a plant whose largest orders come from its largest customers, the second option may be worth the extra 1.2 days.

## Stress Tests: An Order Spike and a Busier Plant

A backlog-based quote stays honest when the shop's load changes, because it lengthens as the queue grows; a fixed quote set for 95% in an average week does not. Each rule's margin was held at its 95% setting from Section 4.

In the first test, orders arrive 40% faster for four weeks from week 20, as in a spring building season. Across orders entered in weeks 20 to 29, the FIFO routing rule kept 84.7% (±4.7) of its promises and the FIFO backlog-plus-work rule 95.2% (±1.1). With the recommended scheduling, the routing rule kept 91.5% (±1.6), backlog plus work 95.0% (±0.6) and the fitted rule 94.1% (±0.8).

FIG fig2-spike-weekly || Weekly on-time delivery (top) and average quoted lead time (bottom) by week of order entry, FIFO dispatch, with orders arriving 40% faster in weeks 20 to 23; margins fixed at their 95% settings, 100 simulated years. || Two panels through a shaded four-week spike: the routing rule's quote stays at 13.7 days while its on-time rate falls to 73% for orders entered in week 24; the backlog-plus-work quote rises from about 8.3 to 13.9 days and its on-time rate stays near 95%. ||

The backlog-plus-work rule did not avoid the spike; it told customers about it. Its average quote rose from about 8.3 days to 13.9 days for orders entered in the first week after the spike, and eased back over the following weeks, while the fixed quote stayed at 13.7 days and kept as few as 73% of promises for orders entered that week (Figure 2). In that week both rules quoted almost three weeks on average, but the backlog-based quote kept 95% of its promises against 73%, because it gave the long dates to the orders at the back of the queue rather than to everyone.

In the second test, order volume was changed for a whole year, moving the welder's load from 66% to 90% without re-tuning any margin (Table 4).

TABLE On-time delivery as the welder's load changes, with margins fixed at their 95% settings.
| Welder load | Routing rule: on time | Backlog plus work: on time | Backlog plus work: average quote (days) |
| 66% | 99.5% | 96.4% | 6.7 |
| 73% | 98.8% | 95.8% | 7.2 |
| 78% | 97.1% | 95.2% | 7.9 |
| 82% | 95.0% | 95.0% | 8.5 |
| 86% | 91.4% | 94.8% | 9.5 |
| 90% | 85.8% | 94.2% | 10.8 |

Both rules use FIFO dispatch; the routing rule quotes 13.7 days at every load. At low load the fixed quote is needlessly long, at 13.7 days against 6.7, and at high load it misses one promise in seven. The backlog-based rule holds 94% to 96% on time across the whole range by adjusting its quotes, so its margin needs re-tuning only when the product mix or routing changes, not with every swing in demand [@vig].

## Implementation Guide for SMEs

A plant can set up backlog-based quotes within a few weeks, with an ERP open-orders report and a spreadsheet.

1. **Confirm the bottleneck.** Use the method in the scheduling paper: compare planned and available hours by work centre, and walk the floor to see where work waits.
2. **Compute the backlog each morning.** From the open work orders, add the planned bottleneck hours of every order not yet past the bottleneck. Divide by the bottleneck's working hours per day. This one number is the heart of the quote.
3. **Quote with Eq. (1).** Quote = (backlog hours + the order's planned hours) ÷ hours per day + margin, rounded up to whole working days, plus shipping days. Start with a margin of 3 days, the value that gave 95% on time in this case with FIFO dispatch, or 2.5 days if quotes are rounded up to whole days.
4. **Tune the margin monthly.** Compare the last three months' promises with actual completions; a single month of about 50 orders is too noisy to act on. If on-time is below 92%, add half a day; if it is above 98%, take half a day off. Change the margin, not the formula, when demand moves.
5. **Fit the formula after six to twelve months.** With enough history, regress actual lead time on the backlog, the order's planned bottleneck hours, its total planned hours and its number of operations (Excel's LINEST works), and quote the prediction plus a margin. This matters most if the shop uses due-date dispatch rules.

### 7.1 A worked quote

On a busy Tuesday morning the open-orders report shows 38 planned welder hours on orders not yet welded. A builder asks for 12 casement windows whose routing adds up to 9 planned hours across all operations. With the 3-day margin, Eq. (1) gives (38 + 9) ÷ 8 + 3 = 8.9, so the quote is 9 working days, plus shipping. The same order entered on a quiet Monday, with 12 hours of welder backlog, would be quoted (12 + 9) ÷ 8 + 3 = 5.6, or 6 working days. The ERP routing rule would quote both orders the same number of days, whatever the queue in front of the welder. Over a year these differences are what let the backlog rule keep 95% of promises with shorter quotes on average: it quotes long when the queue is long and short when it is not, and it quotes large orders longer than small ones, so the long quotes go to the orders that will actually wait.

### 7.2 Pitfalls

- **A stale backlog.** A backlog updated weekly misses the rush that matters. Update it daily, or automatically from the ERP.
- **Sales overrides.** A quote shortened to win an order is a promise the shop has not agreed to. Shorten it only by changing the order's priority, and count it against the margin.
- **Planned hours that are wrong.** The quote is only as good as the routing hours. Compare planned with actual hours for the bottleneck quarterly.
- **Calendar and working days mixed.** Quote in working days, then convert to a calendar date with the plant's shift calendar and holidays.
- **Long quotes lose orders.** This study assumes customers accept every quote. In practice some walk away from a long one; a plant that quotes long in a rush should decide which orders it most wants to keep, and may need overtime rather than a longer quote [@kt].

## Conclusions

A quote built from the current bottleneck backlog and the order's own work keeps more promises with shorter quotes than any fixed lead time.

- In the simulated plant, the ERP routing rule kept 77% of promises at 7.9 days. Reaching 95% with a fixed rule took 13.7 days on average; the backlog-plus-work rule needed 8.5.
- Combined with the scheduling paper's rules, a quoting formula fitted to the plant's history reached 95% on time with an average quote of 7.3 days, shorter than today's quotes.
- With FIFO dispatch, backlog-plus-work quotes left no order more than 10 days late; load-based release with due-date sequencing quoted shorter but left one or two orders a year more than 20 days late, mostly large orders held back at release.
- Backlog-based quotes held window averages of 94% to 96% on time through a four-week order spike and at welder loads from 66% to 90%, without re-tuning, by lengthening quotes when the shop was busy.

The case is a composite. The model assumes customers accept every quote, that planned routing hours are unbiased, and that the bottleneck stays at the welder. As in the scheduling paper, the shop-floor rules (MDD and the release gate) use actual processing times, which a real plant would only know as planned hours. A plant can test the rules on its own order history with the code in the Appendix before changing a single quote.

## Appendix: Python Code

The script below reproduces the paper's base results exactly with the scheduling paper's 100 seeds: the ERP routing rule keeps 76.7% of promises at 7.86 days; set for 95% it quotes 13.73 days; the backlog-plus-work rule keeps 95.0% at 8.55 days with FIFO, and 95.0% at 7.96 days with MDD at the welder and load-based release. It needs Python 3 and NumPy and runs in about 15 seconds. The full model, with the regression fit, the margin sweeps and the stress tests, can be downloaded from this paper's page.

CODE appendix || Compact due-date quoting model on the windows-and-doors job shop: routing and backlog-plus-work quotes with FIFO or load-based release and MDD (Python 3 with NumPy).
"""
