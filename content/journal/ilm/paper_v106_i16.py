"""Chmltech Online Journal, Vol. 106, Issue 16: Can an LLM Assess a Factory? (draft V1, Nov 27 2026).

Model: content/journal/ilm/models/assess/validation_sim.py (validation-study simulation: five LLM behaviours,
two human assessors, quadratic weighted kappa, bootstrap non-inferiority, 300 studies per sample size).
"""

SLUG = "can-an-llm-assess-a-factory-validating-ai-scored-smart-factory-maturity-against-human-assessors"
META = dict(
    volume=106, issue=16,
    title='Can an LLM Assess a Factory? Validating AI-Scored Smart Factory Maturity Against Human Assessors',
    short_title='Can an LLM Assess a Factory? Validating AI Maturity Scores',
    meta='How to prove an LLM can score smart factory maturity as well as a human assessor: evidence-first pipeline, agreement statistics and how many plants to test.',
    keywords=['smart factory maturity', 'Industry 4.0 assessment', 'Smart Industry Readiness Index', 'large language models',
              'LLM-as-a-judge', 'weighted kappa', 'validation study', 'SMEs'],
)
ABSTRACT = "Smart factory maturity assessments such as the Smart Industry Readiness Index score a plant on many dimensions and are expensive for small and mid-sized manufacturers. Large language models can read the same evidence and propose scores, but a score that looks plausible is not a validated one. This paper sets out an evidence-first pipeline in which the model scores one dimension at a time, must quote its evidence and must abstain when evidence is missing, and a validation design that compares it with two independent human assessors. A simulation of that design, with assumed (not measured) model behaviours, 16 dimensions and bands 0 to 5, shows four things. A model as consistent as a human passes a non-inferiority test on weighted kappa (margin 0.10) in all simulated studies with 20 plants and 88% with 10. The same kappa can come from noise or from leniency: both scored about 0.71 against 0.77 between humans, and only the mean band difference (+0.49) exposed the leniency. A model that guesses where evidence is missing passed in at most 2% of studies, yet 92 to 93% of the scores of every flawed model were within one band of the assessors', so within-one-band agreement is a poor acceptance measure. A simulated model that abstains kept human-level agreement on the 70% of dimensions it scored. Validation should therefore report kappa, bias and coverage together, use at least 20 to 30 plants, and accept no band without evidence, because agreement statistics alone cannot reliably catch gap filling."

