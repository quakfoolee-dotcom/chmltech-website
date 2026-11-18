"""Chmltech Online Journal, Vol. 106, Issue 5: Beyond the Unit Price: Total Landed Cost Optimization for SME Sourcing (Nov 17 2026).

Composite case (BC windows-and-doors plant, eight purchased parts). Model: content/journal/ops/models/tlc/ (mixed-integer
program with PuLP 2.9 + CBC; Monte Carlo risk layer, 20,000 years). Red-team checked (model audit and references) before publication."""

SLUG = "beyond-the-unit-price-total-landed-cost-optimization-for-sme-sourcing"
META = dict(
    volume=106, issue=5,
    title='Beyond the Unit Price: Total Landed Cost Optimization for SME Sourcing',
    short_title='Total Landed Cost Optimization for SME Sourcing',
    meta='A sourcing model for SMEs that compares suppliers on total landed cost, not unit price, and finds the lowest-cost plan cuts annual cost by 9%.',
    keywords=['total landed cost', 'supplier selection', 'sourcing', 'mixed-integer programming', 'tariffs and surtaxes', 'ocean freight', 'dual sourcing', 'Monte Carlo simulation'],
)
ABSTRACT = 'Lowest price, highest cost: buying from the supplier with the lowest unit price, or the lowest price plus freight, leaves money on the table for small and mid-sized manufacturers. Duties and surtaxes, inventory in transit, safety stock for long and variable lead times, quality losses, payment terms and the cost of managing each supplier region all sit outside the invoice. This paper builds a total landed cost model for a composite British Columbia windows-and-doors manufacturer that buys eight parts from China, Mexico, the United States or Canada. A mixed-integer program chooses the supplier, freight mode and order frequency for each part, with container loads shared across parts. The lowest-price plan sources everything from China and costs C$630,100 a year. The total-cost plan pays C$62,300 more on supplier invoices but costs C$573,600 a year, 9% less: it keeps compact, labour-intensive hardware in China and moves bulky and surtaxed steel and aluminum parts to Canada. A price-plus-freight rule comes within 1.4% of the optimum. A Monte Carlo simulation of freight rates, exchange rates, tariff scenarios and supply disruptions shows the total-cost plan also has the lowest mean cost, and a 95th-percentile cost C$106,600 below the lowest-price plan. Without surtaxes the chosen plan is the same but the saving falls to 3.5%. A second supplier lowers average cost only when a shortage cannot be covered by a spot buy and costs more than about C$190 per part short; for the worst years, buying the hardware in North America protects better.'

