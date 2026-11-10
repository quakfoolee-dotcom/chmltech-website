import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0])
from insert import apply
J = __file__.rsplit("/", 2)[0] + "/journal/"

apply(J + "physical-ai-foundations-architectures-and-the-sim-to-real-gap.json", [
 dict(sec="3", after=7, ref=("3", 7), sentence="Figure 1 shows the resulting stack: each layer runs faster than the one above it, and observations are fed back to every learned layer.",
      fig=dict(n=1, id="fig1-stack-timescales", caption="The perception, planning and control stack of a current robot learning system, with the update rate of each layer. Rates are those reported for the models named and were measured on different hardware.",
               alt="Layered diagram. From top to bottom: task instruction; a reasoning module based on a vision-language model running at 1 to 10 hertz; an action generator producing action chunks at 50 to 120 hertz; conventional joint servo control running faster still; and the robot and its environment. Arrows pass instructions, plans, target poses and motor commands downward, and a feedback path returns camera images and joint readings to the three control layers.",
               source="Drawn by the author; rates from [7–10].")),
 dict(sec="4", after=7, ref=("4", 7), sentence="Figure 2 plots the two rates for ε = 0.01: over a 50-step task the bound for behavior cloning is 25 mistakes, against 0.5 for the linear rate.",
      fig=dict(n=2, id="fig2-compounding-error", caption="Growth of the expected number of mistakes with task horizon for a per-step error probability ε = 0.01, from Eq. (3). The behavior-cloning bound grows quadratically until it reaches the limit of one mistake per step at <i>T</i> = 100; with interactive relabeling the growth is linear. The vertical axis is logarithmic.",
               alt="Line chart on a logarithmic vertical axis of expected mistakes against task horizon from 1 to 100 steps. The orange curve, epsilon T squared, rises from 0.01 to 100 and meets the dashed grey line T at 100 steps. The blue curve, epsilon T, rises from 0.01 to 1. At 50 steps the curves are marked at 25 mistakes and 0.5 mistakes.",
               source="Author's calculation from Eq. (3), after [11].")),
 dict(sec="7", after=7, ref=("7", 7), sentence="Figure 3 illustrates the narrow, suitable and wide cases.",
      fig=dict(n=3, id="fig3-domain-randomization", caption="Domain randomization, Eq. (5), shown schematically for one simulator parameter. The policy is trained over a distribution <i>p</i>(ξ) of simulator parameters; transfer depends on whether that distribution covers the unknown value of the real system without being so wide that the policy must compromise.",
               alt="Three stacked schematic panels sharing a horizontal axis for a simulator parameter such as friction. A dashed vertical line marks the unknown value of the real system. In panel a, a narrow training distribution lies entirely to the left of the line and transfer fails. In panel b, a moderate distribution covers the line and transfer succeeds. In panel c, a very wide distribution covers the line but gives a conservative policy.",
               source="Schematic drawn by the author, after [22, 24, 25].")),
])