REFS = {
    'siri': ('Singapore Economic Development Board. (2017). <em>The Singapore Smart Industry Readiness Index: Catalysing the transformation of manufacturing</em> [White paper]. EDB.',
        'https://www.edb.gov.sg/content/dam/edb-japan/key-activities/advanced-manufacturing/the-singapore-smart-industry-readiness-index/the-sg-smart-industry-readiness-index-whitepaper.pdf'),
    'siriedb': ('Singapore Economic Development Board. (2019, updated 2026). The Smart Industry Readiness Index.',
        'https://www.edb.gov.sg/en/about-edb/media-releases-publications/advanced-manufacturing-release.html'),
    'acatech': ('Schuh, G., Anderl, R., Dumitrescu, R., Krüger, A., &amp; ten Hompel, M. (Eds.). (2020). <em>Industrie 4.0 Maturity Index: Managing the digital transformation of companies — Update 2020</em> (acatech STUDY). acatech.',
        'https://en.acatech.de/publication/industrie-4-0-maturity-index-update-2020/'),
    'mittal': ('Mittal, S., Khan, M. A., Romero, D., &amp; Wuest, T. (2018). A critical review of smart manufacturing &amp; Industry 4.0 maturity models: Implications for small and medium-sized enterprises (SMEs). <em>Journal of Manufacturing Systems</em>, 49, 194–214.',
        'https://doi.org/10.1016/j.jmsy.2018.10.005'),
    'vance': ('Vance, D., Jin, M., Price, C. R., Nimbalkar, S. U., &amp; Wenning, T. J. (2023). Smart manufacturing maturity models and their applicability: A review. <em>Journal of Manufacturing Technology Management</em>, 34(5), 735–770.',
        'https://doi.org/10.1108/JMTM-03-2022-0103'),
    'schumacher': ('Schumacher, A., Erol, S., &amp; Sihn, W. (2016). A maturity model for assessing Industry 4.0 readiness and maturity of manufacturing enterprises. <em>Procedia CIRP</em>, 52, 161–166.',
        'https://doi.org/10.1016/j.procir.2016.07.040'),
    'sadeqi': ('Sadeqi Bajestani, M., Mun, D., &amp; Kim, D. B. (2026). Human-in-the-loop and large language models in smart manufacturing: Current applications, challenges, and perspectives. <em>Journal of Manufacturing Systems</em>, 86, 913–941.',
        'https://doi.org/10.1016/j.jmsy.2026.04.027'),
    'zheng': ('Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E. P., Zhang, H., Gonzalez, J. E., &amp; Stoica, I. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. <em>Advances in Neural Information Processing Systems</em>, 36 (Datasets and Benchmarks Track).',
        'https://arxiv.org/abs/2306.05685'),
    'gilardi': ('Gilardi, F., Alizadeh, M., &amp; Kubli, M. (2023). ChatGPT outperforms crowd workers for text-annotation tasks. <em>Proceedings of the National Academy of Sciences</em>, 120(30), e2305016120.',
        'https://doi.org/10.1073/pnas.2305016120'),
    'wangfair': ('Wang, P., Li, L., Chen, L., Cai, Z., Zhu, D., Lin, B., Cao, Y., Kong, L., Liu, Q., Liu, T., &amp; Sui, Z. (2024). Large language models are not fair evaluators. <em>Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)</em>, 9440–9450.',
        'https://doi.org/10.18653/v1/2024.acl-long.511'),
    'ji': ('Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y. J., Madotto, A., &amp; Fung, P. (2023). Survey of hallucination in natural language generation. <em>ACM Computing Surveys</em>, 55(12), 1–38.',
        'https://doi.org/10.1145/3571730'),
    'lostmid': ('Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., &amp; Liang, P. (2024). Lost in the middle: How language models use long contexts. <em>Transactions of the Association for Computational Linguistics</em>, 12, 157–173.',
        'https://doi.org/10.1162/tacl_a_00638'),
    'lewis': ('Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W.-t., Rocktäschel, T., Riedel, S., &amp; Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. <em>Advances in Neural Information Processing Systems</em>, 33, 9459–9474.',
        'https://arxiv.org/abs/2005.11401'),
    'rag': ('Lee, Q. F. (2026). Retrieval-augmented generation: Design, evaluation and failure analysis for enterprise knowledge systems. <em>Chmltech Online Journal</em>, 104(3).',
        'https://www.chmltech.com/post/retrieval-augmented-generation-design-evaluation-and-failure-analysis.html'),
    'autonomy': ('Lee, Q. F. (2026). Levels of autonomy and human-in-the-loop design for AI agents: Matching oversight to risk and earning autonomy with evidence. <em>Chmltech Online Journal</em>, 105(7).',
        'https://www.chmltech.com/post/levels-of-autonomy-and-human-in-the-loop-design-for-ai-agents.html'),
    'cohen': ('Cohen, J. (1968). Weighted kappa: Nominal scale agreement with provision for scaled disagreement or partial credit. <em>Psychological Bulletin</em>, 70(4), 213–220.',
        'https://doi.org/10.1037/h0026256'),
    'landis': ('Landis, J. R., &amp; Koch, G. G. (1977). The measurement of observer agreement for categorical data. <em>Biometrics</em>, 33(1), 159–174.',
        'https://doi.org/10.2307/2529310'),
    'bland': ('Bland, J. M., &amp; Altman, D. G. (1986). Statistical methods for assessing agreement between two methods of clinical measurement. <em>The Lancet</em>, 327(8476), 307–310.',
        'https://doi.org/10.1016/S0140-6736(86)90837-8'),
    'shrout': ('Shrout, P. E., &amp; Fleiss, J. L. (1979). Intraclass correlations: Uses in assessing rater reliability. <em>Psychological Bulletin</em>, 86(2), 420–428.',
        'https://doi.org/10.1037/0033-2909.86.2.420'),
    'evalag': ('Lee, Q. F. (2026). Evaluating AI agents: Why public benchmarks mislead and how to build your own evaluation. <em>Chmltech Online Journal</em>, 105(10).',
        'https://www.chmltech.com/post/evaluating-ai-agents-why-benchmarks-mislead-and-how-to-build-your-own-evaluation.html'),
    'readiness': ('Lee, Q. F. (2026). Agent readiness for small and mid-sized firms: Data foundations, process documentation and staged adoption. <em>Chmltech Online Journal</em>, 105(6).',
        'https://www.chmltech.com/post/agent-readiness-for-small-and-mid-sized-firms-data-process-staged-adoption.html'),
}