REFS = {
    'aissaoui': ('Aissaoui, N., Haouari, M., &amp; Hassini, E. (2007). Supplier selection and order lot sizing modeling: A review. <em>Computers &amp; Operations Research</em>, 34(12), 3516–3540.',
        'https://doi.org/10.1016/j.cor.2006.01.016'),
    'burke': ('Burke, G. J., Carrillo, J. E., &amp; Vakharia, A. J. (2007). Single versus multiple supplier sourcing strategies. <em>European Journal of Operational Research</em>, 182(1), 95–112.',
        'https://doi.org/10.1016/j.ejor.2006.07.007'),
    'cscb': ('Canadian Society of Customs Brokers. (2025). Customs Notice 25-28: Steel Goods and Aluminum Goods Surtax Order.',
        'https://cscb.ca/en/article/customs-notice-25-28-steel-goods-and-aluminum-goods-surtax-order'),
    'degraeve': ('Degraeve, Z., Labro, E., &amp; Roodhooft, F. (2000). An evaluation of vendor selection models from a total cost of ownership perspective. <em>European Journal of Operational Research</em>, 125(1), 34–58.',
        'https://doi.org/10.1016/S0377-2217(99)00199-X'),
    'ellram': ('Ellram, L. M. (1995). Total cost of ownership: An analysis approach for purchasing. <em>International Journal of Physical Distribution &amp; Logistics Management</em>, 25(8), 4–23.',
        'https://doi.org/10.1108/09600039510099928'),
    'ghy': ('GHY International. (2026, November 9). Canada extends US tariff relief for businesses to June 2028; now includes non-steel goods.',
        'https://www.ghy.com/?p=31280'),
    'ho': ('Ho, W., Xu, X., &amp; Dey, P. K. (2010). Multi-criteria decision making approaches for supplier evaluation and selection: A literature review. <em>European Journal of Operational Research</em>, 202(1), 16–24.',
        'https://doi.org/10.1016/j.ejor.2009.05.009'),
    'ss': ('Lee, Q. F. (2026). Beyond the formula: Setting safety stock with Monte Carlo simulation. <em>Chmltech Online Journal</em>, 106(3).',
        'https://www.chmltech.com/post/beyond-the-formula-setting-safety-stock-with-monte-carlo-simulation.html'),
    'fcs': ('Lee, Q. F. (2026). Why the ERP schedule fails on the shop floor: Finite-capacity scheduling rules for high-mix manufacturers. <em>Chmltech Online Journal</em>, 106(4).',
        'https://www.chmltech.com/post/why-the-erp-schedule-fails-on-the-shop-floor-finite-capacity-scheduling-rules-for-high-mix-manufacturers.html'),
    'pulp': ("Mitchell, S., O'Sullivan, M., &amp; Dunning, I. (2011). PuLP: A linear programming toolkit for Python. University of Auckland.",
        'https://optimization-online.org/2011/09/3178/'),
    'osler': ("Osler, Hoskin &amp; Harcourt LLP. (2026, September 10). The trade war tit-for-tat continues: United States responds to Canada's retaliatory surtaxes with new tariffs and import prohibitions.",
        'https://www.osler.com/?p=126523'),
    'platts': ('Platts, K. W., &amp; Song, N. (2010). Overseas sourcing decisions – the total cost of sourcing from China. <em>Supply Chain Management: An International Journal</em>, 15(4), 320–331.',
        'https://doi.org/10.1108/13598541011054689'),
    'gcaptain': ('Schuler, M. (2025, December 11). Container shipping index climbs for second week as Asia-Europe rates surge, transpacific slumps. <em>gCaptain</em>.',
        'https://gcaptain.com/container-shipping-index-climbs-for-second-week-as-asia-europe-rates-surge-transpacific-slumps'),
    'shipuniverse': ('ShipUniverse. (2026, October 29). Drewry container rates fall 3% to $4,429 as U.S. trade routes reverse their rally.',
        'https://www.shipuniverse.com/?p=25814'),
    'silver': ('Silver, E. A., Pyke, D. F., &amp; Thomas, D. J. (2017). <em>Inventory and production management in supply chains</em> (4th ed.). CRC Press.',
        'https://doi.org/10.1201/9781315374406'),
    'tomlin': ('Tomlin, B. (2006). On the value of mitigation and contingency strategies for managing supply chain disruption risks. <em>Management Science</em>, 52(5), 639–657.',
        'https://doi.org/10.1287/mnsc.1060.0515'),
    'weber': ('Weber, C. A., Current, J. R., &amp; Benton, W. C. (1991). Vendor selection criteria and methods. <em>European Journal of Operational Research</em>, 50(1), 2–18.',
        'https://doi.org/10.1016/0377-2217(91)90033-R'),
}

CODE = {"appendix": open(__file__.replace("paper_v106_i5.py", "models/tlc/tlc_appendix.py"), encoding="utf-8").read().rstrip()}

DOWNLOADS = [  # served from assets/journal/code/ (V5.42)
    dict(file='tlc_appendix.py', label='Appendix script', note='Base-case total landed cost model (Python 3, PuLP 2.9)'),
    dict(file='chmltech-landed-cost-model.zip', label='Full model', note='Optimization model, Monte Carlo risk layer, freight and shortage sweeps, README'),
]

