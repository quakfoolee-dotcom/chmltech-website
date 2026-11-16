"""Warehouse operations series for Insights (V5.33). Part 3: the receiving dock.

Same distributor as Parts 1 and 2. The numbers come from wh3_model.py (a simulated receiving day, averaged over 20
days), which also feeds the 3D replay in Figure 2 (assets/js/wh3d3.js).

Usage:  python3 content/articles/wh3_articles.py
        python3 content/gen/add_article.py the-dock-door-bottleneck-receiving-put-away-and-cross-docking
        python3 content/gen/series_labels.py
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sizing_articles import js3d, nowrap, svg, fig, txt, CSS, NAVY, BLUE, GREEN, GREEND, ORANGE, RED, PURPLE, MUTED, PALE, DEFS, box
import wh_model as W
import wh3_model as D
from wh_articles import W1, W2, SER, ABC1, SS1

DATE = "2026-11-15"
W3 = "the-dock-door-bottleneck-receiving-put-away-and-cross-docking"
NOTE = ('<p class="oee-note"><em>The distributor, its deliveries and its times are an illustrative example built from stated assumptions. '
        'Detention terms vary by carrier and contract.</em></p>')
f0 = lambda x: f"{x:,.0f}"
money = lambda x: f"${round(x, -2 if x < 10000 else -3):,.0f}"
f1 = lambda x: f"{x:,.1f}"
hm = D.hm

STEPS = [("As-is", {}), ("1. Delivery appointments", dict(appt=True)), ("2. Scan to receive", dict(appt=True, scan=True)),
         ("3. Cross-dock allocated pallets", dict(appt=True, scan=True, xdock=True)), ("4. Second forklift at the peak", dict(appt=True, scan=True, xdock=True, fork=True))]
A = [D.averaged(f) for _, f in STEPS]
A0, A1, A2, A3, A4 = A
N_TR = D.FTL + D.LTL


def fig_flow():
    s = DEFS
    xs = [10, 150, 290, 430, 570]; y = 50; w, h = 120, 54
    names = [["Truck arrives", "and waits"], ["Door and", "dock staff free"], ["Unload and", "check each pallet"], ["Staging lane"], ["Forklift puts", "away to a rack"]]
    for x, n in zip(xs, names): s += box(x, y, w, h, n, fs=12.5)
    for i in range(4):                                           # right face to the next box's left face
        s += f'<line x1="{xs[i] + w}" y1="{y + h / 2}" x2="{xs[i + 1] - 1}" y2="{y + h / 2}" stroke="{NAVY}" stroke-width="1.6" marker-end="url(#ah)"/>'
    # cross-dock branch: down from the staging lane, right to the outbound lanes
    s += box(570, 150, 120, 54, ["Outbound lanes", "(cross-dock)"], fill="#FBEBD3", stroke=ORANGE, fs=12.5)
    s += f'<path d="M{xs[3] + w / 2},{y + h} V{177} H{569}" fill="none" stroke="{ORANGE}" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#ah2)"/>'
    s += f'<defs><marker id="ah2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{ORANGE}"/></marker></defs>'
    s += txt(xs[3] + w / 2 - 8, 146, "Already allocated to an order", "end", ORANGE, 12)
    labs = [("Queue in the yard", 0), ("Unload rate", 2), ("Staging fills", 3), ("Put-away rate", 4)]
    for lab, i in labs: s += txt(xs[i] + w / 2, y - 14, lab, "middle", RED, 12, True)
    s += txt(10, 236, "Red: where the day backs up. A step can only work as fast as the next one clears its output.", fill=MUTED, fs=12)
    return svg("Flow of a pallet through receiving: the truck arrives and waits, gets a door and dock staff, each pallet is unloaded and checked, "
               "it waits in a staging lane, and a forklift puts it away to a rack. A dashed branch from the staging lane sends pallets already allocated "
               "to an order straight to the outbound lanes.", 700, 246, s, 560)


def fig_stage():
    runs = [(D.simulate(), "As-is", RED), (D.simulate(appt=True, scan=True), "Appointments and scanning", ORANGE),
            (D.simulate(appt=True, scan=True, xdock=True, fork=True), "All four fixes", GREEND)]
    x0, y0, w, h = 60, 34, 600, 220; tmax = 15 * 60; ymax = 120; s = ""
    X = lambda t: x0 + t / tmax * w; Y = lambda v: y0 + h - v / ymax * h
    for v in range(0, ymax + 1, 20): s += f'<line x1="{x0}" y1="{Y(v)}" x2="{x0 + w}" y2="{Y(v)}" stroke="#E4E1D8"/>' + txt(x0 - 8, Y(v) + 4, str(v), "end", MUTED, 12)
    for hh in range(0, 16, 2): s += txt(X(hh * 60), y0 + h + 18, hm(hh * 60), "middle", MUTED, 12)
    cap = D.STAGE_LANES * D.STAGE_DEPTH
    s += f'<line x1="{x0}" y1="{Y(cap)}" x2="{x0 + w}" y2="{Y(cap)}" stroke="{NAVY}" stroke-dasharray="5 4"/>' + txt(x0 + w - 4, Y(cap) - 6, f"Staging lanes full ({cap})", "end", NAVY, 12, True)
    s += f'<rect x="{X(D.LOAD_BLOCK[0])}" y="{y0}" width="{X(D.LOAD_BLOCK[1]) - X(D.LOAD_BLOCK[0])}" height="{h}" fill="#ECE9E1" opacity=".7"/>' + txt(X(D.LOAD_BLOCK[0]) + 4, y0 + 14, "Forklift loading", fill=MUTED, fs=11.5)
    for k, (r, lab, c) in enumerate(runs):
        d = f"M{X(0)},{Y(0)}"; prev = 0
        for t, v in r["curve"]: d += f" H{X(t):.1f} V{Y(v):.1f}"
        s += f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2.4"/>'
        s += f'<rect x="{x0 + 14}" y="{y0 + 8 + k * 18}" width="12" height="12" rx="2" fill="{c}"/>' + txt(x0 + 32, y0 + 18 + k * 18, lab, fill=NAVY, fs=12.5, bold=True)
    s += f'<text x="16" y="{y0 + h / 2}" transform="rotate(-90 16 {y0 + h / 2})" text-anchor="middle" font-size="12.5" font-weight="600" fill="{NAVY}">Pallets waiting in staging</text>'
    return svg("Step chart of pallets waiting in staging through one simulated day. As-is, staging passes its 48 spots around midday and stays over "
               "into the evening. With appointments and scanning, trucks are unloaded faster and staging fills even higher, because the single forklift "
               "is now the bottleneck. With all four fixes, staging stays well under its capacity and empties by early afternoon.", 700, 290, s, 560)


def figure_data():
    pos = W.positions(W.LEVELS_NEW); M = W.run(); used = set(M["locs"][4].values())
    free = sorted([i for i in range(len(pos)) if i not in used], key=lambda i: (pos[i]["walk"], pos[i]["k"]))
    sc = {}
    for m, flags in enumerate(D.combos()):
        r = D.simulate(**flags); fi = 0; pal = []
        for p in sorted(r["pallets"], key=lambda p: p["put0"]):
            dest = -1
            if not p["xd"]: dest = free[fi % len(free)]; fi += 1
            pal.append([round(p["enter"], 1), round(p["out"], 1), round(p["put1"], 1), 1 if p["xd"] else 0, p["spot"], dest, p["door"]])
        a = D.averaged(flags)
        sc[m] = dict(tr=[[round(t["arr"], 1), round(t["start"], 1), round(t["end"], 1), t["door"], t["pallets"]] for t in r["trucks"]],
                     p=pal, c=[[t, v] for t, v in r["curve"]],
                     s=[round(a["wait"]), round(a["over2"], 1), round(a["det_year"], -2 if a["det_year"] < 10000 else -3), round(a["dts"], 1), round(a["peak"]), round(a["last"])])
    rack = [[p["cls"], p["id"] in M["p2"] and M["p2"][p["id"]]["h"] or p["h"], M["locs"][4][p["id"]]] for p in M["pallets"] if p["id"] in M["locs"][4]]
    return dict(bld=[W.BLD_X, W.BLD_Z, W.CLEAR_H], rows=W.ROW_Z, aisles=W.AISLE_Z, bays=W.BAYS, bayW=W.BAY_W, rowD=W.ROW_D, x0=W.RACK_X0, perBay=W.PER_BAY,
                beam=W.BEAM, levels=W.LEVELS_NEW, cap=D.STAGE_LANES * D.STAGE_DEPTH, lanes=D.STAGE_LANES, depth=D.STAGE_DEPTH,
                block=D.LOAD_BLOCK, day0=D.DAY0, sc=sc, rack=rack)


def figure_markup():
    data = json.dumps(figure_data(), separators=(",", ":"))
    sw = lambda f, lab: f'<button type="button" class="wh3d-btn wh3d-switch" data-f="{f}" role="switch" aria-checked="false"><i aria-hidden="true"></i><span>{lab}</span></button>'
    return f"""<p>Figure 2 replays one simulated receiving day, from 06:00 to 21:00, at about twelve minutes a second. Trucks queue in the yard, back onto a door and are unloaded into the staging lanes. Forklifts take the pallets to free rack positions from Part&nbsp;1, and cross-dock pallets go straight to the outbound lanes. Switch the fixes on and off in any combination. The numbers are averages over 20 simulated days.</p>