DOWNLOADS = [
    dict(file='llm_assessor_validation_sim.py', label='Simulation script', note='Validation-study simulation: weighted kappa, bias, coverage and non-inferiority power (Python 3, NumPy)'),
]

BODY = r"""
## Introduction

A smart factory maturity assessment answers a simple question at considerable cost: where does this plant stand today, and what should it improve first? Frameworks such as the Smart Industry Readiness Index (SIRI) [@siri] and the acatech Industrie 4.0 Maturity Index [@acatech] break the question into dimensions and describe each level in words. An assessor gathers documents, system extracts, interview notes and a plant walk, then places the plant in a band on each dimension. For a small or mid-sized manufacturer the cost is mostly the assessor's time, and reviews of maturity models note that many were never validated and fit small firms poorly [@mittal, @vance].

Large language models (LLMs) can read a pile of plant documents in minutes and propose a band for every dimension with a fluent justification. That speed is attractive, and LLMs have matched or beaten crowd workers on some text-classification tasks [@gilardi]. But the same models are imperfect judges: their verdicts can change with the order in which answers are shown [@wangfair] and tend to favour longer answers [@zheng]; even the strongest agree with human judges only about as often as humans agree with each other, around 80% on open-ended chat questions [@zheng]; and they can state unsupported content as fact [@ji]. A 2026 review of LLMs in smart manufacturing concluded that human oversight and structured verification remain necessary [@sadeqi].

This paper therefore does not ask whether an LLM *can* produce maturity scores; it clearly can. It asks what must be shown before those scores can be trusted:

- How should an LLM be set up so that its scores can be checked?
- Which statistics show whether it agrees with human assessors, and which failure modes does each statistic miss?
- How many plants does a validation study need?

Section 2 describes what a maturity assessment measures. Section 3 lists how an LLM can go wrong. Section 4 proposes an evidence-first pipeline, Section 5 a validation design, and Section 6 tests that design by simulation. Section 7 turns the results into a protocol, Section 8 states the limitations and Section 9 concludes.

## What a Maturity Assessment Measures

SIRI organizes Industry 4.0 into three building blocks (process, technology and organization), eight pillars and 16 dimensions, each scored in bands from 0 to 5 using a descriptive assessment matrix [@siri]. The programme is now managed by the International Centre for Industrial Transformation, and its assessment is used by both multinationals and small firms [@siriedb]. The acatech index takes a capability view: six stages, from computerization through connectivity, visibility, transparency and predictive capacity to adaptability, assessed across resources, information systems, organizational structure and culture [@acatech]. Academic models follow similar patterns of dimensions and levels [@schumacher]. Table 1 compares the two frameworks used most in practice.

TABLE Two widely used maturity frameworks. || Structure as published by the framework owners [@siri, @acatech].
| Feature | Smart Industry Readiness Index | acatech Industrie 4.0 Maturity Index |
| Structure | 3 building blocks, 8 pillars, 16 dimensions | 4 structural areas, 6 development stages |
| Scale | Bands 0–5 per dimension | Stages 1–6 per capability |
| Evidence | Assessment matrix with descriptive band criteria | Capability questionnaire, interviews, site analysis |
| Output | Profile across 16 dimensions and priorities | Current stage, capability gaps and roadmap |

Three features of these assessments matter for automation. First, every band has a written description, so scoring is a classification against a rubric, not an open judgement. Second, the evidence is mixed: some dimensions can be read from documents and system extracts, others need observation or interviews. Third, small plants often have little documentation; Mittal and colleagues found that most maturity models start at a "level 1" already beyond where many small manufacturers are, and proposed a "level 0" [@mittal], so a large share of dimensions may have thin evidence.

## How an LLM Can Go Wrong Scoring a Plant

Five failure modes matter, and they call for different controls (Table 2).

TABLE Failure modes of an LLM assessor. || The signal column names the check that exposes each failure; kappa, mean band difference and coverage are defined in Section 5.
| Failure mode | What happens | Signal | Control |
| Inconsistency | The same evidence gets different bands on repeated runs or slight rewording | Repeat-run agreement; lower kappa | Fixed rubric text, low temperature, repeat runs |
| Leniency or severity | Bands are systematically too high (or low), for example because documents describe intentions rather than practice | Mean band difference | Rubric anchors that require evidence of practice; calibration examples |
| Filling gaps | A band is given where the evidence says nothing | Coverage near 100% on thin evidence packs; low agreement on dimensions assessors mark as unsupported | Mandatory quotations; "insufficient evidence" as an allowed answer |
| Order and length effects | Verdicts depend on which evidence comes first or which document is longest | Agreement under shuffled evidence | One dimension at a time; balanced evidence |
| Long-context loss | Evidence in the middle of a long pack is overlooked | Lower agreement on dimensions whose evidence is buried | Retrieval of dimension-specific evidence |

Order and length effects are documented for LLM judges of answers, and by analogy may apply to the evidence an assessor reads: swapping the order of the two answers being compared changed GPT-4's verdict often enough to alter model rankings [@wangfair]. Long-context loss is documented for retrieval tasks, where information in the middle of a long input is used less reliably than information at the start or end [@lostmid]. Leniency is the failure an experienced assessor will recognize at once: plant documents describe procedures as written and systems as purchased, and an assessor who reads only the documents will score what the plant intends, not what it does.

Gap filling is the most dangerous because it is invisible. A model asked for a band on all 16 dimensions will usually return 16 bands. When the evidence is silent it tends to fall back on whatever it can infer from the rest of the file and from general expectations of plants like this one, which is exactly the fluent but unsupported output that the hallucination literature describes [@ji].

## An Evidence-First Assessment Pipeline

The pipeline in Figure 1 is designed so that every band can be traced to evidence and every gap is reported.

FIG fig1-pipeline || Evidence-first assessment pipeline. The model sees only the evidence for one dimension at a time, must quote it, and may answer "insufficient evidence"; a human assessor reviews every band until the validation results justify less review. || Five boxes in a row: evidence pack, retrieval per dimension, scoring against the rubric with quoted evidence or insufficient evidence, automatic checks, and assessor review, with a note that agreement is measured before review is relaxed. ||

1. **Evidence pack.** Documents, data extracts, interview notes and plant-walk photos, each tagged with the dimensions it bears on and its type (document, data, observation, interview).
2. **Retrieval per dimension.** Only the evidence tagged for one dimension, plus the rubric text for that dimension, is put in front of the model. This is retrieval-augmented generation [@lewis] applied to a rubric, and the usual retrieval failures apply: missing tags and poorly chunked documents [@rag].
3. **Scoring against the rubric.** The model returns a band, the rubric sentence that matches it, and quotations from the evidence with their sources, or "insufficient evidence". It is told that documents describing plans count only toward intent, not practice.
4. **Automatic checks.** Each quotation must resolve to the cited source; no band may be given without at least one quotation of practice evidence; the same dimension is scored three times and disagreements are flagged.
5. **Assessor review.** A human assessor accepts or changes each band and records why. The reasons become calibration examples for the next version.

### 4.1 What one scored dimension looks like

The output for one dimension should let a reviewer check it in under a minute. An illustrative example, using a connectivity dimension with rubric wording written for this paper rather than taken from any framework, looks like this:

- **Dimension:** shop floor connectivity. **Band proposed:** 2 of 5.
- **Rubric sentence matched:** "Some machines are networked and data are collected from them, but not across the whole shop floor."
- **Practice evidence:** "Lines 1 and 2 PLCs report counts to the MES every minute" (MES configuration export, page 3); "Line 3 counts are written on the shift sheet and keyed in next morning" (interview, production supervisor).
- **Intent evidence, not scored:** "All lines to be connected in 2027" (capital plan).
- **Why not band 3:** the band 3 sentence requires all production equipment to be connected; line 3 is not.
- **Stability:** the same band on three runs.

The rubric sentence shows which description was matched. The quotations show that the band rests on practice, and the capital plan is listed separately so that intent cannot raise the band, which is the direct control on leniency. The "why not the next band" line forces the model to test the boundary, which is where human assessors also disagree most. And if the evidence pack contained nothing about line 3, the correct output would be band 2 with a note that one line is unassessed, or "insufficient evidence" if no line were covered at all.

The same structure makes review fast and turns the reviewer's corrections into data. When an assessor changes a band, the reason is recorded against a specific quotation or rubric sentence, and a pattern of such corrections shows whether the model misreads the rubric, the evidence, or the boundary between bands.

The design matches the staged-autonomy principle of an earlier paper in this series: the model starts as a drafting assistant whose every output is reviewed, and earns less review only with evidence [@autonomy]. It also reflects the data-readiness point made for small firms: the pipeline is only as good as the evidence pack [@readiness].

## A Validation Design

The validation question is whether the model's bands agree with human assessors' bands as well as two human assessors agree with each other. The design follows from that question.

- **Raters.** Two human assessors score each plant independently from the same evidence pack, and may also mark "insufficient evidence"; the model scores it through the pipeline without the human review step.
- **Same evidence.** All three raters see the same pack, so differences reflect scoring, not information. Where some evidence exists only as observation or interview, record which dimensions depend on it; Section 6 simulates that case.
- **Plants and dimensions.** Each plant contributes all its dimensions; plants, not dimensions, are the unit of resampling, because scores within a plant are correlated.
- **Blinding.** Neither human assessor sees the other's bands or the model's output before scoring, and the model's prompts contain no human bands. Otherwise agreement measures copying, not judgement.
- **Case mix.** Validation plants should span the maturity range of the plants the model will assess; a narrow sample lowers both kappas and makes the margin harder to interpret.
- **Reporting by dimension.** Overall statistics are reported together with a table by dimension and by evidence type, so that a model which is reliable on documented dimensions and unreliable on observed ones is not accepted for both.

Agreement on an ordinal scale is measured with Cohen's weighted kappa [@cohen], Eq. (1), with quadratic weights w<sub>ij</sub> = (i − j)<sup>2</sup>/(K − 1)<sup>2</sup> for bands i and j on a K-band scale, observed proportions o<sub>ij</sub> and proportions expected by chance e<sub>ij</sub>:

TEX \kappa_w = 1 - \frac{\sum_{i,j} w_{ij}\, o_{ij}}{\sum_{i,j} w_{ij}\, e_{ij}}

Kappa is 0 for agreement no better than chance and 1 for perfect agreement.

Kappa summarizes how far apart the bands are, but not in which direction. The second statistic is the mean band difference between model and human, with limits of agreement in the style of Bland and Altman [@bland], Eq. (2), where d̄ and s<sub>d</sub> are the mean and standard deviation of the differences:

TEX \bar{d} \pm 1.96\, s_d

The limits show how far a single band can be off. The acceptance criterion in Section 7 uses instead the 95% confidence interval of d̄, computed by resampling plants.

The third is **coverage**, the share of dimensions the model scored rather than marking "insufficient evidence". Coverage is a design choice, not an error, but it must be reported, because a model can raise its agreement by refusing hard cases.

The acceptance test is non-inferiority, Eq. (3): the lower bound of the 95% confidence interval for the difference between the model's average kappa with the two assessors and the kappa between the assessors must lie above −δ. All three kappas are computed on the dimensions the model scored. This paper uses δ = 0.10 and a bootstrap that resamples plants, so that the correlation between kappas sharing an assessor is accounted for.

TEX \mathrm{LB}_{95\%}\left(\tfrac{1}{2}\left[\kappa_{\mathrm{LLM},H_1} + \kappa_{\mathrm{LLM},H_2}\right] - \kappa_{H_1,H_2}\right) > -\delta

In plain terms: the study passes if, even at the unlucky end of its uncertainty, the model agrees with the assessors no more than 0.10 kappa below how well the two assessors agree with each other.

Labels such as "substantial agreement" for kappa between 0.61 and 0.80 are often quoted [@landis], but they were offered as benchmarks, not thresholds, and the comparison with human–human agreement on the same evidence is more informative. Intraclass correlation is an alternative for scores treated as interval data [@shrout]. Quadratic weighted kappa is closely related to the intraclass correlation for agreement, so it would not be expected to change the conclusions below, but it was not computed here.

## Simulating the Validation Study

Before running a validation study on real plants, it is worth knowing how large it must be and what it can detect. A simulation answers both.

### 6.1 Assumptions

Each simulated plant has a latent maturity on each of 16 dimensions: a plant effect drawn from a normal distribution with mean 2.2 and standard deviation 0.7, plus a dimension effect with standard deviation 0.7, so that most bands fall between 1 and 3, a plausible range for small manufacturers. Each rater's band is the latent value plus the rater's bias and random error, rounded and clipped to 0–5. Human assessors have no bias and an error standard deviation of 0.45 band. Five model behaviours are tested:

- **S1:** as consistent as a human (error 0.45, no bias).
- **S2:** noisier than a human (error 0.65).
- **S3:** lenient by half a band (error 0.45).
- **S4:** on 30% of dimensions the deciding evidence is observational (plant walk, interviews) or was missed by retrieval, so the model has nothing usable to read while the human assessors do; the model guesses, taking the average of the plant's other bands and a generic 2.5, plus a random error of 0.6 band (error 0.45 elsewhere).
- **S5:** the same gaps, but the model answers "insufficient evidence" (error 0.45 elsewhere).
- **S6:** a calibration case, a model with error 0.75 whose kappa deficit sits almost exactly at the margin, used to check how often the test passes a model it should not.

These values are assumptions chosen to be plausible, not measurements of any model. Each scenario is run 300 times at each of five study sizes, with 400 bootstrap resamples per study. With 300 studies per point, each pass rate carries a Monte Carlo error of up to about ±3 percentage points.

### 6.2 What each statistic sees

Table 3 gives the large-sample value of each statistic, and Figure 2 shows the same values side by side.

TABLE Agreement statistics by model behaviour (large-sample values). || 4,000 simulated plants per scenario. Kappa is the model's average with the two assessors; exact and within-one-band agreement are against one assessor; the mean band difference is against the assessors' average. Human–human: kappa 0.77, exact agreement 53%, within one band 97% in every scenario.
| Behaviour | Weighted κ with assessors | Exact agreement | Within one band | Mean band difference | Coverage |
| S1 As consistent as a human | 0.77 | 53% | 97% | 0.00 | 100% |
| S2 Noisier than a human | 0.71 | 45% | 93% | 0.01 | 100% |
| S3 Lenient by half a band | 0.71 | 43% | 93% | +0.49 | 100% |
| S4 Gaps, model guesses | 0.64 | 47% | 92% | +0.04 | 100% |
| S5 Gaps, model abstains | 0.77 | 53% | 97% | 0.00 | 70% |

FIG fig3-statistics || Weighted kappa with a human assessor, mean band difference and coverage for each model behaviour; dashed lines mark the human–human kappa, zero bias and full coverage. || Three bar panels. Kappa: 0.77 for the equal and abstaining models, 0.71 for noisy and lenient, 0.64 for guessing. Mean band difference: near zero except the lenient model at 0.49. Coverage: 100% except the abstaining model at 70%. ||

Four findings follow from Table 3 and Figure 2.

1. **The same kappa can come from noise or from leniency.** With the values chosen here, the noisy and lenient models both scored 0.71. Only the mean band difference, +0.49, shows that the lenient model inflates every profile, which would make plants look more mature than they are and steer them toward advanced projects too early. Kappa and bias must be reported together.
2. **Within-one-band agreement cannot separate the failure modes.** The noisy, lenient and guessing models all scored 92–93% within one band, against 97% for the human-level model, and all would clear a 90% threshold. Kappa ranks the guessing model clearly worst (0.64), and its errors sit where the evidence was missing: its kappa was 0.26 on the gap dimensions against 0.77 on the rest. Kappa catches this guess rule only because the guess is poor. A gap-filler that guessed more cleverly, for example from the plant's own average, scored about 0.71 in a check run and would pass the kappa test with enough plants. Only the "no band without evidence" check in Table 4 catches gap filling reliably.
3. **Abstention protects agreement, here by construction.** The abstaining model kept human-level kappa on the 70% of dimensions it scored, because the gaps fall at random and the model abstains exactly on them. In practice evidence is thinnest on low-maturity dimensions, so the scored subset will be easier than the full set, and the abstentions themselves must be checked (Table 4). The unscored dimensions become a list of evidence to collect, which is useful output.
4. **Exact agreement is low even between good raters.** Two human assessors matched exactly only 53% of the time (97% within one band), and so did a model as consistent as a human. Exact agreement is a poor acceptance measure on a six-band scale.

### 6.3 How many plants?

Figure 3 shows the share of simulated studies that pass the non-inferiority test at each study size.

FIG fig2-power || Share of simulated validation studies that pass the non-inferiority test on weighted kappa (margin 0.10), by number of plants and model behaviour; 300 studies per point. || Five lines against plants from 10 to 80. The human-level model passes in 88% of studies at 10 plants and 100% at 20; the abstaining model 82% at 10, 97% at 20 and 100% at 30; the noisy model rises to 81% and the lenient model to 79% at 80 plants; the guessing model stays at 2% or below. ||

A model as consistent as a human passes in 88% of studies with 10 plants and in all studies with 20. The abstaining model, which scores fewer dimensions per plant, passes in 97% with 20 plants and all with 30. The noisy and lenient models sit inside the margin (their true kappa difference is about −0.06 to −0.07, against a margin of −0.10), so they should eventually pass, but even 80 plants gives only 81% and 79% power: a model that is slightly worse than a human is hard to prove acceptable. The guessing model almost never passes (at most 2% of studies), because its kappa deficit (about −0.12) is outside the margin; that the lenient model would eventually pass is the reason for the separate bias criterion in Section 7.

The calibration case S6, a model whose kappa deficit sits almost exactly at the margin, passed in 5 to 6% of studies at every size, against a nominal 2.5%. The percentile bootstrap used here is therefore slightly liberal; a study should treat a narrow pass with caution, or use a more exact interval such as the bias-corrected bootstrap.

CALLOUT Report weighted kappa, mean band difference and coverage together and, under the assumptions here, plan for at least 20 to 30 plants. Within-one-band agreement, a number vendors often quote, cannot distinguish a careful model from one that fills evidence gaps.

Twenty to thirty plants means 40 to 60 human assessments, a real cost. Past files that two assessors scored independently can be reused if their evidence packs were kept. Rerun the downloadable script with your own error levels, because a model even slightly worse than a human needs far more plants.

## A Practical Protocol

Table 4 turns the results into acceptance criteria for an organization that wants to use an LLM in maturity assessments.

TABLE Acceptance criteria for an LLM assessor. || Thresholds are recommendations; δ = 0.10 and |bias| ≤ 0.25 band are judgement calls that an organization should fix before the study, not after.
| Criterion | Measure | Threshold |
| Agreement | Lower 95% bound of ½[κ(LLM, H<sub>1</sub>) + κ(LLM, H<sub>2</sub>)] − κ(H<sub>1</sub>, H<sub>2</sub>), on the dimensions the model scored, plants resampled | Above −0.10 |
| Bias | Mean band difference d̄, 95% interval from resampling plants (not the limits of agreement) | Within ±0.25 band |
| Coverage | Share of dimensions scored | Reported; at least 80% of the model's abstentions also marked insufficient by an assessor; gaps listed for evidence collection |
| No band without evidence | Bands whose quotations resolve to practice evidence | 100% |
| Stability | Same band on three repeat runs and on shuffled evidence | At least 90% of dimensions |
| Study size | Plants scored by two humans and the model | Under the simulated assumptions, at least 20; 30 if the model abstains |

The protocol runs in four steps.

1. **Fix the rubric and the evidence pack format first.** The model, the prompts and the rubric text are frozen before validation. Any change afterwards means validating again, just as for any evaluation set [@evalag].
2. **Collect paired assessments.** Two human assessors score each plant independently from the same pack. Their agreement is itself a finding: if humans agree poorly on a dimension, the rubric for that dimension needs work before any model is judged against it.
3. **Score with the model and test.** Apply Table 4. Break the results down by dimension and by evidence type; a model may do well on document-heavy dimensions and poorly on those that depend on observation.
4. **Deploy with review, then relax it with evidence.** Start with an assessor reviewing every band. After a period of agreement at least as good as in validation, review a stratified sample, for example every band on dimensions with low validation agreement and a random 20% of the rest. Keep logging the assessor's changes; they are the monitoring data.

Confidentiality deserves a line of its own. An evidence pack contains a plant's processes, systems and weaknesses. It should be processed under an agreement that excludes training on client data, or by a model deployed in the assessor's own environment, and the pack should be deleted when the assessment closes.

## Limitations

The simulation shows what a validation study can and cannot detect under stated assumptions; it does not measure any real model. Real model errors are unlikely to be independent normal noise: they cluster on particular dimensions, evidence types and writing styles, which makes per-dimension reporting essential. The human error level of 0.45 band is also an assumption; a real study measures it. Finally, agreement with human assessors is a proxy for accuracy, not accuracy itself. Two assessors who share a training background can agree on a band that does not describe the plant; a plant walk by a third assessor on a sample of plants is the best available check.

## Conclusions

LLMs can produce smart factory maturity scores quickly, but a fluent score is not a validated one. The conclusions of this paper are:

- Set the model up so that it can be checked: one dimension at a time, rubric text in front of it, quotations required, and "insufficient evidence" as an allowed answer.
- Validate against two human assessors scoring the same evidence, and report weighted kappa, mean band difference and coverage together. In simulation, kappa alone gave the same value (0.71) for a noisy and a lenient model, and within-one-band agreement was 92–93% for every flawed model, including one that guessed where evidence was missing.
- A model as consistent as a human passed non-inferiority in all simulated studies with 20 plants (88% with 10); a model that abstains on missing evidence needed 20 to 30. A model slightly worse than a human was hard to prove acceptable even with 80, and the bootstrap test was slightly liberal (5–6% false passes against 2.5%).
- Never accept a band without evidence: a clever gap-filler can pass the kappa test. Abstention lowers coverage but turns gaps into a list of evidence to collect, which is part of what an assessment is for.

The next step is a real validation study on paired assessments. The simulation code can be downloaded with this paper, so that a study can be sized with its own assumptions, and the protocol in Section 7 is written so that an assessment provider can run it on its own files.
"""