BODY = r"""
## Introduction

The supplier with the lowest quote is often not the cheapest supplier once the goods are on the plant floor. Purchasing teams in small and mid-sized enterprises (SMEs) usually compare quotes on unit price, sometimes adding a freight estimate. Much of the cost of buying sits elsewhere: in duties, customs brokerage, inventory on the water, safety stock, rejected parts, deposits paid before shipment and the time spent managing distant suppliers. Ellram's total cost of ownership approach makes these costs visible [@ellram], and studies of offshore sourcing have found that they can erase much of a low-cost country's price advantage [@platts].

Three things make the question sharper for Canadian manufacturers in late 2026:

- **Tariffs depend on origin and end use.** Canada applies a 25% surtax to many Chinese steel and aluminum products, and to goods from other countries made with Chinese-melted steel or Chinese-smelted aluminum, and from September 8, 2026 added surtaxes of 15% to 50% on a wide range of US goods [@osler, @cscb]. On November 9, 2026, Canada extended remission of surtaxes on eligible US goods used in manufacturing or processing to June 30, 2028 [@ghy].
- **Ocean freight is volatile.** Drewry's spot rate for a 40-foot container from Shanghai to Los Angeles was about US$2,100 in December 2025 and US$7,514 on October 29, 2026 [@gcaptain, @shipuniverse].
- **SME volumes rarely fill containers.** A plant that buys a few hundred thousand dollars of parts a year ships less-than-container loads (LCL) at higher rates per cubic metre, unless it consolidates.

This paper shows how an SME can compare suppliers on total landed cost, choose suppliers and freight modes with a small optimization model, and test the choice against freight, currency, tariff and disruption risk. It uses the windows-and-doors plant from the Chmltech scheduling paper [@fcs] as a composite case, and draws on the Chmltech safety stock paper [@ss] for the inventory terms.

## Total Landed Cost

The total landed cost of a part is everything the plant pays, per year, to have that part available on the floor: eight components, of which the invoice shows one. For a part with annual demand D bought from supplier s, shipped by freight mode m in n orders a year, the annual total landed cost is given by Eq. (1):

TEX \begin{aligned} TLC_{s,m,n} = {} & \underbrace{D\,p_s}_{\text{purchase}} + \underbrace{D\,p_s\,\tau_s}_{\text{duty, surtax}} + \underbrace{n\,F_m(D/n) + n\,b_s}_{\text{freight, brokerage}} + \underbrace{q_s D\,(p_s + r)}_{\text{quality}} \\ & + \underbrace{h\,c\,\left(\bar{d}\,\bar{L} + \tfrac{D}{2n} + SS\right)}_{\text{carrying}} + \underbrace{k\,D\,p_s\,t_s}_{\text{payment terms}} + \underbrace{f_s}_{\text{supplier management}} \end{aligned}

Here p is the unit price, τ the duty and surtax rate, F the freight charge for one shipment, b the brokerage fee per import entry, q the defect rate and r the handling cost per defective part, h the carrying rate, c the landed unit cost, d̄ and L̄ mean daily demand and lead time, SS the safety stock, k the cost of capital and t the share-weighted payment timing in years (positive when the plant pays before it receives). The supplier management cost f is paid once per supplier region used, not per part, so in the plan total it is added once for each region rather than in each part's cost. Table 1 shows how each term is set in the case.

TABLE Components of total landed cost and how each is set in the case.
| Component | What it covers | How it is set in the case |
| Purchase | Supplier price, FOB origin (delivered for Canadian suppliers) | Quotes per part and region |
| Duty and surtax | Most-favoured-nation duty plus any surtax, on the value for duty | By part class and origin; three tariff scenarios |
| Freight | Ocean full-container (FCL) or less-than-container (LCL), air, or truck | Per shipment, from volume and weight |
| Brokerage | Customs entry per shipment | C$180 China, C$90 Mexico and US |
| Quality | Rejected parts: price plus C$15 handling | 1.5% China, 1.0% Mexico, 0.5% US, 0.4% Canada |
| Carrying | Inventory in transit, cycle stock and safety stock, at 25% of landed value a year | Safety stock for 95% cycle service |
| Payment terms | Deposit paid before shipment, or supplier credit after receipt | China 30% deposit 35 days before shipment; others net 30; 10% cost of capital |
| Supplier management | Audits, visits, inspections, purchasing time per region | C$8,000 China, C$5,000 Mexico, C$3,000 US, C$1,500 Canada a year |

Safety stock uses the textbook formula with variable demand and lead time [@silver]. The safety stock paper [@ss] shows that the formula understates protection for disruption-prone imports, so the long-tail risk is handled separately, by Monte Carlo simulation in Section 6. Two costs are often left out of supplier comparisons and matter here: carrying cost rises with lead time and order size, and supplier-level costs such as audits and supplier management do not scale with the number of parts [@degraeve]; here they are charged per supplier region. Lead time is measured from shipment to receipt; for China it excludes production time, which enters through the deposit in the payment-terms term. In-transit stock is carried at the full 25% rate, a conservative choice: at a 10% cost-of-capital rate on stock in transit the plan is unchanged and the saving is C$47,900 (7.8%) rather than C$56,500.

## The Case: Eight Purchased Parts

The plant is the composite windows-and-doors maker from the Chmltech scheduling paper [@fcs]: a single-shift vinyl window and door manufacturer in the Lower Mainland. Its supplier invoices for eight purchased parts range from about C$456,000 a year if everything is bought in China to C$600,000 if everything is bought in Canada. China quotes 13% to 37% below Canadian suppliers; the gap is widest on compact, labour-intensive hardware and narrowest on bulky or steel parts (Table 2). All money is in Canadian dollars at an assumed C$1.38 per US dollar.

TABLE Purchased parts, quantities and unit prices by supplier region (C$).
| Part | Annual quantity | Volume (litres per unit) | Weight (kg per unit) | China | Mexico | US | Canada | China below Canada |
| Casement operator | 6,400 | 1.2 | 0.6 | 9.60 | 12.60 | 14.00 | 14.80 | 35% |
| Multipoint lock | 2,600 | 2.5 | 1.4 | 19.50 | — | 29.50 | 31.00 | 37% |
| Patio door roller set | 1,500 | 0.8 | 0.5 | 7.00 | 9.30 | 10.40 | 10.90 | 36% |
| Entry door handleset | 950 | 4.0 | 1.6 | 22.00 | 29.00 | 33.00 | 35.00 | 37% |
| Steel reinforcement bar | 9,000 | 4.0 | 9.0 | 12.20 | — | 13.40 | 14.00 | 13% |
| Aluminum screen frame kit | 3,300 | 6.0 | 0.9 | 6.80 | 7.50 | 8.20 | 8.60 | 21% |
| Weatherstrip roll | 1,400 | 30 | 6.0 | 44.00 | 48.00 | 53.00 | 56.00 | 21% |
| Warm-edge spacer box | 900 | 40 | 12.0 | 132.00 | — | 150.00 | 158.00 | 16% |

Prices are C$ per unit, FOB origin for imports and delivered for Canadian suppliers, which add a C$60 charge per delivery. Chinese suppliers set minimum order quantities of 200 to 2,000 units per order.

Freight and lead times are set from public benchmarks and typical SME quotes (Table 3). The ocean full-container rate uses Drewry's Shanghai to Los Angeles spot rate of US$7,514 on October 29, 2026, rounded to US$7,500, as a proxy for Vancouver; LCL rates move with it. Air freight is used only as emergency cover during a disruption (Section 6); allowing it in the base model does not change the chosen plan, because it costs far more than ocean freight.

TABLE Freight charges and lead times by origin and mode.
| Origin and mode | Freight charge | Lead time, mean ± SD (calendar days) |
| China, full container (40 ft) | US$7,500 ocean + C$2,200 port, documents and drayage; 58 m³ or 24 t | 45 ± 8 |
| China, less than container | C$450 per shipment + C$160 per revenue tonne (m³ or tonne, whichever is larger) | 55 ± 12 |
| China, air | C$300 per shipment + C$7.50 per chargeable kg | 10 ± 3 |
| Mexico, truck | C$300 per shipment + C$0.45 per kg | 10 ± 3 |
| US, truck | C$180 per shipment + C$0.30 per kg | 6 ± 2 |
| Canada, truck | C$60 per delivery | 3 ± 1 |

Tariffs are modelled as scenarios, because the rate on a given part depends on its tariff classification, the origin of its steel or aluminum, and whether a remission order applies. In the base scenario, Chinese parts pay an illustrative most-favoured-nation duty (5% hardware, 3% aluminum, 6.5% plastic, 0% steel), and the steel reinforcement and aluminum screen kits from China also pay the 25% surtax on Chinese steel and aluminum products under Canada's 2024 China surtax order. US parts are assumed to qualify for manufacturing remission, and Mexican and US parts enter duty-free under CUSMA. Two further scenarios add a 25% surtax on all Chinese parts, or remove all surtaxes. These rates illustrate the method; an importer should confirm the classification and the surtax for each part with a customs broker.

## The Optimization Model

A mixed-integer program picks, for every part, one supplier region, one freight mode and one order frequency, so that the plant's total landed cost is as low as possible. Supplier selection has a long literature [@weber, @ho], and supplier selection with lot sizing is a well-studied problem [@aissaoui]; this version is small enough for a spreadsheet solver or a few lines of Python.

The model enumerates every feasible option for each part: four regions, two ocean freight modes for China (full and less-than-container loads), truck for the other regions, and order frequencies of 1, 2, 3, 4, 6, 8, 12, 26 or 52 orders a year. An option is dropped if a Chinese order would fall below the supplier's minimum order quantity. Each option's annual cost follows Section 2. The decisions and constraints are:

- **One option per part:** a binary variable x for each option, with exactly one chosen per part.
- **Shared containers:** a binary variable y(N) chooses N full containers a year from China (N of 1, 2, 3, 4, 6, 8, 12 or 26). Every part sent by full container then ships N times a year, so the parts share each container. The volume and weight of all those parts must fit in N containers: 58 m³ and 24 tonnes each. Each container costs C$12,550 (US$7,500 × 1.38 + C$2,200).
- **Supplier regions:** a binary variable u(r) is 1 if any part comes from region r, which adds that region's management cost once.

The objective adds the cost of the chosen options, the containers and the regions used. With 8 parts the model has about 260 binary variables and solves in under a second with the free CBC solver through PuLP [@pulp]. Standard Excel Solver is limited to 200 decision variables, enough for about six parts with this many options; larger cases need OpenSolver, Frontline's Premium Solver or the Python appendix.

The model is compared with two rules buyers commonly use:

- **Lowest price:** buy each part from the region with the lowest unit price, ship Chinese parts LCL, and order up to monthly where the minimum order allows.
- **Lowest price plus freight:** buy each part from the region with the lowest unit price plus duty, freight and brokerage per unit, ordering quarterly or as close to it as the minimum order allows. This is the comparison many purchasing teams already make.

## Results: Where the Lowest Price Loses

The total-cost plan costs C$573,600 a year, C$56,500 (9.0%) less than buying every part at the lowest price, even though its supplier invoices are C$62,300 higher. It keeps the four compact hardware parts in China and buys the four bulky or surtaxed parts in Canada (Table 4). Figure 1 shows where the saving comes from.

TABLE Supplier region, freight mode and orders a year for each part under the three rules. || Base scenario, container rate US$7,500.
| Part | Lowest price | Lowest price plus freight | Total landed cost |
| Casement operator | China, LCL, 6 a year | China, LCL, 4 a year | China, LCL, 4 a year |
| Multipoint lock | China, LCL, 4 a year | China, LCL, 4 a year | China, LCL, 3 a year |
| Patio door roller set | China, LCL, 3 a year | China, LCL, 3 a year | China, LCL, 2 a year |
| Entry door handleset | China, LCL, 3 a year | China, LCL, 3 a year | China, LCL, 2 a year |
| Steel reinforcement bar | China, LCL, 4 a year | Canada, truck, 4 a year | Canada, truck, monthly |
| Aluminum screen frame kit | China, LCL, 3 a year | Mexico, truck, 4 a year | Canada, truck, 8 a year |
| Weatherstrip roll | China, LCL, 4 a year | Mexico, truck, 4 a year | Canada, truck, monthly |
| Warm-edge spacer box | China, LCL, 4 a year | China, LCL, 4 a year | Canada, truck, monthly |
| **Annual total landed cost** | **C$630,100** | **C$581,500** | **C$573,600** |

FIG fig1-cost-waterfall || Change in annual total landed cost from the lowest-price plan to the total-cost plan, by component; base scenario, container rate US$7,500. || Waterfall bars from C$630,082 for the lowest-price plan: purchase price up C$62,340, then savings in duty and surtax (C$45,459), freight (C$34,968), carrying cost (C$26,701), quality, payment terms and brokerage, and supplier management up C$1,500, ending at C$573,614 for the total-cost plan. ||

Three costs the invoice does not show decide the result:

- **Duties and surtaxes (C$45,500 saved).** The lowest-price plan pays C$52,600 in duty, of which C$33,100 is the 25% surtax on Chinese steel reinforcement and aluminum screen kits. Steel reinforcement is 13% cheaper from China on the invoice but 9% dearer after the surtax.
- **Freight (C$35,000 saved).** Weatherstrip and spacers ship 30 to 40 litres per unit; at LCL rates their freight adds 6% to 14% to the price. Truck delivery from a Canadian supplier costs C$60 a load.
- **Carrying cost (C$26,700 saved).** A Chinese part shipped LCL has a lead time of about 55 days and needs safety stock for a lead time that varies by ±12 days. A Chinese casement operator ordered quarterly ties up about four months of demand, counting goods on the water; Canadian steel reinforcement delivered monthly ties up about three weeks.

The price-plus-freight rule captures most of the gain: it costs C$581,500, 1.4% above the optimum. It falls short in two ways. It orders quarterly when monthly Canadian deliveries carry less stock, and it spreads parts across three regions, paying C$5,000 a year to manage a Mexican supplier for two parts. Order frequency and the number of supplier regions are the details a per-unit comparison cannot see. The surtax explains most of the size of the gain but not the choice: with no surtaxes at all, the total-cost plan is the same, but the lowest-price plan costs C$594,100, so the saving falls to C$20,500 (3.5%).

### 5.1 Freight rates and full containers

The total-cost plan does not depend much on the freight rate: across container rates from US$1,500 to US$11,000, the re-optimized plan's cost moves by C$10,200 (the plan fixed at today's rate by C$4,300), while the lowest-price plan's moves by C$43,600 (Figure 2).

FIG fig2-freight-sweep || Annual total landed cost against the China 40-foot container rate, with LCL rates scaled with the container rate. || Three lines against container rates from US$1,500 to US$11,000: the lowest-price plan rises from about C$603,000 to C$646,000, while the total-cost plan, re-optimized or fixed at the US$7,500 choice, stays between about C$565,000 and C$575,000. ||

Below US$2,500 to US$3,000 per container, the model switches the China parts to three shared full containers a year, and brings the weatherstrip and spacers back to China. Above that rate, the plant's volume (about 97 m³ a year for the six parts that would share containers) does not fill them often enough. Between about US$3,000 and US$4,500, weatherstrip still comes from China by LCL; above that, LCL for the compact hardware plus Canadian supply for the bulky parts wins. The plan chosen at today's US$7,500 rate costs at most C$6,000 a year more than the re-optimized plan at any rate in the range. A sourcing plan can be set at today's freight rate and reviewed when container rates fall below about US$3,000.

## Risk: Freight, Tariffs and Disruptions

The total-cost plan also holds up under uncertainty: across 20,000 simulated years it has the lowest mean cost, C$580,800, and a 95th-percentile cost within C$500 of the lowest (the all-North-America plan) and C$106,600 below the lowest-price plan (Figure 3).

Each simulated year draws five uncertain inputs and prices a fixed plan against them:

- **Container freight rate:** lognormal, median US$4,500, below the US$7,500 base case to reflect the past year, with 90% of years between about US$2,150 and US$9,450; Drewry's Shanghai to Los Angeles rate ran from about US$2,100 in December 2025 to about US$8,000 in October 2026. LCL rates move in proportion. Centring the distribution on US$7,500 instead raises every plan's cost and widens the total-cost plan's lead.
- **Exchange rate:** C$1.38 ± 0.05 per US dollar, applied to all imported prices.
- **Tariff scenario:** the base case (60% of years), US manufacturing remission ending with a 25% surtax on US parts (20%), or a 25% surtax on all Chinese parts (20%). These weights are stress-test assumptions, not forecasts. No plan here buys from the US, so the remission scenario changes no plan's cost; in effect the test weighs the base case against a broader China surtax.
- **China lane disruption:** a 15% chance each year of a port or shipping disruption that delays Chinese parts by 28 to 56 days.
- **Cover during a disruption:** demand in the delay beyond safety stock is met by the backup supplier if there is one (it can double its normal volume), and otherwise by air freight from China or a Canadian spot buy at a 15% premium, whichever is cheaper.

FIG fig3-risk-scatter || Mean against 95th-percentile annual total landed cost for five sourcing plans, 20,000 simulated years each with the same random inputs. || Scatter of five plans: the total-cost plan has the lowest mean (C$581,000) and a 95th percentile of C$617,000, level with all North America (mean C$604,000) and far below the lowest-price plan (mean C$637,000, 95th percentile C$724,000). ||

The lowest-price plan carries the most risk as well as the highest cost: it is fully exposed to freight rates, to a broader China surtax and to every China disruption. The all-North-America plan (the optimum if every Chinese part paid a 25% surtax) has the narrowest spread but costs C$22,800 a year more on average than the total-cost plan, for about the same 95th-percentile cost. If a 25% surtax were applied to all Chinese parts for a full year, the total-cost plan would cost C$613,000, C$9,400 more than switching to North America; a plant can watch for that signal and re-run the model.

### 6.1 When does a second supplier pay?

Dual sourcing is insurance with a known premium: splitting the four China hardware parts 70/30 with a Mexican or Canadian supplier (the model then also moves screen kits and weatherstrip to Mexico, whose management cost is already paid) costs C$16,300 a year more in the base case, because the second supplier's price is higher and the smaller orders carry more cost per unit [@burke]. In this case the premium buys nothing as long as a delay can be covered by air freight or a domestic spot buy. Its mean cost is C$14,200 higher, and its 95th-percentile cost is C$6,700 higher.

The answer changes when a shortage cannot be covered. With no spot market, every part short costs the plant a shortage cost: lost contribution on a window or door that cannot ship, overtime to catch up, or a penalty. Figure 4 shows how the comparison moves as that cost rises.

FIG fig4-shortage-breakeven || Mean annual total landed cost against the cost per part short, with no spot market or air cover; 10,000 simulated years per point. || Three lines against shortage cost from C$0 to C$300 per part: the single-source total-cost plan rises from C$580,000 to C$605,000, crossing the nearly flat dual-sourced plan near C$190 and the flat all-North-America plan near C$280. ||

Compared with the total-cost plan, the second supplier lowers the 95th-percentile cost once a part short costs more than about C$60, and lowers the mean cost above about C$190. It is not the best protection against a bad year, though: the all-North-America plan has a lower 95th-percentile cost than dual sourcing at every shortage cost, for about C$7,000 to C$9,000 a year more on average. A casement window that cannot ship for want of two operators can lose more than C$190 per operator in contribution and goodwill, so for critical parts without a spot market a second supplier is reasonable insurance, consistent with Tomlin's finding that the best mitigation depends on the backup's cost and responsiveness [@tomlin]; a plant most worried about its worst year should consider moving those parts to North America instead. For parts that distributors stock locally, neither is worth its premium.

## Implementation Guide for SMEs

An SME can move from price comparison to total landed cost in four steps, starting with a spreadsheet and its top 20 to 50 purchased parts by spend.

1. **Build the landed cost sheet.** One row per part and supplier option, with columns for each component in Table 1. Pull annual quantities from the ERP, prices from current quotes, volumes and weights from packing lists, and lead times from purchase order and receipt dates. Get duty and surtax rates per tariff classification from the customs broker, including whether a remission order applies.
2. **Add the inventory terms.** Pipeline stock is daily demand × transit days; cycle stock is half an order; safety stock follows the safety stock paper [@ss]. Multiply by the landed unit cost and the carrying rate. These three columns are where distant suppliers lose most often.
3. **Choose with Solver.** Add a 0/1 cell per option, a constraint that each part's cells sum to 1, a 0/1 cell per supplier region with its management cost, and, if containers are worth testing, a 0/1 cell for each number of containers a year, with volume and weight constraints. Standard Excel Solver (Simplex LP) allows 200 decision cells: about six parts with every option, or more if each part is limited to three or four order frequencies. Beyond that, use OpenSolver or the Python appendix.
4. **Stress-test before committing.** Re-run the choice at a container rate half and double today's, with the most likely tariff change, and with the China lane delayed six weeks. A plan that stays near the best in all of them is safe to adopt; a part that flips between suppliers is a candidate for a second source or a shorter contract.

### 7.1 Pitfalls

- **Comparing quotes on different terms.** An FOB Shanghai price, an ex-works Monterrey price and a delivered Vancouver price are not comparable until freight, duty and brokerage are added.
- **Chasing the lowest freight per unit.** Ordering once a year cuts freight per unit but multiplies cycle stock; in this case one order a year costs more than two for every part bought from China, by up to C$12,100 a year for steel reinforcement and C$4,200 for casement operators.
- **Ignoring origin rules.** Surtaxes follow where the steel was melted or the aluminum smelted, not only where the part was made. A part assembled in Mexico from Chinese steel may still pay.
- **Counting suppliers, not regions.** Most supplier management cost (audits, visits, inspection, broker set-up) is per country or region; adding a part to an existing region is cheap, adding a region is not.
- **Treating the model as a forecast.** Tariffs, freight and exchange rates change monthly. Re-run the model quarterly and whenever a surtax, remission order or freight contract changes.

## Conclusions

Comparing suppliers on total landed cost rather than unit price cut this plant's annual cost of eight parts by 9%, while it paid more on supplier invoices.

- The lowest-price plan cost C$630,100 a year; the total-cost plan C$573,600. Surtaxes on Chinese steel and aluminum, LCL freight on bulky parts and the carrying cost of long lead times made up the difference; without surtaxes the plan is the same and the saving is 3.5%.
- Where a part is made matters less than what it is. Compact, labour-intensive hardware stayed in China; bulky, low-value or surtaxed parts came home.
- A price-plus-freight comparison got within 1.4% of the optimum. The rest came from order frequency and from not adding a supplier region for two parts.
- The total-cost plan held up under uncertainty: it had the lowest mean cost across 20,000 simulated years, and its 95th-percentile cost was within C$500 of the lowest and C$106,600 below the lowest-price plan.
- A second supplier lowered average cost only when a shortage could not be covered and cost more than about C$190 per part short; for the worst years, buying the hardware in North America protected better than dual sourcing.

The case is a composite and its prices, tariff rates and risk weights are illustrative. The model leaves out quantity discounts, supplier capacity limits, exchange-rate hedging and the engineering cost of qualifying a new supplier, and it treats a disruption as a delay rather than a quality or supplier failure. Disruptions are modelled only on the China lane: North American supply is assumed reliable and Canadian spot capacity unlimited, which favours the North American plans. The appendix reproduces the base-case plans; the full model, with the risk simulation and sweeps, can be downloaded from this paper's page. The method transfers directly: an SME with clean receipt data and current broker advice can build the landed cost sheet in a day and re-run it each quarter.

## Appendix: Python Code

The script below reproduces the base-case results exactly: C$573,614 a year for the total-cost plan and C$630,082 for the lowest-price plan. It needs Python 3 and PuLP 2.9 (pip install pulp==2.9.0, which includes the CBC solver) and runs in under a second. The risk simulation of Section 6 adds a loop over random freight rates, exchange rates, tariff scenarios and disruptions around the cost function; the full model files, including the risk simulation and the freight and shortage sweeps, can be downloaded from this paper's page.

CODE appendix || Base-case total landed cost model: one supplier, mode and order frequency per part, shared containers and supplier-region costs (Python 3 with PuLP 2.9).
"""