<figure class="wh3d wh3d3" id="wh3d3">
<div class="wh3d-box">
<div class="wh3d-stage">
<canvas role="img" aria-label="3D replay of a receiving day at the example distributor: trucks waiting in the yard and backed onto three inbound dock doors, pallets in the staging lanes and overflowing into the aisle, forklifts carrying pallets to the pallet racks, and cross-dock pallets moving to the outbound lanes."></canvas>
<span class="wh3d-drag" aria-hidden="true">Drag to turn</span>
<span class="wh3d-chip" id="wh3d3-clock">06:00</span>
<p class="wh3d-nogl" id="wh3d3-nogl" hidden>This browser cannot show the 3D model. The switches below still update the numbers.</p>
</div>
<div class="wh3d-panel">
<div class="wh3d3-sw" role="group" aria-label="Fixes">{sw("appt", "Delivery appointments")}{sw("scan", "Scan to receive (ASN)")}{sw("xdock", "Cross-dock allocated pallets")}{sw("fork", "Second forklift 08:00 to 12:00")}</div>
<div class="wh3d-cells">
<div class="wh3d-cell wh3d-key"><span class="k">Average truck wait for a door</span><strong id="wh3d3-wait"></strong></div>
<div class="wh3d-cell wh3d-key"><span class="k">Dock-to-stock time</span><strong id="wh3d3-dts"></strong></div>
<div class="wh3d-cell"><span class="k">Trucks on site over 2 hours</span><strong id="wh3d3-o2"></strong></div>
<div class="wh3d-cell"><span class="k">Detention exposure a year</span><strong id="wh3d3-det"></strong></div>
<div class="wh3d-cell"><span class="k">Peak pallets in staging</span><strong id="wh3d3-peak"></strong></div>
<div class="wh3d-cell"><span class="k">Last pallet put away</span><strong id="wh3d3-last"></strong></div>
</div>
<div class="wh3d3-chart" aria-hidden="true"><svg viewBox="0 0 600 110" preserveAspectRatio="none"><g id="wh3d3-grid"></g><path id="wh3d3-curve" fill="rgba(141,198,63,.18)" stroke="#8DC63F" stroke-width="1.6" vector-effect="non-scaling-stroke"/><line id="wh3d3-cap" stroke="#fff" stroke-dasharray="4 4" opacity=".6" vector-effect="non-scaling-stroke"/><line id="wh3d3-now" stroke="#FFE27A" stroke-width="1.5" vector-effect="non-scaling-stroke"/></svg><p><span>Pallets in staging through the replayed day</span><span>Dashed: the 48 staging spots</span></p></div>
<p class="wh3d-say" id="wh3d3-say" aria-live="polite"></p>
<div class="wh3d-last"><ul class="wh3d-legend"><li><i style="background:#E3C58E"></i>Received pallet</li><li><i style="background:#FF7A5C"></i>Overflow in the aisle</li><li><i style="background:#FF8A3D"></i>Cross-dock pallet</li><li><i style="background:#F2C94C"></i>Forklift</li></ul></div>
</div>
</div>
<figcaption>Figure 2. One simulated receiving day, replayed. {N_TR} trucks bring {f0(A0["n_pal"])} pallets. Three doors are for receiving, and two dock staff unload and check each pallet. One forklift puts away all day but loads outbound trucks from 13:30 to 15:00. The headline numbers are averages over 20 simulated days. The replay shows the first of them, so its own peak and finish times can differ.</figcaption>
<script type="application/json" id="wh3d3-data">{data}</script>
</figure>
"""


def part3():
    trs = "".join(f'<tr><td>{n}</td><td class="num">{f0(a["wait"])}&nbsp;min</td><td class="num">{f1(a["over2"])}</td><td class="num">{money(a["det_year"])}</td>'
                  f'<td class="num">{f1(a["dts"])}&nbsp;h</td><td class="num">{f0(a["peak"])}</td><td class="num">{hm(a["last"])}</td></tr>' for (n, _), a in zip(STEPS, A))
    body = f"""{CSS}