apply(J + "physical-ai-in-process-plants-and-factories-inspection-manipulation-and-control.json", [
 dict(sec="3", after=2, ref=("3", 2), sentence="Figure 1 places the three application classes within the plant hierarchy.",
      fig=dict(n=1, id="fig1-plant-hierarchy", caption="The three classes of physical AI application in relation to the existing plant hierarchy. (A) An inspection robot observes equipment and sends data to maintenance systems and the digital twin. (B) A manipulation robot handles objects. (C) A learned controller writes set points at the supervisory level, within limits. The safety instrumented system remains independent of all three.",
               alt="Block diagram of a plant hierarchy with five stacked layers: operations and maintenance systems including the digital twin; supervisory control; regulatory control; field devices; and process equipment, materials and work areas. An independent safety instrumented system sits beside the control layers and acts on the process. An inspection robot at lower left observes the process and sends inspection data to the top layer. A manipulation robot at lower right handles objects. A learned controller at upper right sends set points within limits to the supervisory control layer.",
               source="Drawn by the author from Sections 2 and 3.")),
 dict(sec="4", after=8, ref=("4", 8), sentence="Figure 2 plots Eq. (1) for three values of <i>p</i><sub>d</sub>.",
      fig=dict(n=2, id="fig2-detection-rounds", caption="Probability that a developing fault has been detected after <i>n</i> independent inspection rounds, Eq. (1), for three detection probabilities per round. The marked points are the values quoted in the text for <i>p</i><sub>d</sub> = 0.3.",
               alt="Line chart of cumulative detection probability against number of inspection rounds from 0 to 12, for per-round detection probabilities of 0.1, 0.3 and 0.5. The curve for 0.3 is marked at 0.30 after one round, 0.76 after four rounds and 0.94 after eight rounds. The curve for 0.5 exceeds 0.9 after four rounds; the curve for 0.1 reaches about 0.72 after twelve rounds.",
               source="Author's calculation from Eq. (1).")),
 dict(sec="7", after=1, ref=("7", 0), sentence="Figure 3 presents the same assessment graphically.",
      fig=dict(n=3, id="fig3-readiness", caption="Indicative technology readiness ranges of the applications in Table 2, grouped by class. The assessment is the author's, as of November 2026.",
               alt="Horizontal range chart of indicative technology readiness levels on a scale of 1 to 9. Robot and drone inspection rounds, 8 to 9. Anomaly detection on inspection data, 6 to 8. Bin picking and depalletizing, 8 to 9. Self-driving laboratories, 5 to 7. General-purpose manipulation with vision-language-action models, 4 to 6. General-purpose humanoid labor, 4 to 6. Learned supervisory control of one unit, 6 to 8. Dashed lines mark level 6, prototype in a relevant environment, and level 9, proven in operation.",
               source="Author's assessment from Table 2; TRL scale after [30].")),
])

apply(J + "safety-reliability-and-economics-of-deploying-physical-ai.json", [
 dict(sec="4", after=1, ref=("4", 1), sentence="Figure 1 shows the arrangement.",
      fig=dict(n=1, id="fig1-safety-architecture", caption="Safety architecture for a learned component. The learned policy proposes actions in a performance channel; a conventional safety-rated layer filters them and can command a protective stop from its own sensing. A run-time monitor that detects unfamiliar inputs or low confidence improves task success but is not part of the safety function.",
               alt="Block diagram. Cameras and joint sensors feed a learned policy labeled performance channel, which sends a proposed action into a safety-rated layer. Inside that layer a safety filter limiting speed, force, workspace and separation passes a safe action to the drives and actuators, and safety-rated sensing such as scanners, light curtains and emergency stop feeds the filter and can command a protective stop directly. Below the policy, a run-time monitor for unfamiliar input and low confidence exchanges signals with the policy and asks a supervisor for help.",
               source="Drawn by the author, after [14, 20, 21].")),
 dict(sec="5", after=3, ref=("5", 3), sentence="Figure 2 plots Eq. (3) for three values of <i>p</i>.",
      fig=dict(n=2, id="fig2-task-success", caption="Probability that a task of <i>n</i> independent steps succeeds, Eq. (3), for three per-step success probabilities. The marked points are the values quoted in the text.",
               alt="Line chart of task success probability against number of steps from 1 to 100. With per-step success of 0.999 the curve falls slowly to about 0.90 at 100 steps and is marked 0.95 at 50 steps. With 0.99 it is marked 0.90 at 10 steps and 0.61 at 50 steps and falls to 0.37 at 100 steps. With 0.95 it falls below 0.1 by 50 steps.",
               source="Author's calculation from Eq. (3).")),
 dict(sec="6", after=11, ref=("6", 11), sentence="Figure 3 shows the dependence of NPV on the intervention fraction for different shift patterns.",
      fig=dict(n=3, id="fig3-npv-intervention", caption="Net present value of the hypothetical cell of Table 2 against intervention fraction, from Eqs. (6) and (7), for one, two and three shifts at 90% availability and for two shifts at 70% availability. The marked points are the three cases of Table 2.",
               alt="Line chart of net present value in thousand US dollars against intervention fraction from 0 to 0.5. Four straight lines slope downward: three shifts at 0.90 availability is highest and stays positive; two shifts at 0.90 availability crosses zero near 0.43; two shifts at 0.70 availability crosses zero near 0.27; one shift at 0.90 availability is negative throughout. Marked points: base case plus 235, low reliability minus 14, single shift minus 81.",
               source="Author's calculation from Eqs. (6) and (7) with the inputs of Table 2.")),
])
print("placed")