<p>At 9:30 in the morning there are three trucks in the yard and two more on the road. The staging lanes filled an hour ago, so pallets are parked in the cross-aisle, and the pickers from Part&nbsp;2 are walking round them. A driver wants to know how much longer, because his carrier starts charging after two hours. Upstairs, sales are promising stock that came in yesterday and still is not in a pick location.</p>
<p>This is the dock door bottleneck, and in most small warehouses it has little to do with the size of the dock. Deliveries arrive at the same time, the staff check paper, and one forklift does everything. This part follows a receiving day at the example distributor and tests four fixes in order.</p>
<h2>How a pallet gets from the truck to the rack</h2>
{fig(fig_flow(), 1, "Receiving is a chain. Speed up one step and the queue moves to the next.")}
<p>Each pallet passes through four steps, and each has its own limit. The yard holds trucks until a door and a person are free. The unload rate depends on how long each pallet takes to unload and check. Staging holds what has been unloaded but not yet put away. The put-away rate is set by the forklifts. The one measure that covers the whole chain is <strong>dock-to-stock time</strong>: the hours from a truck's arrival until its stock is in a location and on the system, ready to pick.</p>
<p>The WERC benchmark puts best-in-class operations at under about 3 hours dock to stock, and its earlier reports gave a median of about 6 hours. Carriers watch a different clock. Most allow about two hours of free time at a receiver before they start charging detention, commonly $50 to $100 an hour.</p>
<h2>The example's receiving day</h2>
<table>
<tr><th>Assumption</th><th class="num">Value</th></tr>
<tr><td>Inbound trucks a day</td><td class="num">{D.FTL} full loads of 24 pallets and {D.LTL} part loads of 4 to 10</td></tr>
<tr><td>Arrivals without appointments</td><td class="num">Bunched around 08:30</td></tr>
<tr><td>Receiving doors, dock staff</td><td class="num">{D.DOORS} doors, {D.UNLOADERS} people</td></tr>
<tr><td>Unload a pallet</td><td class="num">{D.T_UNLOAD} min</td></tr>
<tr><td>Check a pallet against the packing slip, or scan it against the ASN</td><td class="num">{D.T_CHECK:.0f} min, or {D.T_SCAN} min</td></tr>
<tr><td>Staging spots</td><td class="num">{D.STAGE_LANES * D.STAGE_DEPTH} pallets in {D.STAGE_LANES} lanes</td></tr>
<tr><td>Forklift put-away trip</td><td class="num">{D.T_PUT:.0f} min a pallet</td></tr>
<tr><td>Forklift loading outbound trucks</td><td class="num">{hm(D.LOAD_BLOCK[0])} to {hm(D.LOAD_BLOCK[1])}</td></tr>
<tr><td>Detention</td><td class="num">${D.DET_RATE:.0f} an hour after 2 hours on site</td></tr>
</table>
<p>As-is, trucks wait an average of {f0(A0["wait"])} minutes for a door, and about {f1(A0["over2"])} of the {N_TR} trucks a day are on site for more than two hours. If every carrier billed it, that is about {money(A0["det_year"])} a year in detention. Staging peaks at about {f0(A0["peak"])} pallets against {D.STAGE_LANES * D.STAGE_DEPTH} spots. The last pallet is put away at about {hm(A0["last"])}, hours after the dock shift ends, and dock-to-stock averages {f1(A0["dts"])} hours.</p>
<h2>Fix 1: book the deliveries</h2>
<p>Most of the yard queue is self-inflicted: carriers arrive when it suits their route, and most of them want the morning. An appointment schedule spreads them out. Give each supplier a standing slot, size the slots to the load (a full load of floor-stacked pallets needs about two hours of a person's time here), and keep the last slot early enough for put-away to finish within the shift. In the example, slots from 06:30 to 12:30 cut the average wait from {f0(A0["wait"])} to {f0(A1["wait"])} minutes and detention exposure from about {money(A0["det_year"])} to {money(A1["det_year"])} a year. A free spreadsheet calendar is enough to start. Dock scheduling software comes later.</p>
<h2>Fix 2: scan instead of checking paper</h2>
<p>Counting cartons against a packing slip and writing up discrepancies takes the dock staff about {D.T_CHECK:.0f} minutes a pallet here. Ask suppliers for an advance ship notice (ASN) and barcode pallet labels, and receiving becomes a scan with exceptions only. At {D.T_SCAN} minutes a pallet the unload rate rises by about a third, and the average wait falls to {f0(A2["wait"])} minutes.</p>
<p>Look at what happens to staging, though. It now peaks at about {f0(A2["peak"])} pallets, and dock-to-stock barely moves ({f1(A1["dts"])} to {f1(A2["dts"])} hours). The dock is now faster than the forklift, so the queue has moved from the yard into staging. This is why receiving has to be fixed as a chain.</p>
<h2>Fix 3: cross-dock what is already sold</h2>
<p>Some inbound pallets are already allocated to customer orders: back orders, special orders, or a full pallet for one customer. Putting them away only to pick them back out the next morning costs two forklift trips and a day. Flag them on the ASN or the purchase order, and send them from the door straight to the outbound lanes. In the example about a quarter of the pallets qualify. That takes about {f0(A3["n_xd"])} pallets a day off the forklift, cuts dock-to-stock to {f1(A3["dts"])} hours, and keeps staging under its {D.STAGE_LANES * D.STAGE_DEPTH} spots.</p>
<h2>Fix 4: add put-away capacity at the peak</h2>
<p>The last limit is the single forklift during the morning rush. A second truck from 08:00 to 12:00 clears staging as fast as it fills. It does not need a new hire: the batch picking of Part&nbsp;2 freed several picker-hours a day, and one trained picker on a second forklift through the morning covers it. With all four fixes, staging peaks at about {f0(A4["peak"])} pallets, dock-to-stock averages {f1(A4["dts"])} hours, and the last pallet is away by about {hm(A4["last"])}.</p>
{figure_markup()}<h2>The result</h2>
<table>
<tr><th>Step</th><th class="num">Truck wait</th><th class="num">Trucks over 2 h</th><th class="num">Detention a year</th><th class="num">Dock to stock</th><th class="num">Peak in staging</th><th class="num">Last put-away</th></tr>
{trs}
</table>
{fig(fig_stage(), 3, "Pallets waiting in staging through one simulated day. Faster unloading alone fills staging higher. Clearing it needs put-away capacity.")}
<h2>The rules that keep the dock moving</h2>
<ul>
<li><strong>Same-day put-away.</strong> Nothing stays in staging overnight. Stock on the dock cannot be picked and is easy to lose.</li>
<li><strong>Directed put-away.</strong> The system or a simple location rule tells the driver where each pallet goes, using the slotting rules from Part&nbsp;1, so fast movers land at the front.</li>
<li><strong>Receive at the door.</strong> Count or scan as the pallet comes off the truck, not later from the staging lane.</li>
<li><strong>Exceptions to one place.</strong> A damaged or short pallet goes to a marked quarantine spot with a photo and a note, so it does not block a lane.</li>
<li><strong>Measure supplier compliance.</strong> Track which suppliers send ASNs, labels and on-time arrivals, and raise it at review time.</li>
</ul>
<h2>Measures to track</h2>
<table>
<tr><th>Measure</th><th>What it shows</th></tr>
<tr><td>Dock-to-stock time, in hours</td><td>The whole receiving chain in one number</td></tr>
<tr><td>Truck turnaround time and detention charges</td><td>Whether appointments and the dock crew match the arrivals</td></tr>
<tr><td>Pallets in staging at 12:00 and at shift end</td><td>Whether put-away keeps up</td></tr>
<tr><td>Receipts with discrepancies</td><td>Supplier quality, and whether a paper check is still needed</td></tr>
<tr><td>Pallets cross-docked</td><td>Handling avoided</td></tr>
</table>
<h2>Common mistakes</h2>
<ul>
<li><strong>Adding doors.</strong> Doors are rarely the limit. People, checking time and put-away usually are.</li>
<li><strong>Fixing the dock and forgetting the forklift.</strong> A faster unload just moves the queue into staging.</li>
<li><strong>Appointments that run to the end of the day.</strong> A 15:00 delivery is still being put away at 17:00.</li>
<li><strong>Using the cross-aisle as overflow staging.</strong> It blocks the pickers and hides stock.</li>
<li><strong>Accepting paper from every supplier.</strong> Start with the suppliers who send the most pallets.</li>
</ul>
<h2>Key points</h2>
<ul>
<li>Receiving is a chain: yard, unload and check, staging, put-away. Dock-to-stock time measures all of it.</li>
<li>Appointments flatten the morning rush. In the example they cut the average truck wait from {f0(A0["wait"])} to {f0(A1["wait"])} minutes.</li>
<li>Faster unloading moves the queue into staging unless put-away keeps up.</li>
<li>Cross-dock pallets that are already sold, and add put-away capacity at the peak.</li>
<li>With all four fixes, dock-to-stock falls from {f1(A0["dts"])} to {f1(A4["dts"])} hours and the dock finishes within its shift.</li>
</ul>
<p>Earlier in this series: <a href="{W1}.html">Part&nbsp;1</a> won back space and re-slotted the racks, and <a href="{W2}.html">Part&nbsp;2</a> cut the pickers' walking. Next: <a href="phantom-stock-inventory-accuracy-and-cycle-counting.html">Part&nbsp;4</a> deals with phantom stock, when the system says 40 and the shelf says 12. Related: <a href="{SS1}.html">setting safety stock</a>.</p>
<h2>Sources</h2>
<ul>
<li><a href="https://www.yale.com/4a4034/globalassets/coms/yale/north-america/documents/white-papers/yal-1558_werc2026updates_improvingdcmetricswhitepaper.pdf" rel="noopener" target="_blank">Yale: Improving DC metrics, with WERC 2026 DC Measures</a> (dock-to-stock best in class)</li>
<li><a href="https://sps.honeywell.com/us/en/support/blog/productivity/which-metrics-matter-most-to-dc-operations" rel="noopener" target="_blank">Honeywell: Which metrics matter most to DC operations</a> (WERC dock-to-stock median)</li>
<li><a href="https://www.freightwaves.com/news/understanding-detention-pay-clauses" rel="noopener" target="_blank">FreightWaves: Understanding detention pay clauses</a> (free time and rates)</li>
<li><a href="https://otrucking.com/resources/guides/detention-pay-rates-2026/" rel="noopener" target="_blank">OTrucking: Detention pay rates 2026</a> (two-hour free time, average rate)</li>
</ul>
{NOTE}{js3d("wh3d3")}"""
    body = nowrap(body, [(2, 0, 34), (3, 0, 36)])
    return dict(slug=W3, title="The Dock Door Bottleneck: Receiving, Put-Away and Cross-Docking",
                desc="Why trucks queue and staging overflows, and how appointments, scanning, cross-docking and put-away capacity cut dock-to-stock time.",
                cats=["operational-efficiency", "inventory-management"], tags=["receiving", "dock to stock", "put-away", "cross-docking", "dock scheduling", "detention"],
                body=body, date=DATE, author="Quak Foo Lee", read="10 min read", series=SER(3), cover_label="Warehouse operations",
                related=[W2, W1, SS1])


if __name__ == "__main__":
    a = part3()
    json.dump(a, open(os.path.join(HERE, a["slug"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.stderr.write(f"wrote {a['slug']} desc={len(a['desc'])}\n")
    for (n, _), x in zip(STEPS, A): print(n, round(x["wait"]), round(x["over2"], 1), round(x["det_year"]), round(x["dts"], 2), round(x["peak"]), hm(x["last"]), round(x["n_xd"]))
